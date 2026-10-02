import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WALL_SIZE, ICE_WIDTH, ICE_HEIGHT
from sprites import Troll, Fruits, IceBlocks, Player, iceblocks, trolls, fruits, players, all_sprites, winnning_music, losing_music, iglu_inv_surf, iglu_inv_rect
from levels import get_round, lvs, round_final, lv_final
from music import play_music_for_screen
import music as music_mod

music = True
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

from ui import *
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
        for player in players:
            score_str = str(player.pontos).zfill(6)
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
        screen.blit(start_interface,start_rect)
        screen.blit(play_button_surf,play_button_rect)
        screen.blit(help_button_surf,help_button_rect)
        screen.blit(credits_button_surf,credits_button_rect)

    # Levels State
    elif active_screen == "levels":
        screen.blit(levels_interface,levels_rect)
        screen.blit(lv1_button_surf,lv1_button_rect)
        screen.blit(lv2_button_surf,lv2_button_rect)
        screen.blit(lv3_button_surf,lv3_button_rect)
        screen.blit(back_button_surf,back_button_rect)

    # Help State
    elif active_screen == "help":
        screen.blit(help_interface,help_rect)
        screen.blit(menu_button_surf,menu_button_rect)

    # Credits State
    elif active_screen == "credits":
        screen.blit(credits_interface,credits_rect)
        screen.blit(menu_button_surf,menu_button_rect)

    # Update the screen
    pygame.display.update()
    clock.tick(60)
