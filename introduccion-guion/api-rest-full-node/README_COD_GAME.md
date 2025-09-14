# Call of Duty Python 🎮

Un juego de disparos en primera persona (vista desde arriba) inspirado en Call of Duty, desarrollado en Python usando Pygame.

## 🎯 Características del Juego

### Versión Básica (`cod_game.py`)
- Jugador controlable con movimiento fluido (WASD)
- Sistema de apuntado con el mouse
- Enemigos con IA básica que persiguen y disparan
- Sistema de munición y recarga
- Sistema de oleadas progresivas
- HUD con vida, munición y puntuación
- Menús de inicio y game over

### Versión Avanzada (`cod_advanced.py`)
- Todo lo de la versión básica PLUS:
- **IA mejorada**: Los enemigos usan línea de vista (raycast)
- **Mapas con obstáculos**: Paredes, cobertura y estructuras tácticas
- **Física de balas realista**: Las balas rebotan en paredes
- **Minimapa**: Para ver la posición de enemigos
- **Mejor balanceado**: Distancias de combate más estratégicas

## 🚀 Requisitos del Sistema

```bash
pip install pygame
```

## 🎮 Cómo Jugar

### Ejecutar el juego básico:
```bash
python cod_game.py
```

### Ejecutar la versión avanzada:
```bash
python cod_advanced.py
```

## 🕹️ Controles

| Tecla/Acción | Función |
|--------------|---------|
| **W, A, S, D** | Mover jugador |
| **Mouse** | Apuntar |
| **Click Izquierdo** | Disparar |
| **R** | Recargar |
| **ESPACIO** | Comenzar juego / Reiniciar después de game over |

## 🎯 Objetivos del Juego

1. **Sobrevive**: Mantén tu vida por encima de 0
2. **Elimina enemigos**: Cada enemigo vale 100 puntos
3. **Completa oleadas**: Cada oleada trae más enemigos
4. **Usa cobertura**: En la versión avanzada, usa las paredes estratégicamente
5. **Administra munición**: Recarga en momentos seguros

## 🧠 Estrategias de Juego

### Para la Versión Básica:
- Mantén distancia de los enemigos
- Recarga cuando tengas pocos enemigos cerca
- Usa el movimiento para evitar las balas enemigas

### Para la Versión Avanzada:
- **Usa cobertura**: Los enemigos no pueden dispararte si no te ven
- **Flanquea**: Rodea los obstáculos para atacar por sorpresa
- **Control del minimapa**: Observa las posiciones enemigas
- **Combate táctico**: Los enemigos mantienen distancia, úsalo a tu favor

## 🔧 Personalización

Puedes modificar fácilmente:

```python
# En la sección de constantes
SCREEN_WIDTH = 1200    # Ancho de pantalla
SCREEN_HEIGHT = 800    # Alto de pantalla
FPS = 60              # Frames por segundo

# En la clase Player
self.speed = 5        # Velocidad del jugador
self.max_health = 100 # Vida máxima
self.max_ammo = 30    # Munición máxima

# En la clase Enemy
self.speed = 2        # Velocidad del enemigo
self.health = 50      # Vida del enemigo
```

## 🎨 Elementos Visuales

- **Jugador**: Círculo azul con línea direccional blanca
- **Enemigos**: Círculos rojos con barras de vida
- **Balas del jugador**: Puntos amarillos
- **Balas enemigas**: Puntos naranjas
- **Paredes**: Rectángulos grises (solo en versión avanzada)
- **HUD**: Información en tiempo real

## 🏆 Sistema de Puntuación

- **Eliminar enemigo**: +100 puntos
- **Completar oleada**: Munición completa de bonus
- **Supervivencia**: ¡El objetivo es durar lo más posible!

## 🐛 Posibles Mejoras Futuras

- Efectos de sonido y música
- Diferentes tipos de armas
- Power-ups y mejoras
- Multijugador local
- Más tipos de enemigos
- Efectos visuales (explosiones, sangre)
- Sistema de logros

## 📝 Notas de Desarrollo

Este juego fue creado como una demostración de:
- Programación orientada a objetos en Python
- Uso de la librería Pygame
- Implementación de IA básica para videojuegos
- Sistemas de colisión y física simple
- Manejo de eventos y estados de juego

¡Disfruta el juego y no dudes en modificarlo para hacerlo tu propio COD Python! 🔫
