# Usage

- install requirements by running `pip install -r requirements.txt`
- run program by calling `python genericscraper.py` (depending on your python handle you might need to use `python3`)
- input data as asked
- The `genericscrape.py` is the newer version, `downloadimgs.py` is the older, and less flexible variant that needs you to check the target source HTML and make amendments to the python source. `downloadimgs2.py` is a script optimised for `wallpaperflare.com` wich has quite a few high res images 

# Wikipedia (only for `genericscrape.py`)

to scrape images from wikipedia, enter for example a url to an artists "list of works"
usually in wikipedia that is a table with a lot of images.
If it is not available and only some images in the main article are available, just enter that URL

Then say `y` for "nable Wikipedia processing"

Add `a` as the html tag, and `image` as the class
(as of date of writing, please check wikipedia source)

Enter the folder to save your images and hit enter.

This code is capable of downloading thousands of images in a few minutes.
Check your images afterwards: sometimes, it fails to download very large files.
(also check the script `findempty.py` in this same repo for that exact task)

Also, you may want to purge low res images, for that, check the script `purgelowres.py` and adapt is as per your needs.

If you want to ensure you have no images with text in them, check the script `text-scanner.py`

# Misc

This code _can bypass cloudflare bot and scraping sec checks_. It is up to you to do that, I am not encouraging you to "break the law"

This code can scrape any website where images are stored in an `img` tag that is inside (any) html tag whith a distinc `class`
