import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
PLAYER_SIZE = 36
ENEMY_SIZE = 30
PLAYER_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enemy Touch Challenge")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 64)

background_color = (25, 30, 45)
player_color = (70, 190, 255)
enemy_color = (235, 75, 85)
text_color = (245, 245, 245)

player = pygame.Rect(
	WIDTH // 2 - PLAYER_SIZE // 2,
	HEIGHT // 2 - PLAYER_SIZE // 2,
	PLAYER_SIZE,
	PLAYER_SIZE,
)

enemy_positions = [
	(90, 100),
	(260, 90),
	(500, 110),
	(680, 210),
	(120, 420),
	(370, 480),
	(650, 440),
]
enemies = [pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE) for x, y in enemy_positions]
score = 0
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		player.x -= PLAYER_SPEED
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		player.x += PLAYER_SPEED
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		player.y -= PLAYER_SPEED
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		player.y += PLAYER_SPEED

	player.clamp_ip(screen.get_rect())

	for enemy in enemies[:]:
		if player.colliderect(enemy):
			enemies.remove(enemy)
			score += 1

	screen.fill(background_color)
	pygame.draw.rect(screen, player_color, player, border_radius=8)

	for enemy in enemies:
		pygame.draw.rect(screen, enemy_color, enemy, border_radius=6)

	score_text = font.render(f"Score: {score}", True, text_color)
	remaining_text = font.render(f"Enemies left: {len(enemies)}", True, text_color)
	screen.blit(score_text, (20, 18))
	screen.blit(remaining_text, (20, 52))

	if not enemies:
		win_text = large_font.render("You got them all!", True, text_color)
		win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
		screen.blit(win_text, win_rect)

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
