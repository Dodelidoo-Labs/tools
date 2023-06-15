##
# This script is a wrapper for SalesForce's BLIP
# @see https://github.com/salesforce/BLIP/
#
# If you run this in terminal make sure to:
# pip3 install transformers==4.15.0 timm==0.4.12 fairscale==0.4.4
# git clone https://github.com/salesforce/BLIP
# cd /root/BLIP
##

##
# Import all necessary libs
##
import sys
import os
from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from models.blip import blip_decoder

##
# Define the function that will load the image
# We pass a stupidly huge max size for images just to avoid BLIP crashing.
# If you have no super large images, this can be commented out
##
Image.MAX_IMAGE_PIXELS = 10000000000000000000000000  # Set a maximum image size (e.g., 1 billion pixels)
def load_images(image_file, image_size, device):
    raw_image = Image.open(image_file).convert('RGB')

    w, h = raw_image.size
    raw_image.thumbnail((w // 5, h // 5))
    raw_image.show()

    transform = transforms.Compose([
        transforms.Resize((image_size, image_size), interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
    ])
    image = transform(raw_image).unsqueeze(0).to(device)
    return image

## 
# Define device, load the model (see SalesForce doc for more models), and define the source image path
##
image_size = 384
device = 'cuda'  # Assuming you want to use GPU for processing
model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_caption_capfilt_large.pth'
model = blip_decoder(pretrained=model_url, image_size=image_size, vit='base')
model.eval()
model = model.to(device)
image_folder = '/root/images/'  # Specify the path to the images folder

## 
# Get the list of image files in the folder
##
image_files = [
    os.path.join(image_folder, file)
    for file in os.listdir(image_folder)
    if file.endswith('.jpg') or file.endswith('.png')
]

## 
# Loop over each image, and create the txt file with caption
##
for root, folders, files in os.walk(image_folder):
    for file in files:
        if file.endswith('.jpg') or file.endswith('.png'):

            image_file = os.path.join(root, file)
            image = load_images(image_file, image_size=image_size, device=device)

            with torch.no_grad():
                ##
                # beam search. 
                # @see https://github.com/victorchall/EveryDream/blob/main/doc/AUTO_CAPTION.md
                # @see https://github.com/salesforce/BLIP/blob/main/demo.ipynb
                #
                # num_beams: the higher the more precise, the more computing time it needs per image
                # max_length: ED supports max 75 and it is not clear if it uses the same tokenizer as BLIP, so the 75 of BLIP might be MORE or LESS than ED's 75!
                # min_length: Above 30 it produces very detailed captions, however repetition also increases, thus, the higher min_lenght, the higher must be repetition_penalty
                # repetition_penalty: The higher, the less repetitions your caption gets
                ##
                caption = model.generate(image, sample=False, num_beams=9, max_length=75, min_length=16, repetition_penalty=100.0)
                # nucleus sampling
                # caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5)
            
            # Create a text file path in the same folder as the image
            txt_file = os.path.splitext(image_file)[0] + '.txt'
            
            # Check if the text file already exists, and skip if it does
            if os.path.exists(txt_file):
                continue

            # Write the caption to the text file
            with open(txt_file, 'w') as f:
                f.write(caption[0])
                
            print('Caption for {}: {}'.format(image_file, caption[0]))