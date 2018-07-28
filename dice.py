# encoding: utf-8
# author: Matheus D. Rodrigues

### Imports
from PIL import Image, ImageDraw
from time import time

### Global Variables

### Sub Programs
def normalization(img):
    pix = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            oP = pix[x, y]
            nC = int(round((oP[0] * 299/1000) + (oP[1] * 587/1000) + (oP[2] * 114/1000)))
            nP = [nC, nC, nC]

            pix[x, y] = tuple(nP)
    return img

def dither(img):
    pix = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            oP = pix[x, y][0]

            nP = int(round((oP/255)*6) * 255/6)

            pErr = oP - nP

            newPixel = [nP, nP, nP]
            pix[x, y] = tuple(newPixel)

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

def create_list(img, lista):
    pix = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            data = pix[x, y][0]

            data = int(round(data / (255 / 6)))
            
            dados = [x, y, data]
            lista.append(dados)
    return lista

def create_canvas(lista, canvas, blockSize):
    draw = ImageDraw.Draw(canvas)
    for pix in lista:
        if pix[2] == 1:         # 6
            block = blockSize/5
            
            for j in range(1, 6):
                for i in range(1, 6):
                    if 
    return canvas




t0 = time()
myPath = 'c:/Users/MatheusDinizRodrigue/Documents/Testes/PY/Image Manipulation/'
fileName = str(input('Insert the image\'s name: \n'))
typeFile = int(input('1 - .jpg; \n2 - .png.\n'))
typeFile = '.jpg' if typeFile == 1 else '.png'
img = Image.open(myPath+fileName+typeFile).convert('RGB')
tam = int(input('size of the Canvas\n'))
tam = [tam, int(round(tam * (img.size[1] / img.size[0])))]
img = img.resize(tuple(tam))
lista = []
img = normalization(img)
img = dither(img)
img = create_list(img, lista)

blockSize = int(input('Inform the Size of each dice(multiple of 5): \n'))
canvasSize = [tam[0] * blockSize, tam[1] * blockSize]
canvas = Image.new('RGB', tuple(canvasSize), (255, 255, 255))

c = create_canvas(lista, canvas, blockSize)