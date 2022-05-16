import pytesseract
from traitement_ICICI import *
from traitement_canara import *
from traitement_syndicate import *
from traitement_axis import *
import cv2
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def banc_name(image1):

    logo_AXIS = cv2.imread('logo/logo AXIS.tif')
    logo_ICICI = cv2.imread('logo/logo ICICI.tif')
    logo_CANARA = cv2.imread('logo/logo CANARA.tif')
    logo_SYNDICATE = cv2.imread('logo/logo SYNDICATE.tif')
    heat_map1 = cv2.matchTemplate(image1, logo_AXIS, cv2.TM_CCOEFF_NORMED)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(heat_map1)
    heat_map2 = cv2.matchTemplate(image1, logo_ICICI, cv2.TM_CCOEFF_NORMED)
    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(heat_map2)
    heat_map3 = cv2.matchTemplate(image1, logo_CANARA, cv2.TM_CCOEFF_NORMED)
    min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(heat_map3)
    heat_map4 = cv2.matchTemplate(image1, logo_SYNDICATE, cv2.TM_CCOEFF_NORMED)
    min_val4, max_val4, min_loc4, max_loc4 = cv2.minMaxLoc(heat_map4)
    max_val = max(max_val1, max_val2, max_val3, max_val4)
    if max_val == max_val1:
        return ('AXIS', max_loc1)
    elif max_val == max_val2:
        return ('ICICI', max_loc2)
    elif max_val == max_val3:
        return ('CANARA', max_loc3)
    elif max_val == max_val4:
        return ('SYNDICATE', max_loc4)


def traiter(image):
    bank, pos = banc_name(image)
    path = './'
    if bank == 'AXIS':
        pay_champ, rupees_champ, date_champ, ac, sign_champ = exctract_champ_AXIS(
            pos, path, image)
    if bank == 'ICICI':
        pay_champ, rupees_champ, date_champ, ac, sign_champ = exctract_champ_ICICI(
            pos, path, image)
    if bank == 'CANARA':
        pay_champ, rupees_champ, date_champ, ac, sign_champ = exctract_champ_CANARA(
            pos, path, image)
    if bank == 'SYNDICATE':
        pay_champ, rupees_champ, date_champ, ac, sign_champ = exctract_champ_SYNDICATE(
            pos, path, image)
    return(ac, sign_champ)
