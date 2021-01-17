#!/usr/bin/python3
import argparse
import os

from PIL import Image

def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Crop an image into n images.')
    parser.add_argument('infile', help='input image file to crop')
    parser.add_argument('-W', '--width', dest='width', type=int, help='crop width')
    parser.add_argument('-H', '--height', dest='height', type=int, help='crop height')
    parser.add_argument('-o', '--output', dest='output', default='/tmp/crop_script/', help='output folder (default: /tmp/crop_script/)')
    parser.add_argument('-p', '--prefix', dest='prefix', default='crop_', help='crop image prefix (default: "crop_") (eg. "-p myimg_" will generate "myimg_1.png", "myimg_2.png", etc ...)')
    args = parser.parse_args()
    try:
        os.makedirs(args.output)
    except FileExistsError as e:
        pass
    start_num = 0
    for k,piece in enumerate(crop(args.infile,args.height,args.width),start_num):
        img=Image.new('RGBA', (args.height, args.width), 255)
        img.paste(piece)
        path=os.path.join(args.output,args.prefix + str(k) + ".png")
        img.save(path)
