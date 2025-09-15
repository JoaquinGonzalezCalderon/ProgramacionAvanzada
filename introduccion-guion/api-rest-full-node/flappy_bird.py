import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Constantes del juego
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Configuración del juego
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_FREQUENCY = 90  # frames entre tubos

class Bird:
    def __init__(self):
        self.x = 50
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.radius = 20
        
    def update(self):
        # Aplicar gravedad
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def draw(self, screen):
        # Dibujar el pájaro como un círculo amarillo
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        # Añadir un ojo
        pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y - 5)), 3)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, WINDOW_HEIGHT - PIPE_GAP - 100)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        # Tubo superior
        pygame.draw.rect(screen, GREEN, 
                        (self.x, 0, PIPE_WIDTH, self.height))
        # Tubo inferior
        pygame.draw.rect(screen, GREEN, 
                        (self.x, self.height + PIPE_GAP, PIPE_WIDTH, 
                         WINDOW_HEIGHT - self.height - PIPE_GAP))
        
        # Bordes de los tubos
        pygame.draw.rect(screen, BLACK, 
                        (self.x, 0, PIPE_WIDTH, self.height), 3)
        pygame.draw.rect(screen, BLACK, 
                        (self.x, self.height + PIPE_GAP, PIPE_WIDTH, 
                         WINDOW_HEIGHT - self.height - PIPE_GAP), 3)
        
    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        
        # Rectángulos de los tubos
        upper_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        lower_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, 
                               WINDOW_HEIGHT - self.height - PIPE_GAP)
        
        return bird_rect.colliderect(upper_pipe) or bird_rect.colliderect(lower_pipe)
        
    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        
        self.reset_game()
        
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over:
                        self.bird.jump()
                    else:
                        self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
        
    def update(self):
        if self.game_over:
            return
            
        self.frame_count += 1
        
        # Actualizar pájaro
        self.bird.update()
        
        # Verificar si el pájaro toca el suelo o el techo
        if self.bird.y + self.bird.radius >= WINDOW_HEIGHT or self.bird.y - self.bird.radius <= 0:
            self.game_over = True
            
        # Generar nuevos tubos
        if self.frame_count % PIPE_FREQUENCY == 0:
            self.pipes.append(Pipe(WINDOW_WIDTH))
            
        # Actualizar tubos
        for pipe in self.pipes[:]:
            pipe.update()
            
            # Verificar colisiones
            if pipe.collides_with(self.bird):
                self.game_over = True
                
            # Contar puntos
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
                
            # Remover tubos que salieron de pantalla
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
                
    def draw(self):
        # Fondo degradado (cielo)
        for y in range(WINDOW_HEIGHT):
            color_value = int(135 + (120 * y / WINDOW_HEIGHT))
            if color_value > 255:
                color_value = 255
            pygame.draw.line(self.screen, (color_value, min(255, color_value + 20), 255), 
                           (0, y), (WINDOW_WIDTH, y))
        
        # Dibujar tubos
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        # Dibujar pájaro
        self.bird.draw(self.screen)
        
        # Dibujar puntuación
        score_text = self.font.render(f"Puntuación: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)
        # Sombra del texto
        shadow_text = self.font.render(f"Puntuación: {self.score}", True, BLACK)
        shadow_rect = shadow_text.get_rect()
        shadow_rect.topleft = (12, 12)
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(score_text, score_rect)
        
        # Pantalla de game over
        if self.game_over:
            # Superficie semi-transparente
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Texto de game over
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            # Puntuación final
            final_score_text = self.font.render(f"Puntuación Final: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(final_score_text, final_score_rect)
            
            # Instrucciones para reiniciar
            restart_text = self.font.render("Presiona ESPACIO para reiniciar", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
            quit_text = self.font.render("Presiona ESC para salir", True, WHITE)
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
            self.screen.blit(quit_text, quit_rect)
        else:
            # Instrucciones de juego
            if self.frame_count < 180:  # Mostrar por 3 segundos
                instruction_text = self.font.render("Presiona ESPACIO para saltar", True, WHITE)
                instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100))
                # Sombra
                shadow_instruction = self.font.render("Presiona ESPACIO para saltar", True, BLACK)
                shadow_instruction_rect = shadow_instruction.get_rect(center=(WINDOW_WIDTH//2 + 2, WINDOW_HEIGHT//2 + 102))
                self.screen.blit(shadow_instruction, shadow_instruction_rect)
                self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
            
        pygame.quit()

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
