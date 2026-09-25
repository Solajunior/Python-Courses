import math
import random
import sys

import pygame


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600
FPS = 60
FOOD_ON_SCREEN = 6
TREATS_TO_LEVEL_TWO = 8

SKY = (135, 211, 229)
GRASS = (111, 180, 101)
WHITE = (250, 250, 239)
INK = (39, 54, 47)


def make_background():
	background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
	background.fill(GRASS)
	pygame.draw.rect(background, SKY, (0, 0, SCREEN_WIDTH, 150))
	pygame.draw.polygon(background, (116, 190, 177), [(0, 145), (115, 78), (238, 149), (365, 91), (510, 151), (650, 80), (790, 150), (900, 92), (960, 130), (960, 190), (0, 190)])
	pygame.draw.polygon(background, (91, 166, 118), [(0, 164), (145, 112), (294, 169), (435, 119), (602, 175), (755, 113), (914, 170), (960, 151), (960, 220), (0, 220)])

	for cloud_x, cloud_y in ((130, 48), (440, 75), (790, 42)):
		pygame.draw.ellipse(background, WHITE, (cloud_x, cloud_y, 72, 25))
		pygame.draw.circle(background, WHITE, (cloud_x + 19, cloud_y), 17)
		pygame.draw.circle(background, WHITE, (cloud_x + 43, cloud_y - 5), 21)

	for tree_x, tree_y in ((52, 151), (204, 160), (741, 147), (891, 157)):
		pygame.draw.rect(background, (123, 85, 55), (tree_x - 6, tree_y - 31, 12, 39))
		pygame.draw.circle(background, (54, 131, 75), (tree_x, tree_y - 43), 25)
		pygame.draw.circle(background, (73, 151, 81), (tree_x - 16, tree_y - 32), 16)
		pygame.draw.circle(background, (73, 151, 81), (tree_x + 15, tree_y - 31), 17)

	path_points = [(x, 420 + round(math.sin(x / 155) * 24)) for x in range(-20, SCREEN_WIDTH + 30, 12)]
	pygame.draw.lines(background, (194, 174, 122), False, path_points, 104)
	pygame.draw.lines(background, (215, 196, 143), False, path_points, 88)

	randomizer = random.Random(12)
	for _ in range(100):
		x = randomizer.randrange(SCREEN_WIDTH)
		y = randomizer.randrange(205, SCREEN_HEIGHT)
		color = randomizer.choice(((246, 223, 112), (244, 245, 215), (235, 150, 145)))
		pygame.draw.circle(background, (62, 133, 74), (x, y + 3), 3)
		pygame.draw.circle(background, color, (x, y), 2)

	return background


