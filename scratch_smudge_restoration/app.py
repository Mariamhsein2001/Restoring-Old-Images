from flask import Flask, request, jsonify
import os
import base64
from PIL import Image
import io

app = Flask(__name__)

@app.route('/scratch_restoration', methods=['POST'])
def run_pix2pix():
    # Get the image file from the request
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image file provided."}), 400
    
    image_file = request.files['image']
    
    # Save the uploaded image to a temporary location
    input_image_path = '/tmp/input_image.png'
    image_file.save(input_image_path)

    # Define paths and model parameters
    dataroot = '/tmp/'  # You may adjust this based on your model configuration
    name = 'scratch_restoration_experiment'
    model = 'pix2pix'
    gpu_ids = '-1'
    checkpoints_dir = 'checkpoints/'  # Path to your checkpoints
    results_dir = '/tmp/results'  # Temporary results directory
    phase = 'test'
    batch_size = '1'
    dataset_mode = 'single'
    netG = 'unet_256'

    # Ensure the results directory exists
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Construct and execute the command
    command = f"python pytorch-CycleGAN-and-pix2pix/test.py --dataroot {dataroot} --name {name} --model {model} --gpu_ids {gpu_ids} --checkpoints_dir {checkpoints_dir} --results_dir {results_dir} --phase {phase} --batch_size {batch_size} --dataset_mode {dataset_mode} --netG {netG} --no_flip"
    os.system(command)

    output_images_path = os.path.join(results_dir, 'scratch_restoration_experiment/test_latest/images')
    # Path to the output image (assuming it's saved as 'fake_B.png')
    output_image_path = os.path.join(output_images_path, 'fake_B_input_image.png')

    # Convert the output image to Base64
    with open(output_image_path, "rb") as img_file:
        output_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Return the Base64 encoded image
    return jsonify({"status": "success", "restored_image": output_image_base64})


@app.route('/smudged_restoration', methods=['POST'])
def run_pix2pix_smudge():
    # Get the image file from the request
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image file provided."}), 400
    
    image_file = request.files['image']
    
    # Save the uploaded image to a temporary location
    input_image_path = '/tmp/input_image.png'
    image_file.save(input_image_path)

    # Define paths and model parameters for smudged restoration
    dataroot = '/tmp/'  # Adjust based on your model configuration
    name = 'smudged_restoration_experiment'
    model = 'pix2pix'
    gpu_ids = '-1'
    checkpoints_dir = 'checkpoints/'  # Path to your smudged restoration checkpoints
    results_dir = '/tmp/results'  # Temporary results directory
    phase = 'test'
    batch_size = '1'
    dataset_mode = 'single'
    netG = 'unet_256'

    # Ensure the results directory exists
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Construct and execute the command for smudged restoration
    command = f"python pytorch-CycleGAN-and-pix2pix/test_smudged.py --dataroot {dataroot} --name {name} --model {model} --gpu_ids {gpu_ids} --checkpoints_dir {checkpoints_dir} --results_dir {results_dir} --phase {phase} --batch_size {batch_size} --dataset_mode {dataset_mode} --netG {netG} --no_flip"
    os.system(command)

    output_images_path = os.path.join(results_dir, 'smudged_restoration_experiment/test_latest/images')
    # Path to the output image (assuming it's saved as 'fake_B.png')
    output_image_path = os.path.join(output_images_path, 'fake_B_input_image.png')

    # Convert the output image to Base64
    with open(output_image_path, "rb") as img_file:
        output_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Return the Base64 encoded image
    return jsonify({"status": "success", "restored_image": output_image_base64})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
