#!/usr/bin/env python3
"""
Terminal Snake Game
A classic Snake game implementation for the terminal using Python and curses.
"""

import curses
import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

@dataclass
class Position:
    row: int
    col: int
    
    def __add__(self, direction: Direction):
        dr, dc = direction.value
        return Position(self.row + dr, self.col + dc)
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

class Snake:
    def __init__(self, start_pos: Position):
        self.body = [start_pos]
        self.direction = Direction.RIGHT
        self.grow_next = False
    
    def move(self):
        # Get new head position
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        
        # Remove tail unless we're growing
        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False
    
    def grow(self):
        self.grow_next = True
    
    def change_direction(self, new_direction: Direction):
        # Prevent moving directly backwards
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    def check_collision(self, max_row: int, max_col: int) -> bool:
        head = self.body[0]
        
        # Wall collision
        if (head.row < 0 or head.row >= max_row or 
            head.col < 0 or head.col >= max_col):
            return True
        
        # Self collision
        return head in self.body[1:]

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_screen()
        self.reset_game()
    
    def setup_screen(self):
        # Hide cursor
        curses.curs_set(0)
        
        # Set up colors
        curses.start_color()
        # Rainbow colors for snake segments
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)     # Red
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Cyan
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Blue
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Magenta
        # Other game elements
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)     # Food
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)   # UI
        curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Score
        
        # Set non-blocking input
        self.stdscr.nodelay(1)
        self.stdscr.timeout(100)  # 100ms timeout
        
        # Get screen dimensions
        self.max_row, self.max_col = self.stdscr.getmaxyx()
        
        # Create game area (leave space for UI)
        self.game_height = self.max_row - 3
        self.game_width = self.max_col - 2
    
    def reset_game(self):
        # Initialize snake in the middle of the screen
        start_pos = Position(self.game_height // 2, self.game_width // 2)
        self.snake = Snake(start_pos)
        
        # Initialize score
        self.score = 0
        
        # Place first food
        self.place_food()
        
        # Game state
        self.game_over = False
        self.paused = False
    
    def place_food(self):
        while True:
            self.food = Position(
                random.randint(1, self.game_height - 1),
                random.randint(1, self.game_width - 1)
            )
            # Make sure food doesn't spawn on snake
            if self.food not in self.snake.body:
                break
    
    def handle_input(self):
        try:
            key = self.stdscr.getch()
        except:
            return True  # Continue game
        
        if key == -1:  # No input
            return True
        
        # Game controls
        key_direction_map = {
            curses.KEY_UP: Direction.UP,
            ord('w'): Direction.UP,
            ord('W'): Direction.UP,
            curses.KEY_DOWN: Direction.DOWN,
            ord('s'): Direction.DOWN,
            ord('S'): Direction.DOWN,
            curses.KEY_LEFT: Direction.LEFT,
            ord('a'): Direction.LEFT,
            ord('A'): Direction.LEFT,
            curses.KEY_RIGHT: Direction.RIGHT,
            ord('d'): Direction.RIGHT,
            ord('D'): Direction.RIGHT,
        }
        
        if key in key_direction_map:
            self.snake.change_direction(key_direction_map[key])
        elif key == ord(' '):  # Space to pause
            self.paused = not self.paused
        elif key == ord('r') or key == ord('R'):  # R to restart
            self.reset_game()
        elif key == ord('q') or key == ord('Q') or key == 27:  # Q or ESC to quit
            return False
        
        return True
    
    def update_game(self):
        if self.game_over or self.paused:
            return
        
        # Move snake
        self.snake.move()
        
        # Check collision
        if self.snake.check_collision(self.game_height, self.game_width):
            self.game_over = True
            return
        
        # Check food collision
        if self.snake.body[0] == self.food:
            self.score += 10
            self.snake.grow()
            self.place_food()
    
    def draw_border(self):
        # Draw game border
        for i in range(self.game_width + 1):
            self.stdscr.addch(0, i, '─')
            self.stdscr.addch(self.game_height, i, '─')
        
        for i in range(self.game_height + 1):
            self.stdscr.addch(i, 0, '│')
            self.stdscr.addch(i, self.game_width, '│')
        
        # Corners
        self.stdscr.addch(0, 0, '┌')
        self.stdscr.addch(0, self.game_width, '┐')
        self.stdscr.addch(self.game_height, 0, '└')
        self.stdscr.addch(self.game_height, self.game_width, '┘')
    
    def draw_snake(self):
        # Draw snake body with rainbow colors
        rainbow_colors = [1, 2, 3, 4, 5, 6]  # Red, Yellow, Green, Cyan, Blue, Magenta
        
        for i, segment in enumerate(self.snake.body):
            if 0 < segment.row < self.game_height and 0 < segment.col < self.game_width:
                char = '●' if i == 0 else '○'  # Head vs body
                # Cycle through rainbow colors based on segment position
                color_index = rainbow_colors[i % len(rainbow_colors)]
                self.stdscr.addch(segment.row, segment.col, char, curses.color_pair(color_index))
    
    def draw_food(self):
        if 0 < self.food.row < self.game_height and 0 < self.food.col < self.game_width:
            self.stdscr.addch(self.food.row, self.food.col, '◆', curses.color_pair(7))
    
    def draw_ui(self):
        # Score
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(self.game_height + 1, 2, score_text, curses.color_pair(9))
        
        # Controls info
        controls = "Controls: WASD/Arrows=Move, Space=Pause, R=Restart, Q=Quit"
        if len(controls) < self.max_col - 2:
            self.stdscr.addstr(self.game_height + 2, 2, controls, curses.color_pair(8))
        
        # Game status
        if self.game_over:
            msg = "GAME OVER! Press R to restart or Q to quit"
            if len(msg) < self.max_col - 4:
                start_col = (self.max_col - len(msg)) // 2
                self.stdscr.addstr(self.game_height // 2, start_col, msg, 
                                 curses.color_pair(7) | curses.A_BOLD)
        elif self.paused:
            msg = "PAUSED - Press Space to continue"
            if len(msg) < self.max_col - 4:
                start_col = (self.max_col - len(msg)) // 2
                self.stdscr.addstr(self.game_height // 2, start_col, msg, 
                                 curses.color_pair(8) | curses.A_BOLD)
    
    def draw(self):
        self.stdscr.clear()
        
        # Draw game elements
        self.draw_border()
        self.draw_snake()
        self.draw_food()
        self.draw_ui()
        
        # Refresh screen
        self.stdscr.refresh()
    
    def run(self):
        while True:
            # Handle input
            if not self.handle_input():
                break
            
            # Update game state
            self.update_game()
            
            # Draw everything
            self.draw()
            
            # Control game speed
            time.sleep(0.02)

def main():
    """Main function to initialize and run the snake game."""
    def start_game(stdscr):
        # Check minimum terminal size
        height, width = stdscr.getmaxyx()
        if height < 10 or width < 40:
            stdscr.addstr(0, 0, "Terminal too small! Need at least 40x10")
            stdscr.addstr(1, 0, f"Current size: {width}x{height}")
            stdscr.addstr(2, 0, "Press any key to exit...")
            stdscr.getch()
            return
        
        # Create and run game
        game = Game(stdscr)
        game.run()
    
    try:
        curses.wrapper(start_game)
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure your terminal supports the required features.")

if __name__ == "__main__":
    print("🐍 Terminal Snake Game")
    print("===================")
    print("Starting game...")
    print("\nGame Controls:")
    print("  WASD or Arrow Keys - Move snake")
    print("  Space - Pause/Unpause")
    print("  R - Restart game")
    print("  Q or ESC - Quit game")
    print("\nPress Enter to start!")
    input()
    
    main()
