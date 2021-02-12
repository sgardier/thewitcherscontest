import pygame
import settings
"""
@Author :   YANG    Lei     (S201970)
            GARDIER Simon   (S192580)

PlayerBoard(Sprite) : Classe représentant les informations placées au bas d'un joueur
"""
class PlayerBoard(pygame.sprite.Sprite):
    #images du statut de vie
    HP_IMAGES         = [
        pygame.image.load('../medias/board/heart/0.png'),
        pygame.image.load('../medias/board/heart/1.png'),
        pygame.image.load('../medias/board/heart/2.png'),
        pygame.image.load('../medias/board/heart/3.png')
    ]
    #image du statut de recharge d'énergie pour le sort
    COOLDOWN_IMAGES   = [
        pygame.image.load('../medias/board/cooldown/1.png'),
        pygame.image.load('../medias/board/cooldown/2.png'),
        pygame.image.load('../medias/board/cooldown/3.png'),
        pygame.image.load('../medias/board/cooldown/4.png'),
        pygame.image.load('../medias/board/cooldown/5.png'),
        pygame.image.load('../medias/board/cooldown/6.png'),
        pygame.image.load('../medias/board/cooldown/7.png'),
        pygame.image.load('../medias/board/cooldown/8.png'),
        pygame.image.load('../medias/board/cooldown/9.png'),
        pygame.image.load('../medias/board/cooldown/10.png'),
        pygame.image.load('../medias/board/cooldown/11.png'),
        pygame.image.load('../medias/board/cooldown/12.png'),
        pygame.image.load('../medias/board/cooldown/13.png'),
        pygame.image.load('../medias/board/cooldown/14.png'),
        pygame.image.load('../medias/board/cooldown/15.png'),
        pygame.image.load('../medias/board/cooldown/16.png'),
        pygame.image.load('../medias/board/cooldown/17.png'),
        pygame.image.load('../medias/board/cooldown/18.png'),
        pygame.image.load('../medias/board/cooldown/19.png'),
        pygame.image.load('../medias/board/cooldown/20.png'),
        pygame.image.load('../medias/board/cooldown/21.png'),
        pygame.image.load('../medias/board/cooldown/22.png'),
        pygame.image.load('../medias/board/cooldown/23.png'),
        pygame.image.load('../medias/board/cooldown/24.png'),
        pygame.image.load('../medias/board/cooldown/25.png'),
        pygame.image.load('../medias/board/cooldown/26.png'),
        pygame.image.load('../medias/board/cooldown/27.png'),
        pygame.image.load('../medias/board/cooldown/28.png'),
        pygame.image.load('../medias/board/cooldown/29.png')
    ]
    HP_IMAGES_LEN       = len(HP_IMAGES) 
    COOLDOWN_IMAGES_LEN = len(COOLDOWN_IMAGES)
    HP_IMAGE_SIZE       = {'width': HP_IMAGES[0].get_width(),        'height':HP_IMAGES[0].get_height()}
    COOLDOWN_IMAGE_SIZE = {'width': COOLDOWN_IMAGES[0].get_width(),  'height':COOLDOWN_IMAGES[0].get_height()}
    BOARD_SIZE = (100, 80)
    CENTER = BOARD_SIZE[0] // 2

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.board_surface = pygame.Surface(PlayerBoard.BOARD_SIZE)
        self.board_surface.set_colorkey((0,0,0))
        self.image = self.board_surface
        self.rect = self.image.get_rect()

    """
    update() : met à jour le board (vie + cooldown)
    """
    def update(self):
        if self.player.health <= 0:
            self.kill()
        self.rect.midtop = (self.player.rect.midbottom[0], self.player.rect.midbottom[1] + 10)
        self.draw_cooldown()
        self.draw_hp()

    """
    draw_hp() : dessine la vie actuelle du joueur
    """
    def draw_hp(self):
        index = self.player.get_hp()
        CURRENT_HP = PlayerBoard.HP_IMAGES[index]
        self.board_surface.blit(CURRENT_HP, (PlayerBoard.CENTER - PlayerBoard.HP_IMAGE_SIZE['width']//2, 0))

    """
    draw_cooldown() : dessine l'état actuel de l'énergie du joueur (dessine une surface vide dans le cas
    où l'énergie est au max)
    """
    def draw_cooldown(self):
        COOLDOWN = self.player.get_cooldown()
        COOLDOWN_MAX = self.player.COOLDOWN_DURATION
        if COOLDOWN <= COOLDOWN_MAX:
            POSITION = COOLDOWN / COOLDOWN_MAX * PlayerBoard.COOLDOWN_IMAGES_LEN - 1
            SPRITE = PlayerBoard.COOLDOWN_IMAGES[int(POSITION)].convert()
            self.board_surface.blit(SPRITE, (PlayerBoard.CENTER - PlayerBoard.COOLDOWN_IMAGE_SIZE['width']//2, PlayerBoard.HP_IMAGE_SIZE['height']))
        else:
            SPRITE = pygame.Surface((PlayerBoard.COOLDOWN_IMAGE_SIZE['width'], PlayerBoard.COOLDOWN_IMAGE_SIZE['height']))
            rect = SPRITE.get_rect()
            self.board_surface.blit(SPRITE, (PlayerBoard.CENTER - PlayerBoard.COOLDOWN_IMAGE_SIZE['width']//2, PlayerBoard.HP_IMAGE_SIZE['height']))

    
