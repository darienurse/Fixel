import PIL.Image
import sys

class Pixel(object):
	def __init__(self, image):
		self.image = image
		self.x = 0
		self.y = 0

	def __getattr__(self, item):
		if item == 'color':
			return self.image[self.x, self.y]
		else:
			raise AttributeError


class Image(object):
	def __init__(self, name):
		self.name = name
		try:
			self.image_data = PIL.Image.open(name)
		except:
			print "\nSorry, '"+name+"' is not a valid image file. Accepted formats are JPGs, PNGs, and GIFs.\n"
			sys.exit(0)
		self.pixel_data = None

	def __getattr__(self, item):
		if item == 'width':
			return self.image_data.size[0]
		elif item == 'height':
			return self.image_data.size[1]
		else:
			raise AttributeError

	def __getitem__(self, index):
		self.load_pixel_data_if_needed()
		return Color(self.pixel_data[index])

	def __setitem__(self, index, value):
		self.load_pixel_data_if_needed()
		self.pixel_data[index] = value.rgb

	def load_pixel_data_if_needed(self):
		if self.pixel_data is None:
			self.pixel_data = self.image_data.load()

	def set_image_data(self, new_image_data):
		self.image_data = new_image_data
		self.pixel_data = None


class Color(object):
	def __init__(self, rgb):
		rgb_list = list(rgb)
		for i in range(0, 3):
			if rgb_list[i] < 0:
				rgb_list[i] = 0
			elif rgb_list[i] > 255:
				rgb_list[i] = 255
		self.rgb = tuple(rgb_list)

	def __getitem__(self, index):
		return self.rgb[index]

	def __getattr__(self, item):
		if item == 'r':
			return self.rgb[0]
		elif item == 'g':
			return self.rgb[1]
		elif item == 'b':
			return self.rgb[2]
		else:
			return AttributeError

	def __add__(self, right):
		if type(right) is Color:
			return Color((c1 + c2 for c1, c2 in zip(self.rgb, right.rgb)))
		elif type(right) is int:
			return Color((c + right for c in self.rgb))
		else:
			raise TypeError

	def __radd__(self, left):
		if type(left) is int:
			return Color((left + c for c in self.rgb))
		else:
			raise TypeError

	def __sub__(self, right):
		if type(right) is Color:
			return Color((c1 - c2 for c1, c2 in zip(self.rgb, right.rgb)))
		elif type(right) is int:
			return Color((c - right for c in self.rgb))
		else:
			raise TypeError

	def __rsub__(self, left):
		if type(left) is int:
			return Color((left - c for c in self.rgb))
		else:
			raise TypeError

	def __mul__(self, right):
		if type(right) is Color:
			return Color((c1 * c2 for c1, c2 in zip(self.rgb, right.rgb)))
		elif type(right) is int:
			return Color((c * right for c in self.rgb))
		else:
			raise TypeError

	def __rmul__(self, left):
		if type(left) is int:
			return Color((left * c for c in self.rgb))
		else:
			raise TypeError

	def __div__(self, right):
		if type(right) is Color:
			return Color((c1 / c2 for c1, c2 in zip(self.rgb, right.rgb)))
		elif type(right) is int:
			return Color((c / right for c in self.rgb))
		else:
			raise TypeError

	def __rdiv__(self, left):
		if type(left) is int:
			return Color((left + c for c in self.rgb))
		else:
			raise TypeError
