import cv2
import mss

TIME_LOOP = 0.5
TIME_COOLDOWN = 5

counter = 159

died_images_folder = r".\images"

def get_screen_size():
    import tkinter
    root = tkinter.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()

def get_monitoring_area( width, height ):
    return {
        'top': int( height * 0.43 ),
        'left': int( width * 0.4 ),
        'height': int( height * 0.1 ),
        'width': int( width * 0.2 ),
    }

def get_is_died( sct, threshold = 0.8 ):
	import pytesseract
	from fuzzywuzzy import fuzz
	import numpy

	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	punc_trans = str.maketrans( '', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' )

	text = (
		pytesseract.image_to_string(
			cv2.cvtColor(
				numpy.asarray(sct.grab( mon_size )),
				cv2.COLOR_BGR2GRAY
			),
			lang = 'eng',
			config = '--psm 13'
		)
		.translate( punc_trans )
	)

	return fuzz.ratio( 'YOU DIED', text ) > ( threshold * 100 )

def save_die_screen( img, path ):
	cv2.imwrite( img, path )

screen_width, screen_height = get_screen_size()

mon_size = get_monitoring_area( screen_width, screen_height )
full_screen = {
	'top': 0,
	'left': 0,
	'height': screen_height,
	'width': screen_width,
}

with mss.mss() as sct:
	import time
    while True:
        if get_is_died( sct ):
            counter += 1
            print( counter, ratio, text )
			save_die_screen( 
				numpy.asarray(sct.grab( full_screen )),
				f"{died_images_folder}\{counter}.jpg"
			)
            time.sleep( TIME_COOLDOWN )

        time.sleep( TIME_LOOP )
