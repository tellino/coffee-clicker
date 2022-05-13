import pygame
import json
import datetime

from sys import exit
from os.path import isfile

WIDTH = 1000
HEIGHT = 800
FPS = 60
BG_SPEED = 1
LOGIN_BUTTON_SPEED = 1
BROWN = '#834B02'
OPACITY_SWITCH = 15
STAND_SPACE = 10
MAX_OFFLINE_TIME = 2  # Hours

pygame.init()
pygame.display.set_caption('Coffee Clicker')
pygame.display.set_icon(pygame.image.load('data/images/icon/bean.png'))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def play_click():
    if play_sound:
        buy.play()

def play_tap():
    if play_sound:
        click.play()

def get_font(dim):
    return pygame.font.Font('data/fonts/Helvetica Neue.ttf', dim)

def terminate():

    data = {
        'beans': bean_stand.beans,
        'click_upgrade': click_upgrade.level,
        'level_1_autoclick': level_1_autoclick.level,
        'level_2_autoclick': level_2_autoclick.level,
        'level_3_autoclick': level_3_autoclick.level,
        'level_4_autoclick': level_4_autoclick.level,
        'beans_per_second': bean_stand.autoclick_beans,
        'date': str(datetime.datetime.now())
    }

    filename = 'data.json'
    with open(filename, 'w') as f:
        json.dump(data, f)

    pygame.quit()
    exit()

class Background:
    
    def __init__(self):
        self.image = pygame.image.load('data/images/background/empty.png').convert_alpha()
        self.reset()

    def scroll(self):
        if self.rect.top == 0:
            self.reset()

        else:
            self.rect = self.image.get_rect(topleft=(self.rect.top+BG_SPEED, self.rect.left+BG_SPEED))

    def display(self):
        screen.blit(self.image, self.rect)

    def reset(self):
        self.rect = self.image.get_rect(topleft=(-19, -19))

class Button:
    
    def __init__(self, centerx, centery, path_1, path_2, scale):

        self.animation_dir = 1
        self.animation_index = 0
        self.opacity = 255
        
        self.centerx = centerx
        self.centery = centery

        self.df_img = pygame.image.load(path_1).convert_alpha()
        self.df_img = pygame.transform.rotozoom(self.df_img, 0, scale)

        self.hv_img = pygame.image.load(path_2).convert_alpha()
        self.hv_img = pygame.transform.rotozoom(self.hv_img, 0, scale)

        self.rect = self.df_img.get_rect(center=(centerx, centery))

        self.check_hover()
    
    def display(self):
        if self.check_hover():
            screen.blit(self.hv_img, self.rect)
            
        else:
            screen.blit(self.df_img, self.rect)
    
    def animate(self):

        if round(self.animation_index, 1) == 0.5:
            if self.rect.center[1] == self.centery + 5 or self.rect.center[1] == self.centery - 5:
                self.animation_dir *= -1

            self.rect = self.df_img.get_rect(center=(self.centerx, (self.rect.center[1]+LOGIN_BUTTON_SPEED * self.animation_dir)))

            self.animation_index = 0

        else:
            self.animation_index += 0.1

    def check_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def click(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) == 1 and pygame.mouse.get_pressed()[0]

    def update(self):
        self.df_img.set_alpha(self.opacity)
        self.hv_img.set_alpha(self.opacity)

class Bean:
    
    def __init__(self):
        self.image = pygame.image.load('data/images/logo/bean.png')
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=(WIDTH/2, 400))

        self.opacity = 0
        self.animation_dir = 1
    
    def animate(self):
        global bean_animation_amount

        if bean_animation_amount == 10 or bean_animation_amount == -10:
            self.animation_dir *= -1
        
        bean_animation_amount += self.animation_dir

        self.image = pygame.transform.scale(self.image, (self.image.get_width() + bean_animation_amount, self.image.get_height() + bean_animation_amount))
        self.rect = self.image.get_rect(center=(WIDTH/2, 400))

        self.display()
        self.reset()

    def display(self):
        screen.blit(self.image, self.rect)
        
    def update(self):
        self.image.set_alpha(self.opacity)

    def reset(self):
        self.image = pygame.image.load('data/images/logo/bean.png')
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=(WIDTH/2, 400))

    def click(self):
        global bean_stand

        bean_stand.click()
        play_tap()

