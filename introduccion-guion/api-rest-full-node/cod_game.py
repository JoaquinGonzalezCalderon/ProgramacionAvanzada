import pygame
import math
import random
import sys

# Inicializar Pygame
pygame.init()

# Constantes del juego
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 5
        self.angle = 0
        self.max_health = 100
        self.health = self.max_health
        self.ammo = 30
        self.max_ammo = 30
        self.reload_time = 0
        self.shoot_cooldown = 0
        self.score = 0
        
    def move(self, keys):
        # Movimiento con WASD
        dx = 0
        dy = 0
        
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed
            
        # Actualizar posición
        self.x += dx
        self.y += dy
        
        # Mantener dentro de la pantalla
        self.x = max(self.width//2, min(SCREEN_WIDTH - self.width//2, self.x))
        self.y = max(self.height//2, min(SCREEN_HEIGHT - self.height//2, self.y))
    
    def rotate_to_mouse(self, mouse_pos):
        # Calcular ángulo hacia el mouse
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.atan2(dy, dx)
    
    def shoot(self, bullets):
        if self.shoot_cooldown <= 0 and self.ammo > 0:
            # Crear bala en la dirección del jugador
            bullet_x = self.x + math.cos(self.angle) * 25
            bullet_y = self.y + math.sin(self.angle) * 25
            bullets.append(Bullet(bullet_x, bullet_y, self.angle, "player"))
            
            self.ammo -= 1
            self.shoot_cooldown = 10  # Cooldown entre disparos
            return True
        return False
    
    def reload(self):
        if self.ammo < self.max_ammo and self.reload_time <= 0:
            self.reload_time = 60  # 1 segundo a 60 FPS
            
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if self.reload_time > 0:
            self.reload_time -= 1
            if self.reload_time == 0:
                self.ammo = self.max_ammo
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True  # Player died
        return False
    
    def draw(self, screen):
        # Dibujar cuerpo del jugador
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.width//2)
        
        # Dibujar dirección (línea hacia donde apunta)
        end_x = self.x + math.cos(self.angle) * 30
        end_y = self.y + math.sin(self.angle) * 30
        pygame.draw.line(screen, WHITE, (self.x, self.y), (end_x, end_y), 3)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 18
        self.height = 18
        self.speed = 2
        self.angle = 0
        self.health = 50
        self.max_health = 50
        self.shoot_timer = 0
        self.shoot_interval = 90  # Dispara cada 1.5 segundos
        self.detection_range = 300
        
    def update(self, player, bullets):
        # Calcular distancia al jugador
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.detection_range:
            # Mover hacia el jugador
            if distance > 100:  # Mantener cierta distancia
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            
            # Apuntar al jugador
            self.angle = math.atan2(dy, dx)
            
            # Disparar al jugador
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval:
                bullet_x = self.x + math.cos(self.angle) * 20
                bullet_y = self.y + math.sin(self.angle) * 20
                bullets.append(Bullet(bullet_x, bullet_y, self.angle, "enemy"))
                self.shoot_timer = 0
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen):
        # Dibujar enemigo
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.width//2)
        
        # Dibujar barra de vida
        bar_width = 30
        bar_height = 4
        bar_x = self.x - bar_width // 2
        bar_y = self.y - 20
        
        # Fondo de la barra
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Vida actual
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Bullet:
    def __init__(self, x, y, angle, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.owner = owner
        self.damage = 25
        self.radius = 3
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Verificar si está fuera de la pantalla
        if (self.x < 0 or self.x > SCREEN_WIDTH or 
            self.y < 0 or self.y > SCREEN_HEIGHT):
            return True  # Eliminar bala
        return False
    
    def check_collision(self, target_x, target_y, target_radius):
        distance = math.sqrt((self.x - target_x)**2 + (self.y - target_y)**2)
        return distance < (self.radius + target_radius)
    
    def draw(self, screen):
        color = YELLOW if self.owner == "player" else ORANGE
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Call of Duty Python")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Estados del juego
        self.game_state = "menu"  # menu, playing, game_over
        self.wave = 1
        self.enemies_per_wave = 3
        
        self.reset_game()
        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bullets = []
        self.enemies = []
        self.wave = 1
        self.enemies_per_wave = 3
        self.spawn_enemies()
        
    def spawn_enemies(self):
        for _ in range(self.enemies_per_wave):
            # Spawn enemigos en los bordes de la pantalla
            side = random.randint(0, 3)
            if side == 0:  # Arriba
                x = random.randint(0, SCREEN_WIDTH)
                y = 0
            elif side == 1:  # Derecha
                x = SCREEN_WIDTH
                y = random.randint(0, SCREEN_HEIGHT)
            elif side == 2:  # Abajo
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT
            else:  # Izquierda
                x = 0
                y = random.randint(0, SCREEN_HEIGHT)
                
            self.enemies.append(Enemy(x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "playing"
                elif self.game_state == "playing":
                    if event.key == pygame.K_r:
                        self.player.reload()
                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.game_state = "playing"
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "playing" and event.button == 1:  # Click izquierdo
                    if self.player.shoot(self.bullets):
                        pass  # Aquí podrías agregar sonido de disparo
                        
        return True
    
    def update(self):
        if self.game_state != "playing":
            return
            
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        # Actualizar jugador
        self.player.move(keys)
        self.player.rotate_to_mouse(mouse_pos)
        self.player.update()
        
        # Actualizar enemigos
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.bullets)
        
        # Actualizar balas
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
                continue
                
            # Verificar colisiones
            if bullet.owner == "player":
                # Balas del jugador vs enemigos
                for enemy in self.enemies[:]:
                    if bullet.check_collision(enemy.x, enemy.y, enemy.width//2):
                        if enemy.take_damage(bullet.damage):
                            self.enemies.remove(enemy)
                            self.player.score += 100
                        self.bullets.remove(bullet)
                        break
            else:
                # Balas enemigas vs jugador
                if bullet.check_collision(self.player.x, self.player.y, self.player.width//2):
                    if self.player.take_damage(bullet.damage):
                        self.game_state = "game_over"
                    self.bullets.remove(bullet)
        
        # Verificar si todos los enemigos han sido eliminados
        if not self.enemies:
            self.wave += 1
            self.enemies_per_wave += 2
            self.spawn_enemies()
            # Dar munición extra al jugador
            self.player.ammo = self.player.max_ammo
    
    def draw(self):
        self.screen.fill(DARK_GREEN)
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
            
        pygame.display.flip()
    
    def draw_menu(self):
        title_text = self.font.render("CALL OF DUTY PYTHON", True, WHITE)
        start_text = self.small_font.render("Presiona ESPACIO para empezar", True, WHITE)
        controls_text1 = self.small_font.render("Controles: WASD para moverse", True, WHITE)
        controls_text2 = self.small_font.render("Mouse para apuntar, Click izquierdo para disparar", True, WHITE)
        controls_text3 = self.small_font.render("R para recargar", True, WHITE)
        
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 200))
        self.screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 300))
        self.screen.blit(controls_text1, (SCREEN_WIDTH//2 - controls_text1.get_width()//2, 400))
        self.screen.blit(controls_text2, (SCREEN_WIDTH//2 - controls_text2.get_width()//2, 430))
        self.screen.blit(controls_text3, (SCREEN_WIDTH//2 - controls_text3.get_width()//2, 460))
    
    def draw_game(self):
        # Dibujar jugador
        self.player.draw(self.screen)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Dibujar balas
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Dibujar HUD
        self.draw_hud()
    
    def draw_hud(self):
        # Barra de vida
        health_text = self.small_font.render(f"Vida: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # Barra de vida visual
        bar_width = 200
        bar_height = 20
        health_ratio = self.player.health / self.player.max_health
        
        pygame.draw.rect(self.screen, RED, (10, 35, bar_width, bar_height))
        pygame.draw.rect(self.screen, GREEN, (10, 35, bar_width * health_ratio, bar_height))
        
        # Munición
        ammo_text = self.small_font.render(f"Munición: {self.player.ammo}/{self.player.max_ammo}", True, WHITE)
        self.screen.blit(ammo_text, (10, 70))
        
        if self.player.reload_time > 0:
            reload_text = self.small_font.render("RECARGANDO...", True, YELLOW)
            self.screen.blit(reload_text, (10, 95))
        
        # Puntuación y oleada
        score_text = self.small_font.render(f"Puntuación: {self.player.score}", True, WHITE)
        wave_text = self.small_font.render(f"Oleada: {self.wave}", True, WHITE)
        enemies_text = self.small_font.render(f"Enemigos: {len(self.enemies)}", True, WHITE)
        
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 10))
        self.screen.blit(wave_text, (SCREEN_WIDTH - 200, 35))
        self.screen.blit(enemies_text, (SCREEN_WIDTH - 200, 60))
    
    def draw_game_over(self):
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto de game over
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.small_font.render(f"Puntuación Final: {self.player.score}", True, WHITE)
        wave_text = self.small_font.render(f"Llegaste hasta la oleada: {self.wave}", True, WHITE)
        restart_text = self.small_font.render("Presiona ESPACIO para jugar de nuevo", True, WHITE)
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 300))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 350))
        self.screen.blit(wave_text, (SCREEN_WIDTH//2 - wave_text.get_width()//2, 380))
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 430))
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    game = Game()
    game.run()
