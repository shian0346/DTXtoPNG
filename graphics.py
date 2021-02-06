import os
from PIL import Image

# extend the background image to the length of the song
def extend_bg(bg, length):
    bg_w, bg_h = bg.size
    new_im = Image.new('RGB', (521, length))
    w, h = new_im.size
    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            new_im.paste(bg, (i, j))
    return new_im

# put notes into the extended background image
def compose(bg, bl, sl, lc, hh, lp, sd, ht, bd, lt, ft, cy, length, chart):
    offset = {}
    offset["0"] = -1
    offset["1"] = 71
    offset["2"] = 119
    offset["3"] = 170
    offset["4"] = 228
    offset["5"] = 282
    offset["6"] = 345
    offset["7"] = 395
    offset["8"] = 448
    offset["9"] = 0
    offset["10"] = 0
    img = {}
    img["0"] = lc
    img["1"] = hh
    img["2"] = lp
    img["3"] = sd
    img["4"] = ht
    img["5"] = bd
    img["6"] = lt
    img["7"] = ft
    img["8"] = cy
    img["9"] = bl
    img["10"] = sl
    
    for element in chart:
        lane = str(element[1])
        if element[1] >= 9:
            bg.paste(img[lane], (offset[lane], length-element[0]), img[lane].convert('RGBA'))
        else:
            bg.paste(img[lane], (offset[lane], length-element[0]-31), img[lane])
    
    return bg