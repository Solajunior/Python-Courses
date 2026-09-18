import math
import pygame

WIDTH, HEIGHT = 1280, 720
FPS = 60
GRAVITY = 1900
MOVE_SPEED = 360
JUMP_SPEED = 770

WHITE = (250, 250, 255)
BLACK = (18, 18, 24)
DARK = (35, 38, 52)
BLUE = (90, 170, 255)
YELLOW = (255, 220, 90)
PINK = (255, 120, 180)
RED = (255, 80, 80)
MINT = (120, 220, 180)
GREEN = (120, 220, 130)
ORANGE = (255, 160, 70)
CYAN = (90, 255, 220)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 46)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.coyote = 0.0
        self.jump_buffer = 0.0
        self.dead = False

    def update(self, dt, keys, platforms):
        direction = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction += 1

        self.vel.x = direction * MOVE_SPEED

        if self.jump_buffer > 0:
            self.jump_buffer -= dt
        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump_buffer = 0.18

        if self.jump_buffer > 0 and (self.on_ground or self.coyote > 0):
            self.vel.y = -JUMP_SPEED
            self.on_ground = False
            self.coyote = 0
            self.jump_buffer = -1

        self.vel.y += GRAVITY * dt
        self.move(platforms, dt)

    def move(self, platforms, dt):
        self.rect.x += self.vel.x * dt
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel.x > 0:
                    self.rect.right = p.left
                elif self.vel.x < 0:
                    self.rect.left = p.right
                self.vel.x = 0

        self.rect.y += self.vel.y * dt
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel.y >= 0:
                    self.rect.bottom = p.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = p.bottom
                    self.vel.y = 0

        if self.on_ground:
            self.coyote = 0.12
        else:
            self.coyote = max(0, self.coyote - dt)

        if self.rect.top > HEIGHT + 200:
            self.dead = True

    def draw(self, screen, camera_x):
        x = int(self.rect.x - camera_x)
        y = int(self.rect.y)
        pygame.draw.rect(screen, WHITE, (x, y, self.rect.width, self.rect.height))
        pygame.draw.circle(screen, BLACK, (x + 7, y + 15), 3)
        pygame.draw.circle(screen, BLACK, (x + 20, y + 15), 3)
        pygame.draw.arc(screen, BLACK, (x + 7, y + 20, 14, 12), 0.25, 3.0, 2)


