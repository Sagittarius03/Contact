import pygame
import random
import time
from screeninfo import get_monitors
#___________________________________________#
WIDTH = 1280 # ширина игрового окна
HEIGHT =  800 # высота игрового окна
FPS = 60 # частота кадров в секунду

for m in get_monitors():
    if m.height < HEIGHT+100:
        HEIGHT = m.height-100
    if m.width < WIDTH+100:
        WIDTH = m.width-100

lvl = 1
Complexity_index = 0
Complexity = ['Легко', "Средне", "Сложно", "Выживание"]
hints = [
    "У вас всё хорошо, можете смело лететь, коммандер!",
    "Немного сбоят щиты, но ничего страшного",
    "Щиты в ужасном состоянии, будьте окуратны",
    "Их целый Легион, лучше не надо, выиграть здесь нельзя",
]
#___________________________________________#

pygame.init() #Запуск Движка
pygame.mixer.init()  # Иницилизация звука
from volum_config import * #Инициализирует звуки

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Создание Окна
        self.title = pygame.display.set_caption("Контакт") #Имя окна
        self.clock = pygame.time.Clock() #Игровой счётчик
        
        self.pause = False #Игра на паузе?
        self.menu = True #Меню запущено?
        self.running = True #Игры запущена?
        self.game_over = False # Игра проиграна?
        self.group_init()
        
        self.background = None
        self.background_rect = None
    def init_events(self): #Иниц. событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Окно закрывается
                self.running = False
                pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #Игрок стреляет Пробел
                    if player.life >0:
                        player.shoot()
                elif event.key == pygame.K_ESCAPE: #Пауза игры на ESC
                    if self.menu == False:
                        if self.pause == False:
                            self.pause = True
                            for i in sounds: #Поставить заглушку на всех звуках
                                i.mute()
                            pygame.mixer.music.pause() # Поставить паузу на музыке
                            game.text_stop()
                        else:
                            self.pause = False
                            for i in sounds: # Снять заглушку со всех звуков
                                i.unmute()
                            pygame.mixer.music.unpause() # Снять паузу с игровой музыки          

    def group_init(self):
        self.all_sprites = pygame.sprite.Group() #Все спрайты (Для отрисовки на экране)
        self.mobs = pygame.sprite.Group() # Спрайты врагов (Нужны для того, чтобы стреляли или умирали он выстрелов игрока)

        self.booms = pygame.sprite.Group() # Спрайты взрывов, нужен для взаимодействия взрыва торпеды и игрока
        self.bonus = pygame.sprite.Group() # Спрайты бонусов, для взаимодействия игрока и бонусов, которые дают тот или иной эффект

        self.bullets_enemy = pygame.sprite.Group() #Патроны врагов
        self.bullets_player = pygame.sprite.Group() #Патроны игрока
        self.bullets_mine = pygame.sprite.Group() #Патроны мины(торпеды)
        """Для того, чтобы не было путаницы в обработчике столкновений"""

        self.buttons = pygame.sprite.Group() # Группа кнопок в меню игры
        
    def border(self, obj): #Удерживает объект в поле игры
        if obj.rect.right > WIDTH:
            obj.rect.right = WIDTH
        elif obj.rect.left < 0:
            obj.rect.left = 0
        elif obj.rect.top < 0:
            obj.rect.top = 0
        elif obj.rect.bottom > HEIGHT:
            obj.rect.bottom = HEIGHT

    def GameOver(self):
        game.pause = True
        game.game_over = True
        f = pygame.font.SysFont('serif', 148)
        text = f.render("GAME OVER", False,
                        (255, 255, 255))
        game.screen.blit(text, (200, HEIGHT/2-80))

        pygame.display.update()
    def Win(self):
        game.pause = True
        f = pygame.font.SysFont('serif', 148)
        text = f.render("YOU WIN!!!", False,
                        (255, 255, 255))
        game.screen.blit(text, (WIDTH/2-400, HEIGHT/2-150))
        pygame.display.update()
    def text_stop(self):
        f = pygame.font.SysFont('serif', 148)
        text = f.render("ПАУЗА", False,
                        (255, 255, 255))
        game.screen.blit(text, (WIDTH/2-250, HEIGHT/2-80))
        pygame.display.update()
