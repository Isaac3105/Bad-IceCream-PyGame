import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites import iceblocks, trolls, fruits, players, all_sprites, iglu_inv_surf, iglu_inv_rect
from levels import get_round, lvs, round_final, lv_final
from music import play_music_for_screen
from ui import buttons, lv_access, rects, continue_button_rect, back_menu_button_rect, play_button_rect, help_button_rect, credits_button_rect, menu_button_rect, menu_button_surf, lv1_button_rect, lv2_button_rect, lv3_button_rect, back_button_rect, scores, icons, continue_button_surf, back_menu_button_surf, start_interface, start_rect, play_button_surf, help_button_surf, credits_button_surf, levels_interface, levels_rect, lv1_button_surf, lv2_button_surf, lv3_button_surf, back_button_surf, help_interface, help_rect, credits_interface, credits_rect, paused_interface, paused_rect

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bad Ice Cream by Isaac Santos")
        self.clock = pygame.time.Clock()

        self.screens = ["start", "levels", "paused", "gaming", "help", "credits"]
        self.active_screen = "start"

        self.background_surface = pygame.image.load("Resources/background.png").convert_alpha()
        self.background_rect = self.background_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.round_atual = 1
        self.lv_atual = 1
        self.counter = 0
        self.music_on = True

    def restart(self):
        round_data = get_round(self.lv_atual, 1)

        self.round_atual = 1
        all_sprites.empty()
        fruits.empty()
        players.empty()
        iceblocks.empty()
        trolls.empty()

        for i in lvs[self.lv_atual - 1]:
            lvs[self.lv_atual - 1][i] = get_round(self.lv_atual, i)

        for k, i in enumerate(round_data):
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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        if self.active_screen == "gaming" and not players.sprites()[0].winning:
            for j, rect in enumerate(rects):
                if rect.collidepoint(pos):
                    if j == 0 and not players.sprites()[0].morrendo:
                        self.restart()
                    elif j == 1:
                        self.active_screen = "paused"
                    elif j == 2:
                        if self.music_on:
                            pygame.mixer.music.stop()
                            self.music_on = False
                        else:
                            pygame.mixer.music.play(-1)
                            self.music_on = True

        elif self.active_screen == "paused":
            if continue_button_rect.collidepoint(pos):
                self.active_screen = "gaming"
            elif back_menu_button_rect.collidepoint(pos):
                self.restart()
                self.active_screen = "start"

        elif self.active_screen == "start":
            if play_button_rect.collidepoint(pos):
                self.active_screen = "levels"
            elif help_button_rect.collidepoint(pos):
                self.active_screen = "help"
            elif credits_button_rect.collidepoint(pos):
                self.active_screen = "credits"

        elif self.active_screen in ["help", "credits"]:
            if menu_button_rect.collidepoint(pos):
                self.active_screen = "start"

        elif self.active_screen == "levels":
            if lv1_button_rect.collidepoint(pos):
                self.active_screen = "gaming"
                self.lv_atual = 1
                self.restart()
            elif lv2_button_rect.collidepoint(pos) and lv_access[1][1]:
                self.active_screen = "gaming"
                self.lv_atual = 2
                self.restart()
            elif lv3_button_rect.collidepoint(pos) and lv_access[2][1]:
                self.active_screen = "gaming"
                self.lv_atual = 3
                self.restart()
            elif back_button_rect.collidepoint(pos):
                self.active_screen = "start"

    def update_ui_hover(self):
        for button in buttons:
            if buttons[button][0].collidepoint(pygame.mouse.get_pos()) and buttons[button][1]:
                button.set_alpha(180)
            else:
                button.set_alpha(0)
        for lvl in lv_access:
            if lv_access[lvl][0].collidepoint(pygame.mouse.get_pos()):
                lv_access[lvl][2].set_alpha(180)
            else:
                lv_access[lvl][2].set_alpha(0)

    def update_game_logic(self):
        fruits.update()
        all_sprites.update()

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

        for fruta in fruits:
            for gelo in iceblocks:
                if fruta.rect.colliderect(gelo.rect):
                    gelo.image.set_alpha(200)

        now = pygame.time.get_ticks()
        for player in players:
            if player.done:
                self.counter = 0
                self.round_atual += 1
                player.done = False
                fruits.empty()
                if self.round_atual != 1:
                    round_data = lvs[self.lv_atual - 1][self.round_atual]
                    round_data[3] = []
                    round_data[2] = []
                    round_data[0] = []
                    for k, i in enumerate(round_data):
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

        for player in players:
            if len(fruits) == 0:
                if self.round_atual == round_final:
                    player.winning = True
                    if self.counter == 0:
                        player.winning_timer = pygame.time.get_ticks()
                        self.counter = 1
                    if now - player.winning_timer >= 5000:
                        player.winning = False
                        self.restart()
                        if self.lv_atual != lv_final:
                            lv_access[self.lv_atual] = (lv_access[self.lv_atual][0], True, lv_access[self.lv_atual][2])
                        self.active_screen = "levels"
                else:
                    player.done = True

            if player.morto:
                self.restart()
                self.active_screen = "levels"

    def draw(self):
        if self.active_screen == "gaming":
            self.screen.blit(self.background_surface, self.background_rect)
            self.screen.blit(iglu_inv_surf, iglu_inv_rect)

            if not players.sprites()[0].winning:
                fruits.draw(self.screen)
                all_sprites.draw(self.screen)
                iceblocks.draw(self.screen)
            else:
                fruits.draw(self.screen)
                iceblocks.draw(self.screen)
                all_sprites.draw(self.screen)

            for player in players:
                score_str = str(player.pontos).zfill(6)
                self.screen.blit(scores["p"], scores["p"].get_rect(topleft=(60, 2)))
                for index, digit in enumerate(score_str):
                    x = 110 + index * 25
                    y = 0 + 20
                    self.screen.blit(scores[int(digit)], scores[int(digit)].get_rect(topleft=(x, y)))

            x = -120
            rects.clear()
            for i in icons:
                if i == icons[-1]:
                    x = -30
                rect = i.get_rect(topright=(800 + x, 15))
                self.screen.blit(i, rect)
                rects.append(rect)
                x += 40

        elif self.active_screen == "paused":
            self.screen.blit(paused_interface, paused_rect)
            self.screen.blit(continue_button_surf, continue_button_rect)
            self.screen.blit(back_menu_button_surf, back_menu_button_rect)

        elif self.active_screen == "start":
            self.screen.blit(start_interface, start_rect)
            self.screen.blit(play_button_surf, play_button_rect)
            self.screen.blit(help_button_surf, help_button_rect)
            self.screen.blit(credits_button_surf, credits_button_rect)

        elif self.active_screen == "levels":
            self.screen.blit(levels_interface, levels_rect)
            self.screen.blit(lv1_button_surf, lv1_button_rect)
            self.screen.blit(lv2_button_surf, lv2_button_rect)
            self.screen.blit(lv3_button_surf, lv3_button_rect)
            self.screen.blit(back_button_surf, back_button_rect)

        elif self.active_screen == "help":
            self.screen.blit(help_interface, help_rect)
            self.screen.blit(menu_button_surf, menu_button_rect)

        elif self.active_screen == "credits":
            self.screen.blit(credits_interface, credits_rect)
            self.screen.blit(menu_button_surf, menu_button_rect)

    def run(self):
        while True:
            play_music_for_screen(self.active_screen)
            self.handle_events()
            self.update_ui_hover()

            if self.active_screen == "gaming":
                self.update_game_logic()

            self.draw()

            pygame.display.update()
            self.clock.tick(60)
