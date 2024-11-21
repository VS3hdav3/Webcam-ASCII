import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy
import math

ASCII_chars = ["Ñ", "@", "#", "W", "$", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0", "?", "!", "a", "b", "c", ";", ":", "+", "=", "-", ",", ".", "_"]
charsLength = len(ASCII_chars)
interval = charsLength/256
scaleFactor = 0.15
oneCharWidth = 10
oneCharHeight = 18
width = 0
height = 0
video_capture = cv2.VideoCapture(0)
fnt = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', 15)
four_cc = cv2.VideoWriter_fourcc(*"mp4v") # Format of video saved

def getChar(inputInt):
    return ASCII_chars[math.floor(inputInt * interval)]

def main():
    run = True
    first = True
    while run:
        _,im = video_capture.read()
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        color_converted = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(color_converted)
        width, height = im.size
        im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
        width, height = im.size
        scale = (oneCharWidth * width, oneCharHeight * height)
        
        if first:
            out = cv2.VideoWriter("video.mp4", four_cc, 20, scale)
            first = False
        
        pix = im.load()
        outputImage = Image.new('RGB', scale, (0, 0, 0))
        d = ImageDraw.Draw(outputImage)
        
        for i in range(height):
            for j in range(width):
                r, g, b = pix[j, i]
                h = int(r / 3 + g / 3 + b / 3)
                pix[j, i] =  (h, h, h)
                d.text((j * oneCharWidth, i * oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))
        
        outputImage = numpy.array(outputImage)
        outputImage = outputImage[:, :, ::-1].copy()
        cv2.imshow("Webcam-ASCII", outputImage)
        out.write(outputImage)
        
        if cv2.waitKey(1) == ord('q'):
            run = False
        
    
    out.release()
    video_capture.release()
    cv2.destroyAllWindows()

main()