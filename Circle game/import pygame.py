import pygame
import random
import math

# Configuración inicial
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_GREEN = (0, 255, 128)
NEON_YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Orbital: Escape del Vórtice")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 32)

# Jugador
class Player:
    def __init__(self):
        self.radius = 20
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.orbit_radius = 120
        self.speed = 0.04
        self.color = NEON_BLUE
        self.alive = True

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle -= self.speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.speed
        if keys[pygame.K_UP]:
            self.orbit_radius -= 2
        if keys[pygame.K_DOWN]:
            self.orbit_radius += 2
        self.orbit_radius = max(60, min(self.orbit_radius, 250))
        self.x = WIDTH // 2 + int(math.cos(self.angle) * self.orbit_radius)
        self.y = HEIGHT // 2 + int(math.sin(self.angle) * self.orbit_radius)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 4)
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.radius // 2)

# Obstáculos
class Obstacle:
    def __init__(self):
        self.angle = random.uniform(0, 2 * math.pi)
        self.orbit_radius = random.randint(60, 250)
        self.radius = random.randint(15, 30)
        self.speed = random.uniform(0.01, 0.03)
        self.color = random.choice([NEON_PINK, NEON_GREEN, NEON_YELLOW])

    def update(self):
        self.angle += self.speed
        self.x = WIDTH // 2 + int(math.cos(self.angle) * self.orbit_radius)
        self.y = HEIGHT // 2 + int(math.sin(self.angle) * self.orbit_radius)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 3)

    def collide(self, player):
        dist = math.hypot(self.x - player.x, self.y - player.y)
        return dist < self.radius + player.radius - 5

# Efecto de vórtice
def draw_vortex(surface, t):
    for i in range(30):
        r = 60 + i * 6 + int(math.sin(t + i) * 4)
        color = (int(128 + 127 * math.sin(t + i)),
                 int(128 + 127 * math.sin(t + i + 2)),
                 int(128 + 127 * math.sin(t + i + 4)))
        pygame.draw.circle(surface, color, (WIDTH // 2, HEIGHT // 2), r, 2)

def main():
    player = Player()
    obstacles = [Obstacle() for _ in range(7)]
    score = 0
    running = True
    t = 0

    while running:
        clock.tick(FPS)
        t += 0.03
        screen.fill(BLACK)
        draw_vortex(screen, t)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player.alive:
            player.update(keys)
            player.draw(screen)
            for obs in obstacles:
                obs.update()
                obs.draw(screen)
                if obs.collide(player):
                    player.alive = False
            score += 1
        else:
            msg = font.render("¡Game Over! Puntuación: " + str(score // 10), True, NEON_PINK)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
            msg2 = font.render("Presiona R para reiniciar", True, NEON_GREEN)
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 10))
            if keys[pygame.K_r]:
                player = Player()
                obstacles = [Obstacle() for _ in range(7)]
                score = 0

        score_text = font.render("Puntuación: " + str(score // 10), True, NEON_YELLOW)
        screen.blit(score_text, (20, 20))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

    # Mejoras gráficas y funcionales

    # 1. Añadir cambio de posición de obstáculos cada dos vueltas del jugador
    # 2. Mejorar el recuadro del puntaje
    # 3. Mejorar gráficos: brillos, efectos y detalles visuales

    # --- Cambios en la clase Player para contar vueltas ---
class Player:
    def __init__(self):
        self.radius = 20
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.orbit_radius = 120
        self.speed = 0.04
        self.color = NEON_BLUE
        self.alive = True
        self.lap_count = 0
        self._last_angle = 0

    def update(self, keys):
        prev_angle = self.angle
        if keys[pygame.K_LEFT]:
            self.angle -= self.speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.speed
        if keys[pygame.K_UP]:
            self.orbit_radius -= 2
        if keys[pygame.K_DOWN]:
            self.orbit_radius += 2
        self.orbit_radius = max(60, min(self.orbit_radius, 250))
        self.x = WIDTH // 2 + int(math.cos(self.angle) * self.orbit_radius)
        self.y = HEIGHT // 2 + int(math.sin(self.angle) * self.orbit_radius)
        # Contar vueltas (cada vez que pasa por el eje positivo X)
        if (prev_angle % (2 * math.pi)) > (self.angle % (2 * math.pi)):
            self.lap_count += 1

    def draw(self, surface):
        # Efecto de brillo
        for i in range(6, 0, -1):
            alpha_surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surf, (*self.color, 20*i), (self.radius, self.radius), self.radius + i*3)
            surface.blit(alpha_surf, (self.x - self.radius, self.y - self.radius), special_flags=pygame.BLEND_RGBA_ADD)
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 4)
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.radius // 2)

# --- Cambios en la clase Obstacle para reposicionar ---
class Obstacle:
    def __init__(self):
        self.angle = random.uniform(0, 2 * math.pi)
        self.orbit_radius = random.randint(60, 250)
        self.radius = random.randint(15, 30)
        self.speed = random.uniform(0.01, 0.03)
        self.color = random.choice([NEON_PINK, NEON_GREEN, NEON_YELLOW])
        self.x = WIDTH // 2 + int(math.cos(self.angle) * self.orbit_radius)
        self.y = HEIGHT // 2 + int(math.sin(self.angle) * self.orbit_radius)

    def update(self):
        self.angle += self.speed
        self.x = WIDTH // 2 + int(math.cos(self.angle) * self.orbit_radius)
        self.y = HEIGHT // 2 + int(math.sin(self.angle) * self.orbit_radius)

    def draw(self, surface):
        # Efecto de brillo
        for i in range(4, 0, -1):
            alpha_surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surf, (*self.color, 18*i), (self.radius, self.radius), self.radius + i*2)
            surface.blit(alpha_surf, (self.x - self.radius, self.y - self.radius), special_flags=pygame.BLEND_RGBA_ADD)
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 3)

    def collide(self, player):
        dist = math.hypot(self.x - player.x, self.y - player.y)
        return dist < self.radius + player.radius - 5

    def reposition(self):
        self.angle = random.uniform(0, 2 * math.pi)
        self.orbit_radius = random.randint(60, 250)
        self.radius = random.randint(15, 30)
        self.speed = random.uniform(0.01, 0.03)
        self.color = random.choice([NEON_PINK, NEON_GREEN, NEON_YELLOW])

