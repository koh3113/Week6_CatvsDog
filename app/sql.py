import psycopg2
import os
import cv2
import base64
import numpy as np
import tensorflow as tf

conn = psycopg2.connect(user='lenovo', database='coderschool', password='1')
conn.autocommit = True
cursor = conn.cursor()

def create_table():
    query = f"""CREATE TABLE IF NOT EXISTS catvsdog (
            id SERIAL PRIMARY KEY, 
            img bytea, 
            label int
            );
    """
    # column bytea to accept bytes datatype after encode(), type of column bytea is memoryview
    # Chuyển memoryview về bytes = memoryview.tobytes() . Sau đó decode() là ra array của hình
    cursor.execute(query)

def encode(img_path):
    img = cv2.imread(img_path)
    img = cv2.imencode('.jpg', img)
    img_encoded = base64.b64encode(img[1])
    return img_encoded

def decode(img_encoded):
# just pass img column from SQL    
    img_decoded = base64.b64decode(img_encoded[0][0])
    img_decoded = np.frombuffer(img_decoded, dtype=np.uint8)
    img_decoded = cv2.imdecode(img_decoded, 1) # array of image
#     cv2.imwrite('./1.jpg', img_decoded) # if want to restore image
    return img_decoded

def save_into_db(img, label):
    query = f"""
                INSERT INTO catvsdog (img, label) 
                VALUES (%s, %s) 
                RETURNING id;
                """
    img_encoded = encode(img)
    vals = (img_encoded, label)

    cursor.execute(query, vals)


def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    image /= 255.0  # normalize to [0,1] range
    image = 2*image-1  # normalize to [-1,1] range

    return image

def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)