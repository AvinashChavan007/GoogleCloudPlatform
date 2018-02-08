# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import os
import base64
from google.cloud import storage
from flask import Flask, render_template, request
from google.cloud import storage
from google.cloud.storage import Blob
# [END imports]

# [START create_app]
app = Flask(_name_)
key = 'brtJUWneL92g5q0N2gyDSnlPSYAiIy0='
# [END create_app]



# [START form]
@app.route('/')
def index():
    return render_template("upload.html")
# [END form]

@app.route('/upload', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files['file']
    client = storage.Client()
    
    bucket =  client.get_bucket(request.form['uploadbucketname'])
    
    encoded_key = base64.b64encode(key).decode('utf-8')
    
    encryption_key = base64.b64decode(encoded_key)
    blob = Blob(uploaded_file.filename, bucket, encryption_key=encryption_key)
    
    blob.upload_from_file(uploaded_file)
    
    return blob.public_url

@app.route('/download_file', methods=['GET','POST'])
def download():
	file_name = request.form["downloadingfilename"]
	client = storage.Client()
	bucket =  client.get_bucket(request.form['downbucketname'])
	blob = Blob(file_name, bucket, encryption_key=key)
	
	stringfile = blob.download_as_string()
	return stringfile



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]