import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Constantes
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
MARRON = (139, 69, 19)
AMARILLO = (255, 255, 0)
CELESTE = (135, 206, 235)

# Configuración del juego
GRAVEDAD = 0.8
VELOCIDAD_SALTO = -15
VELOCIDAD_MARIO = 5

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO_PANTALLA - 200
        
        # Propiedades de movimiento
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.en_suelo = False
        self.direccion = 1  # 1 derecha, -1 izquierda
        
        # Propiedades del juego
        self.puntos = 0
        self.vidas = 3
    
    def update(self):
        # Aplicar gravedad
        if not self.en_suelo:
            self.velocidad_y += GRAVEDAD
        
        # Actualizar posición
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Límites de pantalla horizontales
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA
        
        # Límite inferior (muerte)
        if self.rect.bottom > ALTO_PANTALLA:
            self.morir()
    
    def saltar(self):
        if self.en_suelo:
            self.velocidad_y = VELOCIDAD_SALTO
            self.en_suelo = False
    
    def mover_izquierda(self):
        self.velocidad_x = -VELOCIDAD_MARIO
        self.direccion = -1
    
    def mover_derecha(self):
        self.velocidad_x = VELOCIDAD_MARIO
        self.direccion = 1
    
    def parar(self):
        self.velocidad_x = 0
    
    def morir(self):
        self.vidas -= 1
        if self.vidas > 0:
            # Reiniciar posición
            self.rect.x = 100
            self.rect.y = ALTO_PANTALLA - 200
            self.velocidad_x = 0
            self.velocidad_y = 0
        
    def dibujar_info(self, pantalla, fuente):
        texto_puntos = fuente.render(f"Puntos: {self.puntos}", True, BLANCO)
        texto_vidas = fuente.render(f"Vidas: {self.vidas}", True, BLANCO)
        pantalla.blit(texto_puntos, (10, 10))
        pantalla.blit(texto_vidas, (10, 40))

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(MARRON)
        self.rect = pygame.Rect(x, y, ancho, alto)

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(MARRON)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.velocidad_x = -2
        self.direccion = -1
    
    def update(self):
        # Mover el Goomba
        self.rect.x += self.velocidad_x
        
        # Si sale de la pantalla, eliminarlo
        if self.rect.right < 0:
            self.kill()

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animación simple
        self.contador_animacion = 0
    
    def update(self):
        # Animación de rotación simple
        self.contador_animacion += 1
        if self.contador_animacion > 30:
            self.contador_animacion = 0

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Mario Bros - Python")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 36)
        
        # Grupos de sprites
        self.todos_sprites = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.monedas = pygame.sprite.Group()
        
        # Crear Mario
        self.mario = Mario()
        self.todos_sprites.add(self.mario)
        
        # Crear nivel inicial
        self.crear_nivel()
        
        # Estado del juego
        self.game_over = False
        self.pausa = False
        
        # Contador para generar enemigos
        self.contador_enemigos = 0
        self.contador_monedas = 0
    
    def crear_nivel(self):
        # Plataforma del suelo principal
        plataforma_suelo = Plataforma(0, ALTO_PANTALLA - 50, ANCHO_PANTALLA, 50)
        self.plataformas.add(plataforma_suelo)
        self.todos_sprites.add(plataforma_suelo)
        
        # Plataformas flotantes
        plataformas_info = [
            (300, 450, 200, 20),
            (600, 350, 150, 20),
            (900, 250, 200, 20),
            (200, 300, 150, 20),
            (800, 150, 180, 20),
        ]
        
        for x, y, ancho, alto in plataformas_info:
            plataforma = Plataforma(x, y, ancho, alto)
            self.plataformas.add(plataforma)
            self.todos_sprites.add(plataforma)
        
        # Monedas iniciales
        posiciones_monedas = [
            (350, 400), (400, 400), (650, 300),
            (950, 200), (250, 250), (850, 100),
            (500, 500), (700, 500)
        ]
        
        for x, y in posiciones_monedas:
            moneda = Moneda(x, y)
            self.monedas.add(moneda)
            self.todos_sprites.add(moneda)
    
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.mario.saltar()
                elif evento.key == pygame.K_p:
                    self.pausa = not self.pausa
                elif evento.key == pygame.K_r and self.game_over:
                    self.reiniciar_juego()
        
        return True
    
    def manejar_input_continuo(self):
        if self.game_over or self.pausa:
            return
            
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.mario.mover_izquierda()
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.mario.mover_derecha()
        else:
            self.mario.parar()
    
    def detectar_colisiones(self):
        # Colisiones con plataformas
        self.mario.en_suelo = False
        colisiones_plataforma = pygame.sprite.spritecollide(self.mario, self.plataformas, False)
        
        for plataforma in colisiones_plataforma:
            # Colisión desde arriba (Mario cae sobre la plataforma)
            if self.mario.velocidad_y > 0 and self.mario.rect.bottom <= plataforma.rect.top + 10:
                self.mario.rect.bottom = plataforma.rect.top
                self.mario.velocidad_y = 0
                self.mario.en_suelo = True
            # Colisión desde abajo (Mario golpea la plataforma)
            elif self.mario.velocidad_y < 0 and self.mario.rect.top >= plataforma.rect.bottom - 10:
                self.mario.rect.top = plataforma.rect.bottom
                self.mario.velocidad_y = 0
        
        # Colisiones con monedas
        monedas_recogidas = pygame.sprite.spritecollide(self.mario, self.monedas, True)
        for moneda in monedas_recogidas:
            self.mario.puntos += 100
        
        # Colisiones con enemigos
        enemigos_tocados = pygame.sprite.spritecollide(self.mario, self.enemigos, False)
        for enemigo in enemigos_tocados:
            # Si Mario salta sobre el enemigo
            if self.mario.velocidad_y > 0 and self.mario.rect.bottom <= enemigo.rect.top + 15:
                enemigo.kill()
                self.mario.puntos += 200
                self.mario.saltar()  # Pequeño rebote
            else:
                # Mario muere
                self.mario.morir()
                if self.mario.vidas <= 0:
                    self.game_over = True
    
    def generar_contenido_dinamico(self):
        if self.game_over or self.pausa:
            return
            
        # Generar enemigos
        self.contador_enemigos += 1
        if self.contador_enemigos > 180:  # Cada 3 segundos aprox
            if random.randint(1, 10) > 7:  # 30% probabilidad
                nuevo_enemigo = Goomba(ANCHO_PANTALLA, ALTO_PANTALLA - 80)
                self.enemigos.add(nuevo_enemigo)
                self.todos_sprites.add(nuevo_enemigo)
            self.contador_enemigos = 0
        
        # Generar monedas ocasionalmente
        self.contador_monedas += 1
        if self.contador_monedas > 300:  # Cada 5 segundos aprox
            if random.randint(1, 10) > 8:  # 20% probabilidad
                x = random.randint(100, ANCHO_PANTALLA - 100)
                y = random.randint(100, ALTO_PANTALLA - 200)
                nueva_moneda = Moneda(x, y)
                self.monedas.add(nueva_moneda)
                self.todos_sprites.add(nueva_moneda)
            self.contador_monedas = 0
    
    def update(self):
        if not self.game_over and not self.pausa:
            self.todos_sprites.update()
            self.detectar_colisiones()
            self.generar_contenido_dinamico()
    
    def dibujar(self):
        # Fondo
        self.pantalla.fill(CELESTE)
        
        # Dibujar todos los sprites
        self.todos_sprites.draw(self.pantalla)
        
        # Información del jugador
        self.mario.dibujar_info(self.pantalla, self.fuente)
        
        # Mensajes de estado
        if self.pausa:
            texto_pausa = self.fuente.render("PAUSA - Presiona P para continuar", True, BLANCO)
            rect_texto = texto_pausa.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2))
            self.pantalla.blit(texto_pausa, rect_texto)
        
        if self.game_over:
            texto_game_over = self.fuente.render("GAME OVER - Presiona R para reiniciar", True, ROJO)
            rect_texto = texto_game_over.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2))
            self.pantalla.blit(texto_game_over, rect_texto)
        
        # Controles
        texto_controles = pygame.font.Font(None, 24).render("Controles: Flechas/WASD = Mover, Espacio = Saltar, P = Pausa", True, BLANCO)
        self.pantalla.blit(texto_controles, (10, ALTO_PANTALLA - 30))
        
        pygame.display.flip()
    
    def reiniciar_juego(self):
        # Limpiar todos los sprites
        self.todos_sprites.empty()
        self.plataformas.empty()
        self.enemigos.empty()
        self.monedas.empty()
        
        # Recrear Mario
        self.mario = Mario()
        self.todos_sprites.add(self.mario)
        
        # Recrear nivel
        self.crear_nivel()
        
        # Resetear estado
        self.game_over = False
        self.pausa = False
        self.contador_enemigos = 0
        self.contador_monedas = 0
    
    def ejecutar(self):
        print("¡Iniciando Mario Bros!")
        print("Controles:")
        print("- Flechas o WASD: Mover")
        print("- Espacio: Saltar")
        print("- P: Pausa")
        print("- R: Reiniciar (cuando sea Game Over)")
        print("\n¡Diviértete!")
        
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.manejar_input_continuo()
            self.update()
            self.dibujar()
            self.reloj.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
