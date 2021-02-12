import pygame
import math
import spell
import settings
"""
@Author :   YANG    Lei     (S201970)
            GARDIER Simon   (S192580)

Player(Sprite) : Classe représentant les joueurs (sorciers)
"""
class Player(pygame.sprite.Sprite):
    #Liste contenant les informations des différents joueurs
    PLAYERS = [
        {   
            'name': 'Le sorcier Bleu',
            'position': (80, settings.WINDOW_DIMENSIONS[1] // 2),
            'sprites_path': [
                pygame.image.load('../medias/player/player1/move/1.png'),
                pygame.image.load('../medias/player/player1/move/2.png'),
                pygame.image.load('../medias/player/player1/move/3.png'),
                pygame.image.load('../medias/player/player1/move/4.png'),
                pygame.image.load('../medias/player/player1/move/5.png'),
                pygame.image.load('../medias/player/player1/move/6.png'),
                pygame.image.load('../medias/player/player1/move/7.png'),
                pygame.image.load('../medias/player/player1/move/8.png')
            ],
            'death_sprites_path':[
                pygame.image.load('../medias/player/player1/die_animation/1.png'),
                pygame.image.load('../medias/player/player1/die_animation/2.png'),
                pygame.image.load('../medias/player/player1/die_animation/3.png'),
                pygame.image.load('../medias/player/player1/die_animation/4.png'),
                pygame.image.load('../medias/player/player1/die_animation/5.png'),
                pygame.image.load('../medias/player/player1/die_animation/6.png'),
                pygame.image.load('../medias/player/player1/die_animation/7.png'),
                pygame.image.load('../medias/player/player1/die_animation/8.png')
            ],
            'keys': {
                'SPELL': pygame.K_r,
                'RIGHT': pygame.K_d,
                'LEFT': pygame.K_a,
                'TOP': pygame.K_w,
                'BOTTOM': pygame.K_s
            }
        },
        {
            'name': 'Le sorcier Vert',
            'position': (settings.WINDOW_DIMENSIONS[0] - 130, settings.WINDOW_DIMENSIONS[1] // 2),
            'sprites_path':[
                pygame.image.load('../medias/player/player2/move/1.png'),
                pygame.image.load('../medias/player/player2/move/2.png'),
                pygame.image.load('../medias/player/player2/move/3.png'),
                pygame.image.load('../medias/player/player2/move/4.png'),
                pygame.image.load('../medias/player/player2/move/5.png'),
                pygame.image.load('../medias/player/player2/move/6.png'),
                pygame.image.load('../medias/player/player2/move/7.png'),
                pygame.image.load('../medias/player/player2/move/8.png')
            ],
            'death_sprites_path':[
                pygame.image.load('../medias/player/player2/die_animation/1.png'),
                pygame.image.load('../medias/player/player2/die_animation/2.png'),
                pygame.image.load('../medias/player/player2/die_animation/3.png'),
                pygame.image.load('../medias/player/player2/die_animation/4.png'),
                pygame.image.load('../medias/player/player2/die_animation/5.png'),
                pygame.image.load('../medias/player/player2/die_animation/6.png'),
                pygame.image.load('../medias/player/player2/die_animation/7.png'),
                pygame.image.load('../medias/player/player2/die_animation/8.png')
            ],
            'keys': {
                'SPELL': pygame.K_m,
                'RIGHT': pygame.K_RIGHT,
                'LEFT': pygame.K_LEFT,
                'TOP': pygame.K_UP,
                'BOTTOM': pygame.K_DOWN
            }
        }
    ]
    #liste des clés de tous les joueurs (utilisée dans keys_manager.py)
    all_players_keys = {}
    for player in PLAYERS:
        for key_name, key in player['keys'].items():
            all_players_keys[key] = False
    
    ANIMATION_SPEED = 1/5
    OFFSET = 17
    PADDING = OFFSET * 2
    HEALTH = 3
    MOVEMENT_SIZE = 5
    COOLDOWN_DURATION = settings.FPS / 3
    DEATH_ANIMATION_DURATION = settings.FPS / 1.5

    def __init__(self, name, sprites_path, death_sprites_path, topleft, keys, inaccessible, spells_group, sprites_group):
        super().__init__()
        #liste d'images créant l'animation de déplacement
        self.sprites = sprites_path
        #indice dans self.sprites de l'image à afficher
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = topleft)
        #rectangle utilisé pour gérer les collisions avec les murs
        self.hitbox = pygame.rect.Rect((self.rect.topleft[0] + Player.OFFSET, self.rect.topleft[1] + Player.OFFSET), (self.rect.width - Player.PADDING, self.rect.height - Player.PADDING))
        #orientation en degrés (Orientation dans le cercle trigonométrique)
        self.orientation = 0
        #touches relatives aux actions du joueur
        self.keys = keys
        #groupe de murs / de textures intraversables
        self.inaccessible_group = inaccessible
        #cooldown du spell
        self.cooldown = Player.COOLDOWN_DURATION + 1
        self.health = Player.HEALTH
        #groupe publique contenant tous les spells présents dans le jeu
        self.spells_group = spells_group
        self.own_spells = []
        #groupe des sprites affichés
        self.all_sprites_group = sprites_group
        #liste d'images créant l'animation de mort
        self.death_sprites = death_sprites_path        
        #indice dans self.death_sprites de l'image à afficher
        self.current_death_animation_duration = 0
        self.isAlive = True
        self.name = name

    """
    update() : mets à jour le joueur s'il est en vie 
    """
    def update(self):
        if self.isAlive:
            self.is_hitted()
            self.walk()
            self.set_cooldown()
            if self.health <= 0:
                self.die()
    
    """
    is_hitted() : vérifie si le joueur est touché par un spell ennemi (spell faisant partie du groupe de spells
    publiques mais pas de son groupe privé). S'il y a collision le spell est retiré des groupes et le joueur perd
    1 HP
    """
    def is_hitted(self):
        for spell in self.spells_group:
                if not spell in self.own_spells and pygame.Rect.colliderect(self.rect, spell.rect):
                    self.set_hp(-1)
                    spell.kill()

    """
    walk() : déplace le joueur dans le cas où un mouvement a eu lieu
    """
    def walk(self):
        if not self.move == [0, 0]:
            previous_position = self.get_position()
            move = (previous_position[0] + self.move[0] * Player.MOVEMENT_SIZE, previous_position[1] + self.move[1] * Player.MOVEMENT_SIZE)
            self.set_position(move)
            for inaccessible_area in self.inaccessible_group:
                if pygame.Rect.colliderect(self.hitbox, inaccessible_area.rect):
                    self.set_position(previous_position)
            self.move_animation()

    """
    die() : gère l'animation de mort et défini le joueur comme mort à la fin de cette dernière 
    """
    def die(self):
        if self.current_death_animation_duration < Player.DEATH_ANIMATION_DURATION:
            current_array_animation_position = self.current_death_animation_duration / Player.DEATH_ANIMATION_DURATION * len(self.death_sprites)
            self.image = pygame.transform.rotate(self.death_sprites[int(current_array_animation_position)], self.orientation)
            self.rect = self.image.get_rect(bottom=self.rect.bottom, centerx=self.rect.centerx)
            self.current_death_animation_duration += 1 
        else:
            self.image = pygame.transform.rotate(self.death_sprites[int(len(self.death_sprites) - 1)], self.orientation)
            self.isAlive = False
    
    """
    publish(keys) : effectue les mises à jour nécessaires en fonction des touches pressées dans keys
    @param dictionnaire de touches avec comme valeur True|False
    """
    def publish(self, keys):
        self.move = [0, 0]
        if keys[self.keys['SPELL']]:
            self.spell()
        if keys[self.keys['RIGHT']] and keys[self.keys['TOP']]:
            self.orientation = 45
            self.move = [math.sqrt(2) / 2, -math.sqrt(2) / 2]
        elif keys[self.keys['RIGHT']] and keys[self.keys['BOTTOM']]:
            self.orientation = 315
            self.move = [math.sqrt(2) / 2, math.sqrt(2) / 2]
        elif keys[self.keys['LEFT']] and keys[self.keys['TOP']]:
            self.orientation = 135
            self.move = [-math.sqrt(2) / 2, -math.sqrt(2) / 2]
        elif keys[self.keys['LEFT']] and keys[self.keys['BOTTOM']]:
            self.orientation = 225
            self.move = [-math.sqrt(2) / 2, math.sqrt(2) / 2]
        elif keys[self.keys['RIGHT']]:
            self.orientation = 0
            self.move = [1, 0]
        elif keys[self.keys['LEFT']]:
            self.orientation = 180
            self.move = [-1, 0]
        elif keys[self.keys['TOP']]:
            self.orientation = 90
            self.move = [0, -1]
        elif keys[self.keys['BOTTOM']]:
            self.orientation = 270
            self.move = [0, 1]
    """
    spell() : crée un spell, l'ajoute au groupe de spell du joueur, l'ajoute au groupe de spells publique,
    l'ajoute au groupe des sprites à afficher
    """
    def spell(self):
        if self.cooldown == Player.COOLDOWN_DURATION + 1:
            self.cooldown = 0
            spell_sprite = spell.Spell(self.rect.center, self.orientation, self.inaccessible_group, self.all_sprites_group)
            self.spells_group.add(spell_sprite)
            self.own_spells.append(spell_sprite)
            self.all_sprites_group.add(spell_sprite)
    """
    move_animation() : Redéfini self.image avec l'image actuelle de l'animation  
    """
    def move_animation(self):
        self.current_sprite += Player.ANIMATION_SPEED
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], self.orientation)

    """
    Accesseurs
    """
    def set_position(self, pos):
        self.rect.topleft = pos
        self.hitbox.topleft = [pos[0] + Player.OFFSET, pos[1] +  Player.OFFSET]

    def get_hp(self):
        return self.health

    def set_hp(self, hp):
        if self.health > 0:
            self.health += hp
            
    def get_cooldown(self):
        return self.cooldown

    def set_cooldown(self):
        if self.cooldown <= Player.COOLDOWN_DURATION:
                self.cooldown += 1

    def get_position(self):
        return self.rect.topleft

    def get_name(self):
        return self.name

    def alive(self):
        return self.isAlive