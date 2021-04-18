import argparse
from enum import Enum
import io
import PySimpleGUI as sg

from google.cloud import vision
from PIL import Image, ImageDraw


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def OpenPic(input_file_path, output_file_path):
    with Image.open(input_file_path) as im:
        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
        im.show()
        # write to stdout
        im.save(output_file_path, "PNG")


if __name__ == '__main__':
    sg.theme("dark blue 3")
    layout = [
        [sg.Text("   Input File"), sg.Input(key="InputFile"), sg.FilesBrowse(key="InputBrowse")],
        [sg.Text("Output File"), sg.Input(key="OutputFile"), sg.FilesBrowse(key="OutputBrowse")],
        [sg.Open(), sg.Cancel()] 
    ]
    window = sg.Window("Select File",layout=layout)

    event, values = window.read()
if event =="Open":
    inputFile = values["InputFile"]
    outputFile = values["OutputFile"]
    OpenPic(inputFile, outputFile)
else:
    exit()
    
