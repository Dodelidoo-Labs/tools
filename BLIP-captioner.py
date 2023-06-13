##
# !pip3 install transformers==4.15.0 timm==0.4.12 fairscale==0.4.4
# !git clone https://github.com/salesforce/BLIP
# %cd /Path/To/BLIP
##
import sys
import os
from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from models.blip import blip_decoder

def load_demo_image(image_file, image_size, device):
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


image_size = 384
device = 'cuda'  # Assuming you want to use GPU for processing

model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_caption_capfilt_large.pth'
model = blip_decoder(pretrained=model_url, image_size=image_size, vit='base')
model.eval()
model = model.to(device)

image_folder = '/workspace/EveryDream/BLIP/images/'  # Specify the path to the image folder

# Get the list of image files in the folder
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg')]

# ...

for root, folders, files in os.walk(image_folder):
    for file in files:
        if file.endswith('.jpg'):
            image_file = os.path.join(root, file)
            image = load_demo_image(image_file, image_size=image_size, device=device)

            with torch.no_grad():
                # beam search
                caption = model.generate(image, sample=False, num_beams=9, min_length=16, max_length=75, repetition_penalty=100.0)
                # nucleus sampling
                # caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5)
                
            # Create a text file path in the same folder as the image
            txt_file = os.path.splitext(image_file)[0] + '.txt'
            
            # Write the caption to the text file
            with open(txt_file, 'w') as f:
                f.write(caption[0])
                
            print('Caption for {}: {}'.format(image_file, caption[0]))
