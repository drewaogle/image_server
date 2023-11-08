#!/bin/env python3
# createImages.py - create testing images
from __future__ import annotations
import argparse
import re
from colorsys import rgb_to_hsv, hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import random
import progressbar
import os
import sys
import os.path

class ImageSize():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def size(self):
        return (self.width, self.height)

    def __str__(self):
        return f"{self.width}x{self.height}"

    @classmethod
    def parse(cls, input_str: str) -> ImageSize:
        width = 0
        height = 0
        fmt = re.compile("(^\d+)\s*(x|X)\s*(\d+)$")

        try:
            result = fmt.match(input_str)
            width = int(result.group(1))
            height = int(result.group(3))
        except:
            print("no")
            raise argparse.ArgumentTypeError(
                f"{input_str} is not a valid image size; requires width x height")

        return ImageSize(width, height)

def getoptions():
    parser = argparse.ArgumentParser(description='Create test images')
    parser.add_argument('-o','--output_path', type=str, required=True, help='Path to output images')
    parser.add_argument('-c', '--image_count', type=int, help='Number of images to create')
    parser.add_argument('-s','--image_dimensions', type=ImageSize.parse, required=True, help='Image Dimension')
    return parser.parse_args()

fnt = None
def load_preferred_font(name, size):
    global fnt
    if fnt is not None:
        return fnt
    try:
        fnt = ImageFont.truetype(name, size)
    except OSError:
        best_font = subprocess.run(
            ["fc-match", "Sans"], stdout=subprocess.PIPE, text=True)
        if best_font.returncode != 0:
            raise Exception("Can't find a font")
        fc_output = best_font.stdout
        font = fc_output.split(":")[0]
        fnt = ImageFont.truetype(font, size)
    return fnt


def complementary_color(orig_color):
    hsv = rgb_to_hsv(*orig_color)
    # rotate hue and invert value
    return tuple(int(v) for v in hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], abs(1 - hsv[2])))

def generate(opts):

    try:
        if not os.path.exists( opts.output_path ):
            os.makedirs( opts.output_path )
    except:
        print(f"Failed to create {opts.output_path}")
        sys.exit(1)
    plur = "s" if opts.image_count != 1 else ""
    print(f"Creating {opts.image_count} image{plur} of dimensions {opts.image_dimensions}")

    w = [
        'Creating ', progressbar.Percentage(),
        ' ', progressbar.Bar(), ' ', progressbar.Counter(), f'/{opts.image_count}',
        ' ', progressbar.Timer(), ' ' , progressbar.ETA() ]
    bar = progressbar.ProgressBar(widgets=w,max_value=opts.image_count)
    fnt = load_preferred_font('DejaVuSans-Bold.ttf', 16)
    for i in range(opts.image_count):
        text = f"Image # {i}"
        output_file = f"{opts.output_path}/{i}.png"
        # choose color based on hash output
        bg_color = tuple(random.randint(0, 255) for _ in range(3))
        fg_color = complementary_color(bg_color)
        canvas = Image.new("RGBA", opts.image_dimensions.size(), bg_color)
        d = ImageDraw.Draw(canvas)
        d.text((10, 10), text, font=fnt, fill=fg_color)
        canvas.save(output_file, 'png')
        bar.update(i)

if __name__ == '__main__':
    opts = getoptions()
    generate(opts)
