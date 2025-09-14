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
BROWN = (139, 69, 19)
DARK_GRAY = (64, 64, 64)

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

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
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        
    def move(self, keys, walls):
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
            
        # Calcular nueva posición
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Verificar colisión con paredes
        new_rect = pygame.Rect(new_x - self.width//2, new_y - self.height//2, self.width, self.height)
        
        collision_x = False
        collision_y = False
        
        # Verificar colisión horizontal
        temp_rect = pygame.Rect(new_x - self.width//2, self.y - self.height//2, self.width, self.height)
        for wall in walls:
            if temp_rect.colliderect(wall.rect):
                collision_x = True
                break
        
        # Verificar colisión vertical
        temp_rect = pygame.Rect(self.x - self.width//2, new_y - self.height//2, self.width, self.height)
        for wall in walls:
            if temp_rect.colliderect(wall.rect):
                collision_y = True
                break
        
        # Aplicar movimiento si no hay colisión
        if not collision_x:
            self.x = new_x
        if not collision_y:
            self.y = new_y
            
        # Mantener dentro de la pantalla
        self.x = max(self.width//2, min(SCREEN_WIDTH - self.width//2, self.x))
        self.y = max(self.height//2, min(SCREEN_HEIGHT - self.height//2, self.y))
        
        # Actualizar rect
        self.rect.center = (self.x, self.y)
    
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
        self.speed = 1.5
        self.angle = 0
        self.health = 50
        self.max_health = 50
        self.shoot_timer = 0
        self.shoot_interval = 120  # Dispara cada 2 segundos
        self.detection_range = 350
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        self.last_seen_player_pos = None
        self.patrol_target = None
        self.stuck_counter = 0
        self.last_x, self.last_y = x, y
        
    def has_line_of_sight(self, player, walls):
        # Verificar línea de vista usando raycast simple
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > self.detection_range:
            return False
            
        # Comprobar si hay paredes en el camino
        steps = int(distance)
        if steps == 0:
            return True
            
        step_x = dx / steps
        step_y = dy / steps
        
        for i in range(steps):
            check_x = self.x + step_x * i
            check_y = self.y + step_y * i
            check_point = pygame.Rect(check_x-2, check_y-2, 4, 4)
            
            for wall in walls:
                if check_point.colliderect(wall.rect):
                    return False
        
        return True
    
    def move_towards_target(self, target_x, target_y, walls):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:  # Solo moverse si no está muy cerca
            # Normalizar dirección
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            
            # Verificar colisión
            new_x = self.x + move_x
            new_y = self.y + move_y
            new_rect = pygame.Rect(new_x - self.width//2, new_y - self.height//2, self.width, self.height)
            
            can_move = True
            for wall in walls:
                if new_rect.colliderect(wall.rect):
                    can_move = False
                    break
            
            if can_move:
                self.x = new_x
                self.y = new_y
                self.stuck_counter = 0
            else:
                self.stuck_counter += 1
                # Si está atascado, intentar rodear el obstáculo
                if self.stuck_counter > 30:
                    self.x += random.randint(-20, 20)
                    self.y += random.randint(-20, 20)
                    self.stuck_counter = 0
        
        self.rect.center = (self.x, self.y)
        
    def update(self, player, bullets, walls):
        # Verificar línea de vista
        has_sight = self.has_line_of_sight(player, walls)
        
        if has_sight:
            self.last_seen_player_pos = (player.x, player.y)
            
            # Mover hacia el jugador pero mantener distancia
            distance_to_player = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
            if distance_to_player > 150:  # Acercarse si está lejos
                self.move_towards_target(player.x, player.y, walls)
            elif distance_to_player < 100:  # Alejarse si está muy cerca
                self.move_towards_target(self.x - (player.x - self.x), self.y - (player.y - self.y), walls)
            
            # Apuntar al jugador
            dx = player.x - self.x
            dy = player.y - self.y
            self.angle = math.atan2(dy, dx)
            
            # Disparar al jugador
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval:
                bullet_x = self.x + math.cos(self.angle) * 20
                bullet_y = self.y + math.sin(self.angle) * 20
                bullets.append(Bullet(bullet_x, bullet_y, self.angle, "enemy"))
                self.shoot_timer = 0
        else:
            # Si no puede ver al jugador, ir a la última posición conocida
            if self.last_seen_player_pos:
                self.move_towards_target(self.last_seen_player_pos[0], self.last_seen_player_pos[1], walls)
                
                # Si llegó a la posición, olvidar al jugador
                dist_to_last_pos = math.sqrt((self.x - self.last_seen_player_pos[0])**2 + 
                                           (self.y - self.last_seen_player_pos[1])**2)
                if dist_to_last_pos < 20:
                    self.last_seen_player_pos = None
    
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
        self.speed = 12
        self.owner = owner
        self.damage = 25
        self.radius = 3
        
    def update(self, walls):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Verificar colisión con paredes
        bullet_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                 self.radius * 2, self.radius * 2)
        
        for wall in walls:
            if bullet_rect.colliderect(wall.rect):
                return True  # Eliminar bala
        
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
        pygame.display.set_caption("Call of Duty Python - Advanced")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Estados del juego
        self.game_state = "menu"  # menu, playing, game_over
        self.wave = 1
        self.enemies_per_wave = 3
        
        # Crear mapa con obstáculos
        self.walls = self.create_map()
        
        self.reset_game()
        
    def create_map(self):
        walls = []
        
        # Paredes del borde (invisibles, para contener el juego)
        walls.append(Wall(-10, -10, SCREEN_WIDTH + 20, 10))  # Arriba
        walls.append(Wall(-10, SCREEN_HEIGHT, SCREEN_WIDTH + 20, 10))  # Abajo
        walls.append(Wall(-10, -10, 10, SCREEN_HEIGHT + 20))  # Izquierda
        walls.append(Wall(SCREEN_WIDTH, -10, 10, SCREEN_HEIGHT + 20))  # Derecha
        
        # Obstáculos en el mapa
        walls.append(Wall(200, 150, 100, 50))   # Bloque horizontal
        walls.append(Wall(500, 100, 50, 200))   # Bloque vertical
        walls.append(Wall(800, 300, 150, 30))   # Pared larga
        walls.append(Wall(300, 400, 80, 80))    # Bloque cuadrado
        walls.append(Wall(700, 500, 120, 40))   # Cobertura
        walls.append(Wall(100, 600, 40, 100))   # Pilar
        walls.append(Wall(900, 200, 60, 150))   # Torre
        walls.append(Wall(400, 650, 200, 30))   # Barrera inferior
        walls.append(Wall(50, 50, 30, 30))      # Pequeño obstáculo
        walls.append(Wall(1000, 600, 80, 80))   # Bunker
        
        return walls
        
    def reset_game(self):
        self.player = Player(100, 100)  # Spawn en esquina segura
        self.bullets = []
        self.enemies = []
        self.wave = 1
        self.enemies_per_wave = 3
        self.spawn_enemies()
        
    def spawn_enemies(self):
        spawn_attempts = 0
        enemies_spawned = 0
        
        while enemies_spawned < self.enemies_per_wave and spawn_attempts < 100:
            # Spawn enemigos en posiciones aleatorias pero seguras
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            
            # Verificar que no spawne dentro de una pared
            enemy_rect = pygame.Rect(x - 9, y - 9, 18, 18)
            can_spawn = True
            
            for wall in self.walls:
                if enemy_rect.colliderect(wall.rect):
                    can_spawn = False
                    break
            
            # Verificar que no spawne muy cerca del jugador
            distance_to_player = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
            if distance_to_player < 200:
                can_spawn = False
            
            if can_spawn:
                self.enemies.append(Enemy(x, y))
                enemies_spawned += 1
            
            spawn_attempts += 1
    
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
        self.player.move(keys, self.walls)
        self.player.rotate_to_mouse(mouse_pos)
        self.player.update()
        
        # Actualizar enemigos
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.bullets, self.walls)
        
        # Actualizar balas
        for bullet in self.bullets[:]:
            if bullet.update(self.walls):
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
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
            else:
                # Balas enemigas vs jugador
                if bullet.check_collision(self.player.x, self.player.y, self.player.width//2):
                    if self.player.take_damage(bullet.damage):
                        self.game_state = "game_over"
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
        
        # Verificar si todos los enemigos han sido eliminados
        if not self.enemies:
            self.wave += 1
            self.enemies_per_wave += 1
            self.spawn_enemies()
            # Dar munición extra al jugador
            self.player.ammo = self.player.max_ammo
    
    def draw(self):
        self.screen.fill(DARK_GREEN)
        
        # Dibujar paredes
        for wall in self.walls[4:]:  # Omitir paredes del borde
            wall.draw(self.screen)
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
            
        pygame.display.flip()
    
    def draw_menu(self):
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        title_text = self.font.render("CALL OF DUTY PYTHON - ADVANCED", True, WHITE)
        start_text = self.small_font.render("Presiona ESPACIO para empezar", True, WHITE)
        controls_text1 = self.small_font.render("Controles: WASD para moverse", True, WHITE)
        controls_text2 = self.small_font.render("Mouse para apuntar, Click izquierdo para disparar", True, WHITE)
        controls_text3 = self.small_font.render("R para recargar", True, WHITE)
        features_text1 = self.small_font.render("• IA mejorada con línea de vista", True, GREEN)
        features_text2 = self.small_font.render("• Mapas con obstáculos y cobertura", True, GREEN)
        features_text3 = self.small_font.render("• Física de balas realista", True, GREEN)
        
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 150))
        self.screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 250))
        self.screen.blit(controls_text1, (SCREEN_WIDTH//2 - controls_text1.get_width()//2, 320))
        self.screen.blit(controls_text2, (SCREEN_WIDTH//2 - controls_text2.get_width()//2, 350))
        self.screen.blit(controls_text3, (SCREEN_WIDTH//2 - controls_text3.get_width()//2, 380))
        self.screen.blit(features_text1, (SCREEN_WIDTH//2 - features_text1.get_width()//2, 450))
        self.screen.blit(features_text2, (SCREEN_WIDTH//2 - features_text2.get_width()//2, 480))
        self.screen.blit(features_text3, (SCREEN_WIDTH//2 - features_text3.get_width()//2, 510))
    
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
        health_ratio = max(0, self.player.health / self.player.max_health)
        
        pygame.draw.rect(self.screen, RED, (10, 35, bar_width, bar_height))
        pygame.draw.rect(self.screen, GREEN, (10, 35, bar_width * health_ratio, bar_height))
        
        # Munición
        ammo_color = WHITE if self.player.ammo > 5 else RED
        ammo_text = self.small_font.render(f"Munición: {self.player.ammo}/{self.player.max_ammo}", True, ammo_color)
        self.screen.blit(ammo_text, (10, 70))
        
        if self.player.reload_time > 0:
            reload_progress = (60 - self.player.reload_time) / 60
            reload_text = self.small_font.render(f"RECARGANDO... {int(reload_progress * 100)}%", True, YELLOW)
            self.screen.blit(reload_text, (10, 95))
        
        # Puntuación y oleada
        score_text = self.small_font.render(f"Puntuación: {self.player.score}", True, WHITE)
        wave_text = self.small_font.render(f"Oleada: {self.wave}", True, WHITE)
        enemies_text = self.small_font.render(f"Enemigos: {len(self.enemies)}", True, WHITE)
        
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 10))
        self.screen.blit(wave_text, (SCREEN_WIDTH - 200, 35))
        self.screen.blit(enemies_text, (SCREEN_WIDTH - 200, 60))
        
        # Mini mapa (opcional)
        minimap_size = 150
        minimap_x = SCREEN_WIDTH - minimap_size - 10
        minimap_y = SCREEN_HEIGHT - minimap_size - 10
        
        # Fondo del minimapa
        pygame.draw.rect(self.screen, BLACK, (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(self.screen, WHITE, (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Jugador en minimapa
        player_mini_x = minimap_x + (self.player.x / SCREEN_WIDTH) * minimap_size
        player_mini_y = minimap_y + (self.player.y / SCREEN_HEIGHT) * minimap_size
        pygame.draw.circle(self.screen, BLUE, (int(player_mini_x), int(player_mini_y)), 3)
        
        # Enemigos en minimapa
        for enemy in self.enemies:
            enemy_mini_x = minimap_x + (enemy.x / SCREEN_WIDTH) * minimap_size
            enemy_mini_y = minimap_y + (enemy.y / SCREEN_HEIGHT) * minimap_size
            pygame.draw.circle(self.screen, RED, (int(enemy_mini_x), int(enemy_mini_y)), 2)
    
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
