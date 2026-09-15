from pathlib import Path

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
FRAME_RATE = 30
PROJECT_FOLDER = Path(__file__).resolve().parent


def load_image(filename, fallback_color):
	"""Load a local image and provide a visible fallback if it is unavailable."""
	image_path = PROJECT_FOLDER / filename
	try:
		return pygame.image.load(image_path).convert()
	except (FileNotFoundError, pygame.error):
		fallback = pygame.Surface((100, 100))
		fallback.fill(fallback_color)
		return fallback


def game_loop():
	pygame.init()
	display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Wildlife Information Display")

	background_image = pygame.transform.scale(
		load_image("wildlife_background.ppm", (31, 78, 66)),
		(SCREEN_WIDTH, SCREEN_HEIGHT),
	)
	wildlife_image = pygame.transform.smoothscale(
		load_image("wildlife_animal.ppm", (182, 93, 54)),
		(280, 280),
	)
	wildlife_rect = wildlife_image.get_rect(center=(SCREEN_WIDTH // 2, 300))

	heading_font = pygame.font.Font(None, 58)
	fact_font = pygame.font.Font(None, 30)
	heading = heading_font.render("RED PANDA", True, pygame.Color("white"))
	fact = fact_font.render(
		"Red pandas use their long tails for balance and warmth.",
		True,
		pygame.Color("white"),
	)
	heading_rect = heading.get_rect(center=(SCREEN_WIDTH // 2, 72))
	fact_rect = fact.get_rect(center=(SCREEN_WIDTH // 2, 535))

	clock = pygame.time.Clock()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		display_surface.blit(background_image, (0, 0))
		display_surface.blit(wildlife_image, wildlife_rect)
		display_surface.blit(heading, heading_rect)
		display_surface.blit(fact, fact_rect)

		pygame.display.flip()
		clock.tick(FRAME_RATE)

	pygame.quit()


if __name__ == "__main__":
	game_loop()