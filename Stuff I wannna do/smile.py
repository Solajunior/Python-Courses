import math
import random
import sys

try:
    import pygame
except ImportError:
    print("This game needs Pygame. Install it with: pip install pygame")
    sys.exit(1)

WIDTH = 960
HEIGHT = 540
FPS = 60

BLACK = (10, 10, 14)
WHITE = (245, 245, 245)
RED = (255, 60, 60)
ORANGE = (255, 140, 60)
YELLOW = (255, 220, 110)
PURPLE = (120, 90, 220)
BLUE = (80, 180, 255)
GREEN = (90, 220, 120)
DARK = (25, 25, 34)


def clamp(value, low, high):
    return max(low, min(value, high))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 16
        self.speed = 240
        self.invuln = 0

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

        self.x = clamp(self.x, self.radius, WIDTH - self.radius)
        self.y = clamp(self.y, self.radius, HEIGHT - self.radius)

        if self.invuln > 0:
            self.invuln -= dt

    def draw(self, screen):
        color = (255, 255, 255)
        if self.invuln > 0:
            color = (255, 220, 120)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x - 5), int(self.y - 3)), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y - 3)), 3)
        pygame.draw.arc(screen, BLACK, (int(self.x - 7), int(self.y - 2), 14, 10), 0.2, math.pi - 0.2, 2)


class Smile:
    def __init__(self, player):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.radius = 28
        self.speed = 80
        self.phase = random.random() * math.tau
        self.spread = random.randint(20, 70)
        self.player = player

    def update(self, dt, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt

        self.x += math.sin(self.phase) * self.spread * dt * 0.4
        self.y += math.cos(self.phase * 1.7) * self.spread * dt * 0.4
        self.phase += dt * 2.2

        self.x = clamp(self.x, self.radius, WIDTH - self.radius)
        self.y = clamp(self.y, self.radius, HEIGHT - self.radius)

    def draw(self, screen):
        head_x = int(self.x)
        head_y = int(self.y)
        pygame.draw.circle(screen, WHITE, (head_x, head_y), self.radius)
        pygame.draw.circle(screen, BLACK, (head_x - 9, head_y - 8), 4)
        pygame.draw.circle(screen, BLACK, (head_x + 9, head_y - 8), 4)
        pygame.draw.arc(screen, BLACK, (head_x - 16, head_y - 2, 32, 22), math.pi * 0.15, math.pi * 0.85, 4)

        # evil glow around the smile
        for i in range(4):
            pygame.draw.circle(screen, (255, 90, 90), (head_x, head_y), self.radius + i * 2, 1)


class Pickup:
    def __init__(self):
        self.x = random.randint(40, WIDTH - 40)
        self.y = random.randint(40, HEIGHT - 40)
        self.radius = 10
        self.pulse = random.random() * math.tau

    def update(self, dt):
        self.pulse += dt * 4

    def draw(self, screen):
        radius = self.radius + int(math.sin(self.pulse) * 3)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), radius)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), radius - 4, 2)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Smile")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.big_font = pygame.font.SysFont(None, 56)
        self.running = True
        self.reset()

    def reset(self):
        self.player = Player(WIDTH / 2, HEIGHT / 2)
        self.smile = Smile(self.player)
        self.pickups = [Pickup() for _ in range(7)]
        self.score = 0
        self.game_over = False
        self.win = False
        self.timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (self.game_over or self.win):
                    self.reset()
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if not self.game_over and not self.win:
            self.player.update(dt, keys)
            self.smile.update(dt, self.player)
            self.timer += dt

            for pickup in self.pickups[:]:
                pickup.update(dt)
                if math.hypot(self.player.x - pickup.x, self.player.y - pickup.y) <= self.player.radius + pickup.radius + 2:
                    self.pickups.remove(pickup)
                    self.score += 1
                    self.smile.speed += 20
                    if self.score >= 7:
                        self.win = True

            if math.hypot(self.player.x - self.smile.x, self.player.y - self.smile.y) <= self.player.radius + self.smile.radius:
                self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)

        # ambient glow
        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow, (30, 30, 50, 180), (int(self.player.x), int(self.player.y)), 180)
        self.screen.blit(glow, (0, 0))

        # floor grid
        for x in range(0, WIDTH, 60):
            pygame.draw.line(self.screen, (25, 25, 30), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 60):
            pygame.draw.line(self.screen, (25, 25, 30), (0, y), (WIDTH, y), 1)

        for pickup in self.pickups:
            pickup.draw(self.screen)

        self.smile.draw(self.screen)
        self.player.draw(self.screen)

        hud = self.font.render(f"Collectibles: {self.score}/7", True, WHITE)
        self.screen.blit(hud, (18, 18))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))
            title = self.big_font.render("YOU WERE CAUGHT", True, RED)
            sub = self.font.render("Press R to restart or ESC to quit", True, WHITE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
            self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))

        if self.win:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((20, 20, 30, 150))
            self.screen.blit(overlay, (0, 0))
            title = self.big_font.render("YOU ESCAPED", True, GREEN)
            sub = self.font.render("Press R to play again", True, WHITE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
            self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))

        if not self.game_over and not self.win:
            hint = self.font.render("Collect 7 glowing lights. Keep moving.", True, (200, 200, 220))
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
    game = Game()
    game.run()
