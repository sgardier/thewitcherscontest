import pygame
import random
import settings
"""
@Author :   YANG    Lei     (S201970)
            GARDIER Simon   (S192580)

decor.py : Script permettant d'afficher les décors
"""

#représentation de la carte
MAP = [
        ['┏', '━', '━', '━', '━', '━', '┳', '━', '━', '━', '━', '┳', '━', '━', '━', '━', '┳', '━', '━', '━', '━', '━', '━', '┓'],
        ['┃', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', '┗', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', '━', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', '↦', '━', '┫'],
        ['┃', ' ', ' ', ' ', ' ', ' ', '┗', '━', '━', '━', '━', ' ', ' ', ' ', ' ', ' ', '↥', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '━', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', '↦', '┳', '↤', ' ', ' ', ' ', ' ', ' ', ' ', '┏', '┓', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', '┃', ' ', ' ', ' ', ' ', '━', ' ', ' ', '┗', '┛', ' ', ' ', '━', '━', '━', '┛', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', '↥', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '↧', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', '↦', '━', '┓', ' ', ' ', ' ', ' ', '┃'],
        ['┃', ' ', '━', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', ' ', ' ', '┃', ' ', ' ', ' ', ' ', '┃'],
        ['┗', '━', '━', '━', '━', '━', '━', '━', '━', '━', '━', '┻', '━', '━', '━', '━', '━', '━', '┻', '━', '━', '━', '━', '┛']
]
MAP_SIZE = (len(MAP[0]), len(MAP))
CASE_SIZE = settings.WINDOW_DIMENSIONS[0] / MAP_SIZE[0]

"""
Wall(Sprite) : classe représentant un mur
"""
class Wall(pygame.sprite.Sprite):

    #Disctionnaire d'images dans lequel on pioche pour créer un mur ayant la bonne orientation
    WALL_PATHS = {
        '┃': pygame.image.load('../medias/decor/walls/vertical-wall.png'),
        '━': pygame.image.load('../medias/decor/walls/horizontal-wall.png'),
        '┓': pygame.image.load('../medias/decor/walls/top-right.png'),
        '┛': pygame.image.load('../medias/decor/walls/bottom-right.png'),
        '┏': pygame.image.load('../medias/decor/walls/top-left.png'),
        '┗': pygame.image.load('../medias/decor/walls/bottom-left.png'),
        '↤': pygame.image.load('../medias/decor/walls/horizontal-wall.png'),
        '↦': pygame.image.load('../medias/decor/walls/horizontal-wall.png'),
        '↥': pygame.image.load('../medias/decor/walls/vertical-wall.png'),
        '↧': pygame.image.load('../medias/decor/walls/vertical-wall.png'),
        '┳': pygame.image.load('../medias/decor/walls/triple-top.png'),
        '┻': pygame.image.load('../medias/decor/walls/triple-bottom.png'),
        '┫': pygame.image.load('../medias/decor/walls/triple-right.png'),
        '┣': pygame.image.load('../medias/decor/walls/triple-left.png')
    }
    def __init__(self, sprite, topleft):
        super().__init__()
        self.image = sprite.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
"""
Ground(Sprite) : Classe représentant un sol
"""
class Ground(pygame.sprite.Sprite):
    
    #Liste d'images dans laquelle on pioche de façon aléatoire pour créer un sol
    GROUND_IMAGES = [
        pygame.image.load('../medias/decor/ground/ground.png'),
        pygame.image.load('../medias/decor/ground/ground1.png')
    ]
    def __init__(self, topleft):
        super().__init__()
        self.image = Ground.GROUND_IMAGES[random.randrange(2)].convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