class BeanStand:

    def __init__(self, beans):
        self.image = pygame.image.load('data/images/stands/bean_stand.png')
        self.rect = self.image.get_rect(center=(WIDTH/2, STAND_SPACE + 50))

        self.beans_per_click = 1

        self.beans = beans
        self.beans_text = get_font(60).render(f'{self.beans}', True, BROWN)
        self.beans_rect = self.beans_text.get_rect(center=(500, STAND_SPACE + self.rect.height/2))

        self.bean_image = pygame.image.load('data/images/logo/bean.png')
        self.bean_image = pygame.transform.scale(self.bean_image, (50, 50))
        self.bean_rect = self.bean_image.get_rect(center=(500, STAND_SPACE + self.rect.height/2))

        # Autoclick #

        self.autoclick_beans = 0
        self.autoclick_beans_text = get_font(35).render(f'{self.autoclick_beans}/second', True, BROWN)
        self.autoclick_beans_rect = self.autoclick_beans_text.get_rect(center=(500, STAND_SPACE + self.rect.height/2))

        self.autoclick_bean_image = pygame.image.load('data/images/logo/bean.png')
        self.autoclick_bean_image = pygame.transform.scale(self.autoclick_bean_image, (32, 32))
        self.autoclick_bean_rect = self.autoclick_bean_image.get_rect(center=(500, STAND_SPACE + self.rect.height/2))
    
    def display(self):
        self.update()
        screen.blit(self.image, self.rect)
        screen.blit(self.bean_image, self.bean_rect)
        screen.blit(self.beans_text, self.beans_rect)

        screen.blit(self.autoclick_bean_image, self.autoclick_bean_rect)
        screen.blit(self.autoclick_beans_text, self.autoclick_beans_rect)
    
    def update(self):
        self.beans_text = get_font(60).render(f'{round(self.beans)}', True, BROWN)
        self.beans_rect = self.beans_text.get_rect(center=(500, STAND_SPACE + self.rect.height/2))

        self.autoclick_beans_text = get_font(35).render(f'{self.autoclick_beans}/second', True, BROWN)
        self.autoclick_beans_rect = self.autoclick_beans_text.get_rect(center=(500, STAND_SPACE + self.rect.height/2))

        text_width = self.beans_rect.width
        bean_width = self.bean_rect.width

        self.bean_rect = self.bean_image.get_rect(center=(WIDTH/2 - (text_width/2 + bean_width - 15), STAND_SPACE + self.rect.height/2 - 15))
        self.beans_rect = self.beans_text.get_rect(center=(WIDTH/2, STAND_SPACE + self.rect.height/2 - 15))

        autoclick_text_width = self.autoclick_beans_rect.width
        autoclick_bean_width = self.autoclick_bean_rect.width

        self.autoclick_bean_rect = self.autoclick_bean_image.get_rect(center=(WIDTH/2 - (autoclick_text_width/2 + autoclick_bean_width - 10), STAND_SPACE + self.rect.height/2 + 25))
        self.autoclick_beans_rect = self.autoclick_beans_text.get_rect(center=(WIDTH/2, STAND_SPACE + self.rect.height/2 + 25))

    def click(self):
        self.beans += self.beans_per_click
        self.beans = round(self.beans, 1)
        self.update()

