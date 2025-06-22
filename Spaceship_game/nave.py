import pygame
import random
import sys

# Inicializar pygame
pygame.init()
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Nave")

# Colores
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
RED = (220, 30, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60

class Nave:
    def __init__(self, x, y, color, left_key, right_key, shoot_key):
        self.x = x
        self.y = y
        self.size = 30
        self.vel = 6
        self.color = color
        self.left_key = left_key
        self.right_key = right_key
        self.shoot_key = shoot_key
        self.last_shot_time = 0
        self.shot_cooldown = 400  # milisegundos
        self.score = 0
        self.vivo = True

    def draw(self, win):
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]
        pygame.draw.polygon(win, self.color, points)

    def move(self, keys):
        if keys[self.left_key]:
            self.x -= self.vel
        if keys[self.right_key]:
            self.x += self.vel
        self.x = max(self.size, min(WIDTH - self.size, self.x))

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            return True
        return False

class Bala:
    def __init__(self, x, y, nave):
        self.x = x
        self.y = y
        self.vel = 10
        self.nave = nave

    def draw(self, win):
        pygame.draw.rect(win, WHITE, (self.x - 2, self.y - 12, 4, 12))

    def move(self):
        self.y -= self.vel

class Enemigo:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.size = 28
        self.speed = speed

    def draw(self, win):
        pygame.draw.rect(win, RED, (self.x - self.size//2, self.y - self.size//2, self.size, self.size))

    def move(self):
        self.y += self.speed

def colision(rect1, rect2):
    return rect1.colliderect(rect2)

def menu():
    font = pygame.font.SysFont("arial", 36)
    selected_option = 0
    options = ["Single Player", "Multiplayer"]

    while True:
        WIN.fill(BLACK)
        title = font.render("Seleccione el modo de juego", True, WHITE)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        for i, option in enumerate(options):
            color = WHITE if i != selected_option else RED
            text = font.render(option, True, color)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, 250 + i*60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 2
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2
                if event.key == pygame.K_RETURN:
                    return selected_option

def main(modo_multijugador):
    clock = pygame.time.Clock()
    balas = []
    enemigos = []
    enemigo_timer = 0
    enemigo_interval = 60
    enemigo_speed = 2
    game_over = False
    font = pygame.font.SysFont("arial", 28)
    big_font = pygame.font.SysFont("arial", 48)
    start_ticks = pygame.time.get_ticks()

    nave1 = Nave(WIDTH // 3, HEIGHT - 60, BLUE, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)

    if modo_multijugador:
        nave2 = Nave(WIDTH * 2 // 3, HEIGHT - 60, GREEN, pygame.K_a, pygame.K_d, pygame.K_w)
        naves = [nave1, nave2]
    else:
        naves = [nave1]

    while True:
        dt = clock.tick(FPS)
        WIN.fill(BLACK)

        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        enemigo_speed = 2 + seconds * 0.1
        enemigo_interval = max(20, 60 - seconds)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main(modo_multijugador)
                return

        keys = pygame.key.get_pressed()
        if not game_over:
            for nave in naves:
                if nave.vivo:
                    nave.move(keys)
                    if keys[nave.shoot_key]:
                        if nave.can_shoot():
                            balas.append(Bala(nave.x, nave.y - nave.size, nave))

        if not game_over:
            enemigo_timer += 1
            if enemigo_timer >= enemigo_interval:
                enemigo_timer = 0
                x = random.randint(30, WIDTH - 30)
                enemigos.append(Enemigo(x, -30, enemigo_speed))

        for bala in balas[:]:
            bala.move()
            bala.draw(WIN)
            if bala.y < -20:
                balas.remove(bala)

        for enemigo in enemigos[:]:
            enemigo.move()
            enemigo.draw(WIN)
            if enemigo.y > HEIGHT + 30:
                enemigos.remove(enemigo)

            for nave in naves:
                if not nave.vivo:
                    continue
                nave_rect = pygame.Rect(nave.x - nave.size, nave.y - nave.size, nave.size*2, nave.size*2)
                enemigo_rect = pygame.Rect(enemigo.x - enemigo.size//2, enemigo.y - enemigo.size//2, enemigo.size, enemigo.size)
                if colision(nave_rect, enemigo_rect):
                    nave.vivo = False

        for bala in balas[:]:
            bala_rect = pygame.Rect(bala.x - 2, bala.y - 12, 4, 12)
            for enemigo in enemigos[:]:
                enemigo_rect = pygame.Rect(enemigo.x - enemigo.size//2, enemigo.y - enemigo.size//2, enemigo.size, enemigo.size)
                if colision(bala_rect, enemigo_rect):
                    try:
                        balas.remove(bala)
                        enemigos.remove(enemigo)
                        bala.nave.score += 10
                    except ValueError:
                        pass

        for nave in naves:
            if nave.vivo:
                nave.draw(WIN)

        # Mostrar puntajes
        score_text1 = font.render(f"Azul: {nave1.score}", True, BLUE)
        WIN.blit(score_text1, (10, 10))
        if modo_multijugador:
            score_text2 = font.render(f"Verde: {nave2.score}", True, GREEN)
            WIN.blit(score_text2, (10, 40))

        # Verificar si el juego termina
        if not game_over and all(not nave.vivo for nave in naves):
            game_over = True

        if game_over:
            over_text = big_font.render("GAME OVER", True, RED)
            WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 100))

            score_over1 = font.render(f"Azul: {nave1.score}", True, BLUE)
            WIN.blit(score_over1, (WIDTH//2 - score_over1.get_width()//2, HEIGHT//2))
            if modo_multijugador:
                score_over2 = font.render(f"Verde: {nave2.score}", True, GREEN)
                WIN.blit(score_over2, (WIDTH//2 - score_over2.get_width()//2, HEIGHT//2 + 40))

            restart_text = font.render("Presiona R para reiniciar", True, WHITE)
            WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))

        pygame.display.update()

if __name__ == "__main__":
    modo = menu()
    main(modo)
