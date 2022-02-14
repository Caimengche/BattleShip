import pygame
import random
import os

#變數命名
WIDTH, HEIGHT = 500, 600
WHITE = (255,255,255)
FPS = 60
GREEN = (0,255,0)
RED = (255, 0 ,0)
YELLOW = (255, 255, 0)
BLACK = (0 , 0 , 0)
speed_ship = 3
score = 0
font_name = pygame.font.match_font("arial")


#遊戲初始化; 視窗設定
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Battle ship")

#載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
bullets_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
#rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

#載入音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
explode_sound =[
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
    ]
background_sound = pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.play(-1, 0 , 0)
pygame.mixer.music.set_volume(0.05)

#時間,畫面更新率
Clock = pygame.time.Clock()
#遊戲迴圈

#分數
def draw_score(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    font_surface = font.render(text, True, WHITE)
    font_rect = font_surface.get_rect()
    font_rect.centerx = x
    font_rect.top = y
    surf.blit(font_surface, font_rect)

#Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,33))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += speed_ship
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= speed_ship
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx ,self.rect.y)
        all_sprite.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rock_imgs)
        self.image_ori = self.image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 - 3)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -40)
        self.speed = random.randrange(2, 10)
        self.speedx = random.randrange(-3,3)
        self.rotation = random.randrange(-3,3)
        self.rotation_degree = 0
    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speedx
        if self.rect.y > HEIGHT or self.rect.x > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-500, -40)
            self.speed = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
        self.rotation_degree += self.rotation
        self.rotation_degree = self.rotation_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.rotation_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullets_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill() #從所有sprite群組中移除bullet


player = Player()
all_sprite = pygame.sprite.Group()
players = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprite.add(player)
players.add(player)


for i in range(8):
    rock = Rock()
    all_sprite.add(rock)
    rocks.add(rock)

running = True
while running:
    Clock.tick(FPS) #一秒鐘最多執行幾次 EX: 一秒中最多執行30次
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                shoot_sound.play()

    #更新遊戲

    all_sprite.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        exp_sound = random.choice(explode_sound)
        exp_sound.play()
        score += hit.radius
        r = Rock()
        all_sprite.add(r)
        rocks.add(r)
    hits = pygame.sprite.groupcollide(players, rocks, False, False, pygame.sprite.collide_circle)
    if hits :
        running = False
    #畫面顯示

    screen.fill(WHITE)
    screen.blit(background_img,(0 ,0))
    all_sprite.draw(screen)
    draw_score(screen, str(score), 18, WIDTH/2, 10 )
    pygame.display.update()

