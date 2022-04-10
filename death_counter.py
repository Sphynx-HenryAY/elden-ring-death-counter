from functools import lru_cache

import cv2
import mss
import numpy

from yaml import load, dump
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

TIME_LOOP = 0.25
TIME_COOLDOWN = 5

CONFIG_FILE = "config.yaml"

@lru_cache()
def load_config():
	try:
		with open( CONFIG_FILE ) as f:
			config = load( f, Loader = Loader )

			if config:
				return config

			raise FileNotFoundError
	except FileNotFoundError:
		with open( f"{CONFIG_FILE}.template" ) as f:
			return load( f, Loader = Loader )

def dump_config( config ):
	with open( CONFIG_FILE, "w" ) as f:
		print( dump( config, Dumper = Dumper ), file = f )

def get_monitoring_area( width, height ):
	return {
		'top': int( height * 0.43 ),
		'left': int( width * 0.4 ),
		'height': int( height * 0.1 ),
		'width': int( width * 0.2 ),
	}

def get_is_died( sct, mon_zone, threshold = 0.8 ):
	import pytesseract
	from fuzzywuzzy import fuzz

	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	punc_trans = str.maketrans( '', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' )

	text = (
		pytesseract.image_to_string(
			cv2.cvtColor(
				numpy.asarray(sct.grab( mon_zone )),
				cv2.COLOR_BGR2GRAY
			),
			lang = 'eng',
			config = '--psm 13'
		)
		.translate( punc_trans )
	)

	return fuzz.ratio( 'YOU DIED', text ) > ( threshold * 100 )

def save_die_screen( path, img ):
	cv2.imwrite( path, img )

def main():
	config = load_config()

	screen_width, screen_height = config['resolution']['width'], config['resolution']['height']

	mon_zone = get_monitoring_area( screen_width, screen_height )
	full_screen = {
		'top': 0,
		'left': 0,
		'height': screen_height,
		'width': screen_width,
	}

	with mss.mss() as sct:
		import time
		while True:
			if get_is_died( sct, mon_zone ):
				config['death_count'] += 1
				print( config['death_count'] )
				save_die_screen( 
					f"{config['died_images_folder']}\{config['death_count']}.jpg",
					numpy.asarray(sct.grab( full_screen )),
				)
				dump_config( config )
				time.sleep( TIME_COOLDOWN )

			time.sleep( TIME_LOOP )

if __name__ == '__main__':
	main()
