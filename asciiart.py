# Python script to generate ASCII art from an image

from PIL import Image
from PIL import ImageStat

grayscale_ramp = " .`:,;'_^\"\\></-!~=)(|j?}{ ][ti+l7v1%yrfcJ32uIC$zwo96sngaT5qpkYVOL40&mG8*xhedbZUSAQPFDXWK#RNEHBM@"


def brightness2gray(brightness):
    # Convert brightness to character
    # 0 is black, 255 is white
    return (grayscale_ramp[int(brightness / 255 * (len(grayscale_ramp) - 1))])


def regionBrightness(img):
    stat = ImageStat.Stat(img)
    return stat.mean[0]


image = Image.open("docs/example.jpg")
# Convert image to grayscale (ITU-R 601-2 luma transform)
image = image.convert("L")
width, height = image.size

w = round(width * 0.005)
h = round(height * 0.01)

cnt_r = 0
cnt_c = 0
outputFile = open("asciiart.txt", "w")
for row in range(height):  # careful: first and last row is not processed
    if (cnt_r == h):
        cnt_r = 0

        for col in range(width):
            if (cnt_c == w):
                cnt_c = 0

                box = (col - 10, row - 10, col, row)
                region = image.crop(box)
                brightness = regionBrightness(region)
                # print(brightness2gray(brightness) + " ", end="")
                outputFile.write(brightness2gray(brightness))

            cnt_c += 1
        # print("\n")
        outputFile.write("\r")

    cnt_r += 1

outputFile.close()
