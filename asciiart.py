# Python script to generate ASCII art from an image

import sys
import random
from PIL import Image
from PIL import ImageStat

# Font size including line spacing
w = 1
h = 2

grayscale_ramp = r"""@%#*+=-:. """ [::-1]
# grayscale_ramp = r"""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """ [::-1]

# Threshold for brightness to use genetic algorithm
brightness_threshold = 100 # 0-255


# Convert brightness to ASCII character
def brightness2char(brightness, x, y, image):
    if brightness > brightness_threshold:
        # GA for bright parts
        return genetic_algorithm_for_bright_parts(x, y, image)
    else:
        # Use grayscale ramp for dark parts
        return grayscale_ramp[int(brightness / 255 * (len(grayscale_ramp) - 1))]


# Get the brightness of an image tile
def getBrightness(img):
    stat = ImageStat.Stat(img)
    return stat.mean[0]


# Pick a random ASCII character from the grayscale ramp
def generate_random_ascii_char():
    return random.choice(grayscale_ramp)


# Evaluate how well an ASCII char matches the brightness of the tile
def fitness_char(char, x, y, image):
    tile = image.crop((x, y, x + w, y + h))
    b = getBrightness(tile)
    c = grayscale_ramp.index(char)
    diff = abs(b - (c * (255 / len(grayscale_ramp))))
    return -diff


def mutate_char(char):
    return random.choice(grayscale_ramp)


def crossover_char(parent1, parent2):
    return parent1 if random.random() < 0.5 else parent2


def genetic_algorithm_for_bright_parts(x, y, image, population_size=len(grayscale_ramp), generations=5, mutation_rate=0.1):
    # Init population with random ASCII chars
    population = [generate_random_ascii_char() for _ in range(population_size)]
    for generation in range(generations):
        scored = [(fitness_char(ind, x, y, image), ind) for ind in population] # Evaluate fitness of each individual
        scored.sort(key=lambda x: x[0], reverse=True) # Sort population by fitness
        best_fitness = scored[0][0]
        print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")
        
        # Select top individuals and perform crossover
        population = []
        for i in range(population_size // 2):
            population.append(scored[i][1])
            population.append(crossover_char(scored[i][1], scored[i+1][1]))
        
        # Mutate individuals
        for i in range(len(population)):
            if random.random() < mutation_rate:
                population[i] = mutate_char(population[i])
    best = sorted([(fitness_char(ind, x, y, image), ind)
                  for ind in population], key=lambda x: x[0], reverse=True)[0][1]
    return best


# Check if a filename is provided
if len(sys.argv) < 2:
    print("Usage: python asciiart.py <image_file>")
    sys.exit(1)

image = Image.open(sys.argv[1])
# Convert image to grayscale (ITU-R 601-2 luma transform)
image = image.convert("L")
width, height = image.size

x = 0
y = 0
outputFile = open("output.txt", "w")
while (y < height):
    while (x < width):
        tile = image.crop((x, y, x + w, y + h))
        brightness = getBrightness(tile)
        outputFile.write(brightness2char(brightness, x, y, image))
        x += w
    x = 0
    y += h
    outputFile.write("\n")
outputFile.close()
