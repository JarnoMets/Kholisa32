from PIL import Image
import sys

def convert_type(raw_img, t_in = "RGBA8888", t_out = "ARGB1555"):
    ret_img = []
    for (i in range(0, len(raw_image)//4)):
        word = ((raw_img[3+i]>0)<<15)+((raw_img[0+i]&0xf8)<<7)+((raw_img[1+i]&0xf8)<<2)+((raw_img[2+i]&0xf8)>>3)
        ret_img.append((word&0xff00)>>8)
        ret_img.append(word&0x00ff)
    
    return bytearray(ret_img)



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
    ARGB1555 = convert_type(a_raw)
    
    fout.write(bytes(ARGB1555))
    
    fout.close()

    return 0






if __name__ == "__main__":
    print("Finished program with error code " + str(main(len(sys.argv), sys.argv)))