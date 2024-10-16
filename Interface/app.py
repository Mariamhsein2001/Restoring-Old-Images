import base64
import os
import requests
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scratched')
def scratched():
    return render_template('scratch_upload.html')

@app.route('/smudged')
def smudged():
    return render_template('smudge_upload.html')

@app.route('/faded')
def faded():
    return render_template('fade_upload.html')

# Function to send the image to the scratch restoration service
def send_image_to_scratch_service(image_file):
    return requests.post(
        os.getenv("SCRATCH_RESTORATION_URL"), 
        files={"image": image_file}
    )

# Function to send the image to the smudge restoration service
def send_image_to_smudge_service(image_file):
    return requests.post(
        os.getenv("SMUDGE_RESTORATION_URL"), 
        files={"image": image_file}
    )
    
# Function to send the image to the smudge restoration service
def send_image_to_fade_service(image_file):
    return requests.post(
        os.getenv("FADE_RESTORATION_URL"), 
        files={"image": image_file}
    )
    
# Route to handle image restoration
@app.route('/scratch_restore', methods=['POST'])
def scratch_restore():
    # Read the uploaded image file
    image_file = request.files['image'].read()
    if not image_file:
        return jsonify({"status": "error", "message": "No image provided."}), 400
    before_image_base64 = base64.b64encode(image_file).decode('utf-8')
    # Forward the image to the scratch restoration service
    restored_image_base64 = send_image_to_scratch_service(image_file)
    
    if restored_image_base64 :
        result = restored_image_base64.json()
        img = result.get("restored_image")
        return render_template('scratch_restoration.html', before_image=before_image_base64,result=img)
    else:
        return jsonify({"status": "error", "message": "Scratch Restoration failed."}), 500

# Route to handle image restoration
@app.route('/smudge_restore', methods=['POST'])
def smudge_restore():
    # Read the uploaded image file
    image_file = request.files['image'].read()
    if not image_file:
        return jsonify({"status": "error", "message": "No image provided."}), 400
    
    before_image_base64 = base64.b64encode(image_file).decode('utf-8')

    # Forward the image to the smudge restoration service
    restored_image_base64 = send_image_to_smudge_service(image_file)
    
    if restored_image_base64 :
        result = restored_image_base64.json()
        img = result.get("restored_image")
        return render_template('smudge_restoration.html', before_image=before_image_base64, result=img)
    else:
        return jsonify({"status": "error", "message": "Smudge Restoration failed."}), 500



@app.route('/fading_restore', methods=['POST'])
def fade_restore():
    # Access the uploaded image file from the request
    image_file = request.files['image'].read()
    
    if not image_file:
        return jsonify({"status": "error", "message": "No image provided."}), 400

    # Convert the image to base64 for displaying the 'before' image
    before_image_base64 = base64.b64encode(image_file).decode('utf-8')

    # Send the image to the fade restoration service (you can rewind or re-read the file content as needed)
    restored_image_response = send_image_to_fade_service(image_file)  # Assuming this sends file content
    
    if restored_image_response:
        result = restored_image_response.json()
        restored_image_base64 = result.get("restored_image")
        
        if restored_image_base64:
            return render_template('fade_restoration.html', 
                                   before_image=before_image_base64, 
                                   result=restored_image_base64)
        else:
            return jsonify({"status": "error", "message": "Restoration result not found."}), 500
    else:
        return jsonify({"status": "error", "message": "Fade restoration service not reachable."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.getenv("PORT"))
