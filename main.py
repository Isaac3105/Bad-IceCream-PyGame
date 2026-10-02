import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WALL_SIZE, ICE_WIDTH, ICE_HEIGHT
from sprites import Troll, Fruits, IceBlocks, Player, iceblocks, trolls, fruits, players, all_sprites, winnning_music, losing_music, iglu_inv_surf, iglu_inv_rect
from levels import get_round, lvs, round_final, lv_final
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bad Ice Cream by Isaac Santos")
clock = pygame.time.Clock()

# Game States
screens = ["start","levels", "paused", "gaming", "help", "credits"]

active_screen = "start"

# Load background
background_surface = pygame.image.load("Resources/background.png").convert_alpha()
background_rect = background_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

round_atual = 1
lv_atual = 1
counter = 0
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
