import pygame
import random
import math

WIDTH = 640
HEIGHT = 480

class Player:
    def __init__(self):
        self.image = pygame.image.load("./assets/spaceship.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.angle = 0

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        screen.blit(rotated_image, (self.x, self.y))

    def move(self, x, y):
        self.x += x
        self.y += y
        if self.x > WIDTH - 64:
            self.x = WIDTH - 64
        if self.x < 0:
            self.x = 0
        if self.y > HEIGHT - 64:
            self.y = HEIGHT - 64
        if self.y < 0:
            self.y = 0
    
    def is_collide(self, enemy):
        if (enemy.x < self.x < enemy.x + 32 and enemy.y < self.y < enemy.y + 32) or (enemy.x < self.x + 32 < enemy.x + 32 and enemy.y < self.y + 32 < enemy.y + 32):
            return True
        return False

    def rotate(self, angle):
        self.angle += angle

class Enemy:
    def __init__(self):
        self.image = pygame.image.load("./assets/monster.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.x = WIDTH / 2
        self.y = HEIGHT
        self.last_update = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000:
            self.x += random.randint(-100, 100)
            self.y += random.randint(-100, 100)
            if self.x == player.x and self.y == player.y:
                self.x += random.randint(-100, 100)
                self.y += random.randint(-100, 100)

            if self.x > WIDTH - 64:
                self.x = WIDTH - 64
            if self.x < 0:
                self.x = 0
            if self.y > HEIGHT - 64:
                self.y = HEIGHT - 64
            if self.y < 0:
                self.y = 0
            self.last_update = now

    def is_collide(self, bullet):
        if self.x < bullet.x + 10 and self.x + 64 > bullet.x and self.y < bullet.y + 10 and self.y + 64 > bullet.y:
            return True
        return False

class Bullet:
    def __init__(self):
        self.image = pygame.image.load("./assets/bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.x = 0
        self.y = 0
        self.angle = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, angle):
        radians = math.radians(angle)  # Convert angle to radians
        speed = 10
        if angle % 180 == 0:
            self.x += speed * math.sin(radians)
            self.y -= speed * math.cos(radians)
        else:
            self.x -= speed * math.sin(radians)
            self.y += speed * math.cos(radians)
        
    def is_collide(self, enemy):
        if self.x < enemy.x + 64 and self.x + 10 > enemy.x and self.y < enemy.y + 64 and self.y + 10 > enemy.y:
            return True
        return False
    
class Font:
    def __init__(self):
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen, text, x, y):
        text = self.font.render(text, True, (255, 255, 255))
        screen.blit(text, (x, y))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player()
        self.enemy = Enemy()
        self.bullet = Bullet()
        self.font = Font()
        self.score = 0
        self.is_gameover = False

    def draw(self):
        self.screen.blit(pygame.image.load("./assets/space.jpg"), (0, 0))
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        self.bullet.draw(self.screen)
        self.font.draw(self.screen, "Score: " + str(self.score), 10, 10)
        pygame.display.update()

    def update(self):
        self.enemy.move(self.player)
        self.bullet.move(self.bullet.angle)
        if self.player.is_collide(self.enemy):
            self.is_gameover = True
        if self.bullet.is_collide(self.enemy):
            self.score += 1
            self.enemy.x = random.randint(0, 640)
            self.enemy.y = random.randint(0, 480)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:  # up
                self.player.move(0, -10)
            if keys[pygame.K_DOWN]:  # down
                self.player.move(0, 10)
            if keys[pygame.K_LEFT]:  # left
                self.player.move(-10, 0)
            if keys[pygame.K_RIGHT]:  # right
                self.player.move(10, 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullet.x = self.player.x + 32
                        self.bullet.y = self.player.y + 32
                        self.bullet.angle = self.player.angle
                    if event.key == pygame.K_a:  # rotate left 90
                        self.player.rotate(90)
                        self.bullet.angle += 90           
                    if event.key == pygame.K_d: # rotate right 90
                        self.player.rotate(-90)
                        self.bullet.angle -= 90
                    
            if self.is_gameover:
                self.font.draw(self.screen, "Game Over", 320, 240)
                pygame.display.update()
                continue
        
            if self.score == 10:
                self.font.draw(self.screen, "You Win", 320, 240)
                pygame.display.update()
                continue

            self.draw()
            self.update()
            clock.tick(30)  # Limit the frame rate to 30 FPS

if __name__ == "__main__":
    game = Game()
    game.run()
