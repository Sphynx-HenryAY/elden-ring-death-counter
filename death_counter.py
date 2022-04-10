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
PUNC_TRANS = str.maketrans( '', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' )

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

@lru_cache()
def get_monitoring_area( top, left, width, height ):
	return {
		'top': top + int( height * 0.43 ),
		'left': left + int( width * 0.4 ),
		'width': int( width * 0.2 ),
		'height': int( height * 0.1 ),
	}

def get_is_died( sct, threshold = 0.8 ):
	import pytesseract
	from fuzzywuzzy import fuzz

	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

	config = load_config()

	text = (
		pytesseract.image_to_string(
			cv2.cvtColor(
				numpy.asarray(sct.grab( get_monitoring_area( **sct.monitors[ config[ "monitor" ] ] ) )),
				cv2.COLOR_BGR2GRAY
			),
			lang = 'eng',
			config = '--psm 13'
		)
		.translate( PUNC_TRANS )
	)

	return fuzz.ratio( 'YOU DIED', text ) > ( threshold * 100 )

def save_die_screen( path, img ):
	cv2.imwrite( path, img )

def main():

	config = load_config()
	config.pop( "terminated", None )

	with mss.mss() as sct:
		import time
		while not config.get( "terminate", False ):
			if get_is_died( sct ):
				config['death_count'] += 1
				dump_config( config )
				save_die_screen( 
					f"{config['died_images_folder']}\{config['death_count']}.jpg",
					numpy.asarray(sct.grab( sct.monitors[ config[ "monitor" ] ] )),
				)
				time.sleep( TIME_COOLDOWN )

			time.sleep( TIME_LOOP )
		else:
			config[ "terminated" ] = config.pop( "terminate" )

def stop():
	load_config()[ "terminate" ] = True

if __name__ == '__main__':
	main()
