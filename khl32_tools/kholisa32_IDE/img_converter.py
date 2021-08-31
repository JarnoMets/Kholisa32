# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets

from PIL import Image
import sys

class Img_converter:
    def __init__(self):
        pass

    def convert_type(raw_img: bytearray, t_in: str = "RGBA8888", t_out: str = "ARGB1555") -> bytearray:
        ret_img = []
        for i in range(0, len(raw_img)//4):
            word = ((raw_img[3+i]>0)<<15)+((raw_img[0+i]&0xf8)<<7)+((raw_img[1+i]&0xf8)<<2)+((raw_img[2+i]&0xf8)>>3)
            ret_img.append((word&0xff00)>>8)
            ret_img.append(word&0x00ff)

        return bytearray(ret_img)

    def convert_img_to_RGBA8888(img) -> bytearray:
        img.load()
        return bytearray(img.tobytes())


    def convert_icon(img) -> bytearray:
        new_img = img.resize((64,64))
        return Img_converter.convert_type(Img_converter.convert_img_to_RGBA8888(new_img))

    def main(argc, argv):
        if argc < 2:
            print("No input file given!")
            return -1

        try:
            img = Image.open(argv[1])
        except:
            print('Could not find "' + argv[1] + '"')
            return -2

        if argc > 2:
            try:
                fout = open(argv[2], "wb")
            except:
                print('Could not open "' + argv[2] + '"')
                return -2
        else:
            fout = open("output.raw","wb")

        img.load()
        raw = img.tobytes()
        a_raw = bytearray(raw)
        ARGB1555 = Img_converter.convert_type(a_raw)

        fout.write(bytes(ARGB1555))

        fout.close()

        return 0