class Timer(): #Счетчик, для задержки функций
    def __init__(self):
        self.time = 0
    def update(self):
        self.time += 0.01
        return self.time
class Mouse(pygame.sprite.Sprite): #Ложный спрайт мыши для менюшки
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
    def update(self):
        self.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))

if True: #Для групировки
    #>Супер классы
    class Shell(pygame.sprite.Sprite): #Класс снярядов
        def __init__(self, ship, image, sound, damage, speed, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

            self.ship = ship
            if self.ship != player and image != "img\Shell\Rocket.png":
                self.image = pygame.transform.rotate(self.image, 180)

            self.sound = sound
            self.speed = speed
            self.damage = damage

            if sound != None:
                sound.play() #Звук
    class Effect(pygame.sprite.Sprite): #Эффекты от попаданий
        def __init__(self, image, sound, damage, timer, x, y,):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x

            self.damage = damage
            self.timer = timer

            game.all_sprites.add(self)
            sound.play()
    class Bonus(pygame.sprite.Sprite): #Бонусы для игрока
        def __init__(self, image, sound, num, speed, x, y):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x

            self.speed = speed
            self.num = num
            self.sound = sound

            game.all_sprites.add(self)
            game.bonus.add(self)

        def update(self):
            self.rect.x += self.speed

            if self.rect.x > WIDTH:
                self.kill()
    class Ship(pygame.sprite.Sprite): #Корабли на поле
        def __init__(self,
                image, 
                scale=None,
                rotate=None,

                speed_x=0, 
                speed_y=0,

                shield=0,
                armor=0,
                life=200,

                x=WIDTH/2, 
                y=HEIGHT/2
        ):
            pygame.sprite.Sprite.__init__(self)
            
            self.image = pygame.image.load(image)
            if scale!=None:
                self.image = pygame.transform.scale(self.image, scale)
            if rotate!=None:
                self.image = pygame.transform.rotate(self.image, rotate)

            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

            self.speedx = 0
            self.speedy = 0

            self.movement_x = speed_x
            self.movement_y = speed_y

            self.shield=shield
            self.armor=armor
            self.life=life

            self.timer_update = Timer()
        def flight(self):
            timer = self.timer_update.update()
            if timer > 1.00 and timer < 1.01:
                self.speedx = random.randint(-self.movement_x, self.movement_x)
                self.speedy = random.randint(-self.movement_y, self.movement_y)
            if timer > 4:
                self.timer_update = Timer()
                self.speedx = 0
                self.speedy = 0

            if self.rect.right == WIDTH:
                self.speedx -= random.randint(2, self.movement_x)
            if self.rect.left == 0:
                self.speedx += random.randint(2, self.movement_x)
            if self.rect.top <= 0:
                self.speedy += self.movement_y
            if self.rect.bottom > HEIGHT/2:
                self.speedy -= self.movement_y

            self.rect.x += self.speedx
            self.rect.y += self.speedy

            game.border(self) # Для удержания объекта на поле боя
    #-----------------------------
    #>Снаряды
    class Bullet(Shell):
        def __init__(self, ship, x, y): #МЕТКА - Выдает ошибку.
            super().__init__(ship, "img\Shell\Bullet.png", sounds[0], damage=15, speed=10, x=x, y=y)
        def update(self):
            if self.ship == player:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
            
            if self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.kill()
    class Rocket(Shell):
        def __init__(self, ship, x, y):
            super().__init__(ship, "img\Shell\Rocket.png", sound=None, damage=45, speed=0.25, x=x, y=y)
            if not(self.ship == player):
                self.image = pygame.transform.rotate(self.image, 180)
        def update(self):
            self.speed += 0.25
            if self.ship == player:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
            
            if self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.kill()
    class Mine(Shell):
        def __init__(self, ship, x, y):
            super().__init__(ship, "img\Shell\Mine.png", sound=None, damage=0, speed=1, x=x, y=y)
            self.speed_x = random
            self.timer = Timer()
            self.timer_speed = Timer()
        def update(self):
            timer_speed = self.timer_speed.update()
            if timer_speed > 2:
                self.speed_x = random.uniform(0.25, 1.00)
                self.timer_speed = Timer()
            if self.ship == player:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

            timer = self.timer.update()
            if timer > 4.3:
                self.boom()
                self.kill()
            
            if self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.kill()
        def boom(self):
            self.explosion = Boom(self.rect.x, self.rect.y)
            game.all_sprites.add(self.explosion)
            game.booms.add(self.explosion)
    #-----------------------------
    #>Эффекты
    class Boom(Effect):
        def __init__(self, x, y):
            super().__init__("img\Effect\BoomMine - Animation\BoomMine1.png", sound=sounds[1], damage=70, timer=4, x=x, y=y)
            self.image = pygame.transform.scale(self.image, (int(160/5), int(161/5)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.index_animation = 1
            game.booms.add(self)
            self.counter = Timer()
        def update(self):
            if self.counter.update() > 0.55:
                self.index_animation += 1
                self.counter = Timer()
                if self.index_animation < 7:
                    self.image = pygame.image.load(f"img\Effect\BoomMine - Animation\BoomMine{self.index_animation}.png")
                    self.image = pygame.transform.scale(self.image, (int(160/4), int(161/4)))
                else:
                    self.kill()

            if self.counter.update() > self.timer:
                self.kill()
    class Boom_Ship(Effect):
        def __init__(self, x, y):
            super().__init__("img\Effect\Boom-Ship.png", sound=sounds[1], damage=70, timer=0.25, x=x, y=y)
            self.index_animation = 1
            self.counter = Timer()
        def update(self):
            if self.counter.update() > self.timer:
                self.kill()
    class Shield_Player(Effect):
        def __init__(self, x, y):
            super().__init__("img\Effect\Shiled_Player.png", sound=sounds[2], damage=0, timer=0.14, x=x, y=y)
            self.index_animation = 1
            self.counter = Timer()
        def update(self):
            if self.counter.update() > self.timer:
                self.kill()
    class Shield_Enemy(Effect):
        def __init__(self, x, y):
            super().__init__("img\Effect\Shiled_Enemy.png", sound=sounds[2], damage=0, timer=0.14, x=x, y=y)
            self.index_animation = 1
            self.counter = Timer()
        def update(self):
            if self.counter.update() > self.timer:
                self.kill()
    #-----------------------------
    class Shield_Bonus(Bonus):
        def __init__(self, x, y):
            super().__init__("img\Bonus\\bonus_shield.png", sound=sounds[4], num= 20, speed=1, x=x, y=y)

        def start_effect(self):
            if player.shield <= 0:
                self.sound.play()
            player.shield += self.num
    class Health_Bonus(Bonus):
        def __init__(self, x, y):
            super().__init__("img\Bonus\\bonus_health.png", sound=sounds[5], num= 50, speed=1, x=x, y=y)

        def start_effect(self):
            self.sound.play()
            player.life += self.num
    class Rocket_Bonus(Bonus):
        def __init__(self, x, y):
            super().__init__("img\Bonus\\bonus_rocket.png", sound=sounds[6], num= 5, speed=1, x=x, y=y)

        def start_effect(self):
            self.sound.play()
            player.rocket += self.num
    #-----------------------------
    #>Корбли
    class Player(Ship):
        def __init__(self, x, y):
            super().__init__(
                image="img\Ship\Player.png",
                scale=(55, 87),
                rotate=None,
                speed_x=8, 
                speed_y=6,

                shield=300,
                armor=100,
                life=100,

                x=x,
                y=y,
            )

            self.rocket = 0

        def update(self):
            self.speedx = 0
            self.speedy = 0

            keystate = pygame.key.get_pressed()

            if keystate[pygame.K_LEFT]:
                self.speedx -= self.movement_x
            if keystate[pygame.K_RIGHT]:
                self.speedx += self.movement_x
            if keystate[pygame.K_DOWN]:
                self.speedy += self.movement_y
            if keystate[pygame.K_UP]:
                self.speedy -= self.movement_y

            self.rect.x += self.speedx
            self.rect.y += self.speedy

            game.border(self) # Для удержания объекта на поле боя
        def shoot(self):
            if self.rocket > 0:
                bullet = Rocket(self, self.rect.centerx, self.rect.top+15)
                self.rocket -= 1
                game.all_sprites.add(bullet)
                game.bullets_player.add(bullet)
            else:
                bullet = Bullet(self, self.rect.centerx, self.rect.top)
                game.all_sprites.add(bullet)
                game.bullets_player.add(bullet)
    class Interceptor(Ship):
        def __init__(self, x, y):
            super().__init__(
                "img\Ship\Interceptor.png",
                scale=None,
                rotate=None,

                speed_x= 10,
                speed_y=3,

                shield=25,
                armor=20,
                life=40,

                x=x,
                y=y)

            self.start_y = y
            self.start_pos = False
            
            self.timer_shoot = Timer()
        def update(self):
            if self.start_pos == False:
                self.rect.y += 2
            if self.rect.y >= self.start_y:
                self.start_pos = True

            if self.start_pos == True:
                self.shooter()
                self.flight()
        def shooter(self):
            timer_time = random.randint(3, 5)
            timer = self.timer_shoot.update()

            if timer > timer_time and timer < timer_time+0.05:
                self.shoot()
            if timer > timer_time+0.10 and timer < timer_time+0.15:
                self.shoot()
            if timer > timer_time+0.20 and timer < timer_time+0.25:
                self.shoot()
            if timer > timer_time+1.5:
                self.timer_shoot = Timer()
        def shoot(self):
            bullet = Bullet(self, self.rect.centerx, self.rect.bottom+10)
            game.all_sprites.add(bullet)
            game.bullets_enemy.add(bullet)
    class Defender(Ship):
        def __init__(self, x, y):
            super().__init__(
                "img\Ship\Fighter jet.png",
                scale=None,
                rotate=None,

                speed_x=5,
                speed_y=0,

                shield=125,
                armor=60,
                life=60,

                x=x,
                y=y,
            )
            self.start_y = y
            self.start_pos = False
            self.timer_shoot = Timer()
        def update(self):
            if self.start_pos == False:
                self.rect.y += 2
            if self.rect.y >= self.start_y:
                self.start_pos = True

            if self.start_pos == True:
                self.shooter()
                self.flight()
        def shooter(self):
            timer = self.timer_shoot.update()
            if timer > 2 and timer < 2.01:
                self.shoot_roket()
                
            if timer > 4 and timer < 4.02:
                self.shoot_bullet()
            if timer > 4.10 and timer < 4.22:
                self.shoot_bullet()
            if timer > 4.20 and timer < 4.22:
                self.shoot_bullet()
            if timer > 5.30:
                self.timer_shoot =  Timer()

        def shoot_roket(self):
            bullet = Rocket(self, self.rect.centerx, self.rect.bottom-20)
            game.all_sprites.add(bullet)
            game.bullets_enemy.add(bullet)
        def shoot_bullet(self):
            bullet = Bullet(self, self.rect.centerx, self.rect.bottom+10)
            game.all_sprites.add(bullet)
            game.bullets_enemy.add(bullet)
    class Bomber(Ship):
        def __init__(self, x, y):
            super().__init__(
                "img\Ship\Bomber.png",
                scale=(120/1.80, 234/1.80),
                rotate=None,

                speed_x=5,
                speed_y=0,

                shield=50,
                armor=200,
                life=20,

                x=x,
                y=y,
            )
            self.start_y = y
            self.start_pos = False
            self.timer_shoot = Timer()
        def update(self):

            if self.start_pos == False:
                self.rect.y += 5
            if self.rect.y >= self.start_y:
                self.start_pos = True

            self.flight()
            timer = self.timer_shoot.update()
            if timer > 2.10 and timer < 2.01:
                self.shoot_roket()
            if timer > 2.40  and timer < 2.41:
                self.shoot_roket()
            if timer > 3.10 and timer < 3.11:
                self.shoot_roket()
            if timer > 4 and timer < 4.01:
                self.shoot_mine()
            if timer > 4.05:
                self.timer_shoot = Timer()

        def shoot_roket(self):
            bullet = Rocket(self, self.rect.centerx, self.rect.bottom+10)
            game.all_sprites.add(bullet)
            game.bullets_enemy.add(bullet)
        def shoot_mine(self):
            bullet = Mine(self, self.rect.centerx, self.rect.bottom+20)
            game.bullets_mine.add(bullet)
            game.all_sprites.add(bullet)
#-----------------------

game = Game()

player = Player(WIDTH/2, HEIGHT-50)
game_timer = time.time() # Время игры
spawn_timer = Timer() #Время Спавна
spawn_bonus_timer = Timer() #Время Спавна

def game_run():
    global spawn_timer, spawn_bonus_timer
    mobs = [Interceptor, Defender, Bomber] #Для быстрого вызова классов

    #> Установк игрового фона
    game.background = pygame.image.load('img\starfield.png').convert()
    game.background_rect = game.background.get_rect()
    #------------------------------------------------------

    #> Действия от Уровня Сложности
    if Complexity_index == 1: #Средний уровень
        player.shield -= 75
    if Complexity_index == 2: #Сложный уровень
        player.shield -= 200

    def create_bonus(bonus_index):
        global spawn_bonus_timer
        spawn_bonus_timer = Timer()
        if bonus_index == 0:
            Shield_Bonus(-10, random.randint(HEIGHT/2, HEIGHT-100))
        if bonus_index == 1:
            Health_Bonus(-10, random.randint(HEIGHT/2, HEIGHT-100))
        if bonus_index == 2:
            Rocket_Bonus(-10, random.randint(HEIGHT/2, HEIGHT-100))
    def next_lvl(): #Запуск следующего уровня
        global lvl, spawn_timer
        spawn_timer = Timer()
        levels(lvl)
        lvl += 1
    def levels(lvl): #Список врагов на уровне
        
        mobss = list()
        if lvl == 1:
            mobss = [
                mobs[0](100,10), 
                mobs[0](1200,10), 
                mobs[0](400,100), 
                mobs[0](800,100)
            ]
        elif lvl == 2:
            mobss = [
                mobs[1](600,40), 
                mobs[0](1200,10),
                mobs[0](100,10),
            ]
        elif lvl == 3:
            mobss = [
                mobs[0](600,50),
                mobs[0](800,50), 
                mobs[2](1200,10),
                mobs[2](100,10),
            ]
        elif lvl == 4:
            mobss = [
                mobs[0](600,70),
                mobs[0](670,50),
                mobs[0](750,70),
                mobs[2](450,30),
                mobs[2](850,30),
            ]
        elif lvl == 5:
            mobss = [
                mobs[0](0+200,10),
                mobs[0](WIDTH-200,10),
                mobs[1](WIDTH/2, 200),
                mobs[2](WIDTH/2-100,70),
                mobs[2](WIDTH/2+100,70),
            ]
        else:
            game.Win() # Если уровни кончились, то игрок выиграл

        for mob in mobss:
            game.all_sprites.add(mob)
            game.mobs.add(mob)
    def survival(): # Выгрузка 5-10 мобов на поле в случайные кординаты, если СЛОЖНОСТЬ: ВЫЖИВАНИЕ
        global spawn_timer
        spawn_timer = Timer()
        mobss = list()
        num = random.randint(5, 10)
        for i in range(num):
            x = random.randint(0, WIDTH)
            y = random.randint(10, 100)
            mobss.append(
                mobs[random.randint(0, 2)](x,y)
            )

        for mob in mobss:
            game.all_sprites.add(mob)
            game.mobs.add(mob)
    def screen_rendering(): #Отрисовка всех объектов и фона игры
        if game.pause == False:
            game.screen.fill((0,0,0))
            game.screen.blit(game.background, game.background_rect)

            game.all_sprites.update()
            game.all_sprites.draw(game.screen)
            pygame.display.update()
    def hit_detect(): # Обработчик попаданий
        #Противники с пулями игрока
        hits = pygame.sprite.groupcollide(game.mobs, game.bullets_player, False, True)
        for hit in hits:
            bullet = hits[hit][0]
            ship = hit

            if hit.shield >= 0:
                Shield_Enemy(bullet.rect.x, bullet.rect.y-25)
                ship.shield -= bullet.damage
            else:
                if ship.armor >= 0:
                    ship.armor -= bullet.damage
                    sounds[7].play()
                else:
                    Boom_Ship(bullet.rect.x, bullet.rect.y-25) #Взрыв при попадании
                    ship.life -= bullet.damage

                    if hit.life <= 0: #Эффект множества взрывов (корабль в клочья)
                        Boom_Ship(ship.rect.centerx, ship.rect.bottom)
                        Boom_Ship(ship.rect.centerx, ship.rect.centery)
                        Boom_Ship(ship.rect.centerx, ship.rect.top)
                        hit.kill()

        #Игрок с вражеским снарядом
        hits = hits = pygame.sprite.spritecollide(player, game.bullets_enemy, True)
        for hit in hits:
            if player.shield >= 0:
                Shield_Player(hit.rect.x, hit.rect.y)
                player.shield -= hit.damage
                if player.shield <= 0:
                    sounds[3].play() #Звук Отключения щитов
            else:
                if player.armor >= 0:
                    player.armor -= hit.damage
                    sounds[7].play()
                else:
                    player.life -= hit.damage
                    Boom_Ship(hit.rect.x, hit.rect.y)

        #Игрок с взрывом мины
        hits= pygame.sprite.spritecollide(player, game.booms, False)
        for hit in hits:
            if player.shield > 0:
                player.shield -= 5
                Shield_Player(hit.rect.x, hit.rect.y)

        #Мина со снарядом
        hits =  pygame.sprite.groupcollide(game.bullets_mine, game.bullets_player, False, True)
        for hit in hits:
            hit.kill()
            boom = Boom(hit.rect.x, hit.rect.y)
            game.all_sprites.add(boom)
            game.booms.add(boom)

        #Мина с игроком
        hits =  pygame.sprite.spritecollide(player, game.bullets_mine, True) 
        for hit in hits:
            hits[0].kill()
            boom = Boom(hit.rect.x, hit.rect.y)
            game.all_sprites.add(boom)
            game.booms.add(boom)
 
        #Бонус с игроком
        hits =  pygame.sprite.spritecollide(player, game.bonus, True)
        for hit in hits:
            hits[0].kill()
            hits[0].start_effect()

        if player.life <= 0:
            Boom_Ship(player.rect.centerx, player.rect.centery)
            player.kill()
            game.GameOver()
            game.pause = True

    #> Запуск фоновой музыки
    pygame.mixer.music.load("sounds\music_battle.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    #------------------------------------------------------

    game.all_sprites.add(player) # Добавляем игрока в игру.
    while game.running:
        timer_game = time.time() - game_timer #Время игры
        
        game.clock.tick(FPS) #Смена кадров
        event = game.init_events() #Инициализация ивентов
        # screen_rendering()
        #------------------------------

        hit_detect() # Обработчик Столкновений

        if game.pause == False and game.game_over == False:
            if timer_game > 2:
                if len(game.mobs.sprites()) == 0: #Проверяет, есть ли в игре враги
                    spawn_bonus_timer.update() #Отсчёт до появления бонусов
                    spawn_timer.update() #Отсчёт до появления врагов
                    if spawn_bonus_timer.time > 3.5:
                        if len(game.bonus.sprites()) < 2:
                            num = range(random.randint(1, 2))
                            for i in num:
                                create_bonus(random.randint(0, 2))
                    
                    if spawn_timer.time > 5:
                        if Complexity_index == 3: #Если СЛОЖНОСТЬ: ВЫЖИВАНИЕ
                            survival()
                        else:
                            next_lvl()

        #------------------------------
        screen_rendering()

def window_run():
    class Button(pygame.sprite.Sprite):
        def __init__(self, text, size, color, x, y):
            pygame.sprite.Sprite.__init__(self)

            self.text = text
            self.color = color
            self.font = pygame.font.SysFont("Arial", size)

            self.textSurf = self.font.render(self.text, 1, self.color)
            self.width = self.textSurf.get_width()
            self.height = self.textSurf.get_height()-20

            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((50,160,200))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
        def update(self):
            self.textSurf = self.font.render(self.text, 1, self.color)
            self.image.blit(self.textSurf, (0, self.height-self.height-10))
    
    class Hint(pygame.sprite.Sprite):
        def __init__(self, text, size, color, x, y):
            pygame.sprite.Sprite.__init__(self)

            self.text = text
            self.words = self.text.split(" ")
            
            self.color = color
            self.font = pygame.font.SysFont("Arial", size)

            for i in range(len(self.words)):
                self.words[i] = self.font.render(self.words[i], 1, self.color)

            self.textSurf = self.font.render(self.text, 1, self.color)
            self.width = self.textSurf.get_width()+20
            self.height = self.textSurf.get_height()

            self.image = pygame.Surface((self.width, self.height))
            
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

            if self.rect.right > WIDTH:
                self.height = self.height+self.height+10
                self.image = pygame.Surface((self.width, self.height))

            self.i = 10
            self.i2 = 0
            self.image.fill((50,160,200))
            for word in range(len(self.words)):
                if word != 0:
                    self.i += self.words[word-1].get_width()+10
                
                if self.rect.x+self.i > WIDTH-200:
                    self.i = 0+10
                    self.i2 = 40
                    
                self.image.blit(self.words[word], (self.i, self.height-self.height-10+self.i2))
            
            
    global hints, Complexity_index
    buttons = list()
    buttons.append(Button("СТАРТ", 72, (255,0,0), 50, 100))
    buttons.append(Button("СЛОЖНОСТЬ:", 72, (255,0,0), 50, 200))
    buttons.append(Button("ВЫХОД", 72, (255,0,0), 50, 400))
    buttons.append(Hint(Complexity[Complexity_index], 72, (255,0,0), 500, 200))
    buttons.append(Hint(hints[Complexity_index], 48, (255,0,0), 500, 400))

    

    mouse = Mouse()

    for i in buttons:
        game.buttons.add(i)
    
    game.buttons.draw(game.screen)
    def menu_events_init():
        global hints, Complexity_index
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Окно закрывается
                game.running = False
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hits:
                    if hits[0].text == 'СТАРТ':
                        game.menu = False
                        game_run()
                        break
                    if hits[0].text == 'СЛОЖНОСТЬ:':
                        buttons = game.buttons.sprites()
                        buttons[4].kill()
                        buttons[-1].kill()

                        Complexity_index +=1
                        if Complexity_index >= 4:
                            Complexity_index=0
                        comp = Hint(Complexity[Complexity_index], 72, (255,0,0), 500, 200)
                        game.buttons.add(comp)
                        comp = Hint(hints[Complexity_index], 48, (255,0,0), 500, 400)
                        
                        game.buttons.add(comp)
                    if hits[0].text == 'ВЫХОД':
                        game.running = False
                        pygame.display.quit()
    def screen_rendering():
        game.screen.fill((50,160,200))
        game.buttons.update()
        game.buttons.draw(game.screen)
        pygame.display.update()
        

    while game.running:
        menu_events_init()
        game.clock.tick(FPS)
        #-----------------------------
        
        mouse.update()

        hits = pygame.sprite.spritecollide(mouse, game.buttons, False)
        if hits:
            if not(hits[0].text in Complexity):
                hits[0].color=(255,255,0)
        else:
            buttons = game.buttons.sprites()
            for button in buttons:
                buttons[buttons.index(button)].kill()
                game.buttons.add(buttons[buttons.index(button)])
                buttons[buttons.index(button)].color=(255,0,0)

        #-----------------------------
        screen_rendering()
    
#>--------------------------------------------------------------------

window_run()

print("Игра завершена")