class ClickUpgrade:
    
    def __init__(self, level):
        
        self.level = level
        self.cost = 20
        for level in range(self.level):
            self.cost = round(self.cost * 1.75)

        self.image = pygame.image.load('data/images/upgrades/click_upgrade/click_upgrade.png')
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.rect = self.image.get_rect(center=(WIDTH/2, 700))

        self.hover_image = pygame.image.load('data/images/upgrades/click_upgrade/clicked_click_upgrade.png')
        self.hover_image = pygame.transform.scale(self.hover_image, (180, 180))
        self.hover_image_rect = self.hover_image.get_rect(center=(WIDTH/2, 700))

        self.lvl_text = get_font(40).render(f'lvl.{self.level}', True, BROWN)
        self.lvl_rect = self.lvl_text.get_rect(center=(WIDTH/2 + 7, 670))

        self.cost_image = pygame.image.load('data/images/logo/bean.png')
        self.cost_image = pygame.transform.scale(self.cost_image, (24, 24))
        self.cost_image_rect = self.cost_image.get_rect(center=(WIDTH/2, 710))

        self.cost_text = get_font(40).render(f'{self.cost}', True, BROWN)
        self.cost_text_rect = self.cost_text.get_rect(center=(WIDTH/2, 710))
    
    def display(self):

        self.update()

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.hover_image, self.hover_image_rect)
        
        else:
            screen.blit(self.image, self.rect)

        screen.blit(self.lvl_text, self.lvl_rect)

        screen.blit(self.cost_image, self.cost_image_rect)
        screen.blit(self.cost_text, self.cost_text_rect)
    
    def update(self):

        self.lvl_text = get_font(40).render(f'lvl.{self.level}', True, BROWN)
        self.lvl_rect = self.lvl_text.get_rect(center=(WIDTH/2 + 7, 685))
        
        self.cost_text = get_font(30).render(f'{self.cost}', True, BROWN)
        self.cost_text_rect = self.cost_text.get_rect(center=(WIDTH/2, 670))

        cost_width = self.cost_text_rect.width
        image_width = self.cost_image_rect.width

        self.cost_image_rect = self.cost_image.get_rect(center=(WIDTH/2 - (cost_width/2 + image_width - 15) + 5, 645 + self.rect.height/2))
        self.cost_text_rect = self.cost_text.get_rect(center=(WIDTH/2 + 10 + 5, 645 + self.rect.height/2))
    
    def click(self):

        if bean_stand.beans >= self.cost:

            if play_sound:
                buy.play()

            bean_stand.beans -= self.cost
            self.level += 1
            self.cost = round(self.cost * 1.75)
            bean_stand.beans_per_click = round(bean_stand.beans_per_click * 1.2, 1)

class AutoclickUpgrade:


    
    def __init__(self, level, cost, bps, path_1, path_2, centerx, centery):

        self.x = centerx
        self.y = centery

        self.bean_icon = pygame.image.load('data/images/logo/bean.png')
        self.bean_icon = pygame.transform.scale(self.bean_icon, (24, 24))
        
        self.level = level
        self.cost = cost

        for level in range(self.level):
            self.cost = round(self.cost * 1.75)

        self.bean_per_second = bps

        for level in range(self.level):
            bean_stand.autoclick_beans += self.bean_per_second

        self.image = pygame.image.load(path_1)
        self.image = pygame.transform.scale(self.image, (180, 180))

        self.hover_image = pygame.image.load(path_2)
        self.hover_image = pygame.transform.scale(self.hover_image, (180, 180))

        self.rect = self.image.get_rect(center=(centerx, centery))
        self.hover_rect = self.hover_image.get_rect(center=(centerx, centery))

        self.lvl_text = get_font(40).render(f'lvl.{self.level}', True, BROWN)
        self.lvl_rect = self.lvl_text.get_rect(center=(WIDTH/2 + 7, 670))

        self.cost_image = pygame.image.load('data/images/logo/bean.png')
        self.cost_image = pygame.transform.scale(self.cost_image, (24, 24))
        self.cost_image_rect = self.cost_image.get_rect(center=(WIDTH/2, 710))

        self.cost_text = get_font(40).render(f'{self.cost}', True, BROWN)
        self.cost_text_rect = self.cost_text.get_rect(center=(WIDTH/2, 710))
    
    def display(self):

        self.update()

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.hover_image, self.hover_rect)
        
        else:
            screen.blit(self.image, self.rect)
        
        screen.blit(self.lvl_text, self.lvl_rect)
        screen.blit(self.bean_icon, self.bean_icon_rect)
        screen.blit(self.cost_text, self.cost_rect)
        
    def update(self):

        self.lvl_text = get_font(40).render(f'lvl.{self.level}', True, BROWN)
        self.lvl_rect = self.lvl_text.get_rect(center=(self.x, self.y - 15))

        self.cost_text = get_font(30).render(f'{self.cost}', True, BROWN)
        self.cost_rect = self.cost_text.get_rect(center=(self.x + self.bean_icon.get_width(), self.y + 30))

        self.bean_icon_rect = self.bean_icon.get_rect(center=(self.x - self.cost_text.get_width()/2, self.y + 30))

    def click(self):
        if bean_stand.beans >= self.cost:

            if play_sound:
                buy.play()

            bean_stand.beans -= self.cost
            self.level += 1
            self.cost = round(self.cost * 1.75)
            bean_stand.autoclick_beans += self.bean_per_second

