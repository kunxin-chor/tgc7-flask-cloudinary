# Requirements:

```
pip3 install flask
pip3 install pymongo
pip3 install dnspython
pip3 install python-dotenv
```

# 1. Sign up for a Cloudinary Account

# 2. Save the cloud name and the upload preset in the .env file

# 3. Retrieve the cloud name and the upload preset from the .env file in the Flask app
```
CLOUD_NAME = os.environ.get("CLOUD_NAME")
UPLOAD_PRESET = os.environ.get("UPLOAD_PRESET")
```

# 3. Pass the cloud name and the upload preset to the Upload Widget script
```
<script type="text/javascript">
    var myWidget = cloudinary.createUploadWidget({
        cloudName: '{{cloud_name}}', 
        uploadPreset: '{{upload_preset}}'}, (error, result) => { 
            if (!error && result && result.event === "success") { 
            console.log('Done! Here is the image info: ', result.info); 
            }
        }
    )

    document.getElementById("upload_widget").addEventListener("click", function(){
            myWidget.open();
    }, false);
</script>
```

# 4. Setup a form to capture the uploaded image url
```
<form method="POST">
    <div>
        <label>Title:</label>
        <input type="text" name="title"/>
    </div>
    <div>
        <a id="upload_widget" class="cloudinary-button">Upload files</a>
        <input type="hidden" id="uploaded_file_url" name="uploaded_file_url"/>
        <br/>
        <p>Uploaded File Name:<span id="uploaded_file_name"></span></p>
    </div>       
    
    <input type="submit" value="Save"/>
</form>
```

# 5. Change the JavaScript to put in the image url into the hidden form field
```
var myWidget = cloudinary.createUploadWidget({
        cloudName: '{{cloud_name}}', 
        uploadPreset: '{{upload_preset}}'}, (error, result) => { 
            if (!error && result && result.event === "success") { 
                console.log('Done! Here is the image info: ', result.info); 
                let fileURL = document.querySelector('#uploaded_file_url');
                fileURL.value = result.info.url;
            }
        }
    )
```

# 6. Process the form and save its data to Mongo as usual
```
    title = request.form.get('title')
    uploaded_file_url = request.form.get('uploaded_file_url')
    client[DB_NAME].pictures.insert_one({
        'title': title,
        'uploaded_file_url': uploaded_file_url
    })
```

