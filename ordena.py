# encoding: utf-8
# author: Matheus D. rodrigues

### Imports
from PIL import Image
from time import time

### Sub Programs
def ordena(img):
    lista = []
    pix = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            data = [x, y, pix[x, y]]
            lista.append(data)

    for i in range(0, len(lista)-1):
        mini = i
        for j in range(i, len(lista)):
            colors_i = ((lista[i][2][0]*100) + (lista[i][2][1]*10) + (lista[i][2][2]))/3
            colors_j = ((lista[j][2][0]*100) + (lista[j][2][1]*10) + (lista[j][2][2]))/3
            print('checking', i, j ,sep=" | ")

            if colors_i < colors_j:
                mini = j
        if mini != i:
            print('changing things up')
            lista[i], lista[mini] = lista[mini], lista[i]
    return lista

def create_canvas(lista, canvas):
    pix = canvas.load()
    for y in range(canvas.size[1]):
        for x in range(canvas.size[0]):
            ind = (canvas.size[0]*y)+x
            pix[x, y] = lista[ind][2]
    return canvas

### Main Program
t0 = time()
myPath = 'c:/Users/MatheusDinizRodrigue/Documents/Testes/PY/Image Manipulation/'
fileName = str(input('Insert the image\'s name: \n'))
typeFile = int(input('1 - .jpg; \n2 - .png.\n'))
typeFile = '.jpg' if typeFile == 1 else '.png'

img = Image.open(myPath+fileName+typeFile).convert('RGB')

lista = ordena(img)
canvas = Image.new('RGB', img.size, (255, 255, 255))

canvas = create_canvas(lista, canvas)
canvas.save(fileName+'_ordena.jpg')
t1 = time()

print("Execution time: %d" %(int(round(t0-t1))))