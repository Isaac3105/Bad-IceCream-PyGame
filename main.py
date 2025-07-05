import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 820, 622
WALL_SIZE = 50
ICE_WIDTH, ICE_HEIGHT = 40, 58
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bad Ice Cream by Isaac Santos")
clock = pygame.time.Clock()

# Game States
screens = ["start","levels", "paused", "gaming", "help", "credits"]

active_screen = "start"

# Load background
background_surface = pygame.image.load("Resources/background.png").convert_alpha()
background_rect = background_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Iglu (Invisible Obstacle)
iglu_inv_surf = pygame.Surface((160, 173), pygame.SRCALPHA)
iglu_inv_surf.fill((0, 0, 0, 0)) 
iglu_inv_rect = iglu_inv_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Classes
class Fruits(pygame.sprite.Sprite):
    def __init__(self,x,y,fruit,fruits, iceblocks):
        super().__init__()
        self.image = pygame.image.load(f"Resources/fruits/{fruit}.webp")
        self.rect = self.image.get_rect(center=(x, y))
        self.adicional = 1
        self.limite = 50
        self.counter = 0
        self.fruits = fruits
        self.icegroup = iceblocks

    def animation(self):
        self.counter += 1.25
        if self.counter == int(self.counter):
            self.rect.y -= self.adicional
        if self.counter >= self.limite:
            self.counter = 0
            self.adicional = -self.adicional

    def reset_animation(self):
        self.counter = 0
        self.adicional = 1


    def update(self):
        self.animation()      


class Troll(pygame.sprite.Sprite):
    def __init__(self,x,y,iceblocks,trolls,dic=(0, 0, "frente", 0)):
        super().__init__()
        self.image =  pygame.transform.scale2x(pygame.image.load("Resources/troll/frente/part1.png"))
        self.image.set_colorkey((49, 202, 49))  
        self.rect = self.image.get_rect(topright = (x,y))
        self.andando_frente = [pygame.transform.scale2x(pygame.image.load(f"Resources/troll/frente/part{i}.png")) for i in range(1,9)]
        self.andando_tras = [pygame.transform.scale2x(pygame.image.load(f"Resources/troll/tras/part{i}.png")) for i in range(1,9)]
        self.andando_direita = [pygame.transform.scale2x(pygame.image.load(f"Resources/troll/direita/part{i}.png")) for i in range(1,9)]
        self.andando_esquerda = [pygame.transform.scale2x(pygame.image.load(f"Resources/troll/esquerda/part{i}.png")) for i in range(1,9)]
        self.duvidoso = [pygame.transform.scale2x(pygame.image.load(f"Resources/troll/duvida/part{i}.png")) for i in range(1,7)]
        self.ice_group = iceblocks
        self.trolls = trolls
        self.andando = True
        self.duvido = False
        self.cuspindo = False 
        self.destroying = False
        self.winning = False
        self.dir, self.esq, self.fre, self.tra = dic
        self.counter = 0
        self.index_movimento = 0
        self.duvidoso_index = 0
        self.speed = 1
        self.speed_end = 0
        self.c = 0

    def animation_andando(self):
        if self.fre:
            self.image = self.andando_frente[int(self.index_movimento)]
        elif self.tra:
            self.image = self.andando_tras[int(self.index_movimento)]
        elif self.esq:
            self.image = self.andando_esquerda[int(self.index_movimento)]
        elif self.dir:
            self.image = self.andando_direita[int(self.index_movimento)]
        self.image.set_colorkey((49, 202, 49))  
        self.index_movimento += 0.15
        if self.index_movimento >= 8:
            self.index_movimento = 0
        
    def duvidoso_animation(self):
        self.image = self.duvidoso[int(self.duvidoso_index)]
        self.image.set_colorkey((49, 202, 49))  
        self.duvidoso_index += 0.1
        if self.duvidoso_index >= 6:
            self.duvidoso_index = 0
        self.possible_way()

    def possible_way(self):
        """Finds a valid way for troll. Else, troll becomes duvidoso."""
        x, y = self.rect.topleft

        # Define direções possíveis
        ways = {
            "tra": (x, y - ICE_HEIGHT),
            "fre": (x, y + ICE_HEIGHT),
            "esq": (x - ICE_WIDTH, y),
            "dir": (x + ICE_WIDTH, y)
        }

        # Filtra apenas as direções válidas
        valid_choices = []
        for direction, pos in ways.items():
            if (
                not any(iceblock.rect.topleft == pos for iceblock in self.ice_group) and  # Sem gelo
                not any(trolle.rect.topleft == pos for trolle in self.trolls if trolle != self) and  # Sem trolls
                50 <= pos[0] < SCREEN_WIDTH - 50 and 50 <= pos[1] < SCREEN_HEIGHT - 50  # Dentro dos limites
            ):
                valid_choices.append(direction)

        # Se houver direções válidas, escolhe uma aleatória
        if valid_choices:
            escolha = random.choice(valid_choices)
            self.dir, self.esq, self.fre, self.tra = 0, 0, 0, 0  # Reseta direções
            setattr(self, escolha, 1)  # Ativa a direção escolhida

            # Define tempo de movimento baseado na direção
            if escolha in ["tra", "fre"]:
                self.counter = 58
            else:
                self.counter = 40
            self.andando = True
            self.duvido = False
        else:
            self.duvido = True
            self.andando = False

    def update(self):
        if self.counter > 0 and not self.duvido:
            self.andando = True

        if self.andando:
            if self.tra:
                self.counter = 40
            elif self.fre:
                self.counter = 40
            elif self.dir:
                self.counter = 58
            elif self.esq:
                self.counter = 58

        # Impede que o troll saia das bordas
        if self.rect.right > SCREEN_WIDTH-50 or self.rect.left < 50 or self.rect.top < 50 or self.rect.bottom > SCREEN_HEIGHT-50:
            self.rect.bottomleft = self.last_pos
            self.possible_way()

        # Colisão com o iglu
        if self.rect.colliderect(iglu_inv_rect):
            self.rect.bottomleft = self.last_pos
            self.possible_way()

        # Colisão com outros trolls
        for trolle in self.trolls:
            if trolle != self and self.rect.colliderect(trolle):
                self.possible_way()
                self.rect.bottomleft = self.last_pos
                

        # Colisão com blocos de gelo
        for iceblock in self.ice_group:
            if self.rect.colliderect(iceblock):
                self.rect.bottomleft = self.last_pos
                self.possible_way()

        if self.andando:
            self.duvido = False
            self.animation_andando()
        
        if self.duvido:
            self.duvidoso_animation()
            self.andando = False

        # Atualiza a última posição
        self.last_pos = self.rect.bottomleft


