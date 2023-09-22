import sys
from PIL import Image
import json
import re

def extract_image_metadata(image_path):
    try:
        # Open the image using PIL
        image = Image.open(image_path)

        # Get the metadata dictionary
        metadata_dict = image.info
        print(metadata_dict)
        if 'parameters' in metadata_dict:
            parameters = metadata_dict['parameters']

            # Extract details from the parameters string
            prompt_match = re.search(r"\(\((.*)\)\)", parameters)
            neg_prompt_match = re.search(r"Negative prompt: ([^\n]+)", parameters)
            steps_match = re.search(r"Steps: (\d+)", parameters)
            sampler_match = re.search(r"Sampler: ([^\n]+)", parameters)
            cfg_scale_match = re.search(r"CFG scale: (\d+)", parameters)
            seed_match = re.search(r"Seed: (\d+)", parameters)
            size_match = re.search(r"Size: ([^\n]+)", parameters)
            model_hash_match = re.search(r"Model hash: ([^\n]+)", parameters)
            model_match = re.search(r"Model: ([^\n]+)", parameters)
            denoising_strength_match = re.search(r"Denoising strength: ([^\n]+)", parameters)
            mask_blur_match = re.search(r"Mask blur: (\d+)", parameters)

            if prompt_match:
                print("Prompt:", prompt_match.group(1))

            if neg_prompt_match:
                print("Negative Prompt:", neg_prompt_match.group(1))

            if steps_match:
                print("Steps:", steps_match.group(1))

            if sampler_match:
                print("Sampler:", sampler_match.group(1))

            if cfg_scale_match:
                print("CFG Scale:", cfg_scale_match.group(1))

            if seed_match:
                print("Seed:", seed_match.group(1))

            if size_match:
                print("Size:", size_match.group(1))

            if model_hash_match:
                print("Model Hash:", model_hash_match.group(1))

            if model_match:
                print("Model:", model_match.group(1))

            if denoising_strength_match:
                print("Denoising Strength:", denoising_strength_match.group(1))

            if mask_blur_match:
                print("Mask Blur:", mask_blur_match.group(1))

        if 'sd-metadata' in metadata_dict:
            sd_metadata = metadata_dict['sd-metadata']
            sd_metadata_dict = json.loads(sd_metadata)

            if 'image' in sd_metadata_dict:
                image_info = sd_metadata_dict['image']

                if 'prompt' in image_info:
                    print("Prompt:", image_info['prompt'])

                if 'steps' in image_info:
                    print("Steps:", image_info['steps'])

                if 'cfg_scale' in image_info:
                    print("CFG Scale:", image_info['cfg_scale'])

                if 'seed' in image_info:
                    print("Seed:", image_info['seed'])

                if 'postprocessing' in image_info:
                    print("Postprocessing:")
                    for item in image_info['postprocessing']:
                        print("- Type:", item['type'])
                        if 'strength' in item:
                            print("  Strength:", item['strength'])
                        if 'scale' in item:
                            print("  Scale:", item['scale'])
                        if 'denoise_str' in item:
                            print("  Denoise Strength:", item['denoise_str'])

    except (AttributeError, KeyError, IndexError):
        print("No metadata found.")

# Get the file path from command-line arguments
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    # Prompt the user to enter the file path if not provided as an argument
    file_path = input("Enter the file path: ")

# Remove any leading or trailing spaces
file_path = file_path.strip()

# Call the function to extract metadata from the image
extract_image_metadata(file_path)
