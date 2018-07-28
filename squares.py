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
    tamanho = 0
    draw = ImageDraw.Draw(canvas)
    for pix in lista:
        if pix[0] == 1:
            x1 = (pix[1] * blockSize)                  # +   5
            x2 = ((pix[1] * blockSize) + blockSize)    # -   5
            y1 = (pix[2] * blockSize)                  # +   5
            y2 = ((pix[2] * blockSize) + blockSize)    # -   5
            xy = [(x1, y1), (x2, y2)]
            tamanho+=1
            draw.rectangle(xy, '#edc0b4', 'black')
        else:
            ## Definir Cor automaticamente com base na largura da imagem
            # colorBlock = remap(0, size[0], 0, 255)
            # r = int(round(colorBlock(pix[1])))
            # g = int(round(colorBlock(pix[2])))
            # b = int(round(colorBlock((pix[1] + pix[2]/2))))

            # blockColor = [int(r), int(g), int(b), 255]

            # ## Definir cor com base em um padrão pré-selecionado
            # rainbow = [[255 , 0     , 0     , 255], 
            #            [255 , 127   , 0     , 255], 
            #            [255 , 255   , 0     , 255], 
            #            [0   , 255   , 0     , 255],
            #            [0   , 255   , 255   , 255], 
            #            [0   , 0     , 255   , 255], 
            #            [139 , 0     , 255   , 255]]

            # blockColor = [0, 0, 0, 0]
            # base = int(round(size[1]/8))
            # if pix[2] <= base*1:
            #     blockColor = rainbow[0]

            # if pix[2] > base*1 and pix[2] <= base*2:
            #     # R
            #     picker_R = remap(base*1, base*2, rainbow[0][0], rainbow[1][0])
            #     r = picker_R(pix[2])

            #     # G
            #     picker_G = remap(base*1, base*2, rainbow[0][1], rainbow[1][1])
            #     g = picker_G(pix[2])

            #     # B
            #     picker_B = remap(base*1, base*2, rainbow[0][2], rainbow[1][2])
            #     b = picker_B(pix[2])

            #     blockColor = [int(r), int(g), int(b), 255]

            # if pix[2] > base*2 and pix[2] <= base*3:
            #     # R
            #     picker_R = remap(base*2, base*3, rainbow[1][0], rainbow[2][0])
            #     r = picker_R(pix[2])

            #     # G
            #     picker_G = remap(base*2, base*3, rainbow[1][1], rainbow[2][1])
            #     g = picker_G(pix[2])

            #     # B
            #     picker_B = remap(base*2, base*3, rainbow[1][2], rainbow[2][2])
            #     b = picker_B(pix[2])

            #     blockColor = [int(r), int(g), int(b), 255]

            # if pix[2] > base*3 and pix[2] <= base*4:
            #     # R
            #     picker_R = remap(base*3, base*4, rainbow[2][0], rainbow[3][0])
            #     r = picker_R(pix[2])

            #     # G
            #     picker_G = remap(base*3, base*4, rainbow[2][1], rainbow[3][1])
            #     g = picker_G(pix[2])

            #     # B
            #     picker_B = remap(base*3, base*4, rainbow[2][2], rainbow[3][2])
            #     b = picker_B(pix[2])

            #     blockColor = [int(r), int(g), int(b), 255]

            # if pix[2] > base*4 and pix[2] <= base*5:
            #     # R
            #     picker_R = remap(base*4, base*5, rainbow[3][0], rainbow[4][0])
            #     r = picker_R(pix[2])

            #     # G
            #     picker_G = remap(base*4, base*5, rainbow[3][1], rainbow[4][1])
            #     g = picker_G(pix[2])

            #     # B
            #     picker_B = remap(base*4, base*5, rainbow[3][2], rainbow[4][2])
            #     b = picker_B(pix[2])

            #     blockColor = [int(r), int(g), int(b), 255]

            # if pix[2] > base*5 and pix[2] <= base*6:
            #     # R
            #     picker_R = remap(base*5, base*6, rainbow[4][0], rainbow[5][0])
            #     r = picker_R(pix[2])

            #     # G
            #     picker_G = remap(base*5, base*6, rainbow[4][1], rainbow[5][1])
            #     g = picker_G(pix[2])

            #     # B
            #     picker_B = remap(base*5, base*6, rainbow[4][2], rainbow[5][2])
            #     b = picker_B(pix[2])

            #     blockColor = [int(r), int(g), int(b), 255]

            # if pix[2] > base*6 and pix[2] <= base*7:
            #     # R
            #     picker_R = remap(base*6, base*7, rainbow[5][0], rainbow[6][0])
            #     r = picker_R(pix[2])

            #     # G
            #     picker_G = remap(base*6, base*7, rainbow[5][1], rainbow[6][1])
            #     g = picker_G(pix[2])

            #     # B
            #     picker_B = remap(base*6, base*7, rainbow[5][2], rainbow[6][2])
            #     b = picker_B(pix[2])

            #     blockColor = [int(r), int(g), int(b), 255]

            # if pix[2] > base*7:
            #     blockColor = rainbow[6]

            x1 = (pix[1] * blockSize)                  # +   5
            x2 = ((pix[1] * blockSize) + blockSize)    # -   5
            y1 = (pix[2] * blockSize)                  # +   5
            y2 = ((pix[2] * blockSize) + blockSize)    # -   5
            xy = [(x1, y1), (x2, y2)]

            draw.rectangle(xy, 'black', 'white')
    print('%d Gold, %d Preto || %d total \nWidth: %d || Height: %d' %(tamanho, (len(lista)-tamanho), len(lista), img.size[0], img.size[1]))
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

canvas = draw_canvas(lista, canvas, img.size, blockSize)
canvas.save(fileName+'_beads.png')
t1 = time()

print("Execution Time around %d seconds" %(int(round(t1 - t0))))