class OptionButton:

    def __init__(self, x, y):

        self.image = pygame.image.load('data/images/buttons/option.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))

        self.hover_image = pygame.image.load('data/images/buttons/clicked_option.png')
        self.hover_image = pygame.transform.scale(self.hover_image, (100, 100))
        self.hover_rect = self.hover_image.get_rect(center=(x, y))
    
    def display(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.hover_image, self.hover_rect)

        else:
            screen.blit(self.image, self.rect)
    
    def click(self):
        pass

class Option:
    
    def __init__(self):
        
        self.image = pygame.image.load('data/images/background/option_background.png')
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))

        self.close_button = pygame.image.load('data/images/buttons/close_button/close_button.png')
        self.close_button = pygame.transform.scale(self.close_button, (75, 75))
        self.close_rect = self.close_button.get_rect(center=(950, 50))

        self.hover_close_button = pygame.image.load('data/images/buttons/close_button/clicked_close_button.png')
        self.hover_close_button = pygame.transform.scale(self.hover_close_button, (75, 75))

        self.text = get_font(70).render('OPTIONS', True, BROWN)
        self.text_rect = self.text.get_rect(center=(WIDTH/2, 150))

        self.sound_text = get_font(50).render('Sound', True, BROWN)
        self.sound_rect = self.sound_text.get_rect(center=(300, 300))

        self.music_text = get_font(50).render('Music', True, BROWN)
        self.music_rect = self.music_text.get_rect(center=(300, 400))

        self.on_button = pygame.image.load('data/images/buttons/on_button/on_button.png')
        self.on_button = pygame.transform.scale(self.on_button, (100, 80))

        self.hover_on_button = pygame.image.load('data/images/buttons/on_button/clicked_on_button.png')
        self.hover_on_button = pygame.transform.scale(self.hover_on_button, (100, 80))

        self.off_button = pygame.image.load('data/images/buttons/off_button/off_button.png')
        self.off_button = pygame.transform.scale(self.off_button, (100, 80))

        self.hover_off_button = pygame.image.load('data/images/buttons/off_button/clicked_off_button.png')
        self.hover_off_button = pygame.transform.scale(self.hover_off_button, (100, 80))

        self.sound_button = self.on_button.get_rect(center=(700, 300))
        self.music_button = self.on_button.get_rect(center=(700, 400))
        
     
    def display(self):
        screen.blit(self.image, self.rect)
        
        if self.close_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.hover_close_button, self.close_rect)
        
        else:
            screen.blit(self.close_button, self.close_rect)

        screen.blit(self.text, self.text_rect)
        screen.blit(self.sound_text, self.sound_rect)

        if play_sound:
            if self.sound_button.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.hover_on_button, self.sound_button)
            
            else:
                screen.blit(self.on_button, self.sound_button)
        
        else:
            if self.sound_button.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.hover_off_button, self.sound_button)
            
            else:
                screen.blit(self.off_button, self.sound_button)
        
        screen.blit(self.music_text, self.music_rect)

        if play_music:
            if self.music_button.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.hover_on_button, self.music_button)
            
            else:
                screen.blit(self.on_button, self.music_button)
        
        else:
            if self.music_button.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.hover_off_button, self.music_button)
            
            else:
                screen.blit(self.off_button, self.music_button)

if isfile('data.json'):
    with open('data.json') as f:
        data = json.load(f)
    
    beans = data['beans']
    click_upgrades = data['click_upgrade']

    level_1_autoclicks = data['level_1_autoclick']
    level_2_autoclicks = data['level_2_autoclick']
    level_3_autoclicks = data['level_3_autoclick']
    level_4_autoclicks = data['level_4_autoclick']

    beans_per_second = data['beans_per_second']

    old_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S.%f')
    new_date = datetime.datetime.now()

    max_difference = MAX_OFFLINE_TIME * 3600
    difference = new_date - old_date

    if difference.total_seconds() > max_difference:
        beans_boost = round(beans_per_second * max_difference)
    
    else:
        beans_boost = round(beans_per_second * difference.total_seconds())

    beans += beans_boost

else:

    beans = 0
    click_upgrades = 0

    level_1_autoclicks = 0
    level_2_autoclicks = 0
    level_3_autoclicks = 0
    level_4_autoclicks = 0

bg = Background()
login = Button(WIDTH/2, 500, 'data/images/login/login_1.png', 'data/images/login/login_2.png', 1)
leave = Button(WIDTH/2, 620, 'data/images/leave/leave_1.png', 'data/images/leave/leave_2.png', 0.75)
bean = Bean()
bean_stand = BeanStand(beans)
click_upgrade = ClickUpgrade(click_upgrades)

