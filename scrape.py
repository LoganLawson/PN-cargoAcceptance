#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 18:27:07 2022

@author: ll
stolen from
https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
"""

import os
import requests
from pdfminer.high_level import extract_text_to_fp
import tempfile

def getpdf(url, path, filename):
    response = requests.get(
        url,
        allow_redirects=True)
    open(path.name +'/' + filename, 'wb').write(response.content)
    
def extractImages(path, filename):
    tf = open("new.txt", "w")
    f = open(path.name + "/" + filename, "rb")
    extract_text_to_fp(f, tf, output_dir=path.name + "/pics")
    f.close()
    tf.close()
     
def main():
    url = "http://web.portnelson.co.nz/Webcam/CargoAcceptance.pdf" 
    filename = "x.pdf"
    path = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None, ignore_cleanup_errors=False)
    getpdf(url, path, filename)
    extractImages(path, filename)
    print(path.name)
    print(os.listdir(path.name))
    print(os.listdir(path.name + '/pics'))
    print(os.listdir(path.name))
    
    
main()
if __name__ == "__main__":
    main()
    
