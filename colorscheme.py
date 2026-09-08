import numpy as np
from PIL import Image
import sys
from pprint import pp as pretty_print


def _to_linear(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _from_linear(c):
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def _lab_f(t):
    d = 6 / 29
    return t ** (1 / 3) if t > d ** 3 else t / (3 * d ** 2) + 4 / 29

def _lab_f_inv(t):
    d = 6 / 29
    return t ** 3 if t > d else 3 * d ** 2 * (t - 4 / 29)

def _hex_to_lab(h):
    r, g, b = _to_linear(int(h[0:2], 16)), _to_linear(int(h[2:4], 16)), _to_linear(int(h[4:6], 16))
    # sRGB → XYZ D65, normalized by D65 white point
    x = _lab_f((r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047)
    y = _lab_f((r * 0.2126729 + g * 0.7151522 + b * 0.0721750) / 1.00000)
    z = _lab_f((r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883)
    return 116 * y - 16, 500 * (x - y), 200 * (y - z)

def _lab_to_hex(L, a, b):
    fy = (L + 16) / 116
    x = _lab_f_inv(a / 500 + fy) * 0.95047
    y = _lab_f_inv(fy)          * 1.00000
    z = _lab_f_inv(fy - b / 200) * 1.08883
    r = max(0.0, min(1.0, _from_linear( 3.2404542 * x - 1.5371385 * y - 0.4985314 * z)))
    g = max(0.0, min(1.0, _from_linear(-0.9692660 * x + 1.8760108 * y + 0.0415560 * z)))
    b = max(0.0, min(1.0, _from_linear( 0.0556434 * x - 0.2040259 * y + 1.0572252 * z)))
    return '{:02x}{:02x}{:02x}'.format(round(r * 255), round(g * 255), round(b * 255))

def to_light_mode(color_scheme):
    def invert(h):
        L, a, b = _hex_to_lab(h)
        return _lab_to_hex(100.0 - L, a, b)
    return {color: {v: invert(h) for v, h in variants.items()} for color, variants in color_scheme.items()}


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
	color_scheme = extract_color_scheme(image_path)
	if '--light' in sys.argv:
		color_scheme = to_light_mode(color_scheme)
	sys.stdout.write({
		"kak" : kak,
		"css" : css,
		"alacritty" : alacritty
	}[sys.argv[1]](color_scheme))

main('/dev/stdin')
