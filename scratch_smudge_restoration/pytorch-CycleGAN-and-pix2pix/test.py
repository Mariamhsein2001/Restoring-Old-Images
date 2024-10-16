import os
from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util.visualizer import save_images
from util import html
from util import util  # Import util for tensor2im and saving images
from PIL import Image  # Import for image resizing

if __name__ == '__main__':
    opt = TestOptions().parse()  # get test options
    opt.num_threads = 0   # test code only supports num_threads = 0
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling
    opt.no_flip = True    # no flip
    opt.display_id = -1   # no visdom display; test code saves results to HTML

    dataset = create_dataset(opt)  # create a dataset
    model = create_model(opt)      # create a model
    model.setup(opt)               # regular setup

    # Create web directory for saving HTML results
    web_dir = os.path.join(opt.results_dir, opt.name, f'{opt.phase}_{opt.epoch}')
    if opt.load_iter > 0:
        web_dir = f'{web_dir}_iter{opt.load_iter}'
    print(f'Creating web directory: {web_dir}')
    webpage = html.HTML(web_dir, f'Experiment = {opt.name}, Phase = {opt.phase}, Epoch = {opt.epoch}')

    # Test with eval mode if specified
    if opt.eval:
        model.eval()
    save_dir = os.path.join(opt.results_dir, opt.name, 'test_latest', 'images')  # Updated path
    os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

 # Test loop for running inference and saving images
    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only test on opt.num_test images
            break
        model.set_input(data)  # unpack data from data loader
        model.test()           # run inference

        visuals = model.get_current_visuals()  # get image results
        img_path = model.get_image_paths()     # get image paths

        # Get original image size from the input image
        original_img_path = data['A_paths'][0]  # This is specific for paired data (use the correct key for your case)
        original_img = Image.open(original_img_path).convert('RGB')
        original_size = original_img.size  # Get original size (width, height)

        # Extract image ID from image path
        img_id = os.path.splitext(os.path.basename(img_path[0]))[0]

        # Resize the output back to original size and save it
        for label, im_data in visuals.items():
            im = util.tensor2im(im_data)  # Convert tensor to image
            im = Image.fromarray(im)  # Convert array to PIL Image
            im = im.resize(original_size, Image.BICUBIC)  # Resize to original size

            # Save resized image in the specified directory
            save_path = os.path.join(save_dir, f'{label}_{img_id}.png')
            im.save(save_path)  # Save the resized image

        webpage.save()  # Save the final HTML results
