# Usage

Helps you find most common aspect ratios in a dataset, then run over them and either resize or crop any outlyiers

1. Run `arlister.py`
2. Update `arcleaner.py` `aspect_ratios` with the Ar's of your dataset
3. Activate `Add user input check after each image processing` code section in `get_closest_aspect_ratio` function and comment out these 2 sections in the code:
```
resized_img = img.resize((resize_width, resize_height))
resized_img.save(file_path)
```
```
cropped_img = img.crop((left, top, right, bottom))
cropped_img.save(file_path)
```
4. Run the script - it will be useful to see by how much how many images are resized or cropped. You can abort (`n`) or proceed (`y`)
5. Finally run the script with the code from step 3 reverted to original (you can keep the safecheck `y/n` of course) to run the script and effectively resize/crop


# Additional
The `archecker.py` creates a CSV with all aspect ratios found and count of images in each.


