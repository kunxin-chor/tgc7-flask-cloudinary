from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv
import cloudinary

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
CLOUD_NAME = os.environ.get("CLOUD_NAME")
UPLOAD_PRESET = os.environ.get("UPLOAD_PRESET")
API_SECRET = os.environ.get("CLOUD_SECRET")

DB_NAME = "artworks"

client = pymongo.MongoClient(MONGO_URI)


@app.route('/')
def upload():
    return render_template('upload.template.html',
                           cloud_name=CLOUD_NAME,
                           upload_preset=UPLOAD_PRESET)


@app.route('/', methods=['POST'])
def process_upload():
    title = request.form.get('title')
    uploaded_file_url = request.form.get('uploaded_file_url')
    client[DB_NAME].pictures.insert_one({
        'title': title,
        'uploaded_file_url': uploaded_file_url
    })

    return "Image Uploaded"


@app.route('/gallery')
def gallery():
    pictures = client[DB_NAME].pictures.find()
    return render_template('gallery.template.html', all_pictures=pictures)


@app.route('/generate-signature', methods=["POST"])
def generate_signature():
    signature = cloudinary.utils.api_sign_request(request.json.params_to_sign,
                                                  API_SECRET)
    return {
        "signature": signature
    }


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
