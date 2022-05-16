import cv2
import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def exctract_champ_CANARA(max_loc, path, image):

    n, m, _ = image.shape
    pay_champ = image[max_loc[1]+170*n//1100:max_loc[1]+320 *
                      n//1100, max_loc[0]+100*m//2365:max_loc[0]+1400*m//2365]
    gray = cv2.cvtColor(pay_champ, cv2.COLOR_BGR2GRAY)
    pay_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    rupees_champ = image[max_loc[1]+280*n//1100:max_loc[1] +
                         420*n//1100, max_loc[0]+250*m//2365:max_loc[0]+1600*m//2365]
    gray = cv2.cvtColor(rupees_champ, cv2.COLOR_BGR2GRAY)
    rupees_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    date_champ = image[max_loc[1]+70*n//1100:max_loc[1]+145 *
                       n//1100, max_loc[0]+1700*m//2365:max_loc[0]+2300*m//2365]
    gray = cv2.cvtColor(date_champ, cv2.COLOR_BGR2GRAY)
    date_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    montant_champ = image[max_loc[1]+380*n//1100:max_loc[1] +
                          520*n//1100, max_loc[1]+1800*m//2365:max_loc[1]+2350*m//2365]
    gray = cv2.cvtColor(montant_champ, cv2.COLOR_BGR2GRAY)
    montant_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    AC_champ = image[max_loc[1]+520*n//1100:max_loc[1]+650 *
                     n//1100, max_loc[0]+180*m//2365:max_loc[0]+1000*m//2365]
    gray = cv2.cvtColor(AC_champ, cv2.COLOR_BGR2GRAY)
    AC_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    results_AC = pytesseract.image_to_data(AC_champ, output_type=Output.DICT)
    for e in results_AC['text']:
        if len(e) > 6:
            ac = e
    file_ac = open(path+'/AC.txt', "a")
    try:
        file_ac.write(ac)
        file_ac.close()
    except:
        print("An exception occurred")

    sign_champ = image[max_loc[1]+500*n//1100:max_loc[1] +
                       870*n//1100, -700*m//2365:-70*m//2365]
    gray = cv2.cvtColor(sign_champ, cv2.COLOR_BGR2GRAY)
    sign_champ = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    results = pytesseract.image_to_data(sign_champ, output_type=Output.DICT)

    if 'Please' in results['text']:
        index = results['text'].index('Please')
        x = results["left"][index]
        y = results["top"][index]
        w = results["width"][index]
        h = results["height"][index]
        cv2.rectangle(sign_champ, (x-10, y), (x+w+150, y+h+5), (255, 0, 0), -1)
    elif 'sign' in results['text']:
        index = results['text'].index('sign')
        x = results["left"][index]
        y = results["top"][index]
        w = results["width"][index]
        h = results["height"][index]
        cv2.rectangle(sign_champ, (x-90, y-5),
                      (x+w+100, y+h+5), (255, 0, 0), -1)
    elif 'above' in results['text']:
        index = results['text'].index('above')
        x = results["left"][index]
        y = results["top"][index]
        w = results["width"][index]
        h = results["height"][index]
        cv2.rectangle(sign_champ, (x-135, y-5),
                      (x+w+10, y+h+5), (255, 0, 0), -1)

    return(pay_champ, rupees_champ, date_champ, ac, sign_champ)
