# Flappy Bird en Python

Un clon del famoso juego Flappy Bird implementado en Python usando pygame.

## Descripción

Este es un juego simple donde controlas un pájaro amarillo que debe volar entre tubos verdes sin tocarlos. El objetivo es obtener la mayor puntuación posible pasando entre los tubos.

## Características

- ✨ Física realista con gravedad
- 🎮 Controles simples (solo barra espaciadora)
- 📊 Sistema de puntuación
- 🎨 Gráficos coloridos con fondo degradado
- 🔄 Reinicio automático del juego
- 💥 Detección de colisiones precisa

## Requisitos

Para ejecutar este juego necesitas:

- Python 3.6 o superior
- pygame

## Instalación

1. **Instalar Python** (si no lo tienes):
   - Descarga Python desde [python.org](https://python.org)
   - Asegúrate de que Python esté en tu PATH

2. **Instalar pygame**:
   ```bash
   pip install pygame
   ```

3. **Ejecutar el juego**:
   ```bash
   python flappy_bird.py
   ```

## Cómo Jugar

### Controles
- **ESPACIO**: Hacer que el pájaro salte/vuele hacia arriba
- **ESC**: Salir del juego
- **ESPACIO** (en Game Over): Reiniciar el juego

### Reglas
1. El pájaro cae constantemente debido a la gravedad
2. Presiona ESPACIO para hacer que el pájaro vuele hacia arriba
3. Evita tocar los tubos verdes, el suelo o el techo
4. Ganas un punto cada vez que pasas entre un par de tubos
5. El juego termina cuando el pájaro toca cualquier obstáculo

### Objetivo
- ¡Consigue la mayor puntuación posible!
- Cada tubo que pases suma 1 punto

## Estructura del Código

El juego está organizado en las siguientes clases:

### `Bird`
- Maneja la física del pájaro (gravedad, salto)
- Dibuja el pájaro en pantalla
- Detecta colisiones

### `Pipe`
- Crea y maneja los tubos obstáculos
- Genera alturas aleatorias
- Detecta colisiones con el pájaro

### `FlappyBirdGame`
- Clase principal que maneja el juego
- Bucle principal del juego
- Manejo de eventos y entrada del usuario
- Renderizado de gráficos

## Personalización

Puedes modificar las constantes al inicio del archivo para personalizar el juego:

```python
# Configuración del juego
GRAVITY = 0.5          # Fuerza de gravedad
JUMP_STRENGTH = -10    # Fuerza del salto
PIPE_SPEED = 3         # Velocidad de los tubos
PIPE_WIDTH = 50        # Ancho de los tubos
PIPE_GAP = 150         # Espacio entre tubos
PIPE_FREQUENCY = 90    # Frames entre tubos nuevos
```

## Posibles Mejoras

- Añadir sonidos y música
- Implementar diferentes niveles de dificultad
- Agregar sprites más elaborados
- Sistema de high scores
- Efectos de partículas
- Power-ups especiales

## Créditos

Implementado en Python usando pygame. Inspirado en el juego original Flappy Bird de Dong Nguyen.

## Licencia

Este proyecto es de uso libre para propósitos educativos y de aprendizaje.

---

¡Disfruta jugando y aprendiendo! 🐦✨