class IceBlocks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load("Resources/Ice_Block_horizontal.webp"))
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,ice_group,trolls,fruits):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/frente/part1.png"))
        self.image.set_colorkey((49, 202, 49))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.quebrando = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_quebrando_gelo/part{i}.png")) for i in range(1,9)]
        self.cuspindo_direita_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_gelo/da direita/part{i}.png")) for i in range(1,9)]
        self.cuspindo_esquerda_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_gelo/da esquerda/part{i}.png")) for i in range(1,9)]
        self.cuspindo_frente_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_gelo/de frente/part{i}.png")) for i in range(1,13)]
        self.cuspindo_tras_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_gelo/de tras/part{i}.png")) for i in range(1,13)]
        self.morrendo_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_morte/part{i}.png")) for i in range(1,16)]
        self.andando_frente_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_andando/frente/part{i}.png")) for i in range(1,9)]
        self.andando_tras_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_andando/tras/part{i}.png")) for i in range(1,9)]
        self.andando_esq_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_andando/esquerda/part{i}.png")) for i in range(1,9)]
        self.andando_dir_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_andando/direita/part{i}.png")) for i in range(1,9)]
        self.comendo_frente_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_comendo/frente/part{i}.png")) for i in range(1,8)]
        self.comendo_tras_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_comendo/tras/part{i}.png")) for i in range(1,8)]
        self.comendo_esq_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_comendo/esquerda/part{i}.png")) for i in range(1,8)]
        self.comendo_dir_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_comendo/direita/part{i}.png")) for i in range(1,8)]
        self.vencendo_lista = [pygame.transform.scale2x(pygame.image.load(f"Resources/choco/choco_vencendo/part{i}.png")) for i in range(1,7)]
        self.comendo_index = 0
        self.quebrando_index = 0
        self.cuspindo_index = 0
        self.morrendo_index = 0
        self.andando_index = 0
        self.vencendo_index = 0
        self.last_pos = self.rect.bottomleft
        self.dir, self.esq, self.fre, self.tra = 0, 0, 1, 0
        self.c = 0
        self.c2 = 0
        self.counter = 0
        self.speed = 4
        self.speed_end = 2
        self.morto = False
        self.winning = False
        self.destroying = False
        self.cuspindo = False
        self.morrendo = False
        self.andando = False
        self.comendo = False
        self.duvido = False
        self.done = False
        self.trolls = trolls
        self.ice_group = ice_group
        self.fruits = fruits
        self.fruta_comida = None
        self.pontos = 0
        self.winning_timer = 0

    def animation_comendo(self):
        if self.fre:
            self.image = self.comendo_frente_lista[int(self.comendo_index)]
        elif self.tra:
            self.image = self.comendo_tras_lista[int(self.comendo_index)]
        elif self.esq:
            self.image = self.comendo_esq_lista[int(self.comendo_index)]
        elif self.dir:
            self.image = self.comendo_dir_lista[int(self.comendo_index)]
        self.comendo_index += 0.7
        self.image.set_colorkey((49, 202, 49))
        if self.comendo_index >= 7:
            self.comendo_index = 0
            self.comendo = False
            self.fruits.remove(self.fruta_comida)
            self.pontos += 50

    def animation_andando(self):
        if self.fre:
            self.image = self.andando_frente_lista[int(self.andando_index)]
        elif self.tra:
            self.image = self.andando_tras_lista[int(self.andando_index)]
        elif self.esq:
            self.image = self.andando_esq_lista[int(self.andando_index)]
        elif self.dir:
            self.image = self.andando_dir_lista[int(self.andando_index)]
        self.andando_index += 0.15
        self.image.set_colorkey((49, 202, 49))
        if self.andando_index >= 8:
            self.andando_index = 0

    def animation_morrendo(self):
        self.image = self.morrendo_lista[int(self.morrendo_index)]
        self.morrendo_index += 0.10
        self.image.set_colorkey((49, 202, 49))
        if self.morrendo_index >= 15:
            self.morrendo_index = 0
            self.morrendo = False
            self.morto = True

    def animation_vencendo(self):
        self.image = self.vencendo_lista[int(self.vencendo_index)]
        self.vencendo_index += 0.15
        self.image.set_colorkey((49, 202, 49))
        if self.vencendo_index >= 6:
            self.vencendo_index = 0
            self.winning = False

    def animation_quebrando(self):
        self.image = self.quebrando[int(self.quebrando_index)]
        self.quebrando_index += 0.25
        if self.quebrando_index >= 7:
            self.quebrando_index = 0
            self.destroying = False
            self.destroy_ice()
            if self.fre:
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/frente/part1.png"))
            elif self.tra:
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/tras/part1.png"))
            elif self.dir:
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/direita/part1.png"))
            elif self.esq:
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/esquerda/part1.png"))
        self.image.set_colorkey((49, 202, 49))

    def animation_cuspindo_gelo(self):
        if self.fre:
            self.image = self.cuspindo_frente_lista[int(self.cuspindo_index)]
            self.cuspindo_index += 0.33
            if self.cuspindo_index >= 12:
                self.cuspindo_index = 0
                self.cuspindo = False
                self.place_ice()
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/frente/part1.png"))
        elif self.tra:
            self.image = self.cuspindo_tras_lista[int(self.cuspindo_index)]
            self.cuspindo_index += 0.25
            if self.cuspindo_index >= 12:
                self.cuspindo_index = 0
                self.cuspindo = False
                self.place_ice()
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/tras/part1.png"))
        elif self.dir:
            self.image = self.cuspindo_direita_lista[int(self.cuspindo_index)]
            self.cuspindo_index += 0.25
            if self.cuspindo_index >= 8:
                self.cuspindo_index = 0
                self.cuspindo = False
                self.place_ice()
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/direita/part1.png"))
        elif self.esq:
            self.image = self.cuspindo_esquerda_lista[int(self.cuspindo_index)]
            self.cuspindo_index += 0.25
            if self.cuspindo_index >= 8:
                self.cuspindo_index = 0
                self.cuspindo = False
                self.place_ice()
                self.image = pygame.transform.scale2x(pygame.image.load("Resources/choco/choco_andando/esquerda/part1.png"))
        self.image.set_colorkey((49, 202, 49))

    def place_ice(self):
        """Places ice continually in the direction of the player until it reaches an obstacle"""
        x, y = self.rect.topleft
        direction = None

        if self.esq:
            x -= ICE_WIDTH
            direction = "left"
        elif self.dir:
            x += self.rect.width
            direction = "right"
        elif self.fre:
            y += self.rect.height
            direction = "down"
        elif self.tra:
            y -= ICE_HEIGHT
            direction = "up"

        while WALL_SIZE <= x <= SCREEN_WIDTH - WALL_SIZE - ICE_WIDTH and WALL_SIZE <= y <= SCREEN_HEIGHT - WALL_SIZE - ICE_HEIGHT:
            new_ice = IceBlocks(x, y)

            # Stop placing ice if it collides with iglu or player
            if new_ice.rect.colliderect(iglu_inv_rect) or new_ice.rect.colliderect(self.rect):
                return

            # Stop if it collides with other ice blocks
            if any(new_ice.rect.colliderect(iceblock.rect) for iceblock in self.ice_group):
                return

            # Stop if it collides with trolls
            if any(new_ice.rect.colliderect(troll) for troll in self.trolls):
                return

            self.ice_group.add(new_ice)

            # Move to the next ice position
            if direction == "left":
                x -= ICE_WIDTH
            elif direction == "right":
                x += ICE_WIDTH
            elif direction == "down":
                y += ICE_HEIGHT
            elif direction == "up":
                y -= ICE_HEIGHT
    
    def get_ice_direction(self):
        """Return a dictionary indicating which directions have ice blocks."""
        x, y = self.rect.topleft
        directions = {
            "esq": (x - ICE_WIDTH, y),
            "dir": (x + ICE_WIDTH, y),
            "tra": (x, y - ICE_HEIGHT),
            "fre": (x, y + ICE_HEIGHT)
        }

        ice_nearby = {}

        for direction, position in directions.items():
            for iceblock in self.ice_group:
                if iceblock.rect.topleft == position:
                    ice_nearby[direction] = True
                    break  # No need to check further for this direction

        return ice_nearby
    
    def is_ice_nearby(self):
        """Check if there is an ice block adjacent to the player."""
        x, y = self.rect.topleft  # Get player's position
        
        # Define the four adjacent positions
        adjacent_positions = [
            (x - ICE_WIDTH, y),  # Left
            (x + ICE_WIDTH, y),  # Right
            (x, y - ICE_HEIGHT),  # Up
            (x, y + ICE_HEIGHT)   # Down
        ]
        
        # Check if any ice block exists at one of these positions
        for iceblock in self.ice_group:
            if (iceblock.rect.topleft in adjacent_positions):
                return True  # Ice block found nearby

        return False
    
    def destroy_ice(self):
        "Destroys ice continually"
        directions = self.get_ice_direction()

        try:
            to_remove = []  

            if self.fre and directions.get("fre"):
                yatual = self.rect.y
                while True:
                    found = False
                    for iceblock in self.ice_group:
                        if iceblock.rect.x == self.rect.x and iceblock.rect.y == yatual + ICE_HEIGHT:
                            to_remove.append(iceblock)
                            found = True
                            break
                    if not found:
                        break
                    yatual += ICE_HEIGHT

            if self.tra and directions.get("tra"):
                yatual = self.rect.y
                while True:
                    found = False
                    for iceblock in self.ice_group:
                        if iceblock.rect.x == self.rect.x and iceblock.rect.y == yatual - ICE_HEIGHT:
                            to_remove.append(iceblock)
                            found = True
                            break
                    if not found:
                        break
                    yatual -= ICE_HEIGHT

            if self.esq and directions.get("esq"):
                xatual = self.rect.x
                while True:
                    found = False
                    for iceblock in self.ice_group:
                        if iceblock.rect.y == self.rect.y and iceblock.rect.x == xatual - ICE_WIDTH:
                            to_remove.append(iceblock)
                            found = True
                            break
                    if not found:
                        break
                    xatual -= ICE_WIDTH

            if self.dir and directions.get("dir"):
                xatual = self.rect.x
                while True:
                    found = False
                    for iceblock in self.ice_group:
                        if iceblock.rect.y == self.rect.y and iceblock.rect.x == xatual + ICE_WIDTH:
                            to_remove.append(iceblock)
                            found = True
                            break
                    if not found:
                        break
                    xatual += ICE_WIDTH

            for iceblock in to_remove:
                self.ice_group.remove(iceblock)

        except KeyError:
            pass

    def update(self):
        keys = pygame.key.get_pressed()
        speed = 5
        
        # Ice creation
        if keys[pygame.K_f] and (not self.morrendo) and (not self.destroying) and self.rect.bottomleft == self.last_pos:
            self.cuspindo = True
        
        # Ice destruction
        if keys[pygame.K_SPACE] and self.is_ice_nearby() and (not self.morrendo) and (not self.cuspindo) and self.rect.bottomleft == self.last_pos:
            self.destroying = True

        # Movement
        if (not self.destroying) and (not self.cuspindo) and (not self.morrendo)  and (not self.andando) and (not self.winning):
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if self.counter == 0:
                    self.dir, self.esq, self.fre, self.tra = 1, 0, 0, 0
                    self.counter = 10
                    self.andando = False
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if self.counter == 0:
                    self.dir, self.esq, self.fre, self.tra = 0, 1, 0, 0
                    self.counter = 10
                    self.andando = False
            elif keys[pygame.K_w] or keys[pygame.K_UP]:
                if self.counter == 0:
                    self.dir, self.esq, self.fre, self.tra = 0, 0, 0, 1
                    self.counter = 14
                    self.andando = False
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                if self.counter == 0:
                    self.dir, self.esq, self.fre, self.tra = 0, 0, 1, 0
                    self.counter = 14
                    self.andando = False

        # Keep player inside the walls
        self.rect.x = max(WALL_SIZE, min(self.rect.x, SCREEN_WIDTH - WALL_SIZE - self.rect.width))
        self.rect.y = max(WALL_SIZE, min(self.rect.y, SCREEN_HEIGHT - WALL_SIZE - self.rect.height))

        # Prevent player from colliding with iglu
        if self.rect.colliderect(iglu_inv_rect):
            self.rect.bottomleft = self.last_pos

        # Prevent player from walking into ice
        for iceblock in self.ice_group:
            if self.rect.colliderect(iceblock):
                self.rect.bottomleft = self.last_pos

        #Player dies if he touches enemies
        if any(self.rect.colliderect(troll) for troll in self.trolls):
            self.morrendo = True

        # Fruit disappears if player comes in contact with the fruit
        for fruit in self.fruits:
            if self.rect.colliderect(fruit):
                self.comendo = True
                self.fruta_comida = fruit

        if self.destroying:
            self.animation_quebrando()

        if self.cuspindo:
            self.animation_cuspindo_gelo()

        if self.morrendo:
            pygame.mixer.music.stop()
            losing_music.play()
            pygame.mixer.music.play()
            self.animation_morrendo()

        if self.andando:
            self.animation_andando()
        
        if self.comendo:
            self.animation_comendo()

        if self.winning:
            pygame.mixer.music.stop()
            winnning_music.play()
            pygame.mixer.music.play()
            self.andando = False
            self.animation_vencendo()


        self.last_pos = self.rect.bottomleft

