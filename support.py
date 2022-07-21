from csv import reader
from os import listdir
import pygame


def csv_import(filepath):  # import csv for map layout
    map=[]
    with open(filepath) as file:
        raw = reader(file, delimiter = ',')
        for row in raw:
            map.append(list(row))

        return map

def import_graphics(filepath): # helper fcn for importing graphics
    filelist = []
    imagelist = []
    for file in sorted(listdir(filepath)):
        filelist.append(file)

    for file in filelist:
        image = pygame.image.load(f'{filepath}/{file}').convert_alpha()
        imagelist.append(image)

    return imagelist





