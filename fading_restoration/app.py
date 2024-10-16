import torch
from flask import Flask, request, jsonify
from PIL import Image
import torchvision.transforms as transforms
import base64
import io
import torch.nn as nn
from model.model import DnCNN

# Initialize the Flask app
app = Flask(__name__)



# Load the pre-trained model
model_dir = 'model/dncnn_finetuned_faded.pth'
model = DnCNN()  # Instantiate the model
model.load_state_dict(torch.load(model_dir, map_location=torch.device('cpu')))  # Load weights
model.eval()

# Transformation to convert image to tensor
transform = transforms.Compose([
    transforms.Resize((256, 256)), 
    transforms.ToTensor(),
])

# Helper function to convert a tensor to a base64 string
def tensor_to_base64(tensor,original_size):
    # Convert the tensor to a numpy array
    output_img = tensor.squeeze().permute(1, 2, 0).numpy()  # Convert to HWC format
    output_img = (output_img * 255).clip(0, 255).astype('uint8')  # Scale back to [0, 255]

    # Convert the numpy array to a PIL image
    img = Image.fromarray(output_img)
    
    # Resize the output image back to the original size
    output_img_resized = img.resize(original_size, Image.Resampling.BICUBIC)

    # Create a BytesIO buffer
    buffered = io.BytesIO()
    output_img_resized.save(buffered, format="PNG")  # Save as PNG

    # Convert the buffer to base64
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

# Route to handle image upload and restoration
@app.route('/faded_restoration', methods=['POST'])
def restore_image():
    # Check if an image is uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    # Open the image
    img = Image.open(image_file).convert('RGB')
    original_size = img.size
    # Convert the image to tensor
    img_tensor = transform(img).unsqueeze(0)  # Add batch dimension

    # Run the image through the model
    with torch.no_grad():
        output = model(img_tensor)

    # Convert the output tensor to base64
    output_base64 = tensor_to_base64(output,original_size)

    # Return the base64 image as a JSON response
    return jsonify({
        'restored_image': output_base64,
        'message': 'Restoration successful!'
    })

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