# Music themes
music = True
current_music = "placeholder"
winnning_music = pygame.mixer.Sound("Resources/music/WinMusic.mp3")
losing_music = pygame.mixer.Sound("Resources/music/LoseMusic.mp3")

# Switching songs through screens
def play_music_for_screen(active_screen):
    global current_music
    music_files = {
        "start": "Resources/music/MenuMusic.mp3",
        "levels": "Resources/music/MenuMusic.mp3", 
        "paused": "Resources/music/MenuMusic.mp3", 
        "help": "Resources/music/MenuMusic.mp3", 
        "credits": "Resources/music/MenuMusic.mp3",
        "gaming": "Resources/music/GameMusic.mp3",
    }

    if current_music != music_files[active_screen]:
        pygame.mixer.music.load(music_files[active_screen])
        pygame.mixer.music.play(-1)  # Loop indefinitely
        current_music = music_files[active_screen]

# Sprite groups
iceblocks = pygame.sprite.Group()
trolls = pygame.sprite.Group()
fruits = pygame.sprite.Group()
players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(players,trolls) 

# Niveis e rounds
lv1_round1 = [
        [Troll(130,224,iceblocks,trolls),
        Troll(730,224,iceblocks,trolls)],

        [Fruits(110,y,"grapes",fruits,iceblocks) for y in range(144,550,58)] + 
        [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks)] +
        [Fruits(110+15*40,y,"grapes",fruits,iceblocks) for y in range(144,550,58)],

        [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
        [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
        [IceBlocks(50+4*40,y) for y in range(50+58*2,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*2,50+58*7,58)] + 
        [IceBlocks(50+5*40,50+58*2),IceBlocks(50+12*40,50+58*2),IceBlocks(50+5*40,50+58*6),IceBlocks(50+12*40,50+58*6)],

        [Player(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
        ]

lv1_round2 = [
        [troll for troll in trolls],

        [Fruits(110,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
        [Fruits(110,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
        [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
        [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
        [Fruits(110+40,144,"peach",fruits,iceblocks),Fruits(110+40,550-58,"peach",fruits,iceblocks),Fruits(110+14*40,144,"peach",fruits,iceblocks),Fruits(110+14*40,550-58,"peach",fruits,iceblocks)] +
        [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks)],

        [iceblock for iceblock in iceblocks],

        [player for player in players],
        ]

lv1_round3 = [
        [troll for troll in trolls],

        [Fruits(x,144,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
        [Fruits(x,550-58,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
        [Fruits(110,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
        [Fruits(110+15*40,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
        [Fruits(4*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
        [Fruits(13*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
        [Fruits(5*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(5*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks), Fruits(12*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(12*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks)],

        [iceblock for iceblock in iceblocks],

        [player for player in players],
        ]

lv2_round1 = [
        [Troll(250,224,iceblocks,trolls),
        Troll(610,224,iceblocks,trolls),
        Troll(130,282,iceblocks,trolls),
        Troll(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls),
        Troll(730,398,iceblocks,trolls)],

        [Fruits(110,y,"strawberry",fruits,iceblocks) for y in range(144,550,58)] + 
        [Fruits(4*40 + 20 + 50,1*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(4*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(5*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(9*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(6*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks), Fruits(13*40 + 20 + 50,58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(13*40 + 20 + 50,4*58 + 29 + 50,"strawberry",fruits,iceblocks)] +
        [Fruits(110+15*40,y,"strawberry",fruits,iceblocks) for y in range(282+29,492,58)],

        [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
        [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
        [IceBlocks(50+4*40,y) for y in range(50+58*6,50+58*8,58)] + [IceBlocks(50+11*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+5*40,y) for y in range(50+58*1,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*5,50+58*8,58)] +
        [IceBlocks(50+3*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+14*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+2*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+12*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+6*40,y) for y in range(50+58*1,50+58*5,58)] + [IceBlocks(x,SCREEN_HEIGHT-50 -58*3) for x in range(50+40*6,50+40*11,40)] +
        [IceBlocks(50+10*40,50+58*7)] +
        [IceBlocks(x,50+2*58) for x in range(50+40*7,50+40*11,40)] + [IceBlocks(50+15*40,y) for y in range(50+58*1,50+58*8,58)] +
        [IceBlocks(50+16*40,y) for y in range(50+58*1,50+58*4,58)],

        [Player(370,50 + 58,iceblocks,trolls,fruits)],
        ]

lv2_round2 = [
        [troll for troll in trolls],

        [Fruits(50 + col * 40 +20, 50 + row * 58 + 29, "orange", fruits, iceblocks)
        for col in range(0,18) for row in range(0,4,2)] +
        [Fruits(50 + col * 40 +20, 622 - 50 - row * 58 - 29, "orange", fruits, iceblocks)
        for col in range(0,18) for row in range(0,4,2)] +

        [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
        for col in range(0,7) for row in range(0,4,2)] +
        [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
        for col in range(11,18) for row in range(0,4,2)],
        

        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

lv2_round3 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks)],

        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

lv3_round1 = [
        [Troll(330,50+58,iceblocks,trolls),
        Troll(410,50+58,iceblocks,trolls),
        Troll(530,50+58,iceblocks,trolls),
        Troll(410,50+58*7,iceblocks,trolls),
        Troll(530,50+58*7,iceblocks,trolls),
        Troll(330,50+58*7,iceblocks,trolls)],

        [Fruits(70,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*1,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*2,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*3,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*4,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*5,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*6,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] +
        [Fruits(70 + 40*11,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*12,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*13,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*14,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*15,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*16,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*17,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)],

        [IceBlocks(50,y) for y in range(50,622-58,58*2)] + [IceBlocks(90,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(130,y) for y in range(50,622-58,58*2)] + [IceBlocks(170,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(210,y) for y in range(50,622-58,58*2)] + [IceBlocks(250,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(290,y) for y in range(50,622-58,58*2)] + [IceBlocks(290+5*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+6*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+7*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+8*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+9*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+10*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+11*40,y) for y in range(50,622-58,58*2)] +
        [IceBlocks(x,50) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58),IceBlocks(450,50+58)] + [IceBlocks(x,50+58*2) for x in range(330,290+5*40,40)] +
        [IceBlocks(x,50+58*6) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58*7),IceBlocks(450,50+58*7)] + [IceBlocks(x,50+58*8) for x in range(330,290+5*40,40)],

        [Player(730,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
        ]

lv3_round2 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks)] +
        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + x * 40 + 20, 50 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)],
        
        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

lv3_round3 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks)] +
        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + x * 40 + 20, 50 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)],
        
        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

# Simple way to get unaltered lists for any round of any level
def get_round(level, round):

    l1_r1 = [
            [Troll(130,224,iceblocks,trolls),
            Troll(730,224,iceblocks,trolls)],

            [Fruits(110,y,"grapes",fruits,iceblocks) for y in range(144,550,58)] + 
            [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"grapes",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"grapes",fruits,iceblocks)] +
            [Fruits(110+15*40,y,"grapes",fruits,iceblocks) for y in range(144,550,58)],
            [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
            [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
            [IceBlocks(50+4*40,y) for y in range(50+58*2,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*2,50+58*7,58)] + 
            [IceBlocks(50+5*40,50+58*2),IceBlocks(50+12*40,50+58*2),IceBlocks(50+5*40,50+58*6),IceBlocks(50+12*40,50+58*6)],

            [Player(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
            ]

    l1_r2 = [
            [troll for troll in trolls],

            [Fruits(110,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
            [Fruits(110,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
            [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(144,144+58*2,58)] + 
            [Fruits(110+15*40,y,"peach",fruits,iceblocks) for y in range(550-58,550-58*3,-58)] + 
            [Fruits(110+40,144,"peach",fruits,iceblocks),Fruits(110+40,550-58,"peach",fruits,iceblocks),Fruits(110+14*40,144,"peach",fruits,iceblocks),Fruits(110+14*40,550-58,"peach",fruits,iceblocks)] +
            [Fruits(5*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(5*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks), Fruits(12*40 + 20 + 50,3*58 + 29 + 50,"peach",fruits,iceblocks),Fruits(12*40 + 20 + 50,5*58 + 29 + 50,"peach",fruits,iceblocks)],

            [iceblock for iceblock in iceblocks],

            [player for player in players],
            ]

    l1_r3 = [
            [troll for troll in trolls],

            [Fruits(x,144,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
            [Fruits(x,550-58,"pear",fruits,iceblocks) for x in range(110,820-50-40,40)] + 
            [Fruits(110,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
            [Fruits(110+15*40,y,"pear",fruits,iceblocks) for y in range(144+58,550-58,58)] +
            [Fruits(4*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
            [Fruits(13*40 + 20 + 50,y,"pear",fruits,iceblocks) for y in range(2*58 + 29 + 50,7*58 + 29 + 50,58)] +
            [Fruits(5*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(5*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks), Fruits(12*40 + 20 + 50,2*58 + 29 + 50,"pear",fruits,iceblocks),Fruits(12*40 + 20 + 50,6*58 + 29 + 50,"pear",fruits,iceblocks)],

            [iceblock for iceblock in iceblocks],

            [player for player in players],
            ]

    l2_r1 = [
            [Troll(250,224,iceblocks,trolls),
            Troll(610,224,iceblocks,trolls),
            Troll(130,282,iceblocks,trolls),
            Troll(450,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls),
            Troll(730,398,iceblocks,trolls)],

            [Fruits(110,y,"strawberry",fruits,iceblocks) for y in range(144,550,58)] + 
            [Fruits(4*40 + 20 + 50,1*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(4*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(5*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(9*40 + 20 + 50,7*58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(6*40 + 20 + 50,5*58 + 29 + 50,"strawberry",fruits,iceblocks), Fruits(13*40 + 20 + 50,58 + 29 + 50,"strawberry",fruits,iceblocks),Fruits(13*40 + 20 + 50,4*58 + 29 + 50,"strawberry",fruits,iceblocks)] +
            [Fruits(110+15*40,y,"strawberry",fruits,iceblocks) for y in range(282+29,492,58)],

            [IceBlocks(50,y) for y in range(50,622-58,58)] + [IceBlocks(730,y) for y in range(50,622-58,58)] + 
            [IceBlocks(x,50) for x in range(50+40,820-50-40,40)] + [IceBlocks(x,622-50-58) for x in range(50+40,820-50-40,40)] + 
            [IceBlocks(50+4*40,y) for y in range(50+58*6,50+58*8,58)] + [IceBlocks(50+11*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+5*40,y) for y in range(50+58*1,50+58*7,58)] + [IceBlocks(50+13*40,y) for y in range(50+58*5,50+58*8,58)] +
            [IceBlocks(50+3*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+14*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+2*40,y) for y in range(50+58*1,50+58*8,58)] + [IceBlocks(50+12*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+6*40,y) for y in range(50+58*1,50+58*5,58)] + [IceBlocks(x,SCREEN_HEIGHT-50 -58*3) for x in range(50+40*6,50+40*11,40)] +
            [IceBlocks(50+10*40,50+58*7)] +
            [IceBlocks(x,50+2*58) for x in range(50+40*7,50+40*11,40)] + [IceBlocks(50+15*40,y) for y in range(50+58*1,50+58*8,58)] +
            [IceBlocks(50+16*40,y) for y in range(50+58*1,50+58*4,58)],
            [Player(370,50 + 58,iceblocks,trolls,fruits)],
            ]

    l2_r2 = [
            [troll for troll in trolls],

            [Fruits(50 + col * 40 +20, 50 + row * 58 + 29, "orange", fruits, iceblocks)
            for col in range(0,18) for row in range(0,4,2)] +
            [Fruits(50 + col * 40 +20, 622 - 50 - row * 58 - 29, "orange", fruits, iceblocks)
            for col in range(0,18) for row in range(0,4,2)] +

            [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
            for col in range(0,7) for row in range(0,4,2)] +
            [Fruits(50 + col * 40 +20, 224 + row * 58 + 29, "orange", fruits, iceblocks)
            for col in range(11,18) for row in range(0,4,2)],
            

            [Iceblock for Iceblock in iceblocks],
            [player for player in players],
            ]

    l2_r3 = [
            [troll for troll in trolls],

            [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
            [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"pepper",fruits,iceblocks) for x in range(7, 11)] +
            [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"pepper",fruits,iceblocks),
            Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"pepper",fruits,iceblocks)],

            [Iceblock for Iceblock in iceblocks],
            [player for player in players],
            ]

    l3_r1 = [
        [Troll(330,50+58,iceblocks,trolls),
        Troll(410,50+58,iceblocks,trolls),
        Troll(530,50+58,iceblocks,trolls),
        Troll(410,50+58*7,iceblocks,trolls),
        Troll(530,50+58*7,iceblocks,trolls),
        Troll(330,50+58*7,iceblocks,trolls)],

        [Fruits(70,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*1,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*2,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*3,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*4,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*5,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*6,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] +
        [Fruits(70 + 40*11,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*12,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*13,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*14,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*15,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)] + 
        [Fruits(70 + 40*16,y,"lemon",fruits,iceblocks) for y in range(144-58,550+58,58*2)] + 
        [Fruits(70 + 40*17,y,"lemon",fruits,iceblocks) for y in range(144,550,58*2)],

        [IceBlocks(50,y) for y in range(50,622-58,58*2)] + [IceBlocks(90,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(130,y) for y in range(50,622-58,58*2)] + [IceBlocks(170,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(210,y) for y in range(50,622-58,58*2)] + [IceBlocks(250,y) for y in range(50+58,622-58*2,58*2)] + 
        [IceBlocks(290,y) for y in range(50,622-58,58*2)] + [IceBlocks(290+5*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+6*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+7*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+8*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+9*40,y) for y in range(50,622-58,58*2)] + 
        [IceBlocks(290+10*40,y) for y in range(50+58,622-58*2,58*2)] + [IceBlocks(290+11*40,y) for y in range(50,622-58,58*2)] +
        [IceBlocks(x,50) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58),IceBlocks(450,50+58)] + [IceBlocks(x,50+58*2) for x in range(330,290+5*40,40)] +
        [IceBlocks(x,50+58*6) for x in range(330,290+5*40,40)] + [IceBlocks(330,50+58*7),IceBlocks(450,50+58*7)] + [IceBlocks(x,50+58*8) for x in range(330,290+5*40,40)],

        [Player(730,SCREEN_HEIGHT-50 -58*2,iceblocks,trolls,fruits)],
        ]

    l3_r2 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"kiwi",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"kiwi",fruits,iceblocks)] +

        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,6)] +
        
        [Fruits(50 + x * 40 + 20, 50 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"kiwi",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"kiwi",fruits,iceblocks) for y in range(2,8)],

        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]

    l3_r3 = [
        [troll for troll in trolls],

        [Fruits(50 + x * 40 + 20, 50 + 2 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + x * 40 + 20, 50 + 6 * 58 + 29,"green apple",fruits,iceblocks) for x in range(7, 11)] +
        [Fruits(50 + 6 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 6 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 3 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 4 * 58 + 29,"green apple",fruits,iceblocks),
        Fruits(50 + 11 * 40 + 20, 50 + 5 * 58 + 29,"green apple",fruits,iceblocks)] +
        [Fruits(50 + x * 40 + 20, 50 + 1 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + x * 40 + 20, 50 + 7 * 58 + 29,"green apple",fruits,iceblocks) for x in range(5, 13)] +
        [Fruits(50 + 5 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + 12 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,6)] +
        [Fruits(50 + x * 40 + 20, 50 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + x * 40 + 20, 50 + 8 * 58 + 29,"green apple",fruits,iceblocks) for x in range(3, 15)] +
        [Fruits(50 + 2 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)] +
        [Fruits(50 + 15 * 40 + 20, 50 + y * 58 + 29,"green apple",fruits,iceblocks) for y in range(2,8)],
        
        [Iceblock for Iceblock in iceblocks],

        [player for player in players],
        ]
    
    if level == 1 == round:
        return l1_r1
    elif level == 1 and round == 2:
        return l1_r2
    elif level == 1 and round == 3:
        return l1_r3
    elif level == 2 and round == 1:
        return l2_r1
    elif level == 2 and round == 2:
        return l2_r2
    elif level == 2 and round == 3:
        return l2_r3
    elif level == 3 and round == 1:
        return l3_r1
    elif level == 3 and round == 2:
        return l3_r2
    elif level == 3 and round == 3:
        return l3_r3

# Dicionários para níveis
lv1_rounds = {1:lv1_round1, 2:lv1_round2, 3:lv1_round3}

lv2_rounds = {1: lv2_round1, 2: lv2_round2, 3: lv2_round3}

lv3_rounds = {1: lv3_round1, 2: lv3_round2, 3: lv3_round3}

lvs = [lv1_rounds,lv2_rounds,lv3_rounds]

round_final = 3
lv_final = 3
round_atual = 1
lv_atual = 1

counter = 0

# Restart do Nível
def restart():
    global round_atual, players, trolls, iceblocks, all_sprites, fruits

    round = get_round(lv_atual,1)

    round_atual = 1
    all_sprites.empty()
    fruits.empty()
    players.empty()
    iceblocks.empty()
    trolls.empty()

    for i in lvs[lv_atual-1]:
        lvs[lv_atual-1][i] = get_round(lv_atual,i)

    for k, i in enumerate(round):
        if k == 0:
            for j in i:
                trolls.add(j)
                all_sprites.add(j)
        if k == 1:
            for j in i:
                fruits.add(j)
                j.reset_animation()
        if k == 2:
            for j in i:
                iceblocks.add(j)
        if k == 3:
            for j in i:
                players.add(j)
                all_sprites.add(j)

#Instancias do Minimenu e derivados
if True:
    icons = [pygame.transform.scale_by(pygame.image.load(f"Resources/minimenu/{i}.png"),3) for i in ["restart","pause","music"]]
    for icon in icons:
        icon.set_colorkey((131, 206, 82, 255))
    rects = []
    continue_button_surf = pygame.image.load("Resources/minimenu/pressed_pause_button.png")
    continue_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 209//2, SCREEN_HEIGHT//2 - 7, 209, 54)
    back_menu_button_surf = pygame.image.load("Resources/minimenu/pressed_back_menu_button.png")
    back_menu_button_rect = pygame.Rect(296,365,228,54)
    buttons = {continue_button_surf : (continue_button_rect,True), back_menu_button_surf :(back_menu_button_rect,True)}

#Instancias do Start e derivados
if True:
    play_button_surf = pygame.image.load("Resources/menu/pressed_play_button.png")
    play_button_rect = pygame.Rect(496, 129, 281, 105)

    help_button_surf = pygame.image.load("Resources/menu/pressed_help_button.png")
    help_button_rect = pygame.Rect(494, 265, 281, 105)

    credits_button_surf = pygame.image.load("Resources/menu/pressed_credits_button.png")
    credits_button_rect = pygame.Rect(494, 396, 281, 105)

    buttons.update({
        play_button_surf: (play_button_rect,True),
        help_button_surf: (help_button_rect,True),
        credits_button_surf: (credits_button_rect,True)
    })

#Instancias da Interface dos Níveis e derivados
if True:
    lv1_button_surf = pygame.image.load("Resources/levels_interface/pressed_lvl1_button.png")
    lv1_button_rect = pygame.Rect(269, 101, 91, 89)
    lv2_button_surf = pygame.image.load("Resources/levels_interface/pressed_lvl2_button.png")
    lv2_button_rect = pygame.Rect(268 + 92, 101, 92, 89)
    lv3_button_surf = pygame.image.load("Resources/levels_interface/pressed_lvl3_button.png")
    lv3_button_rect = pygame.Rect(268 + 93*2 -1, 101, 93, 89)
    back_button_surf = pygame.image.load("Resources/levels_interface/pressed_back_button.png")
    back_button_rect = pygame.Rect(301,509,211,101)

    lv_access = {    
        0: (lv1_button_rect,True,lv1_button_surf),
        1: (lv2_button_rect,False,lv2_button_surf),
        2: (lv3_button_rect,False,lv3_button_surf)}

    buttons.update({
        back_button_surf:(back_button_rect,True)
    })

#Instancias do Help e derivados
if True:
    menu_button_surf = pygame.image.load("Resources/help/pressed_back_menu_button.png")
    menu_button_rect = pygame.Rect(288,483,228,54)

    buttons.update({
        menu_button_surf:(menu_button_rect,True)
    })

#Instancias do Credits e derivados
if True:
    menu_button_surf = pygame.image.load("Resources/credits/pressed_back_menu_button.png")
    menu_button_rect = pygame.Rect(288,483,228,54)

    buttons.update({
        menu_button_surf:(menu_button_rect,True)
    })

# Game loop
while True:
    # Play music:
    play_music_for_screen(active_screen)

    for event in pygame.event.get():
        # Closing the game window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pressed down button system
        if True:
            for button in buttons:
                if buttons[button][0].collidepoint(pygame.mouse.get_pos()) and buttons[button][1]:
                    button.set_alpha(180)
                else:
                    button.set_alpha(0)
            for lvl in lv_access:
                #if lv_access[lvl][0].collidepoint(pygame.mouse.get_pos()) and lv_access[lvl][1]: esse é para não dar hover em 
                #níveis que vc ainda não pode jogar

                if lv_access[lvl][0].collidepoint(pygame.mouse.get_pos()): # esse é para dar hover independentemente se 
                #vc já passou ou não no nível
                    lv_access[lvl][2].set_alpha(180)
                else:
                    lv_access[lvl][2].set_alpha(0)

        #All buttons system
        if event.type == pygame.MOUSEBUTTONDOWN:
            for j, rect in enumerate(rects):
                if rect.collidepoint(event.pos) and active_screen == "gaming" and not players.sprites()[0].winning: 
                    if j == 0 and not players.sprites()[0].morrendo:
                        restart()
                    elif j == 1:
                        active_screen = "paused"
                    elif j == 2:
                        if music:
                            pygame.mixer.music.stop()
                            music = False
                        else:
                            pygame.mixer.music.play(-1)
                            music = True

            if active_screen == "paused":
                if continue_button_rect.collidepoint(event.pos):
                    active_screen = "gaming"
                elif back_menu_button_rect.collidepoint(event.pos) :
                    restart()
                    active_screen = "start"

            elif active_screen == "start":
                if play_button_rect.collidepoint(event.pos):
                    active_screen = "levels"
                elif help_button_rect.collidepoint(event.pos):
                    active_screen = "help"
                elif credits_button_rect.collidepoint(event.pos):
                    active_screen = "credits"

            elif active_screen == "help":
                if menu_button_rect.collidepoint(event.pos):
                    active_screen = "start"

            elif active_screen == "credits":
                if menu_button_rect.collidepoint(event.pos):
                    active_screen = "start"

            elif active_screen == "levels":
                if lv1_button_rect.collidepoint(event.pos):
                    active_screen = "gaming"
                    lv_atual = 1
                    restart()
                elif lv2_button_rect.collidepoint(event.pos) and lv_access[1][1]:
                    active_screen = "gaming"
                    lv_atual = 2
                    restart()
                elif lv3_button_rect.collidepoint(event.pos) and lv_access[2][1]:
                    active_screen = "gaming"
                    lv_atual = 3
                    restart()
                elif back_button_rect.collidepoint(event.pos):
                    active_screen = "start"

    # Gaming State
    if active_screen == "gaming":

        # Draw background
        screen.blit(background_surface, background_rect)
        screen.blit(iglu_inv_surf, iglu_inv_rect)

        # Update sprites
        fruits.update()
        all_sprites.update()

        # Grid-moving system for player and trolls
        for player in all_sprites:
            if player.counter > 0 and not player.duvido and not player.winning:
                player.andando = True
            else:
                player.andando = False
            if not player.cuspindo and not player.destroying and not player.winning:
                if player.tra:
                    if player.counter > 0:
                        player.counter -= 1
                        player.rect.y -= player.speed
                        if player.counter == 1:
                            player.rect.y -= player.speed_end
                elif player.fre:
                    if player.counter > 0:
                        player.counter -= 1
                        player.rect.y += player.speed
                        if player.counter == 1:
                            player.rect.y += player.speed_end
                elif player.dir:
                    if player.counter > 0:
                        player.counter -= 1
                        player.rect.x += player.speed
                elif player.esq:
                    if player.counter > 0:
                        player.counter -= 1
                        player.rect.x -= player.speed

        # Add tranparency to the iceblocks covering fruits
        for fruta in fruits:
            for gelo in iceblocks:
                if fruta.rect.colliderect(gelo.rect):
                    gelo.image.set_alpha(200)

        # Draw everything
        if not players.sprites()[0].winning:
            fruits.draw(screen)
            all_sprites.draw(screen)
            iceblocks.draw(screen)
        else:
            fruits.draw(screen)
            iceblocks.draw(screen)
            all_sprites.draw(screen)

        # Montando layout do proximo round
        now = pygame.time.get_ticks()
        for player in players:
            if player.done:
                counter = 0
                round_atual += 1
                player.done = False
                fruits.empty()
                if round_atual != 1:
                    round = lvs[lv_atual-1][round_atual]
                    round[3] = []
                    round[2] = []
                    round[0] = []
                    for k, i in enumerate(round):
                        if k == 0:
                            for j in i:
                                trolls.add(j)
                                all_sprites.add(j)
                        if k == 1:
                            for j in i:
                                fruits.add(j)
                        if k == 2:
                            for j in i:
                                iceblocks.add(j)
                        if k == 3:
                            for j in i:
                                players.add(j)
                                all_sprites.add(j)

        # Check Winning Condition
        for player in players:
            if len(fruits) == 0:
                if round_atual == round_final:
                    player.winning = True
                    if counter == 0:
                        player.winning_timer = pygame.time.get_ticks()
                        counter = 1
                    if now - player.winning_timer >= 5000:
                        player.winning = False
                        restart()
                        if lv_atual != lv_final:
                            lv_access[lv_atual] = (lv_access[lv_atual][0],True,lv_access[lv_atual][2])
                        active_screen = "levels"
                else:
                    player.done = True

        # Check if player lost the level
        for player in players:
            if player.morto:
                restart()
                active_screen = "levels"

        # Score HUD
        if True:
            digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
            scores = {"p":pygame.transform.scale_by(pygame.image.load(f"Resources/score/player1.png"),2)}
            scores["p"].set_colorkey((131, 206, 82, 255))
            for i, name in enumerate(digit_names):
                img = pygame.transform.scale_by(pygame.image.load(f"Resources/score/{name}.png"),2.5)
                img.set_colorkey((131, 206, 82, 255))
                scores[i] = img
            for player in players:
                score_str = str(player.pontos)
                while len(score_str) < 6:
                    score_str = "0" + score_str
                screen.blit(scores["p"], scores["p"].get_rect(topleft=(60, 2)))
                for index, digit in enumerate(score_str):
                    x = 110 + index * 25
                    y = 0 + 20
                    screen.blit(scores[int(digit)], scores[int(digit)].get_rect(topleft=(x, y)))

        # MiniMenu HUD
        if True:
            x = -120
            rects.clear()
            for i in icons:
                if i == icons[-1]:
                    x = -30
                rect = i.get_rect(topright = (800+x,15))
                screen.blit(i, rect)
                rects.append(rect)
                x += 40

    # Pause State
    elif active_screen == "paused":
        paused_interface = pygame.image.load("Resources/minimenu/Paused.webp")
        paused_rect = paused_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        continue_button_rect = pygame.Rect(SCREEN_WIDTH//2 + 2 - 209//2, SCREEN_HEIGHT//2 - 8, 209, 58)
        screen.blit(paused_interface,paused_rect)
        screen.blit(continue_button_surf,continue_button_rect)
        screen.blit(back_menu_button_surf,back_menu_button_rect)

    # Start State
    elif active_screen == "start":
        start_interface = pygame.image.load("Resources/menu/start.png")
        start_rect = start_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        screen.blit(start_interface,start_rect)
        screen.blit(play_button_surf,play_button_rect)
        screen.blit(help_button_surf,help_button_rect)
        screen.blit(credits_button_surf,credits_button_rect)

    # Levels State
    elif active_screen == "levels":
        start_interface = pygame.image.load("Resources/levels_interface/levels.png")
        start_rect = start_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        screen.blit(start_interface,start_rect)
        screen.blit(lv1_button_surf,lv1_button_rect)
        screen.blit(lv2_button_surf,lv2_button_rect)
        screen.blit(lv3_button_surf,lv3_button_rect)
        screen.blit(back_button_surf,back_button_rect)

    # Help State
    elif active_screen == "help":
        help_interface = pygame.image.load("Resources/help/background.png")
        help_rect = help_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        screen.blit(help_interface,help_rect)
        screen.blit(menu_button_surf,menu_button_rect)

    # Credits State
    elif active_screen == "credits":
        credits_interface = pygame.image.load("Resources/credits/background.png")
        credits_rect = credits_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        screen.blit(credits_interface,credits_rect)
        screen.blit(menu_button_surf,menu_button_rect)

    # Update the screen
    pygame.display.update()
    clock.tick(60)
