#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:40:51 2022

@author: henry
"""


import argparse
import os
import fitz # install using: pip install PyMuPDF


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default= 'input', help='folder of documents to be evaluated')
parser.add_argument('--output', type=str, default= 'classification.csv', help='csv with name of document and classification')
opt, unknown = parser.parse_known_args()


path, output = opt.path, opt.output

pdf_files = [f for f in os.listdir(path) if f.endswith('.pdf')]


for file in pdf_files:

my_pdf = 'input/REGISTRO_01609857H.pdf'

my_pdf = 'input/JustificantePresentación_40798540J.pdf'

from PyPDF2 import PdfReader

reader = PdfReader(my_pdf)
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
    


# ================== pip install PyMuPDF ======================== #


with fitz.open(my_pdf) as doc:
    text = ""
    for page in doc:
        text += page.get_text()

print(text)
