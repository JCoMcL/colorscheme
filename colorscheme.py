import numpy as np
from PIL import Image
import sys

def kak(color_scheme: dict):
	out = ""
	for color, variants in color_scheme.items():
		for variant, hex_val in variants.items():
			out += f"declare-option -hidden str {color}_{variant} \"rgb:{hex_val}\"\n"
	return out

def css(color_scheme: dict):
	out = ":root {\n"
	for color, variants in color_scheme.items():
		for variant, hex_val in variants.items():
			out += f"  --{color}-{variant}: #{hex_val};\n"
	out += "}"
	return out

def extract_color_scheme(image_path):
	# Load image
	img = Image.open(image_path)
	img_array = np.array(img)

	# Assuming columns are colors, rows are variations
	colors = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']
	variations = ['muddy', 'dark', 'bright', 'light', 'pale']

	# Extract colors
	color_scheme = {}
	for col, color_name in enumerate(colors):
		color_variants = {}
		for row, variation in enumerate(variations):
			# Extract color from image
			pixel_color = img_array[row, col]
			hex_color = '{:02x}{:02x}{:02x}'.format(pixel_color[0], pixel_color[1], pixel_color[2])
			color_variants[variation] = hex_color
		color_scheme[color_name] = color_variants

	return color_scheme


# Usage
def main(image_path):
	sys.stdout.write({
		"kak" : kak,
		"css" : css,
	}[sys.argv[1]](extract_color_scheme(image_path)))

main('/dev/stdin')
