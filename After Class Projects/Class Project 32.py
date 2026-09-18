import math
import sys

import pygame

WIDTH = 960
HEIGHT = 540
FPS = 60

BLACK = (10, 10, 14)
WHITE = (245, 245, 245)


def clamp(value, low, high):
    return max(low, min(value, high))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.speed = 240
        self.wall_touch_timer = 0
        self.hat_offset = 0
        self.color_index = 0
        self.colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]
        self.wall_colors = {
            "left": 0,
            "right": 1,
            "top": 2,
            "bottom": 3,
        }

    def update(self, dt, keys):
        move_x = 0
        move_y = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += 1

        if move_x != 0 or move_y != 0:
            length = math.hypot(move_x, move_y)
            move_x /= length
            move_y /= length

            self.x += move_x * self.speed * dt
            self.y += move_y * self.speed * dt

        prev_x = self.x
        prev_y = self.y
        next_x = clamp(self.x, self.size // 2, WIDTH - self.size // 2)
        next_y = clamp(self.y, self.size // 2, HEIGHT - self.size // 2)
        self.x = next_x
        self.y = next_y

        if self.x != prev_x or self.y != prev_y:
            self.hat_offset = 0

        left_hit = prev_x < self.size // 2 and next_x == self.size // 2
        right_hit = prev_x > WIDTH - self.size // 2 and next_x == WIDTH - self.size // 2
        top_hit = prev_y < self.size // 2 and next_y == self.size // 2
        bottom_hit = prev_y > HEIGHT - self.size // 2 and next_y == HEIGHT - self.size // 2

        if left_hit or right_hit or top_hit or bottom_hit:
            self.wall_touch_timer = 0.25
            if left_hit:
                self.color_index = self.wall_colors["left"]
            elif right_hit:
                self.color_index = self.wall_colors["right"]
            elif top_hit:
                self.color_index = self.wall_colors["top"]
            elif bottom_hit:
                self.color_index = self.wall_colors["bottom"]

        self.wall_touch_timer = max(0, self.wall_touch_timer - dt)
        self.hat_offset += dt * 7

    def draw(self, screen):
        hat_color = (200, 200, 200)
        square_color = self.colors[self.color_index]

        hat_x = int(self.x)
        hat_y = int(self.y - self.size / 2 - 12 + math.sin(self.hat_offset) * 3)
        pygame.draw.rect(screen, hat_color, (hat_x - 16, hat_y - 4, 32, 10))
        pygame.draw.rect(screen, hat_color, (hat_x - 11, hat_y - 14, 22, 10))

        pygame.draw.rect(screen, square_color, (int(self.x - self.size // 2), int(self.y - self.size // 2), self.size, self.size))

        if self.wall_touch_timer > 0:
            pulse = 1 + (0.25 - self.wall_touch_timer) * 8
            pygame.draw.rect(screen, (220, 220, 220), (int(self.x - self.size // 2 - 6), int(self.y - self.size // 2 - 6), self.size + 12, self.size + 12), 2)
            pygame.draw.rect(screen, square_color, (int(self.x - self.size // 2 - 2), int(self.y - self.size // 2 - 2), self.size + 4, self.size + 4), 1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("White Square")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.running = True
        self.reset()

    def reset(self):
        self.player = Player(WIDTH / 2, HEIGHT / 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)

    def draw(self):
        self.screen.fill(BLACK)

        for x in range(0, WIDTH, 60):
            pygame.draw.line(self.screen, (25, 25, 30), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 60):
            pygame.draw.line(self.screen, (25, 25, 30), (0, y), (WIDTH, y), 1)

        self.player.draw(self.screen)

        hint = self.font.render("Move with WASD or arrows", True, WHITE)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 42))

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as exc:
        print(f"Game crashed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as exc:
        print(f"Game crashed: {exc}")
        sys.exit(1)
