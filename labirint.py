from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def shoot(self):
        bullet = Bullet('bullet.png', 15, 15, self.rect.right, self.rect.centery, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 0:
            self.side = "right"
        if self.rect.x >= 600:
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
        if self.rect.x > 710:
            self.kill()

picture = transform.scale(image.load('index.jpg'), (700,500))
wall1 = GameSprite('brick.png', 1, 500, -1, 0)
wall2 = GameSprite('brick.png', 1, 500, 701, 0)
wall3 = GameSprite('brick.png', 700, 1, 0, -1)
wall4 = GameSprite('brick.png', 700, 1, 0, 501)
wall5 = GameSprite('brick.png', 80, 80, 1000, 1000)
wall6 = GameSprite('brick.png', 80, 300, 100, 100)
wall7 = GameSprite('brick.png', 80, 300, 500, 100)
wall8 = GameSprite('brick.png', 200, 80, 180, 100)
wall9 = GameSprite('brick.png', 200, 80, 300, 320)
player = Player('background.png', 50, 50, 0, 0, 0, 0)
enemy1 = Enemy('Troll.png', 100, 100, 600, 0, 1)
enemy2 = Enemy('Troll.png', 100, 100, 1320, 100, 1)
enemy3 = Enemy('Troll.png', 100, 100, 2040, 200, 1)
enemy4 = Enemy('Troll.png', 100, 100, 2760, 300, 1)
enemy5 = Enemy('Troll.png', 100, 100, 3480, 400, 1)
goal = GameSprite('goal.png', 90, 90, 615, 400)

walls = sprite.Group()
walls.add(wall1)
walls.add(wall2)
walls.add(wall3)
walls.add(wall4)
walls.add(wall5)
walls.add(wall6)
walls.add(wall7)
walls.add(wall8)
walls.add(wall9)

enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)

bullets = sprite.Group()

window = display.set_mode((700,500))
display.set_caption('Моя перавя игра')

run = True
wall5_random = 0

while run:
    time.delay(10)
    window.blit(picture,(0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed -= 2
            elif e.key == K_RIGHT:
                player.x_speed += 2
            elif e.key == K_UP:
                player.y_speed -= 2
            elif e.key == K_DOWN:
                player.y_speed += 2
            elif e.key == K_SPACE:
                player.shoot()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed += 2
            elif e.key == K_RIGHT:
                player.x_speed -= 2
            elif e.key == K_UP:
                player.y_speed += 2
            elif e.key == K_DOWN:
                player.y_speed -= 2
    
    player.update()

    if sprite.spritecollide(player, enemies, False):
        player.rect.x = 0
        player.rect.y = 0
    if sprite.spritecollide(player, walls, False):
        player.rect.x = player_rect_x
        player.rect.y = player_rect_y

    if sprite.collide_rect(player, goal):
        goal.rect.x = randint(0, 620)
        goal.rect.y = randint(0, 420)
        
    if sprite.groupcollide(bullets, enemies, True, True):
        enemy3 = Enemy('Troll.png', 100, 100, 600, randint(000,400), 1)
        enemies.add(enemy3)

    wall5_random += 1
    if wall5_random > 500:
        wall5.rect.x = randint(0,620)
        wall5.rect.y = randint(0,420)
        wall5_random = 0
           
    player.reset()
    goal.reset()
    player_rect_x = player.rect.x
    player_rect_y = player.rect.y
    

    walls.update()
    enemies.update()
    bullets.update()
    walls.draw(window)
    enemies.draw(window)
    bullets.draw(window)

    display.update()