# --- Mejorar el vórtice con más efectos ---
def draw_vortex(surface, t):
    for i in range(30):
        r = 60 + i * 6 + int(math.sin(t + i) * 4)
        color = (
            int(128 + 127 * math.sin(t + i)),
            int(128 + 127 * math.sin(t + i + 2)),
            int(128 + 127 * math.sin(t + i + 4))
        )
        pygame.draw.circle(surface, color, (WIDTH // 2, HEIGHT // 2), r, 2)
    # Añadir líneas radiales
    for i in range(16):
        angle = t + i * (2 * math.pi / 16)
        x1 = WIDTH // 2 + int(math.cos(angle) * 60)
        y1 = HEIGHT // 2 + int(math.sin(angle) * 60)
        x2 = WIDTH // 2 + int(math.cos(angle) * 240)
        y2 = HEIGHT // 2 + int(math.sin(angle) * 240)
        pygame.draw.aaline(surface, (80, 255, 255, 80), (x1, y1), (x2, y2))

# --- Mejorar el recuadro del puntaje ---
def draw_score_box(surface, score):
    box_w, box_h = 220, 60
    box_x, box_y = 10, 10
    # Fondo translúcido
    s = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 0, 0, 180), (0, 0, box_w, box_h), border_radius=18)
    pygame.draw.rect(s, NEON_YELLOW, (0, 0, box_w, box_h), 4, border_radius=18)
    surface.blit(s, (box_x, box_y))
    # Texto
    score_text = font.render("Puntuación: " + str(score // 10), True, NEON_YELLOW)
    surface.blit(score_text, (box_x + 18, box_y + 12))

# --- Modificar main para integrar todo ---
def main():
    player = Player()
    obstacles = [Obstacle() for _ in range(7)]
    score = 0
    running = True
    t = 0
    last_lap = 0

    while running:
        clock.tick(FPS)
        t += 0.03
        screen.fill(BLACK)
        draw_vortex(screen, t)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player.alive:
            player.update(keys)
            player.draw(screen)
            # Cambiar posición de obstáculos cada 2 vueltas
            if player.lap_count // 2 > last_lap:
                for obs in obstacles:
                    obs.reposition()
                last_lap = player.lap_count // 2
            for obs in obstacles:
                obs.update()
                obs.draw(screen)
                if obs.collide(player):
                    player.alive = False
            score += 1
        else:
            msg = font.render("¡Game Over! Puntuación: " + str(score // 10), True, NEON_PINK)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
            msg2 = font.render("Presiona R para reiniciar", True, NEON_GREEN)
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 10))
            if keys[pygame.K_r]:
                player = Player()
                obstacles = [Obstacle() for _ in range(7)]
                score = 0
                last_lap = 0

        draw_score_box(screen, score)
        pygame.display.flip()

    pygame.quit()