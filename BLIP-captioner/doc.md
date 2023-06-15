# Description

This is a custom wrapper for SalesForce's BLIP to automatically caption images.

# How it works

It basically scans recursively through your source image folder(s) and creates a .txt file for each image (png or jpg) found. It gives the txt file the same name as the image file and puts the caption into the text file.
This is then 100% ED compatible.

# How to use it

To run it, you need a GPU and a disk to store your files.  
It does not need to be the most potent thing out there.

I run it for 10GB of data (6000+ images) effortlessly on a dirt cheap 3090 with 10GB GPU ram on vast.ai

The most crucial is bandwidth (for up and download), disk space (if you run large datasets)

When setting up the instance, you can use any image that enables Jupiter. I did it on the Vast TensorFlow Image.

You can either run the code using the Notebook available, or, directly in the instance's terminal.
If you run it throuh the terminal you can NOT run the entire file at once.
You will haveto split it into single parts. 

To understand how to split it, or, if you just generally prefer Notebooks, there is oen available in the repo.
I do not reccomend the notebook for very large datasets, as it can cause some unexpected warnings in the screen of the Jupiter notebook

If using the notebook run EACH cell after each other, do NOT run them all at once.

See the code for more comments.