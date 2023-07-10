from PIL import Image
from .models import Config

def check_image(path):
	try:
		config = Config.objects.all()[0]
		img = Image.open(path)
		format = img.format
		print("format = " , format)
		return (format == 'JPEG' and config.is_jpg) or (format == 'PNG' and config.is_png)
	except IOError:
		return False



def is_corrupted_image(img):
	try:
		w, h, channel = img.shape
		return False
	except:
		return True
