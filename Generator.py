import multiprocessing as mp

from PIL import Image
from PIL import ImageStat
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps

import os
import numpy as np
import matplotlib.pyplot as plt
import time as time
import math as math
import cv2
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dataset_size", type=int,
                    help="Size of the generated dataset")
parser.add_argument("-lv", "--large_vocab", action="store_true",
                    help="Use Large Vocab, Default is Small Vocab")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="(Verbose) Display progress of generation")
parser.add_argument("-mt", "--multithreading", action="store_true",
                    help="Use multithreading")


# Get how bright an image is
def get_brightness(im_file, file_mode = False):
    if file_mode:    
        im = Image.open(im_file)
    else:
        im = im_file
    stat = ImageStat.Stat(im)
    gs = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)) 
         for r,g,b in im.getdata())
    return sum(gs)/stat.count[0]


# Get Color for font, depending on brightness of background
def get_color(brightness, sample = False):
    T = random.randint(175, 255)
    
    color_brightness = 0
    if brightness > 130:
        color_brightness = 0
        while True:
            R, G, B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            color_brightness = math.sqrt(0.299*(R**2) + 0.587*(G**2) + 0.114*(B**2))
            if color_brightness < 10:
                break
    elif brightness < 130:
        color_brightness = 0
        while True:
            R, G, B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            color_brightness = math.sqrt(0.299*(R**2) + 0.587*(G**2) + 0.114*(B**2))
            if color_brightness > 240:
                break
    
    if sample:
        sample_draw(R, G, B, T)
    
    return color_brightness, R, G, B, T


def get_text_image(it, dataset_size, hindi_vocab, background_images, Fonts):
    text = random.choice(hindi_vocab)
    back = random.choice(background_images)
    font = random.choice(Fonts)

    brightness = get_brightness(Image.open(back))
    col, R, G, B, T = get_color(brightness)
        
    base = Image.open(back)
    font = ImageFont.truetype("Fonts/"+font, 30, layout_engine=ImageFont.LAYOUT_RAQM, encoding = "unic")
    txt = Image.new('L', (font.getsize(text)[0], font.getsize(text)[1]))
    
    draw = ImageDraw.Draw(txt)
    
    draw.text((3, 0), text, font=font, fill=T)
    
    angle = random.randint(-4, 4)
    w = txt.rotate(angle,  expand=1)
    
    base.paste(ImageOps.colorize(w, (0,0,0), (R, G, B)), (0,0),  w)
    im1 = base.crop((0, 0, w.size[0]+3, w.size[1]+3))
    im1.save("Train/"+str(it)+".jpg")
    
    f = open("annotations.txt", "a+")
    f.write(str(it) + " " + text + "\n")
    f.close()

    print("Actual progress:- ", (it+1), " / ", dataset_size)

    return im1


def runner(ds, vocab_v, mt, verbose):

    dataset_size = ds
    vocab_index = 0
    background_index = 0
    font_index = 0

    if ds < 1:
        print("Enter valid dataset size!")
        return

    try:
        os.mkdir("Train")
    except FileExistsError:
        print("Train Directory exists!")

    hindi_vocab = []
    if vocab_v == "small":
        f = open("Small_hindi_vocab.txt", "r")
    else:
        f = open("Large_hindi_vocab.txt", "r")
    lines = f.readlines()

    for word in lines:
        hindi_vocab.append(word[:-1])
            
    f.close()

    # Store Background Images
    background_images = []
    for img in os.listdir("Backgrounds/"):
        if img.startswith('.') is False:
            background_images.append("Backgrounds/" + img)

    # Store Fonts
    Fonts = []
    for font in os.listdir("Fonts/"):
        if font.startswith('.') is False:
            Fonts.append(font)

    if mt:
        pool = mp.Pool(mp.cpu_count())
        [pool.apply_async(get_text_image, args=(i, dataset_size, hindi_vocab, background_images, Fonts)) for i in range(dataset_size)]
        pool.close()
        pool.join()
    else:
        for i in range(dataset_size):
            get_text_image(i, dataset_size, hindi_vocab, background_images, Fonts)

    print("Dataset generation complete!")
    

if __name__ == '__main__':
    args = parser.parse_args()

    ds = args.dataset_size
    vocab_v = args.large_vocab
    mt = args.multithreading
    verbose = args.verbose

    runner(ds, vocab_v, mt, verbose)