class Pet(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((62, 58), pygame.SRCALPHA)
		pygame.draw.ellipse(self.image, (190, 119, 72), (5, 19, 49, 34))
		pygame.draw.circle(self.image, (207, 143, 91), (43, 25), 20)
		pygame.draw.ellipse(self.image, (129, 77, 56), (30, 4, 13, 22))
		pygame.draw.ellipse(self.image, (129, 77, 56), (48, 9, 11, 19))
		pygame.draw.ellipse(self.image, (250, 224, 187), (40, 31, 19, 12))
		pygame.draw.circle(self.image, INK, (47, 22), 2)
		pygame.draw.circle(self.image, INK, (58, 29), 3)
		pygame.draw.ellipse(self.image, (190, 119, 72), (10, 43, 14, 10))
		pygame.draw.ellipse(self.image, (190, 119, 72), (37, 43, 14, 10))
		self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
		self.speed = 270

	def update(self, delta_time, keys):
		direction_x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
		direction_y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
		length = math.hypot(direction_x, direction_y)
		if length:
			self.rect.x += round(direction_x / length * self.speed * delta_time)
			self.rect.y += round(direction_y / length * self.speed * delta_time)
		self.rect.clamp_ip(pygame.Rect(0, 112, SCREEN_WIDTH, SCREEN_HEIGHT - 112))


class Food(pygame.sprite.Sprite):
	def __init__(self, position):
		super().__init__()
		self.image = pygame.Surface((34, 34), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (132, 79, 47), (17, 17), 14)
		pygame.draw.circle(self.image, (91, 53, 39), (17, 17), 14, 2)
		for dot_x, dot_y in ((12, 12), (21, 11), (13, 21), (21, 22)):
			pygame.draw.circle(self.image, (224, 165, 94), (dot_x, dot_y), 2)
		self.rect = self.image.get_rect(center=position)


class PetFoodGame:
	def __init__(self):
		self.pet = Pet()
		self.foods = pygame.sprite.Group()
		self.score = 0
		self.level = 1
		self.completed = False
		for _ in range(FOOD_ON_SCREEN):
			self.foods.add(self._spawn_food())

	def _spawn_food(self):
		for _ in range(100):
			position = (random.randint(45, SCREEN_WIDTH - 45), random.randint(145, SCREEN_HEIGHT - 45))
			food = Food(position)
			if food.rect.colliderect(self.pet.rect.inflate(70, 70)):
				continue
			if any(food.rect.colliderect(existing.rect.inflate(28, 28)) for existing in self.foods):
				continue
			return food
		return Food((random.randint(45, SCREEN_WIDTH - 45), random.randint(145, SCREEN_HEIGHT - 45)))

	def update(self, delta_time, keys):
		if self.completed:
			return
		self.pet.update(delta_time, keys)
		collected_food = pygame.sprite.spritecollide(self.pet, self.foods, True)
		for _ in collected_food:
			self.score += 1
			if self.score >= TREATS_TO_LEVEL_TWO:
				self.level = 2
				self.completed = True
				break
			self.foods.add(self._spawn_food())

	def draw(self, screen, background, title_font, ui_font, message_font):
		screen.blit(background, (0, 0))
		self.foods.draw(screen)
		screen.blit(self.pet.image, self.pet.rect)

		pygame.draw.rect(screen, (255, 255, 244), (18, 16, 330, 78), border_radius=12)
		pygame.draw.rect(screen, (66, 111, 73), (18, 16, 330, 78), 3, border_radius=12)
		screen.blit(title_font.render("TREAT TRAIL", True, INK), (34, 23))
		status = ui_font.render(f"Level {self.level}    Treats {self.score}/{TREATS_TO_LEVEL_TWO}", True, INK)
		screen.blit(status, (35, 59))
		controls = ui_font.render("Move: WASD or arrow keys     Quit: Esc", True, INK)
		pygame.draw.rect(screen, (255, 255, 244), (SCREEN_WIDTH // 2 - 227, SCREEN_HEIGHT - 48, 454, 32), border_radius=9)
		screen.blit(controls, controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 32)))

		if self.completed:
			overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
			overlay.fill((23, 39, 31, 155))
			screen.blit(overlay, (0, 0))
			panel = pygame.Rect(0, 0, 500, 190)
			panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
			pygame.draw.rect(screen, (255, 252, 231), panel, border_radius=18)
			pygame.draw.rect(screen, (76, 137, 78), panel, 5, border_radius=18)
			message = message_font.render("LEVEL 2 COMPLETE!", True, (50, 107, 62))
			subtitle = ui_font.render("Your pet found every treat!", True, INK)
			screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 24)))
			screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 32)))


def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Treat Trail - Pet Food Collection")
	clock = pygame.time.Clock()
	background = make_background()
	title_font = pygame.font.SysFont("trebuchetms", 25, bold=True)
	ui_font = pygame.font.SysFont("trebuchetms", 19)
	message_font = pygame.font.SysFont("trebuchetms", 38, bold=True)
	game = PetFoodGame()
	running = True

	while running:
		delta_time = min(clock.tick(FPS) / 1000, 0.05)
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

		game.update(delta_time, pygame.key.get_pressed())
		game.draw(screen, background, title_font, ui_font, message_font)
		pygame.display.flip()

	pygame.quit()
	sys.exit()


if __name__ == "__main__":
	main()
