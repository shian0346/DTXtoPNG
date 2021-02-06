import os
import sys
import base64
import information
import pixels
import graphics
from PIL import Image
from pathlib import Path

# open chip and background images
print("reading image files...")
image_folder = os.path.join(Path(__file__).parent, "images")
bg = Image.open(os.path.join(image_folder, "BG.png"))
bd = Image.open(os.path.join(image_folder, "BD.png"))
cy = Image.open(os.path.join(image_folder, "CY.png"))
ft = Image.open(os.path.join(image_folder, "FT.png"))
hh = Image.open(os.path.join(image_folder, "HH.png"))
ht = Image.open(os.path.join(image_folder, "HT.png"))
lc = Image.open(os.path.join(image_folder, "LC.png"))
lp = Image.open(os.path.join(image_folder, "LP.png"))
lt = Image.open(os.path.join(image_folder, "LT.png"))
sd = Image.open(os.path.join(image_folder, "SD.png"))
bl = Image.open(os.path.join(image_folder, "BGL1.png"))
sl = Image.open(os.path.join(image_folder, "BGL2.png"))

# get simfiles' directories
print("reading simfiles...")
intputdir = os.path.join(Path(__file__).parent, "input")
simfiles = os.listdir(intputdir)
chartsdir = os.path.join(Path(__file__).parent, "output")

# iterate through all simfiles
progress_checker = 0
invalid = '<>:"/\|?*' 
for simfile in simfiles:
    # open simfile
    opendir = os.path.join(intputdir, simfile)
    # convert simfile into information
    d = information.dictify(opendir)
    # convert information into pixel positions
    p = pixels.getpixels(d)
    l = pixels.getlength(d)
    # set saving directory
    filename = str(d["ARTIST"])+" "+str(d["TITLE"])+" "+str(d["DLEVEL"])+".png"
    for char in invalid: filename = filename.replace(char, '') # remove invalid characters
    savedir = os.path.join(chartsdir, filename)
    # make chart
    chart_img = graphics.compose(graphics.extend_bg(bg,l), bl, sl, lc, hh, lp, sd, ht, bd, lt, ft, cy, l, p)
    try: chart_img.save(savedir)
    except: chart_img.save(os.path.join(chartsdir, "invalid_songname"+" "+str(d["DLEVEL"])+".png"))
    # report
    progress_checker += 1
    print('{:.1%}'.format(progress_checker/len(simfiles))+" DONE: "+d["TITLE"]+" "+str(d["DLEVEL"]))