import pygame
import sys
"""
@Author :   YANG    Lei     (S201970)
            GARDIER Simon   (S192580)

KeysManager : Détermine quelles touches sont pressées et publie les résultats
"""
class KeysManager():

    def __init__(self, subscribers, keys_map):
        #liste d'abonnés nécessitant une liste de touches pressées
        self.subscribers = subscribers
        #liste de touches dont on veut connaitre l'état
        self.keys_map = keys_map

    """
    manage_keys() : met à jour self.keys_map en fonction des touches pressées lors de l'appel à manage_keys()
    """
    def manage_keys(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evenement.type == pygame.KEYDOWN:
                if evenement.key in self.keys_map:
                    self.keys_map[evenement.key] = True
            if evenement.type == pygame.KEYUP:
                if evenement.key in self.keys_map:
                    self.keys_map[evenement.key] = False
        self.publish()

    """
    publish() : publie la mise à jour des touches chez les abonnés
    """
    def publish(self):
        for subscriber in self.subscribers:
            subscriber.publish(self.keys_map)
