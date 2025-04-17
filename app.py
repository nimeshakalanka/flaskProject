from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime
import cloudinary
import cloudinary.uploader
from pymongo import MongoClient

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

cloudinary.config(
  cloud_name = "dluwvqdaz",
  api_key = "734782482834278",
  api_secret = "aBZQjye7DZmaKEU06ii_mW090Dc"
)

client = MongoClient("mongodb+srv://drldxqy:admin@cluster0.iow2yxe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") 
db = client['image_gallery']
images_collection = db['images']

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data_url = request.form['image']
    header, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)

    filename = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    with open(filename, 'wb') as f:
        f.write(data)

    result = cloudinary.uploader.upload(filename)
    image_url = result['secure_url']

    images_collection.insert_one({
        "url": image_url,
        "timestamp": datetime.now()
    })

    os.remove(filename)

    print(f"Uploaded to {image_url}")
    return jsonify({"image_url": image_url})

@app.route('/gallery')
def gallery():
    images = list(images_collection.find().sort("timestamp", -1)) 
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
