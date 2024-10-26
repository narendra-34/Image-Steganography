#!/usr/bin/python

import os, sys
import numpy
from PIL import Image

def main():
	
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		
		print ("Example:")
		print ("python decode.py img/output.png img/res.png")
		
		return
	if len(sys.argv) >= 2:
		img_path = sys.argv[1]
	if len(sys.argv) >= 3:
		output_path = sys.argv[2]
		filename, file_ext = os.path.splitext(output_path)
		output_path = filename + '.png'
	else:
		output_path = 'images/decoded_image.png'
	decoded_image = decode(Image.open(img_path))
	decoded_image.save(output_path)

def extract_hidden_pixels(image, width_visible, height_visible, pixel_count):
	
	hidden_image_pixels = ''
	idx = 0
	for col in range(width_visible):
		for row in range(height_visible):
			if row == 0 and col == 0:
				continue
			r, g, b = image[col, row]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			hidden_image_pixels += r_binary[4:8] + g_binary[4:8] + b_binary[4:8]
			if idx >= pixel_count * 2:
				return hidden_image_pixels
	return hidden_image_pixels

def reconstruct_image(image_pixels, width, height):
	
	image = Image.new("RGB", (width, height))
	image_copy = image.load()
	idx = 0
	for col in range(width):
		for row in range(height):
			r_binary = image_pixels[idx:idx+8]
			g_binary = image_pixels[idx+8:idx+16]
			b_binary = image_pixels[idx+16:idx+24]
			image_copy[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary,2))
			idx += 24
	return image
	
def decode(image):
	
	image_copy = image.load()
	width_visible, height_visible = image.size
	r, g, b = image_copy[0, 0]
	r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
	w_h_binary = r_binary + g_binary + b_binary
	width_hidden = int(w_h_binary[0:12], 2)
	height_hidden = int(w_h_binary[12:24], 2)
	pixel_count = width_hidden * height_hidden
	hidden_image_pixels = extract_hidden_pixels(image_copy, width_visible, height_visible, pixel_count)
	decoded_image = reconstruct_image(hidden_image_pixels, width_hidden, height_hidden)
	return decoded_image

def add_leading_zeros(binary_number, expected_length):
	
	length = len(binary_number)
	return (expected_length - length) * '0' + binary_number

def rgb_to_binary(r, g, b):
	
	return add_leading_zeros(bin(r)[2:], 8), add_leading_zeros(bin(g)[2:], 8), add_leading_zeros(bin(b)[2:], 8)

if __name__ == '__main__':
	main()