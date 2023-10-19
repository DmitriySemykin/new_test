#Создай собственный Шутер!
from pygame import *
from random import *
from time import time as time1
#создай окно игры
clock = time.Clock()
game = True
finish = False
FPS = 60
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))#задай фон сцены
speed = 10
#музыка
mixer.init()
music_tracks = ['aaa.mp3', 'aa.mp3', 'aaaa.mp3']
random_track = choice(music_tracks)
mixer.music.load(random_track)
mixer.music.play()
fire = mixer.Sound('fire.ogg')
#монстры и астероиды
monsters = sprite.Group() #группа монстров
asteroids = sprite.Group() #группа астероидов
#счетчик 
font.init()
lost = 0
count = 0
hp = 5
font1 = font.Font(None, 36)
#пули
bullets = sprite.Group()
#Победа и Проигрыш
win = font1.render('YOU WIN', True, (255, 215, 0))
lose = font1.render('YOU LOSE', True, (200, 5, 0))
#перезарядка
num_fire = 0
rel_time = False #переменная-флаг с логическими значениями, отвечающая на вопрос: «Идёт ли перезарядка?».
#текст о перезарядки
text_reload = font1.render('Wait, reload...', True, (255, 215, 0))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.player_speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.player_speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    direction = "down"  # Начинаем движение вниз
    def update(self):
        if self.direction == "down":
            if self.rect.y < 500:  
                self.rect.y += self.player_speed
            else:
                self.direction = "up" 
        elif self.direction == "up":
            if self.rect.y > 10: 
                self.rect.y -= self.player_speed
            else:
                self.direction = "down"  

        global lost
        if self.rect.y > 499:
            self.rect.y = -10
            self.rect.x = randint(10, 500)
            self.player_speed = randint(1, 4)
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.player_speed 
        if self.rect.y > 500:
            self.kill()

rocket = Player("rocket.png", 350, 400, 10)

for i in range(1, 6):
    ufo = Enemy('ufo.png', randint(15, 600), -10, randint(1, 4))
    monsters.add(ufo)

for i in range(1, 6):
    asteroid = Enemy('asteroid.png', randint(15, 600), -10, randint(1, 4))
    asteroids.add(asteroid)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            if num_fire < 5 and rel_time == False:
                num_fire += 1
                rocket.fire()
                fire.play()

            if num_fire >= 5 and rel_time == False:
                lost_time = time1()
                #зафиксировать текущее время
                rel_time = True


    if finish != True:
        window.blit(background, (0, 0))

        rocket.update() 
        monsters.update()
        bullets.update()
        asteroids.update()
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprite_list1 = sprite.spritecollide(
        rocket, monsters, False
        )

        sprite_list2 = sprite.groupcollide(
        bullets, monsters, True, True
        )
        
        sprite_list3 = sprite.spritecollide(
        rocket, asteroids, True, False
        )

        for i in sprite_list2:
            count +=1
            ufo = Enemy('ufo.png', randint(15, 600), -10, randint(1, 4))
            monsters.add(ufo)

        for i in sprite_list3:
            hp -= 1
            asteroid = Enemy('asteroid.png', randint(15, 600), -10, randint(1, 4))
            asteroids.add(asteroid)


        #наши надписи
        text_lose = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))
        text_count = font1.render("Счёт:" + str(count), True, (255, 255, 255)) 
        #СЧЁТЧИК ЖИЗНЕЙ 
        hp_1 = font1.render("HP: " + str(hp), True, (255, 85, 25))

        window.blit(hp_1, (600, 60))
        window.blit(text_lose, (40, 70))
        window.blit(text_count, (40, 40))


        #лист для столкновения ракеты с астероидами
       
        if count >= 10:
            finish = True
            window.blit(win, (300, 200))

        if lost >= 10 or sprite_list1:
            finish = True
            window.blit(lose, (300, 200))

        if hp <= 0:
            finish = True
            window.blit(lose, (300, 200))

        if rel_time == True:
            time_now = time1()
            if time_now - lost_time < 3:
                window.blit(text_reload, (250, 400))
            else:
                num_fire = 0
                rel_time = False

        
        
    clock.tick(FPS)
    display.update()


"""
#создай игру "Лабиринт"!
from pygame import *
#создай окно игры
clock = time.Clock()
FPS = 60
window = display.set_mode((700, 500))
display.set_caption('Догонялки')
background = transform.scale(image.load('background.jpg'), (700, 500))#задай фон сцены
speed = 10
game = True
finish = False
#Надписи выйгрыша и проигрыша
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN', True, (255, 215, 0))
lose = font.render('YOU LOSE', True, (200, 5, 0))

#музыка
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')

money2 = mixer.Sound("money.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

money = GameSprite('treasure.png', 590, 400, 0)

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.player_speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.player_speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.player_speed
        if keys_pressed[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.player_speed

hero = Player('hero.png', 90, 70, 10)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = "right"  # Начинаем движение вправо
    def update2(self):
        if self.direction == "right":
            if self.rect.x < 630:  # Проверка, чтобы не выйти за правую границу
                self.rect.x += self.player_speed
            else:
                self.direction = "left"  # Если достигли правой границы, меняем направление на влево
        elif self.direction == "left":
            if self.rect.x > 400:  # Проверка, чтобы не выйти за левую границу
                self.rect.x -= self.player_speed
            else:
                self.direction = "right"  # Если достигли левой границы, меняем направление на вправо

enemy = Enemy('cyborg.png', 600, 300, 4)

class Wall(sprite.Sprite): 
    def __init__(self, wall_width, wall_height, wall_x,wall_y): 
        super().__init__() 
        self.width = wall_width 
        self.height = wall_height 
        self.image = Surface((self.width, self.height)) 
        self.image.fill((255,0,0)) 
        self.rect = self.image.get_rect() 
        self.rect.x = wall_x 
        self.rect.y = wall_y 
     
    def draw_wall(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))

stena = Wall(690,10,12,50)
stena2 = Wall(100,10,12,140)
stena3 = Wall(10,240,400,140)
stena4 = Wall(690,10,12,490)
stena5 = Wall(210,10,200,140)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        hero.reset()
        enemy.reset()

        hero.update()
        enemy.update2()
        money.reset()

        stena.draw_wall() 
        stena2.draw_wall() 
        stena3.draw_wall()
        stena4.draw_wall()
        stena5.draw_wall()


        if sprite.collide_rect(hero, money):
            finish = True
            money2.play()
            window.blit(win, (200, 200))
        if sprite.collide_rect(hero, enemy) or sprite.collide_rect(hero, stena) or sprite.collide_rect(hero, stena2) or sprite.collide_rect(hero, stena3) or sprite.collide_rect(hero, stena4) or sprite.collide_rect(hero, stena5):
            finish = True
            kick.play()
            window.blit(lose, (200, 200))
        
    
        clock.tick(FPS)
        display.update()
"""