level_1_autoclick = AutoclickUpgrade(level_1_autoclicks, 100, 1, 'data/images/upgrades/upgrade_1/upgrade_1.png', 'data/images/upgrades/upgrade_1/clicked_upgrade_1.png', 100, 200)
level_2_autoclick = AutoclickUpgrade(level_2_autoclicks, 250, 3, 'data/images/upgrades/upgrade_2/upgrade_2.png', 'data/images/upgrades/upgrade_2/clicked_upgrade_2.png', 100, 400)
level_3_autoclick = AutoclickUpgrade(level_3_autoclicks, 500, 7, 'data/images/upgrades/upgrade_3/upgrade_3.png', 'data/images/upgrades/upgrade_3/clicked_upgrade_3.png', 900, 200)
level_4_autoclick = AutoclickUpgrade(level_4_autoclicks, 1500, 20, 'data/images/upgrades/upgrade_4/upgrade_4.png', 'data/images/upgrades/upgrade_4/clicked_upgrade_4.png', 900, 400)

option_button = OptionButton(50, 40)
option_menu = Option()

click = pygame.mixer.Sound('data/sounds/click.wav')
buy = pygame.mixer.Sound('data/sounds/buy.wav')
music = pygame.mixer.Sound('data/sounds/music.wav')

logo = pygame.image.load('data/images/logo/bean.png')
logo_rect = logo.get_rect(center=(WIDTH/2, 120))

title = get_font(100).render('Coffee Clicker', True, BROWN)
title_rect = title.get_rect(center=(WIDTH/2, 260))

menu = True
game = False
option = False
opacity = 255
bean_animation_index = 0
bean_animation_amount = 0

autoclick_timer = pygame.USEREVENT + 1
pygame.time.set_timer(autoclick_timer, 1000)

play_music = True
play_sound = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        if event.type == autoclick_timer:
            bean_stand.beans += bean_stand.autoclick_beans
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                
                if menu:
                    
                    if login.rect.collidepoint(event.pos):
                        play_click()
                        menu = False
                        menu_leaving = True

                    elif leave.rect.collidepoint(event.pos):
                        play_click()
                        terminate()
                
                elif game:

                    if option_button.rect.collidepoint(event.pos):
                        play_click()
                        game = False
                        option = True

                    if bean.rect.collidepoint(event.pos):
                        
                        bean.click()

                    if click_upgrade.rect.collidepoint(event.pos):
                        
                        click_upgrade.click()
                    
                    if level_1_autoclick.rect.collidepoint(event.pos):

                        level_1_autoclick.click()
                    
                    if level_2_autoclick.rect.collidepoint(event.pos):

                        level_2_autoclick.click()
                    
                    if level_3_autoclick.rect.collidepoint(event.pos):

                        level_3_autoclick.click()
                    
                    if level_4_autoclick.rect.collidepoint(event.pos):

                        level_4_autoclick.click()

                elif option:

                    if option_menu.sound_button.collidepoint(pygame.mouse.get_pos()):
                        play_click()
                        play_sound = not play_sound
                    
                    if option_menu.music_button.collidepoint(pygame.mouse.get_pos()):
                        play_click()
                        play_music = not play_music
                    
                    if option_menu.close_rect.collidepoint(pygame.mouse.get_pos()):
                        play_click()
                        option = False
                        game = True

    bg.scroll()
    bg.display()

    if menu:
        login.display()
        login.animate()

        leave.display()
        leave.animate()

        screen.blit(logo, logo_rect)
        screen.blit(title, title_rect)
    
    elif menu_leaving:

        login.opacity = opacity
        leave.opacity = opacity
        logo.set_alpha(opacity)
        title.set_alpha(opacity)

        login.update()
        leave.update()

        login.display()
        leave.display()
        screen.blit(logo, logo_rect)
        screen.blit(title, title_rect)

        opacity -= OPACITY_SWITCH

        if opacity == 0:
            menu_leaving = False
            game_entering = True

    elif game_entering:
        bean.opacity = opacity

        bean.update()
        bean.display()

        opacity += OPACITY_SWITCH

        if opacity == 255:
            game_entering = False
            game = True
    
    elif game:
        bean.animate()
        bean_stand.display()

        click_upgrade.display()

        level_1_autoclick.display()
        level_2_autoclick.display()
        level_3_autoclick.display()
        level_4_autoclick.display()

        option_button.display()

    elif option:
        option_menu.display()

    if not play_music:
        music.stop()
    
    if play_music and not pygame.mixer.get_busy():
        music.play()
        music.set_volume(0.1)

    clock.tick(FPS)
    pygame.display.update()