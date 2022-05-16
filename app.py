import re
import smtplib
from flask import Flask, render_template, request ,   g, redirect,render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tensorflow.python.keras.models import load_model
import keras
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import pickle
import numpy as np
from traitement import *


import pickle
import numpy as np
app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
 
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
 
#Creating model table for our CRUD database
class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    iduser = db.Column(db.Integer)
    name = db.Column(db.String(100))
    msg = db.Column(db.String(100))
    reponse = db.Column(db.String(100))
    statut = db.Column(db.String(100))
 
 
    def __init__(self,iduser, name, msg,reponse ,statut):
 
        self.name = name
        self.iduser = iduser
        self.msg = msg
        self.reponse = reponse
        self.statut = statut

 

class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    statut = db.Column(db.String(100))
 
 
    def __init__(self, name, email, password,statut):
 
        self.name = name
        self.email = email
        self.password = password
        self.statut = statut
 


class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    iduser = db.Column(db.Integer)
    name = db.Column(db.String(100))
    cheque = db.Column(db.String(100))
    etat = db.Column(db.String(100))
    date = db.Column(db.Date)
 
 
    def __init__(self,iduser, name, cheque,etat ,date):
 
        self.name = name
        self.iduser = iduser
        self.cheque = cheque
        self.etat = etat
        self.date = date

 

class User:
    def __init__(self, id, username, password,statut):
        self.id = id
        self.username = username
        self.password = password
        self.statut = statut

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
clients = Client.query.all()
for c in clients :
    users.append(User(id=c.id, username=c.name, password=c.password,statut=c.statut))






@app.before_request
def before_request():
    g.user = None
    users = []
    clients = Client.query.all()
    for c in clients :
      users.append(User(id=c.id, username=c.name, password=c.password,statut=c.statut))
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = []
    clients = Client.query.all()
    for c in clients :
      users.append(User(id=c.id, username=c.name, password=c.password,statut=c.statut))
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password and user.statut =="1":
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('man'))

    return render_template('register.html')

@app.route('/back')
def profile2():
    checks = Data.query.all()
    up=Data.query.count()    
    nb=Client.query.count()

    i=0;
    for n in checks :
        if n.etat == "valide":
            i=i+1;
    nbv = i;

    j=0;
    for t in checks :
        if t.etat == "non valide":
            j=j+1;
    nbnv = j;
    
    
    
    #if not g.user:
        #return redirect(url_for('login'))

    return render_template('index2.html',checks=checks , nb=nb ,nbv=nbv ,nbnv=nbnv ,up=up)
    


@app.route('/client')
def client():
    nd=[]
    nd.append(0)
    nd1=[]
    nd1.append(0)
    client = Client.query.all()
    for c in client :
        nd.append(Data.query.filter( Data.name == c.name ).count())
        nd1.append(Data.query.filter( Data.etat == "non valide" ,Data.name == c.name ).count())
    return render_template('tables-data.html',client=client,nd=nd,nd1=nd1)

@app.route('/message')
def message():
   
    message = Message.query.all()
   
    return render_template('message.html',message=message)

@app.route('/profile')
def profile():
    checks = Data.query.all()
    message=Message.query.all()
    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html',checks=checks,message=message)

@app.route('/', methods=['GET','POST'])
def man():
    clients = Client.query.all()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        passw = request.form['password']
        statut = '1'
        my_data = Client(name, email, passw,statut)
        db.session.add(my_data)
        db.session.commit()
        message="Welcome Mr/Mme "+name+" to your Bank"
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("khalil.monastiri@esprit.tn","SS04ACAB13121803")
        server.sendmail("khalil.monastiri@esprit.tn",email,message,"hdhd")
        return redirect(url_for('man'))

    return render_template('register.html')
  
    

@app.route('/message', methods=['GET','POST'])
def msg():
   

    if request.method == 'POST':
        name = request.form['name']
        iduser = request.form['iduser']
        msg = request.form['msg']
        reponse=""
        statut = '1'
        my_data = Message(iduser,name, msg, reponse,statut)
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('index.html')
           
    

    




# hna tamel chargement mtta l modele
model = pickle.load(open('iri.pkl', 'rb'))



@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        myc=Client.query.filter(Client.id == request.form['idu'])
        my_data = Data.query.get(request.form.get('id'))
        
        my_data.etat = request.form['etat']
        
 
        db.session.commit()
        for y in myc :
            email=y.email
            if request.form['etat'] == "valide" :
              message="Your  Check '"+my_data.cheque+"' Was Validate Successfully"
            else :
              message="Your Check '"+my_data.cheque+"' Was Rejected !"
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("khalil.monastiri@esprit.tn","SS04ACAB13121803")
        server.sendmail("khalil.monastiri@esprit.tn",email,message)
        return redirect(url_for('profile2'))

@app.route('/update2', methods = ['GET', 'POST'])
def update2():
 
    if request.method == 'POST':
        my_data = Client.query.get(request.form.get('id'))
 
        my_data.statut = request.form['statut']
        
 
        db.session.commit()
        
 
        return redirect(url_for('client'))



@app.route('/update3', methods = ['GET', 'POST'])
def update3():
 
    if request.method == 'POST':
        my_data = Message.query.get(request.form.get('id'))
 
        my_data.reponse = request.form['reponse']
        my_data.statut ='0'
        
 
        db.session.commit()
        
 
        return redirect(url_for('msg'))







@app.route('/predict', methods=['POST'])
def home():
  
    data5 = request.form['cheque']
    if request.method == 'POST':
        iduser = request.form['iduser']
        name = request.form['name']
        etat = request.form['etat']
        cheque = request.form['cheque']
        date=datetime.now()
        arr = np.array([[1, 1, 1, 1]])
        
        image_file_name = "static/"+data5
        img = cv2.imread(image_file_name)
        ac, sign = traiter(img)

    # save img
        cv2.imwrite('result.png', sign)

    # load result Image
        image2 = image.load_img('result.png', target_size=(64, 64)) #cv2.imread('result.png')
    #image1 = cv2.imread('RIB/911010049001545.png')
    # load model
    
        model = keras.models.load_model("modelcnn.h5")   
    #FEHD model
        test_image = image.img_to_array(image2)
        test_image = test_image/255
        test_image = np.expand_dims(test_image, axis=0)
        pred = model.predict(test_image)


        if pred < 0 :
            etat="non valide"
        elif pred<0.5 :
            etat="en attente"
        else : etat="valide"


        my_data = Data(iduser,name, cheque,etat, date)
        db.session.add(my_data)
        db.session.commit()
 
       

    # save image
    #cv2.imwrite('result.png', sign)

    # load result Image
    #image2 = cv2.imread('result.png')
    #image1 = cv2.imread('RIB/'+ac+'.png')
    # load model
    #model = keras.models.load_model('modelsm.h5')
    #image1 = np.array(image1)
    #image2 = np.array(image2)
    #image1 = image1/255.0
    #image2 = image2/255.0
    #pred = model.predict([image1,image2])
    
    return render_template('pred.html', data=pred ,data2=data5)


if __name__ == "__main__":
    app.run(debug=True)















