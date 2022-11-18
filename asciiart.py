# Python script to generate ASCII art from an image

import sys
from PIL import Image
from PIL import ImageStat

# Font size including line spacing
w = 12
h = 24

grayscale_ramp = r"""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """ [::-1]


def brightness2char(brightness):
    return (grayscale_ramp[int(brightness / 255 * (len(grayscale_ramp) - 1))])


def getBrightness(img):
    stat = ImageStat.Stat(img)
    return stat.mean[0]


# Check if a filename is provided
if len(sys.argv) < 2:
    print("Usage: python asciiart.py <image_file>")
    sys.exit(1)

image = Image.open(sys.argv[1])
image = image.convert("L") # Convert image to grayscale (ITU-R 601-2 luma transform)
width, height = image.size

x = 0
y = 0
outputFile = open("asciiart.txt", "w")
while (y < height):
    while (x < width):
        tile = image.crop((x, y, x + w, y + h))
        brightness = getBrightness(tile)
        outputFile.write(brightness2char(brightness))
        x += w
    x = 0
    y += h
    outputFile.write("\n")
outputFile.close()
