
from traitement import *
from flask import Flask, request, jsonify
import werkzeug
from tensorflow.python.keras.models import load_model
import os
import numpy as np


app = create_app()



@app.route("/upload", methods=['POST'])
def upload():
    
    imageFile = request.files['image']
    filename = werkzeug.utils.secure_filename(imageFile.filename)
    imageFile.save("./uploadedimages/"+filename)

    # read image
    image_file_name = "./uploadedimages/"+filename
    image = cv2.imread(image_file_name)
    ac, sign = traiter(image)

    # save image
    cv2.imwrite('result.png', sign)

    # load result Image
    image2 = cv2.imread('result.png')
    image1 = cv2.imread('RIB/'+ac+'.png')
    # load model
    model = load_model('modelsm.pt')
    image1 = np.array(image1)
    image2 = np.array(image2)
    image1 = image1/255.0
    image2 = image2/255.0
    pred = model.predict([image1, image2])
    
    if pred >= 0.8:
       return "VALIDE !" #VALIDE!
    else:
        return "NON VALIDE !" #NON VALIDE 
    

if __name__ == '__main__':
    app.run(debug=True)



