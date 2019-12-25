import os
from flask import Flask, Blueprint,request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from blueprints import *
import cv2
import base64
import sql
import tensorflow as tf
import pathlib as p

model = tf.keras.models.load_model('models/3_96_25k.h5')

upload_api = Blueprint('upload_api', __name__)


	
@upload_api.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      try:
        f = request.files['file']
        f.save(os.path.join(str(p.Path.cwd() /'static'/'images'),secure_filename(f.filename)))
        preprocess_img = sql.load_and_preprocess_image(os.path.join(str(p.Path.cwd() /'static'/'images' / str(f.filename))))
        preprocess_img = tf.reshape(preprocess_img,[1,192,192,3])
        predict = model.predict(preprocess_img)
        d = {0: 'cat',
                1: 'dog'}
        predict = d[predict.argmax()]
        return render_template('predict.html', img=f.filename, predict = predict)		
      except:
        data = request.json
        print('1' not in data)
        img_name = data.split(" ")[0]
        path = os.path.join(str(p.Path.cwd() /'static'/'images' / img_name))
        if '1' not in data:
          label = {"cat":1,"dog":0}.get(data.split(" ")[1])
          sql.save_into_db(path,label) 
        os.remove(path)
        return render_template('predict.html', img="", predict = "") 
if __name__ == '__main__':
   app.run(debug = True)
