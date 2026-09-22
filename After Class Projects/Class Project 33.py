import sys

import pygame


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
ROAD_RECT = pygame.Rect(0, 185, SCREEN_WIDTH, 190)
ROAD_LEFT = 70
ROAD_RIGHT = SCREEN_WIDTH - 70

SKY = (112, 190, 221)
GRASS = (76, 156, 91)
ROAD = (54, 58, 66)
ROAD_EDGE = (235, 197, 71)
WHITE = (245, 245, 245)
CAR_COLORS = [(220, 58, 58), (42, 119, 209), (241, 156, 44), (55, 166, 104), (167, 83, 184)]


class Car(pygame.sprite.Sprite):
	"""A drawable car that reverses and signals when it reaches the road edge."""

	def __init__(self, x, y):
		super().__init__()
		self.colors = CAR_COLORS
		self.color_index = 0
		self.speed = 210
		self.direction = 1
		self.boundary_hit = False
		self.image = pygame.Surface((126, 58), pygame.SRCALPHA)
		self.rect = self.image.get_rect(center=(x, y))
		self._draw_car()

	def _draw_car(self):
		self.image.fill((0, 0, 0, 0))
		body_color = self.colors[self.color_index]
		pygame.draw.rect(self.image, body_color, (8, 22, 110, 25), border_radius=8)
		pygame.draw.polygon(self.image, body_color, [(30, 22), (47, 5), (83, 5), (101, 22)])
		pygame.draw.polygon(self.image, (176, 224, 236), [(50, 9), (63, 9), (63, 20), (40, 20)])
		pygame.draw.polygon(self.image, (176, 224, 236), [(67, 9), (80, 9), (93, 20), (67, 20)])
		pygame.draw.circle(self.image, (28, 31, 37), (30, 48), 12)
		pygame.draw.circle(self.image, (28, 31, 37), (96, 48), 12)
		pygame.draw.circle(self.image, (178, 184, 190), (30, 48), 5)
		pygame.draw.circle(self.image, (178, 184, 190), (96, 48), 5)
		pygame.draw.rect(self.image, (255, 239, 145), (109, 28, 8, 8), border_radius=2)
		pygame.draw.rect(self.image, (194, 38, 42), (9, 28, 8, 8), border_radius=2)

	def update(self, dt):
		self.boundary_hit = False
		self.rect.x += round(self.speed * self.direction * dt)
		if self.rect.left <= ROAD_LEFT:
			self.rect.left = ROAD_LEFT
			self.direction = 1
			self.boundary_hit = True
		elif self.rect.right >= ROAD_RIGHT:
			self.rect.right = ROAD_RIGHT
			self.direction = -1
			self.boundary_hit = True

		if self.boundary_hit:
			self.color_index = (self.color_index + 1) % len(self.colors)
			self._draw_car()


class TrafficLight:
	def __init__(self):
		self.colors = [(220, 55, 58), (244, 190, 55), (62, 185, 92)]
		self.active = 0
		self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 24, 48, 48, 122)

	def change(self):
		self.active = (self.active + 1) % len(self.colors)

	def draw(self, screen):
		pygame.draw.rect(screen, (38, 42, 48), self.rect, border_radius=8)
		pygame.draw.rect(screen, (25, 28, 32), self.rect, 3, border_radius=8)
		for index, color in enumerate(self.colors):
			light_color = color if index == self.active else tuple(value // 5 for value in color)
			pygame.draw.circle(screen, light_color, (self.rect.centerx, 70 + index * 35), 13)
		pygame.draw.rect(screen, (38, 42, 48), (self.rect.centerx - 5, self.rect.bottom, 10, 34))


def draw_scene(screen, car_group, traffic_light, font):
	screen.fill(SKY)
	pygame.draw.rect(screen, GRASS, (0, 145, SCREEN_WIDTH, SCREEN_HEIGHT - 145))
	pygame.draw.rect(screen, ROAD, ROAD_RECT)
	pygame.draw.line(screen, ROAD_EDGE, (0, ROAD_RECT.top), (SCREEN_WIDTH, ROAD_RECT.top), 5)
	pygame.draw.line(screen, ROAD_EDGE, (0, ROAD_RECT.bottom), (SCREEN_WIDTH, ROAD_RECT.bottom), 5)
	for x in range(0, SCREEN_WIDTH, 80):
		pygame.draw.rect(screen, WHITE, (x, ROAD_RECT.centery - 4, 48, 8))
	traffic_light.draw(screen)
	car_group.draw(screen)
	title = font.render("BOUNDARY DRIVE", True, (25, 54, 65))
	hint = font.render("The car changes color and the signal changes at each road boundary", True, (25, 54, 65))
	screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 22)))
	screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 505)))


def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Moving Car Sprite")
	clock = pygame.time.Clock()
	font = pygame.font.Font(None, 27)
	traffic_light = TrafficLight()
	car = Car(ROAD_LEFT + 80, ROAD_RECT.centery)
	car_group = pygame.sprite.Group(car)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

		car_group.update(clock.get_time() / 1000)
		if car.boundary_hit:
			traffic_light.change()
		draw_scene(screen, car_group, traffic_light, font)
		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()
	sys.exit()


if __name__ == "__main__":
	main()
