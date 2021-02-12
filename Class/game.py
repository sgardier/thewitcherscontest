import pygame
import menu
import party
import player
import keys_manager
"""
@Author :   YANG    Lei     (S201970)
            GARDIER Simon   (S192580)

Game() : Classe gérant la logique du programme et tous ses composants
        - Les objets player
        - Les menus de départ/fin
        - La partie en elle-même
        - L'interaction clavier et écran
"""

class Game():

    def __init__(self, window, fps, clock, title):
        self.window = window
        self.window_size = self.window.get_size()
        self.FPS = fps
        self.clock = clock
        self.inGame = True
        self.quit_key = pygame.K_ESCAPE
        self.menu = menu.Menu(self.window_size, self.window, title, True)
        self.end_menu = menu.EndMenu(self.window_size, self.window, False)
        self.party = party.Party(self.window, False)
        self.keys_map = {
            self.party.party_key : False,
            self.menu.menu_key : False,
            self.quit_key : False
        }
        self.keys_map.update(player.Player.all_players_keys)
        self.subscribers = [self, self.party]
        self.keys_manager = keys_manager.KeysManager(self.subscribers, self.keys_map)

    """
    loop() : boucle principale du programme (appelé dans main.py)
    """
    def loop(self):
        while self.inGame:
            #enregistre les touches pressées (et publie le dictionnaire obtenu)
            self.keys_manager.manage_keys()
            if self.menu.inMenu:
                self.menu.draw()
            if self.party.inParty:
                if self.party.generated:
                    if not self.party.play():
                        self.end_menu.inEndMenu = True
                else:
                    self.party.create()
            if self.end_menu.inEndMenu:
                self.end_menu.set_loser(self.party.loser)
                self.end_menu.draw()

            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    """
    publish(keys) : effectue les actions demandés par l'utilisateur en fonction du contexte
    @param dictionnaire des touches utilisées dans le jeu avec comme valeur True|False
    """
    def publish(self, keys):
        #Quitte le programme
        if keys[self.quit_key]:
            self.inGame = False
        if self.end_menu.inEndMenu:
            #Si le joueur veut revenir au menu principal
            if keys[self.menu.menu_key]:
                self.end_menu.inEndMenu = False
                self.end_menu.death_message = None
                self.menu.inMenu = True
        if self.menu.inMenu:
            #Si le joueur veut lancer une nouvelle partie
            if keys[self.party.party_key]:
                self.menu.inMenu = False
                self.party.inParty = True