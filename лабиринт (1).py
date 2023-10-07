import pygame
from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)



        self.x_speed = player_x_speed
        self.y_speed = player_y_speed



    def update(self):
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top,p.rect.bottom)

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 30, 30, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    side = "left"

    def __init__(self, player_image: object, player_x: object, player_y: object, size_x: object, size_y: object, player_speed: object) -> object:
        GameSprite.__init__(self,player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed



class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()



win_width = 700
win_height = 500

display.set_caption('Лабиринт')
windows = display.set_mode((win_width,win_height))

background_image = image.load('fill.jpg')

clock = pygame.time.Clock()


barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

wall1 = GameSprite('wall.png', win_width/2 - win_width, win_height/2, 350, 50)
wall2 = GameSprite('wall.png',380,150,50,350)

packman = Player('packman.png', 100, 100, 100, 100, 0, 0)

enemy = Enemy('enemy.png', 450, 200, 80, 80, 2)

win_sprite = GameSprite('wolf.png',590,400,70,70)

monsters.add(enemy)

barriers.add(wall1)
barriers.add(wall2)

lose_image = image.load('lose.jpg')
win_image = image.load('win.jpg')

run = True

while run:

    windows.blit(background_image, (0, -300))

    packman.update()
    packman.reset()

    wall1.reset()
    wall2.reset()

    bullets.update()
    bullets.draw(windows)

    monsters.update()
    monsters.draw(windows)

    win_sprite.update()
    win_sprite.reset()


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    hits = sprite.spritecollide(packman, monsters, False)
    for enemy in hits:
        windows.blit(lose_image, (0, 0))
        pygame.display.update()
        time.delay(5000)
        run = False

    if sprite.collide_rect(packman, win_sprite):
        windows.blit(win_image, (-250, 0))
        pygame.display.update()
        time.delay(5000)
        run = False

    hits = sprite.groupcollide(monsters, bullets, True, True)
    for enemy, bullet_list in hits.items():
        enemy.kill()


    pygame.display.update()
    clock.tick(40)