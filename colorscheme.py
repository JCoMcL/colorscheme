import numpy as np
from PIL import Image
import sys
from pprint import pp as pretty_print

def kak(color_scheme: dict):
	out = ""
	for color, variants in color_scheme.items():
		for variant, hex_val in variants.items():
			out += f"declare-option -hidden str {color}_{variant} \"rgb:{hex_val}\"\n"
	return out

def css(color_scheme: dict):
	out = ":root {\n"
	for color, variants in color_scheme.items():
		out += ''.join([ f"  --{color}-{variant}: #{hex_val};\n" for variant, hex_val in variants.items() ])
	out += "}"
	return out

def alacritty(color_scheme: dict):
	magenta = color_scheme['purple']
	del color_scheme['purple']
	color_scheme['magenta'] = magenta

	out = ["[colors]"]
	out.append("[colors.normal]")
	out += [f"{color} = \"#{variants["bright"]}\"" for color, variants in color_scheme.items()]

	out.append("[colors.bright]")
	out += [f"{color} = \"#{variants["light"]}\"" for color, variants in color_scheme.items()]

	out.append("[colors.dim]")
	out += [f"{color} = \"#{variants["dark"]}\"" for color, variants in color_scheme.items()]

	return '\n'.join(out)

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
		"alacritty" : alacritty
	}[sys.argv[1]](extract_color_scheme(image_path)))

main('/dev/stdin')