class MovingPlatform:
    def __init__(self, x, y, w, h, axis, start, end, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.axis = axis
        self.start = start
        self.end = end
        self.speed = speed
        self.direction = 1

    def update(self, dt):
        if self.axis == 'x':
            self.rect.x += self.speed * self.direction * dt
            if self.rect.x <= self.start:
                self.rect.x = self.start
                self.direction = 1
            elif self.rect.x >= self.end:
                self.rect.x = self.end
                self.direction = -1
        else:
            self.rect.y += self.speed * self.direction * dt
            if self.rect.y <= self.start:
                self.rect.y = self.start
                self.direction = 1
            elif self.rect.y >= self.end:
                self.rect.y = self.end
                self.direction = -1


class Enemy:
    def __init__(self, x, y, radius, speed, axis, start, end):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.axis = axis
        self.start = start
        self.end = end
        self.direction = 1
        self.phase = 0

    def update(self, dt):
        self.phase += dt * 5
        if self.axis == 'x':
            self.x += self.speed * self.direction * dt
            if self.x <= self.start:
                self.x = self.start
                self.direction = 1
            elif self.x >= self.end:
                self.x = self.end
                self.direction = -1
        else:
            self.y += self.speed * self.direction * dt
            if self.y <= self.start:
                self.y = self.start
                self.direction = 1
            elif self.y >= self.end:
                self.y = self.end
                self.direction = -1

    def draw(self, screen, camera_x):
        cx = int(self.x - camera_x)
        cy = int(self.y)
        pygame.draw.circle(screen, WHITE, (cx, cy), self.radius)
        pygame.draw.circle(screen, BLACK, (cx - 8, cy - 7), 5)
        pygame.draw.circle(screen, BLACK, (cx + 8, cy - 7), 5)
        pygame.draw.arc(screen, BLACK, (cx - 16, cy - 2, 32, 22), 0.25, 3.0, 4)


class SpikeTrap:
    def __init__(self, x, y, w, h, invisible=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.invisible = invisible
        self.active = False
        self.flash = 0.0

    def update(self, player, dt):
        if self.invisible:
            near_x = abs(player.rect.centerx - self.rect.centerx) < 130
            near_y = abs(player.rect.centery - self.rect.centery) < 120
            self.active = near_x and near_y
        else:
            self.active = True

        if self.active:
            self.flash = min(1.0, self.flash + dt * 6)
        else:
            self.flash = max(0.0, self.flash - dt * 5)

    def hurts(self, player):
        return self.active and self.rect.colliderect(player.rect)

    def draw(self, screen, camera_x):
        if not self.invisible or self.flash > 0.0:
            rect = self.rect.move(-camera_x, 0)
            if self.invisible:
                color = (255, 90, 100)
                alpha = max(35, int(90 * self.flash))
                surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                surf.fill((255, 90, 100, alpha))
                screen.blit(surf, rect)
            else:
                tri_points = [
                    (rect.left, rect.bottom),
                    (rect.centerx, rect.top),
                    (rect.right, rect.bottom)
                ]
                pygame.draw.polygon(screen, RED, tri_points)
                pygame.draw.line(screen, (120, 20, 20), (rect.left, rect.bottom), (rect.centerx, rect.top), 2)
                pygame.draw.line(screen, (120, 20, 20), (rect.centerx, rect.top), (rect.right, rect.bottom), 2)


class Tripmine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.triggered = False
        self.timer = 0.0
        self.exploded = False

    def update(self, player, dt):
        if self.exploded:
            return
        if not self.triggered:
            dist = math.hypot(player.rect.centerx - self.x, player.rect.centery - self.y)
            if dist < 90:
                self.triggered = True
                self.timer = 0.18
        else:
            self.timer -= dt
            if self.timer <= 0:
                self.exploded = True

    def hurts(self, player):
        if not self.triggered or self.exploded:
            return False
        dist = math.hypot(player.rect.centerx - self.x, player.rect.centery - self.y)
        return dist < self.radius + 24

    def draw(self, screen, camera_x):
        cx = int(self.x - camera_x)
        cy = int(self.y)
        if self.exploded:
            pygame.draw.circle(screen, (255, 180, 80), (cx, cy), 26, 2)
            return

        color = RED if self.triggered else MINT
        pygame.draw.circle(screen, color, (cx, cy), self.radius)
        pygame.draw.circle(screen, BLACK, (cx, cy), self.radius - 4)
        if self.triggered:
            pygame.draw.circle(screen, (255, 220, 120), (cx, cy), 5)


class FakeFloor:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.triggered = False
        self.alpha = 255

    def update(self, player, dt):
        if not self.triggered and self.rect.colliderect(player.rect):
            self.triggered = True
        if self.triggered:
            self.alpha = max(0, self.alpha - 500 * dt)

    def draw(self, screen, camera_x):
        if self.alpha <= 0:
            return
        rect = self.rect.move(-camera_x, 0)
        color = (60, 70, 90, self.alpha)
        surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surf.fill((60, 70, 90, int(self.alpha)))
        screen.blit(surf, rect)


class Level:
    def __init__(self, stage_num):
        self.stage_num = stage_num
        self.width = 2100 + stage_num * 140
        self.platforms = []
        self.hazards = []
        self.spikes = []
        self.tripmines = []
        self.fake_floors = []
        self.moving_platforms = []
        self.enemies = []
        self.spawn_x = 70
        self.spawn_y = HEIGHT - 120
        self.goal_x = self.width - 120
        self.build()

    def build(self):
        self.platforms.append(pygame.Rect(0, HEIGHT - 52, 220, 52))
        self.platforms.append(pygame.Rect(self.width - 250, HEIGHT - 52, 250, 52))

        x = 210
        for i in range(18 + self.stage_num * 2):
            block_w = 70 + max(0, self.stage_num - 10) * 5 + (i % 4) * 14
            block_h = 18
            y = HEIGHT - 170 - ((i * 27 + self.stage_num * 11) % 190)
            self.platforms.append(pygame.Rect(x, y, block_w, block_h))
            x += block_w + 30 + (self.stage_num % 5) * 4
            if i % 3 == 0 and self.stage_num > 0:
                self.spikes.append(SpikeTrap(x - 22, y + block_h - 2, min(60, block_w - 8), 14, invisible=(self.stage_num > 2 and i % 2 == 0)))

        for i in range(1 + self.stage_num // 4):
            wx = 420 + i * (150 + self.stage_num * 4)
            wy = HEIGHT - 250 - (i % 3) * 65
            moving = MovingPlatform(wx, wy, 110, 18, 'x', wx - 90, wx + 150 + self.stage_num * 3, 90 + i * 12)
            self.moving_platforms.append(moving)
            self.platforms.append(moving.rect)

        for i in range(1 + self.stage_num // 3):
            ex = 330 + i * 200 + self.stage_num * 9
            ey = HEIGHT - 120 - (i % 4) * 55
            enemy = Enemy(ex, ey, 18, 110 + self.stage_num * 4, 'x', ex - 90, ex + 180)
            self.enemies.append(enemy)

        if self.stage_num >= 3:
            for i in range(1 + self.stage_num // 5):
                spike_x = 780 + i * 180 + self.stage_num * 6
                self.spikes.append(SpikeTrap(spike_x, HEIGHT - 70, 70, 16, invisible=True))

        if self.stage_num >= 5:
            for i in range(1 + self.stage_num // 4):
                mx = 920 + i * 220 + self.stage_num * 7
                my = HEIGHT - 150 - (i % 2) * 90
                self.tripmines.append(Tripmine(mx, my))

        if self.stage_num >= 8:
            for i in range(1 + self.stage_num // 6):
                fx = 600 + i * 260 + self.stage_num * 8
                fy = HEIGHT - 110
                self.fake_floors.append(FakeFloor(fx, fy, 80, 18))

        if self.stage_num >= 10 and self.stage_num % 3 == 1:
            self.spikes.append(SpikeTrap(self.width - 520, HEIGHT - 110, 140, 18, invisible=True))

        self.name = [
            'Smile Startup', 'Warm-Up Grin', 'Tiny Teeth', 'Panic Laugh', 'Fake Calm',
            'Annoying Eyes', 'Very Friendly', 'Mildly Evil', 'Cheeky Warning', 'Wobbly Smile',
            'Tiny Trap', 'Spooky Laughter', 'Unhinged Joy', 'Cruel Grin', 'A Little Too Real',
            'Smiley Squeeze', 'No Escape', 'Laughing Floor', 'Bad Vibes', 'Jealous Teeth',
            'False Safety', 'Sneaky Eyes', 'Murderous Grin', 'The Smile Returns', 'Neon Nightmare',
            'Perfectly Still', 'Room For Rage', 'Worse Than Before', 'Goodbye Health', 'The Scream',
            'Smile Logic', 'Glaring Teeth', 'Troll Stage', 'You Should Leave', 'Actually No',
            'Hate This', 'Very Mean', 'Still Smiling', 'This Is Unfair', 'Why Is It Moving',
            'The Smile Hates You', 'You Knew It', 'Unlucky', 'No More Patience', 'Maze of Rage',
            'Smile At Your Doom', 'Dreadful Laugh', 'Trickery Everywhere', 'Aggressive Clown', 'Bigger Teeth',
            'Just One More', 'You Are Already Mad', 'It Is Watching', 'The Floor Hates You', 'Smile To The End',
            'Last One', 'Final Grin', 'Smile Wins'
        ][min(self.stage_num, 59)]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Smile Rage Platformer')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 26)
        self.big_font = pygame.font.SysFont('arial', 48, bold=True)
        self.stage_num = 0
        self.deaths = 0
        self.message_timer = 0.0
        self.win = False
        self.load_stage()

    def load_stage(self):
        self.level = Level(self.stage_num)
        self.player = Player(self.level.spawn_x, self.level.spawn_y)
        self.camera_x = 0
        self.stage_message = f'Stage {self.stage_num + 1}: {self.level.name}'
        self.message_timer = 2.5

    def respawn_player(self):
        self.deaths += 1
        self.player = Player(self.level.spawn_x, self.level.spawn_y)
        self.camera_x = 0
        self.message_timer = 1.3
        self.stage_message = 'RESPAWN'

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.win:
            return

        self.message_timer = max(0, self.message_timer - dt)

        for mp in self.level.moving_platforms:
            mp.update(dt)

        for enemy in self.level.enemies:
            enemy.update(dt)

        for trap in self.level.spikes:
            trap.update(self.player, dt)

        for mine in self.level.tripmines:
            mine.update(self.player, dt)

        for floor in self.level.fake_floors:
            floor.update(self.player, dt)

        solid_platforms = list(self.level.platforms)
        for mp in self.level.moving_platforms:
            solid_platforms.append(mp.rect)
        for floor in self.level.fake_floors:
            if floor.alpha > 10:
                solid_platforms.append(floor.rect)

        self.player.update(dt, keys, solid_platforms)

        for trap in self.level.spikes:
            if trap.hurts(self.player):
                self.respawn_player()
                return

        for mine in self.level.tripmines:
            if mine.hurts(self.player):
                self.respawn_player()
                return

        for enemy in self.level.enemies:
            if math.hypot(self.player.rect.centerx - enemy.x, self.player.rect.centery - enemy.y) <= self.player.rect.width * 0.8 + enemy.radius:
                self.respawn_player()
                return

        if self.player.rect.top > HEIGHT + 200:
            self.respawn_player()
            return

        if self.player.rect.right >= self.level.goal_x:
            self.stage_num += 1
            if self.stage_num >= 60:
                self.win = True
            else:
                self.load_stage()
                self.message_timer = 2.5
                self.stage_message = f'Stage {self.stage_num + 1}: {self.level.name}'

        self.camera_x = max(0, min(self.player.rect.centerx - WIDTH * 0.35, self.level.width - WIDTH))

    def draw_background(self):
        self.screen.fill(BLACK)
        for i in range(0, WIDTH + 30, 40):
            pygame.draw.line(self.screen, DARK, (i, 0), (i, HEIGHT), 1)
        for i in range(0, HEIGHT + 30, 40):
            pygame.draw.line(self.screen, DARK, (0, i), (WIDTH, i), 1)

        for i in range(5):
            x = (i * 270 + self.camera_x * 0.25) % (WIDTH + 200)
            y = 120 + i * 110
            pygame.draw.circle(self.screen, (30, 45, 60), (int(x), int(y)), 38)
            pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), 18)
            pygame.draw.circle(self.screen, BLACK, (int(x) - 6, int(y) - 6), 4)
            pygame.draw.circle(self.screen, BLACK, (int(x) + 6, int(y) - 6), 4)
            pygame.draw.arc(self.screen, BLACK, (int(x) - 15, int(y) + 2, 30, 18), 0.2, math.pi - 0.2, 3)

    def draw(self):
        self.draw_background()

        offset = self.camera_x

        for p in self.level.platforms:
            rect = p.move(-offset, 0)
            pygame.draw.rect(self.screen, (45, 48, 66), rect)
            pygame.draw.rect(self.screen, (80, 90, 110), rect.inflate(-6, -6), 2)

        for floor in self.level.fake_floors:
            floor.draw(self.screen, offset)

        for trap in self.level.spikes:
            trap.draw(self.screen, offset)

        for mine in self.level.tripmines:
            mine.draw(self.screen, offset)

        for enemy in self.level.enemies:
            enemy.draw(self.screen, offset)

        goal_rect = pygame.Rect(self.level.goal_x - offset, HEIGHT - 90, 34, 90)
        pygame.draw.rect(self.screen, YELLOW, goal_rect)
        pygame.draw.circle(self.screen, BLACK, (int(goal_rect.centerx), int(goal_rect.top + 22)), 10)
        pygame.draw.circle(self.screen, BLACK, (int(goal_rect.centerx - 8), int(goal_rect.top + 22)), 3)
        pygame.draw.circle(self.screen, BLACK, (int(goal_rect.centerx + 8), int(goal_rect.top + 22)), 3)
        pygame.draw.arc(self.screen, BLACK, (int(goal_rect.left + 5), int(goal_rect.top + 28), 24, 18), 0.2, 3.0, 3)

        self.player.draw(self.screen, offset)

        stage_text = self.font.render(f"Stage {self.stage_num + 1} / 60", True, WHITE)
        self.screen.blit(stage_text, (20, 18))

        deaths_text = self.font.render(f"Deaths: {self.deaths}", True, ORANGE)
        self.screen.blit(deaths_text, (20, 46))

        name_text = self.font.render(self.level.name, True, PINK)
        self.screen.blit(name_text, (20, 74))

        if self.message_timer > 0:
            prompt = self.big_font.render(self.stage_message, True, BLUE)
            self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 24))

        if self.win:
            banner = self.big_font.render('YOU DID IT', True, GREEN)
            sub = self.font.render('All 60 smile stages cleared. Rage completed.', True, WHITE)
            self.screen.blit(banner, (WIDTH // 2 - banner.get_width() // 2, HEIGHT // 2 - 30))
            self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 30))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            if not self.win:
                self.update(dt)
            self.draw()
        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
