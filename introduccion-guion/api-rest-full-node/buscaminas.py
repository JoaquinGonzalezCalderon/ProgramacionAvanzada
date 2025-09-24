import tkinter as tk
from tkinter import messagebox
import random

class Buscaminas:
    def __init__(self, filas=10, columnas=10, minas=15):
        self.filas = filas
        self.columnas = columnas
        self.num_minas = minas
        self.tablero = []
        self.botones = []
        self.banderas = set()
        self.reveladas = set()
        self.juego_terminado = False
        self.primer_click = True
        
        # Crear la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Buscaminas")
        self.ventana.resizable(False, False)
        
        # Frame superior para información del juego
        self.frame_info = tk.Frame(self.ventana)
        self.frame_info.pack(pady=5)
        
        self.label_minas = tk.Label(self.frame_info, text=f"Minas: {self.num_minas}", font=('Arial', 12))
        self.label_minas.pack(side=tk.LEFT, padx=10)
        
        self.boton_reiniciar = tk.Button(self.frame_info, text="Reiniciar", command=self.reiniciar_juego, font=('Arial', 12))
        self.boton_reiniciar.pack(side=tk.RIGHT, padx=10)
        
        # Frame para el tablero
        self.frame_tablero = tk.Frame(self.ventana)
        self.frame_tablero.pack(pady=5)
        
        self.crear_interfaz()
        self.inicializar_tablero()
    
    def inicializar_tablero(self):
        """Inicializa el tablero sin minas (se colocan en el primer click)"""
        self.tablero = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.banderas = set()
        self.reveladas = set()
        self.juego_terminado = False
        self.primer_click = True
        
        # Resetear botones
        for i in range(self.filas):
            for j in range(self.columnas):
                self.botones[i][j].config(text="", bg="SystemButtonFace", state="normal")
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica con botones"""
        self.botones = []
        for i in range(self.filas):
            fila_botones = []
            for j in range(self.columnas):
                boton = tk.Button(
                    self.frame_tablero,
                    width=2,
                    height=1,
                    font=('Arial', 12, 'bold'),
                    command=lambda r=i, c=j: self.click_izquierdo(r, c)
                )
                boton.bind("<Button-3>", lambda e, r=i, c=j: self.click_derecho(r, c))
                boton.grid(row=i, column=j, padx=1, pady=1)
                fila_botones.append(boton)
            self.botones.append(fila_botones)
    
    def colocar_minas(self, fila_segura, col_segura):
        """Coloca las minas en el tablero evitando la posición del primer click"""
        minas_colocadas = 0
        while minas_colocadas < self.num_minas:
            fila = random.randint(0, self.filas - 1)
            col = random.randint(0, self.columnas - 1)
            
            # No colocar mina en la posición del primer click ni si ya hay una mina
            if (fila != fila_segura or col != col_segura) and self.tablero[fila][col] != -1:
                self.tablero[fila][col] = -1  # -1 representa una mina
                minas_colocadas += 1
        
        # Calcular números para cada celda
        self.calcular_numeros()
    
    def calcular_numeros(self):
        """Calcula los números para cada celda basado en las minas adyacentes"""
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] != -1:  # Si no es una mina
                    contador = 0
                    # Verificar las 8 celdas adyacentes
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.filas and 0 <= nj < self.columnas:
                                if self.tablero[ni][nj] == -1:
                                    contador += 1
                    self.tablero[i][j] = contador
    
    def click_izquierdo(self, fila, col):
        """Maneja el click izquierdo en una celda"""
        if self.juego_terminado or (fila, col) in self.banderas:
            return
        
        # Si es el primer click, colocar las minas
        if self.primer_click:
            self.colocar_minas(fila, col)
            self.primer_click = False
        
        if (fila, col) in self.reveladas:
            return
        
        # Si es una mina, terminar el juego
        if self.tablero[fila][col] == -1:
            self.game_over()
            return
        
        # Revelar la celda
        self.revelar_celda(fila, col)
        
        # Verificar si se ganó el juego
        if self.verificar_victoria():
            self.victoria()
    
    def click_derecho(self, fila, col):
        """Maneja el click derecho para colocar/quitar banderas"""
        if self.juego_terminado or (fila, col) in self.reveladas:
            return
        
        if (fila, col) in self.banderas:
            # Quitar bandera
            self.banderas.remove((fila, col))
            self.botones[fila][col].config(text="", bg="SystemButtonFace")
        else:
            # Colocar bandera
            self.banderas.add((fila, col))
            self.botones[fila][col].config(text="🚩", bg="yellow")
        
        # Actualizar contador de minas
        minas_restantes = self.num_minas - len(self.banderas)
        self.label_minas.config(text=f"Minas: {minas_restantes}")
    
    def revelar_celda(self, fila, col):
        """Revela una celda y sus adyacentes si es necesario"""
        if (fila, col) in self.reveladas or (fila, col) in self.banderas:
            return
        
        self.reveladas.add((fila, col))
        valor = self.tablero[fila][col]
        
        # Configurar colores según el número
        colores = {
            0: "lightgray",
            1: "blue", 2: "green", 3: "red", 4: "purple",
            5: "maroon", 6: "turquoise", 7: "black", 8: "gray"
        }
        
        if valor == 0:
            self.botones[fila][col].config(text="", bg="lightgray", relief="sunken")
            # Si es 0, revelar celdas adyacentes automáticamente
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = fila + di, col + dj
                    if 0 <= ni < self.filas and 0 <= nj < self.columnas:
                        if (ni, nj) not in self.reveladas:
                            self.revelar_celda(ni, nj)
        else:
            color_texto = colores.get(valor, "black")
            self.botones[fila][col].config(
                text=str(valor), 
                bg="lightgray", 
                fg=color_texto,
                relief="sunken"
            )
    
    def game_over(self):
        """Termina el juego mostrando todas las minas"""
        self.juego_terminado = True
        
        # Mostrar todas las minas
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] == -1:
                    if (i, j) in self.banderas:
                        self.botones[i][j].config(text="💣", bg="green")
                    else:
                        self.botones[i][j].config(text="💣", bg="red")
                elif (i, j) in self.banderas and self.tablero[i][j] != -1:
                    # Bandera mal colocada
                    self.botones[i][j].config(text="❌", bg="orange")
        
        messagebox.showinfo("Game Over", "¡Has perdido! Haz click en una mina.")
    
    def verificar_victoria(self):
        """Verifica si el jugador ha ganado"""
        celdas_seguras = self.filas * self.columnas - self.num_minas
        return len(self.reveladas) == celdas_seguras
    
    def victoria(self):
        """Maneja la victoria del jugador"""
        self.juego_terminado = True
        
        # Colocar banderas en todas las minas no marcadas
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] == -1 and (i, j) not in self.banderas:
                    self.botones[i][j].config(text="🚩", bg="green")
        
        messagebox.showinfo("¡Victoria!", f"¡Felicidades! Has ganado el juego.\nTiempo: ¡Excelente!")
    
    def reiniciar_juego(self):
        """Reinicia el juego"""
        self.inicializar_tablero()
        self.label_minas.config(text=f"Minas: {self.num_minas}")
    
    def ejecutar(self):
        """Inicia el juego"""
        self.ventana.mainloop()

def main():
    """Función principal para ejecutar el juego"""
    print("¡Bienvenido al Buscaminas!")
    print("Instrucciones:")
    print("- Click izquierdo: Revelar celda")
    print("- Click derecho: Colocar/quitar bandera")
    print("- El objetivo es revelar todas las celdas sin minas")
    print()
    
    # Opciones de dificultad
    print("Selecciona la dificultad:")
    print("1. Fácil (9x9, 10 minas)")
    print("2. Intermedio (16x16, 40 minas)")
    print("3. Difícil (16x30, 99 minas)")
    print("4. Personalizado")
    
    try:
        opcion = input("Ingresa tu opción (1-4): ").strip()
        
        if opcion == "1":
            juego = Buscaminas(9, 9, 10)
        elif opcion == "2":
            juego = Buscaminas(16, 16, 40)
        elif opcion == "3":
            juego = Buscaminas(16, 30, 99)
        elif opcion == "4":
            filas = int(input("Número de filas: "))
            columnas = int(input("Número de columnas: "))
            minas = int(input("Número de minas: "))
            
            if minas >= filas * columnas:
                print("Error: El número de minas debe ser menor que el total de celdas.")
                return
            
            juego = Buscaminas(filas, columnas, minas)
        else:
            print("Opción no válida. Usando configuración por defecto (10x10, 15 minas).")
            juego = Buscaminas()
        
        juego.ejecutar()
        
    except ValueError:
        print("Entrada no válida. Usando configuración por defecto (10x10, 15 minas).")
        juego = Buscaminas()
        juego.ejecutar()
    except KeyboardInterrupt:
        print("\n¡Gracias por jugar!")

if __name__ == "__main__":
    main()
