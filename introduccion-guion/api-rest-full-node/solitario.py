import pygame
import random
import sys
from enum import Enum

# Inicializar pygame
pygame.init()

# Constantes
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 800
FPS = 60

# Colores
VERDE_MESA = (0, 100, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
AZUL = (0, 0, 200)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)
AMARILLO = (255, 255, 0)

# Dimensiones de cartas
ANCHO_CARTA = 80
ALTO_CARTA = 110
MARGEN = 10

class Palo(Enum):
    CORAZONES = "♥"
    DIAMANTES = "♦"
    TREBOLES = "♣"
    ESPADAS = "♠"

class Color(Enum):
    ROJO = 1
    NEGRO = 2

class Carta:
    def __init__(self, valor, palo):
        self.valor = valor  # 1-13 (A, 2-10, J, Q, K)
        self.palo = palo
        self.boca_arriba = False
        self.rect = pygame.Rect(0, 0, ANCHO_CARTA, ALTO_CARTA)
        self.siendo_arrastrada = False
        
    @property
    def color(self):
        return Color.ROJO if self.palo in [Palo.CORAZONES, Palo.DIAMANTES] else Color.NEGRO
    
    @property
    def nombre_valor(self):
        if self.valor == 1:
            return "A"
        elif self.valor <= 10:
            return str(self.valor)
        elif self.valor == 11:
            return "J"
        elif self.valor == 12:
            return "Q"
        elif self.valor == 13:
            return "K"
    
    def puede_ir_sobre(self, otra_carta):
        """Verifica si esta carta puede ir sobre otra en el tableau"""
        if otra_carta is None:
            return self.valor == 13  # Solo reyes pueden ir en espacios vacíos
        return (self.color != otra_carta.color and 
                self.valor == otra_carta.valor - 1)
    
    def puede_ir_a_foundation(self, pila_foundation):
        """Verifica si esta carta puede ir a una pila foundation"""
        if not pila_foundation:
            return self.valor == 1  # Solo ases pueden ir en foundations vacías
        carta_superior = pila_foundation[-1]
        return (self.palo == carta_superior.palo and 
                self.valor == carta_superior.valor + 1)
    
    def dibujar(self, pantalla, x, y):
        self.rect.x = x
        self.rect.y = y
        
        if self.boca_arriba:
            # Dibujar carta boca arriba
            pygame.draw.rect(pantalla, BLANCO, self.rect)
            pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
            
            # Dibujar valor y palo
            fuente = pygame.font.Font(None, 24)
            color_texto = ROJO if self.color == Color.ROJO else NEGRO
            
            # Valor en la esquina superior izquierda
            texto_valor = fuente.render(self.nombre_valor, True, color_texto)
            pantalla.blit(texto_valor, (x + 5, y + 5))
            
            # Palo en la esquina superior izquierda (debajo del valor)
            fuente_palo = pygame.font.Font(None, 20)
            texto_palo = fuente_palo.render(self.palo.value, True, color_texto)
            pantalla.blit(texto_palo, (x + 5, y + 25))
            
            # Palo grande en el centro
            fuente_centro = pygame.font.Font(None, 48)
            texto_centro = fuente_centro.render(self.palo.value, True, color_texto)
            rect_centro = texto_centro.get_rect(center=(x + ANCHO_CARTA//2, y + ALTO_CARTA//2))
            pantalla.blit(texto_centro, rect_centro)
            
        else:
            # Dibujar carta boca abajo
            pygame.draw.rect(pantalla, AZUL, self.rect)
            pygame.draw.rect(pantalla, BLANCO, self.rect, 2)
            
            # Patrón en el dorso
            for i in range(5):
                for j in range(7):
                    pygame.draw.circle(pantalla, BLANCO, 
                                     (x + 10 + i * 15, y + 10 + j * 13), 3)

class Mazo:
    def __init__(self):
        self.cartas = []
        self.crear_mazo()
        self.mezclar()
    
    def crear_mazo(self):
        for palo in Palo:
            for valor in range(1, 14):
                self.cartas.append(Carta(valor, palo))
    
    def mezclar(self):
        random.shuffle(self.cartas)
    
    def repartir_carta(self):
        return self.cartas.pop() if self.cartas else None

class Solitario:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Solitario - Klondike")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        # Estado del juego
        self.puntos = 0
        self.movimientos = 0
        self.tiempo_inicio = pygame.time.get_ticks()
        self.juego_ganado = False
        
        # Drag & Drop
        self.carta_arrastrada = None
        self.cartas_arrastradas = []
        self.offset_arrastre = (0, 0)
        self.origen_arrastre = None
        
        self.nuevo_juego()
    
    def nuevo_juego(self):
        # Crear nuevo mazo
        self.mazo = Mazo()
        
        # Inicializar pilas
        self.stock = []  # Cartas restantes
        self.waste = []  # Cartas descartadas del stock
        self.foundation = [[] for _ in range(4)]  # Pilas objetivo (A-K)
        self.tableau = [[] for _ in range(7)]  # Columnas principales
        
        # Repartir cartas al tableau
        for col in range(7):
            for fila in range(col + 1):
                carta = self.mazo.repartir_carta()
                if fila == col:  # Última carta boca arriba
                    carta.boca_arriba = True
                self.tableau[col].append(carta)
        
        # Cartas restantes van al stock
        while self.mazo.cartas:
            self.stock.append(self.mazo.repartir_carta())
        
        # Reiniciar estado
        self.puntos = 0
        self.movimientos = 0
        self.tiempo_inicio = pygame.time.get_ticks()
        self.juego_ganado = False
    
    def obtener_posicion_pila(self, nombre_pila, indice=0):
        """Obtiene la posición x,y de una pila específica"""
        if nombre_pila == "stock":
            return (MARGEN, MARGEN)
        elif nombre_pila == "waste":
            return (MARGEN * 2 + ANCHO_CARTA, MARGEN)
        elif nombre_pila == "foundation":
            return (MARGEN * 4 + ANCHO_CARTA * 3 + indice * (ANCHO_CARTA + MARGEN), MARGEN)
        elif nombre_pila == "tableau":
            return (MARGEN + indice * (ANCHO_CARTA + MARGEN), MARGEN * 3 + ALTO_CARTA)
    
    def obtener_carta_en_posicion(self, pos):
        """Obtiene la carta que está en una posición específica"""
        x, y = pos
        
        # Verificar waste (solo la carta superior)
        if self.waste:
            waste_x, waste_y = self.obtener_posicion_pila("waste")
            if (waste_x <= x <= waste_x + ANCHO_CARTA and 
                waste_y <= y <= waste_y + ALTO_CARTA):
                return self.waste[-1], "waste", len(self.waste) - 1
        
        # Verificar foundation
        for i, pila in enumerate(self.foundation):
            if pila:
                found_x, found_y = self.obtener_posicion_pila("foundation", i)
                if (found_x <= x <= found_x + ANCHO_CARTA and 
                    found_y <= y <= found_y + ALTO_CARTA):
                    return pila[-1], "foundation", i
        
        # Verificar tableau
        for col, pila in enumerate(self.tableau):
            tab_x, tab_y = self.obtener_posicion_pila("tableau", col)
            
            for i, carta in enumerate(reversed(pila)):
                carta_y = tab_y + (len(pila) - 1 - i) * 20
                if (tab_x <= x <= tab_x + ANCHO_CARTA and 
                    carta_y <= y <= carta_y + ALTO_CARTA and 
                    carta.boca_arriba):
                    return carta, "tableau", col
        
        # Verificar stock
        if self.stock:
            stock_x, stock_y = self.obtener_posicion_pila("stock")
            if (stock_x <= x <= stock_x + ANCHO_CARTA and 
                stock_y <= y <= stock_y + ALTO_CARTA):
                return self.stock[-1], "stock", 0
        
        return None, None, None
    
    def obtener_secuencia_valida(self, carta, pila_origen, indice_pila):
        """Obtiene la secuencia válida que se puede arrastrar desde una carta"""
        if pila_origen != "tableau":
            return [carta]
        
        pila = self.tableau[indice_pila]
        indice_carta = pila.index(carta)
        secuencia = pila[indice_carta:]
        
        # Verificar que la secuencia sea válida (alternando colores, descendente)
        for i in range(len(secuencia) - 1):
            if not secuencia[i + 1].puede_ir_sobre(secuencia[i]):
                return [carta]  # Solo la primera carta si la secuencia no es válida
        
        return secuencia
    
    def puede_soltar_en(self, cartas, pila_destino, indice_destino):
        """Verifica si se pueden soltar las cartas en el destino"""
        if not cartas:
            return False
        
        primera_carta = cartas[0]
        
        if pila_destino == "foundation":
            # Solo una carta puede ir a foundation
            if len(cartas) > 1:
                return False
            return primera_carta.puede_ir_a_foundation(self.foundation[indice_destino])
        
        elif pila_destino == "tableau":
            pila = self.tableau[indice_destino]
            carta_superior = pila[-1] if pila else None
            return primera_carta.puede_ir_sobre(carta_superior)
        
        return False
    
    def mover_cartas(self, cartas, origen, indice_origen, destino, indice_destino):
        """Mueve cartas de origen a destino"""
        # Remover cartas del origen
        if origen == "waste":
            self.waste.remove(cartas[0])
        elif origen == "foundation":
            for carta in cartas:
                self.foundation[indice_origen].remove(carta)
        elif origen == "tableau":
            for carta in cartas:
                self.tableau[indice_origen].remove(carta)
        
        # Agregar cartas al destino
        if destino == "foundation":
            self.foundation[indice_destino].extend(cartas)
            self.puntos += 10
        elif destino == "tableau":
            self.tableau[indice_destino].extend(cartas)
            if origen == "waste":
                self.puntos += 5
        
        # Voltear carta si es necesario
        if origen == "tableau" and self.tableau[indice_origen]:
            carta_superior = self.tableau[indice_origen][-1]
            if not carta_superior.boca_arriba:
                carta_superior.boca_arriba = True
                self.puntos += 5
        
        self.movimientos += 1
        self.verificar_victoria()
    
    def click_stock(self):
        """Maneja el click en el stock"""
        if self.stock:
            # Mover carta del stock al waste
            carta = self.stock.pop()
            carta.boca_arriba = True
            self.waste.append(carta)
        else:
            # Reiniciar stock desde waste
            while self.waste:
                carta = self.waste.pop()
                carta.boca_arriba = False
                self.stock.append(carta)
    
    def verificar_victoria(self):
        """Verifica si el jugador ha ganado"""
        for pila in self.foundation:
            if len(pila) != 13:
                return False
        
        self.juego_ganado = True
        self.puntos += 1000
        return True
    
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F2:
                    self.nuevo_juego()
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Click izquierdo
                    pos = pygame.mouse.get_pos()
                    carta, pila_origen, indice = self.obtener_carta_en_posicion(pos)
                    
                    if pila_origen == "stock":
                        self.click_stock()
                    elif carta and carta.boca_arriba:
                        # Iniciar arrastre
                        self.carta_arrastrada = carta
                        self.origen_arrastre = (pila_origen, indice)
                        self.cartas_arrastradas = self.obtener_secuencia_valida(carta, pila_origen, indice)
                        self.offset_arrastre = (pos[0] - carta.rect.x, pos[1] - carta.rect.y)
                        
                        for c in self.cartas_arrastradas:
                            c.siendo_arrastrada = True
            
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1 and self.carta_arrastrada:  # Soltar
                    pos = pygame.mouse.get_pos()
                    
                    # Encontrar destino
                    destino_encontrado = False
                    
                    # Verificar foundation
                    for i in range(4):
                        found_x, found_y = self.obtener_posicion_pila("foundation", i)
                        if (found_x <= pos[0] <= found_x + ANCHO_CARTA and 
                            found_y <= pos[1] <= found_y + ALTO_CARTA):
                            if self.puede_soltar_en(self.cartas_arrastradas, "foundation", i):
                                self.mover_cartas(self.cartas_arrastradas, 
                                                self.origen_arrastre[0], self.origen_arrastre[1],
                                                "foundation", i)
                                destino_encontrado = True
                            break
                    
                    # Verificar tableau si no se encontró en foundation
                    if not destino_encontrado:
                        for i in range(7):
                            tab_x, tab_y = self.obtener_posicion_pila("tableau", i)
                            if (tab_x <= pos[0] <= tab_x + ANCHO_CARTA and 
                                tab_y <= pos[1]):
                                if self.puede_soltar_en(self.cartas_arrastradas, "tableau", i):
                                    self.mover_cartas(self.cartas_arrastradas,
                                                    self.origen_arrastre[0], self.origen_arrastre[1],
                                                    "tableau", i)
                                    destino_encontrado = True
                                break
                    
                    # Resetear arrastre
                    for c in self.cartas_arrastradas:
                        c.siendo_arrastrada = False
                    self.carta_arrastrada = None
                    self.cartas_arrastradas = []
                    self.origen_arrastre = None
        
        return True
    
    def dibujar(self):
        self.pantalla.fill(VERDE_MESA)
        
        # Dibujar áreas de las pilas
        self.dibujar_areas_pilas()
        
        # Dibujar stock
        stock_x, stock_y = self.obtener_posicion_pila("stock")
        if self.stock:
            self.stock[-1].dibujar(self.pantalla, stock_x, stock_y)
        else:
            # Dibujar área vacía con símbolo de reinicio
            pygame.draw.rect(self.pantalla, GRIS_CLARO, (stock_x, stock_y, ANCHO_CARTA, ALTO_CARTA))
            pygame.draw.rect(self.pantalla, NEGRO, (stock_x, stock_y, ANCHO_CARTA, ALTO_CARTA), 2)
            fuente = pygame.font.Font(None, 24)
            texto = fuente.render("↻", True, NEGRO)
            rect_texto = texto.get_rect(center=(stock_x + ANCHO_CARTA//2, stock_y + ALTO_CARTA//2))
            self.pantalla.blit(texto, rect_texto)
        
        # Dibujar waste
        waste_x, waste_y = self.obtener_posicion_pila("waste")
        if self.waste:
            # Mostrar hasta 3 cartas del waste
            for i, carta in enumerate(self.waste[-3:]):
                offset_x = i * 20
                carta.dibujar(self.pantalla, waste_x + offset_x, waste_y)
        
        # Dibujar foundation
        for i, pila in enumerate(self.foundation):
            found_x, found_y = self.obtener_posicion_pila("foundation", i)
            if pila:
                pila[-1].dibujar(self.pantalla, found_x, found_y)
        
        # Dibujar tableau
        for col, pila in enumerate(self.tableau):
            tab_x, tab_y = self.obtener_posicion_pila("tableau", col)
            
            for i, carta in enumerate(pila):
                if not carta.siendo_arrastrada:
                    carta_y = tab_y + i * 20
                    carta.dibujar(self.pantalla, tab_x, carta_y)
        
        # Dibujar cartas siendo arrastradas
        if self.carta_arrastrada:
            pos = pygame.mouse.get_pos()
            for i, carta in enumerate(self.cartas_arrastradas):
                carta_x = pos[0] - self.offset_arrastre[0]
                carta_y = pos[1] - self.offset_arrastre[1] + i * 20
                carta.dibujar(self.pantalla, carta_x, carta_y)
        
        # Dibujar información del juego
        self.dibujar_info()
        
        pygame.display.flip()
    
    def dibujar_areas_pilas(self):
        """Dibujar las áreas donde van las pilas"""
        # Área del waste
        waste_x, waste_y = self.obtener_posicion_pila("waste")
        if not self.waste:
            pygame.draw.rect(self.pantalla, GRIS, (waste_x, waste_y, ANCHO_CARTA, ALTO_CARTA))
            pygame.draw.rect(self.pantalla, NEGRO, (waste_x, waste_y, ANCHO_CARTA, ALTO_CARTA), 2)
        
        # Áreas de foundation
        for i in range(4):
            found_x, found_y = self.obtener_posicion_pila("foundation", i)
            if not self.foundation[i]:
                pygame.draw.rect(self.pantalla, GRIS, (found_x, found_y, ANCHO_CARTA, ALTO_CARTA))
                pygame.draw.rect(self.pantalla, NEGRO, (found_x, found_y, ANCHO_CARTA, ALTO_CARTA), 2)
                
                # Dibujar símbolo del palo
                palos = [Palo.CORAZONES, Palo.DIAMANTES, Palo.TREBOLES, Palo.ESPADAS]
                fuente = pygame.font.Font(None, 36)
                color_palo = ROJO if palos[i] in [Palo.CORAZONES, Palo.DIAMANTES] else NEGRO
                texto = fuente.render(palos[i].value, True, color_palo)
                rect_texto = texto.get_rect(center=(found_x + ANCHO_CARTA//2, found_y + ALTO_CARTA//2))
                self.pantalla.blit(texto, rect_texto)
        
        # Áreas de tableau
        for i in range(7):
            tab_x, tab_y = self.obtener_posicion_pila("tableau", i)
            if not self.tableau[i]:
                pygame.draw.rect(self.pantalla, GRIS, (tab_x, tab_y, ANCHO_CARTA, ALTO_CARTA))
                pygame.draw.rect(self.pantalla, NEGRO, (tab_x, tab_y, ANCHO_CARTA, ALTO_CARTA), 2)
    
    def dibujar_info(self):
        """Dibujar información del juego"""
        y_info = ALTO_PANTALLA - 100
        
        # Puntos
        texto_puntos = self.fuente.render(f"Puntos: {self.puntos}", True, BLANCO)
        self.pantalla.blit(texto_puntos, (MARGEN, y_info))
        
        # Movimientos
        texto_movimientos = self.fuente.render(f"Movimientos: {self.movimientos}", True, BLANCO)
        self.pantalla.blit(texto_movimientos, (MARGEN + 200, y_info))
        
        # Tiempo
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60
        texto_tiempo = self.fuente.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, BLANCO)
        self.pantalla.blit(texto_tiempo, (MARGEN + 400, y_info))
        
        # Controles
        controles = [
            "Click para seleccionar carta",
            "Arrastrar para mover",
            "Click en stock para voltear carta",
            "F2: Nuevo juego"
        ]
        
        for i, control in enumerate(controles):
            texto = self.fuente_pequena.render(control, True, BLANCO)
            self.pantalla.blit(texto, (MARGEN, y_info + 40 + i * 20))
        
        # Mensaje de victoria
        if self.juego_ganado:
            texto_victoria = self.fuente.render("¡FELICITACIONES! ¡HAS GANADO!", True, AMARILLO)
            rect_victoria = texto_victoria.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2))
            pygame.draw.rect(self.pantalla, NEGRO, rect_victoria.inflate(20, 10))
            self.pantalla.blit(texto_victoria, rect_victoria)
    
    def ejecutar(self):
        print("¡Iniciando Solitario Klondike!")
        print("\nControles:")
        print("- Click en una carta para seleccionarla")
        print("- Arrastra cartas para moverlas")
        print("- Click en el stock (esquina superior izquierda) para voltear cartas")
        print("- F2: Nuevo juego")
        print("\nReglas:")
        print("- Construye secuencias descendentes alternando colores en el tableau")
        print("- Mueve cartas a las pilas foundation en orden ascendente por palo (A-K)")
        print("- Solo los reyes pueden ir en espacios vacíos del tableau")
        print("- ¡Mueve todas las cartas a las foundations para ganar!")
        print("\n¡Buena suerte!")
        
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.dibujar()
            self.reloj.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    juego = Solitario()
    juego.ejecutar()
