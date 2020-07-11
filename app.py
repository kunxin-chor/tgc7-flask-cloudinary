from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
CLOUD_NAME = os.environ.get("CLOUD_NAME")
UPLOAD_PRESET = os.environ.get("UPLOAD_PRESET")


@app.route('/')
def upload():
    return render_template('upload.template.html',
                           cloud_name=CLOUD_NAME,
                           upload_preset=UPLOAD_PRESET)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
