import cv2
import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"


def exctract_champ_AXIS(max_loc, path, image):
    n, m, _ = image.shape
    pay_champ = image[max_loc[1]+200*n//1100:max_loc[1]+300 *
                      n//1100, max_loc[0]+40*m//2365:max_loc[0]+1600*m//2365]
    gray = cv2.cvtColor(pay_champ, cv2.COLOR_BGR2GRAY)
    pay_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    rupees_champ = image[max_loc[1]+300*n//1100:max_loc[1] +
                         400*n//1100, max_loc[0]+50*m//2365:max_loc[0]+1600*m//2365]
    gray = cv2.cvtColor(rupees_champ, cv2.COLOR_BGR2GRAY)
    rupees_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    date_champ = image[max_loc[1]+40*n//1100:max_loc[1]+130 *
                       n//1100, max_loc[0]+1650*m//2365:max_loc[0]+2200*m//2365]
    gray = cv2.cvtColor(date_champ, cv2.COLOR_BGR2GRAY)
    date_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    montant_champ = image[max_loc[1]+370*n//1100:max_loc[1]+500 *
                          n//1100, max_loc[1]+1650*m//2365:max_loc[1]+2250*m//2365]
    gray = cv2.cvtColor(montant_champ, cv2.COLOR_BGR2GRAY)
    montant_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    AC_champ = image[max_loc[1]+490*n//1100:max_loc[1]+590*n //
                     1100, max_loc[0]+150*m//2365:max_loc[0]+600*m//2365]
    gray = cv2.cvtColor(AC_champ, cv2.COLOR_BGR2GRAY)
    AC_champ = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)[1]
    results_AC = pytesseract.image_to_data(AC_champ, output_type=Output.DICT)

    for e in results_AC['text']:
        if len(e) > 6:
            ac = e

    sign_champ = image[max_loc[1]+500*n//1100:max_loc[1] +
                       880*n//1100, -700*m//2365:-70*m//2365]
    gray = cv2.cvtColor(sign_champ, cv2.COLOR_BGR2GRAY)
    sign_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    results = pytesseract.image_to_data(sign_champ, output_type=Output.DICT)
    if 'Please' in results['text']:
        index = results['text'].index('Please')
        x = results["left"][index]
        y = results["top"][index]
        w = results["width"][index]
        h = results["height"][index]
        cv2.rectangle(sign_champ, (x-10, y-40),
                      (x+w+150, y+h+10), (255, 0, 0), -1)
    elif 'sign' in results['text']:
        index = results['text'].index('sign')
        x = results["left"][index]
        y = results["top"][index]
        w = results["width"][index]
        h = results["height"][index]
        cv2.rectangle(sign_champ, (x-80, y-40),
                      (x+w+100, y+h+10), (255, 0, 0), -1)
    elif 'above' in results['text']:
        index = results['text'].index('above')
        x = results["left"][index]
        y = results["top"][index]
        w = results["width"][index]
        h = results["height"][index]
        cv2.rectangle(sign_champ, (x-125, y-40),
                      (x+w+10, y+h+10), (255, 0, 0), -1)

    return(pay_champ, rupees_champ, date_champ, ac, sign_champ)
