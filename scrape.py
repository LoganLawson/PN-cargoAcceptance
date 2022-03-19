#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 18:27:07 2022

@author: ll
stolen from + many others 
https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/amp/
https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
"""

import os
import glob
import requests
from pdfminer.high_level import extract_text_to_fp
import tempfile
from PIL import Image
import cv2
import pytesseract
import imutils

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def getpdf(url, path, filename):
    response = requests.get(
        url,
        allow_redirects=True)
    open(path +'/' + filename, 'wb').write(response.content)
    
def extractLargestImage(path, filename):
    tf = open("new.txt", "w")
    f = open(path + "/" + filename, "rb")
    extract_text_to_fp(f, tf, output_dir=path + "/pics")
    f.close()
    tf.close()
    
    # get largest
    pics = os.listdir(path + "/pics")
    pics = [path + "/pics/" + x for x in pics]
    print(pics)
    largestImage = max(pics, key =  lambda x: os.stat(x).st_size)
    
    for f in pics:
        if f != largestImage:
            print(f)
            os.remove(f)
        
    # return largest image filename for ocr
    return largestImage
        
    
    
def recognise(img, out):
    f = Image.open(img)
    f.save(img[0:-3]+'png', 'png')
    img = img[0:-3]+'png'
    # Read image from which text needs to be extracted
    img = cv2.imread(img)
     
    # Preprocessing the image starts
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
     
    # Specify structure shape and kernel size. 
    # Kernel size increases or decreases the area 
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect 
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
     
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
     
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
    
                                                     cv2.CHAIN_APPROX_NONE)
     
    # Creating a copy of image
    im2 = img.copy()
     
    # A text file is created and flushed
    file = open(out, "w+")
    file.write("")
    file.close()
     
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
    
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        file = open(out, "a")
    
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        # Appending the text into file
        file.write(text)
        file.write("\n")

        # Close the file
        file.close
    
def main():
    # url = "http://web.portnelson.co.nz/Webcam/CargoAcceptance.pdf" 
    # filename = "x.pdf"
    # path = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None, ignore_cleanup_errors=False)
    # getpdf(url, path, filename)
    # extractImages(path, filename)
    # print(path)
    # print(os.listdir(path))
    # print(os.listdir(path + '/pics'))
    # print(os.listdir(path))
    
    # test 1  
    #recognise('test1/pics/x.bmp', 'test1/out.txt')
    
    # test2
    url = "http://web.portnelson.co.nz/Webcam/CargoAcceptance.pdf" 
    filename = "x.pdf"
    path = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None, ignore_cleanup_errors=False)
    path = 'test1'
    getpdf(url, path, filename)
    targetImage = extractLargestImage(path, filename)
    recognise(targetImage, path + '/out.txt')
    
main()
    
    
