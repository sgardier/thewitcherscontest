import pygame
pygame.init()
import game
import settings
"""
@Author :   YANG    Lei     (S201970)
            GARDIER Simon   (S192580)

main.py : Script de lancement du jeu
"""

"""INITIALISATION"""
pygame.display.set_caption(settings.GAME_TITLE)
clock           = pygame.time.Clock()
window          = pygame.display.set_mode(settings.WINDOW_DIMENSIONS)
sprites_group   = pygame.sprite.pygame.sprite.RenderUpdates()
pygame.display.set_icon(settings.icon)

"""GAME MANAGER LOADING"""
game = game.Game(window, settings.FPS, clock, settings.GAME_TITLE)

"""LAUCH THE GAME"""
game.loop()