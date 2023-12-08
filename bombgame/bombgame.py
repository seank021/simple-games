import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Grid:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y

    def handle_event(self, event):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other, event):
        pass


class Player(Grid):
    def __init__(self, x, y, game, move_keys, color):
        super().__init__(x, y, game, color)
        self.color = color
        self.move_keys = move_keys
        self.bombs_near = 0
        self.move = 0
        self.life = 3

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.x -= 1
                self.move += 1
            elif event.key == pygame.K_RIGHT:
                self.x += 1
                self.move += 1
            elif event.key == pygame.K_UP:
                self.y -= 1
                self.move += 1
            elif event.key == pygame.K_DOWN:
                self.y += 1
                self.move += 1
            elif event.key == pygame.K_SPACE:
                self.life -= 1

    def interact(self, other, event):
        if isinstance(other, Bomb):
            dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

            for direction in dirs:
                if self.x == other.x + direction[0] and self.y == other.y + direction[1]:
                    self.bombs_near += 1

            if self.x == other.x and self.y == other.y:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        other.active = False
                        other.change_color(BLUE)
                        self.life += 1

    def go_out(self):
        if not (4 < self.x < self.game.n_cols+5 and 4 < self.y < self.game.n_rows+5):
            self.game.gameover()


class Bomb(Grid):
    def __init__(self, game):
        self.color = BLACK
        x = random.randint(5, game.n_cols + 4)
        y = random.randint(5, game.n_rows + 4)
        while (x,y) in game.bomb_coords():
            x = random.randint(5, game.n_cols + 4)
            y = random.randint(5, game.n_rows + 4)

        super().__init__(x, y, game, self.color)

    def change_color(self, color):
        self.color = color


class Game:
    block_size = 20

    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('Game')
        self.display = pygame.display.set_mode((n_cols * self.block_size + 200, n_rows * self.block_size + 200))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.game_over = False
        self.bomb_list = []
        self.player = None
        self.timelimit = 160

    def active_bombs(self):
        for obj in self.bomb_list:
            if obj.active:
                yield obj

    def bomb_coords(self):
        coord_list = []
        for bomb in self.bomb_list:
            coord_list.append((bomb.x, bomb.y))
        return coord_list

    def num_active_bombs(self):
        count = 0
        for obj in self.active_bombs():
            count += 1
        return count

    def gameover(self):
        self.game_over = True

    def play(self, n_bombs):
        self.player = Player(15, 15, self, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), WHITE)
        self.bomb_list = []
        for i in range(n_bombs):
            self.bomb_list.append(Bomb(self))
        initial_time = pygame.time.get_ticks()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.gameover(self)
                    break

                self.player.handle_event(event)

                self.player.bombs_near = 0
                for bomb in self.active_bombs():
                    self.player.interact(bomb, event)

                self.player.go_out()

            time = (self.timelimit*1000-(pygame.time.get_ticks()-initial_time))//1000 + 1
            if time <= 0:
                self.gameover()

            self.display.fill(BLACK)

            for bomb in self.bomb_list:
                bomb.draw()
            self.player.draw()

            for i in range(0, self.n_rows + 1):
                pygame.draw.line(self.display, WHITE, (100, 100 + self.block_size * i), (self.n_cols * self.block_size + 100, 100 + self.block_size * i))
            for i in range(0, self.n_cols + 1):
                pygame.draw.line(self.display, WHITE, (100 + self.block_size * i, 100), (100 + self.block_size * i, self.n_rows * self.block_size + 100))

            sf = pygame.font.SysFont('Monospace', 18)
            txt1 = sf.render('Bombs near me: ' + str(self.player.bombs_near), True, WHITE)
            self.display.blit(txt1, (100, 15))

            txt2 = sf.render('Remaining bombs: ' + str(self.num_active_bombs()), True, WHITE)
            self.display.blit(txt2, (100, 40))

            txt3 = sf.render('Life: ' + str(self.player.life), True, WHITE)
            self.display.blit(txt3, (100, 65))

            txt4 = sf.render('Move: '+ str(self.player.move), True, WHITE)
            self.display.blit(txt4, (400, 15))

            txt5 = sf.render('Time: ' + str(time), True, WHITE)
            self.display.blit(txt5, (400, 40))

            pygame.display.update()

            if self.num_active_bombs() == 0 or self.player.life == 0:
                self.gameover()

            if self.game_over:
                sf = pygame.font.SysFont('Monospace', 50, bold=True)
                words = [None, 'Good!', 'Great!', 'Excellent!']
                if self.num_active_bombs() == 0:
                    result1_1 = sf.render(words[self.player.life], True, GREEN)
                    result1_2 = sf.render("You succeeded!", True, GREEN)
                    result1_3 = sf.render("(%d times moved)" % self.player.move, True, GREEN)
                    self.display.blit(result1_1, (50, 150))
                    self.display.blit(result1_2, (50, 220))
                    self.display.blit(result1_3, (50, 290))
                    pygame.display.update()
                    pygame.time.wait(3000)
                elif time == 0:
                    result2_1 = sf.render("Time Over…", True, RED)
                    result2_2 = sf.render("Try again!", True, RED)
                    self.display.blit(result2_1, (50, 220))
                    self.display.blit(result2_2, (50, 270))
                    pygame.display.update()
                    pygame.time.wait(2000)
                else:
                    result3_1 = sf.render("You failed…", True, RED)
                    result3_2 = sf.render("Try again!", True, RED)
                    self.display.blit(result3_1, (50, 200))
                    self.display.blit(result3_2, (50, 270))
                    pygame.display.update()
                    pygame.time.wait(2000)


if __name__ == "__main__":
    Game(n_rows=20, n_cols=20).play(n_bombs=25)