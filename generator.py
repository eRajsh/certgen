from PIL import Image

#brightness_4
# Python program to generate WordCloud

# importing all necessery modules
from textcloud import TextCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageShow, ImageDraw, ImageFont, ImageFilter
import cv2
from sketchify import sketch

# define all variables
PHOTOPATH = ''
BG = ''
FONT = ''
THXFONT = ''
SIGNATUREFONT= ''
TEXTCLOUD = ''
MGRNAME = ""
TEAMMEMBERNAME = ""
STRENGTHPATH = ''
OFOLDERPATH = ''
CERTPATH = ''
CLOUDMASK = ''
MASKOUTLINE = ''
SKETCHSIZE = (700, 700)

# generate sketch
def gen_sketch():
    sketch.normalsketch(PHOTOPATH+TEAMMEMBERNAME+'.png', OFOLDERPATH, TEAMMEMBERNAME+'_sketch', 10)

#soften image edges
def soften_edges(sketch_file):
    # Open an image
    RADIUS = 20

    # Open an image
    im = Image.open(sketch_file)

    # Paste image on white background
    diam = 2 * RADIUS
    back = Image.new('RGB', (im.size[0] + diam, im.size[1] + diam), (255, 255, 255))
    back.paste(im, (RADIUS, RADIUS))

    # Create paste mask
    mask = Image.new('L', back.size, 0)
    draw = ImageDraw.Draw(mask)
    x0, y0 = 0, 0
    x1, y1 = back.size
    for d in range(diam + RADIUS):
        x1, y1 = x1 - 1, y1 - 1
        alpha = 255 if d < RADIUS else int(255 * (diam + RADIUS - d) / diam)
        draw.rectangle([x0, y0, x1, y1], outline=alpha)
        x0, y0 = x0 + 1, y0 + 1

    # Blur image and paste blurred edge according to mask
    blur = back.filter(ImageFilter.GaussianBlur(RADIUS / 2))
    back.paste(blur, mask=mask)
    back.save(sketch_file)
    
# Generate Cloud
def gen_cloud():

    #Load teammember details
    a_file = open(STRENGTHPATH+TEAMMEMBERNAME+'.txt', "r")
    list_of_sentences = [(line.strip()) for line in a_file]
    a_file.close()

    #Generate Strength Sentence Frequency List
    strength_frequency = {}
    count = 30
    iter_num = 0
    for sentence in list_of_sentences:
        iter_num+=1
        strength_frequency[sentence] = count
        count = 22 if iter_num == 1 else 12 if iter_num ==2 else 7 if iter_num ==3 else 4 if iter_num == 4 else 7-iter_num
        if count < 2:
            count=1


    #Select Cloud Shape (mask)
    #sentences = len(list_of_sentences)
    #maskname = 'jetfighter.jpg' if sentences > 25 else 'diamond.jpg' if sentences > 20 else 'oval.jpg' if sentences > 15 else 'diamond.jpg'
    custom_mask = np.array(Image.open(CLOUDMASK))

    #Generate Cloud
    textcloud = TextCloud(width=1000, height=1000,
                          background_color="rgba(255, 255, 255, 0)",
                          mode = 'RGBA',
                          min_font_size=20,
                          max_font_size=400,
                          contour_color = "white",
                          font_path= FONT,
                          mask=custom_mask).generate(strength_frequency)

    #save to file
    strength_cloud=np.array(textcloud)
    cv2.imwrite(OFOLDERPATH+TEAMMEMBERNAME+'_cloud.png', strength_cloud)
    #"""


# Generate the Certificate
def gen_cert():

    # Merge cloud outline on the background
    cloudoutline = Image.open(MASKOUTLINE)
    cert = Image.open(BG)
    cert.paste(cloudoutline, (-60, 1100), cloudoutline)

    # Merge Textcloud on the background
    textcloud = Image.open(OFOLDERPATH+TEAMMEMBERNAME+'_cloud.png')
    cert.paste(textcloud, (-100, 1250), textcloud)

    # Soften the sketch egdes and merge sketch on the background
    sketchfile = OFOLDERPATH+TEAMMEMBERNAME+'_sketch.png'
    soften_edges(sketchfile)
    sktch = Image.open(sketchfile)
    sktch = sktch.resize(SKETCHSIZE)
    cert.paste(sktch, (50, 50))

    # Write Thankyou
    font = ImageFont.truetype(FONT, 75)
    d = ImageDraw.Draw(cert)
    d.text((885, 50), "Thank you ", font=font, fill=(247, 155, 68))

    # Write Name!
    font = ImageFont.truetype(FONT, 250)
    d = ImageDraw.Draw(cert)
    d.text((860, 125), TEAMMEMBERNAME.split(" ", 1)[0], font=font, fill=(247, 155, 68))

    # Signature
    sigfont = ImageFont.truetype(SIGNATUREFONT, 80)
    d.text((1600, 2900), MGRNAME, font=sigfont, fill=(247, 155, 68))

    # Add the Date
    datefont = ImageFont.truetype(FONT, 30)
    d.text((1600, 3030), 'Jan 2021', font=datefont, fill=(247, 155, 68))

    cert.save(CERTPATH+TEAMMEMBERNAME+'.png',"PNG", quality=100)
