# encoding: utf-8
# author: Matheus D. Rodrigues

### Imports
from PIL import Image, ImageDraw
from pathlib import Path
from time import time

### Sub Programs (Functions)
def normalization(img):
    pix = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            oP = pix[x, y]

            nColor = 0
            for c in oP:
                nColor += c
            nColor = int(round((nColor/3)))

            nP = [nColor, nColor, nColor]

            pix[x, y] = tuple(nP)
    return img

def dither(img):
    pix = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            oP = pix[x, y][0]

            nP = 255 if oP > 127 else 0

            pErr = oP - nP

            Ntuple = [int(round(nP)), int(round(nP)), int(round(nP))]
            pix[x, y] = tuple(Ntuple)

            if (x+1 < img.size[0]):
                oP = pix[x+1, y][0]
                nP = oP + (pErr * (7/16))
                pix[x+1, y] = tuple([int(round(nP)), int(round(nP)), int(round(nP))])

            if (x-1 > 0 and y+1 < img.size[1]):
                oP = pix[x-1, y+1][0]
                nP = oP + (pErr * (3/16))
                pix[x-1, y+1] = tuple([int(round(nP)), int(round(nP)), int(round(nP))])

            if (y+1 < img.size[1]):
                oP = pix[x, y+1][0]
                nP = oP + (pErr * (5/16))
                pix[x, y+1] = tuple([int(round(nP)), int(round(nP)), int(round(nP))])

            if (x+1 < img.size[0] and y+1 < img.size[1]):
                oP = pix[x+1, y+1][0]
                nP = oP + (pErr * (1/16))
                pix[x+1, y+1] = tuple([int(round(nP)), int(round(nP)), int(round(nP))])
            
    return img

def get_data(img, lista):
    pix = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            valor = 0 if pix[x, y][0] == 255 else 1
            res = [valor, x, y]
            lista.append(res)
    return lista

def remap(inMin, inMax, outMin, outMax):
    def remaper(x): 
        return ((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)
    return remaper

def draw_canvas(lista, canvas, size, blockSize):
    draw = ImageDraw.Draw(canvas)
    for pix in lista:
        if pix[0] == 0:
            pass
        else:
            colorBlock = remap(0, size, 0, 255)
            r = int(round(colorBlock(pix[1])))
            g = int(round(colorBlock(pix[2])))
            b = int(round(colorBlock((pix[1] + pix[2]/2))))
            blockColor = [g, r, b, 255]

            x1 = (pix[1] * blockSize)                   +   10
            x2 = ((pix[1] * blockSize) + blockSize)     -   10
            y1 = (pix[2] * blockSize)                   +   10
            y2 = ((pix[2] * blockSize) + blockSize)     -   10
            xy = [(x1, y1), (x2, y2)]
            draw.rectangle(xy, tuple(blockColor), None)
    return canvas

### Main Program (Calls and fine detailing)
t0 = time()
myPath = 'c:/Users/MatheusDinizRodrigue/Documents/Testes/PY/Image Manipulation/'
fileName = str(input('Insert the image\'s name: \n'))
typeFile = int(input('1 - .jpg; \n2 - .png.\n'))
typeFile = '.jpg' if typeFile == 1 else '.png'

img = Image.open(myPath+fileName+typeFile).convert('RGB')
tam = int(input('size of the Canvas\n'))
tam = [tam, int(round(tam * (img.size[1] / img.size[0])))]
img = img.resize(tuple(tam))
blockSize = int(input('Inform the Size of each block: \n'))
canvasSize = [tam[0] * blockSize, tam[1] * blockSize]
canvas = Image.new('RGBA', tuple(canvasSize), (255, 255, 255, 0))

img = normalization(img)
img = dither(img)
lista = []
lista = get_data(img, lista)

canvas = draw_canvas(lista, canvas, img.size[0], blockSize)
canvas.save(fileName+'_draw.png')
t1 = time()

print("Execution Time: %f " %(t1 - t0))