from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
# Flask utils
from flask import Flask, redirect, url_for, request, render_template

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


# Flask utils
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)                               #Initialize the flask App
# model = pickle.load(open('model.pkl', 'rb'))

#default page of our web-app
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/upload_image')
def upload_image():
    return render_template('upload_image.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    # Main page
    return render_template('index.html')

import tensorflow as tf
print(tf.__version__)
# Model files

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json
# load json and create model
MODEL_ARCHITECTURE = 'cnn_64.json'
MODEL_WEIGHTS = 'cnn_64.h5'
#json_file = open(MODEL_ARCHITECTURE)
#loaded_model_json = json_file.read()
#json_file.close()
#model = model_from_json(loaded_model_json)
# load weights into new model
#model.load_weights(MODEL_WEIGHTS)
#print("Loaded model from disk")

#Conv2D = tf.compat.v1.layers.conv2d


# Load your trained model
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import json

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
# Load the model from external files
json_file = open(MODEL_ARCHITECTURE)
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(MODEL_WEIGHTS)
model.summary()
# Get weights into the model

print('Model loaded. Check http://127.0.0.1:5000/')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname('./uploads')
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds)
        # Make prediction
        preds=preds[0][0]
        if preds > 0.5:
            preds="The Person is Infected With Pneumonia"
        else:
            preds="The Person is NORMAL"
        
        os.remove(file_path)
    
    return preds



from tensorflow.keras.preprocessing import image
# ::: MODEL FUNCTIONS :::
def model_predict(img_path, model):
	'''
		Args:
			-- img_path : an URL path where a given image is stored.
			-- model : a given Keras CNN model.
	'''

	IMG = image.load_img(img_path).convert('L')
	print(type(IMG))
	# Pre-processing the image
	IMG_ = IMG.resize((64, 64))
	print(type(IMG_))
	IMG_ = np.asarray(IMG_) #/ 255.0
	print(IMG_.shape)
	IMG_ = IMG_.reshape((1,64, 64, 1))
	
	#print(model)

	#model.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer='adam')
	prediction = model.predict(IMG_)
    
	return prediction


if __name__ == "__main__":
    app.run(debug=True)