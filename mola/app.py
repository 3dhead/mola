import subprocess

from PIL import Image, ImageOps


def run():
    im = Image.open("/home/maroslaw/Downloads/ben-den-engelsen-lQFEdIBghv0-unsplash.jpg").convert("L")

    im2 = ImageOps.colorize(im, black=(46, 52, 64), white=(255, 255, 255))

    im2.show()


if __name__ == "__main__":
    run()
