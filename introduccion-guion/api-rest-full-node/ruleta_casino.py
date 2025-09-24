import tkinter as tk
from tkinter import messagebox
import random
import math
import time

class RuletaCasino:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 RULETA CASINO 🎰")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d5f0d')
        self.root.resizable(False, False)
        
        # Variables del juego
        self.dinero = 1000
        self.apuestas = {}  # {tipo_apuesta: cantidad}
        self.numero_ganador = None
        self.girando = False
        self.angulo_rueda = 0
        
        # Números de la ruleta europea (0-36)
        self.numeros_ruleta = list(range(37))  # 0 a 36
        self.numeros_rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.numeros_negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        
        # Orden visual de los números en la rueda
        self.orden_rueda = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 
                          24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        
        self.crear_interfaz()
        self.actualizar_dinero()
    
    def crear_interfaz(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#0d5f0d')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="🎰 RULETA EUROPEA 🎰", 
                              font=('Arial', 28, 'bold'), 
                              fg='gold', bg='#0d5f0d')
        title_label.pack()
        
        # Frame principal que contiene rueda y mesa
        main_frame = tk.Frame(self.root, bg='#0d5f0d')
        main_frame.pack(pady=10, padx=20)
        
        # Frame izquierdo para la rueda
        wheel_frame = tk.Frame(main_frame, bg='#0d5f0d')
        wheel_frame.pack(side=tk.LEFT, padx=20)
        
        # Canvas para la rueda
        self.wheel_canvas = tk.Canvas(wheel_frame, width=350, height=350, bg='#8B4513', 
                                     relief=tk.RAISED, bd=5)
        self.wheel_canvas.pack()
        
        # Resultado
        self.resultado_frame = tk.Frame(wheel_frame, bg='#0d5f0d')
        self.resultado_frame.pack(pady=10)
        
        self.resultado_label = tk.Label(self.resultado_frame, text="Resultado: -", 
                                       font=('Arial', 18, 'bold'),
                                       fg='white', bg='#0d5f0d')
        self.resultado_label.pack()
        
        # Botón girar
        self.girar_btn = tk.Button(wheel_frame, text="🎲 GIRAR RULETA", 
                                  command=self.girar_ruleta,
                                  font=('Arial', 16, 'bold'),
                                  bg='#FF4500', fg='white',
                                  relief=tk.RAISED, bd=3,
                                  width=15, height=2)
        self.girar_btn.pack(pady=10)
        
        # Frame derecho para la mesa de apuestas
        self.crear_mesa_apuestas(main_frame)
        
        # Frame inferior para información y controles
        info_frame = tk.Frame(self.root, bg='#0d5f0d')
        info_frame.pack(pady=10)
        
        # Dinero
        self.dinero_label = tk.Label(info_frame, text=f"💰 Dinero: ${self.dinero}", 
                                    font=('Arial', 16, 'bold'),
                                    fg='gold', bg='#0d5f0d')
        self.dinero_label.pack(pady=5)
        
        # Frame de controles
        controls_frame = tk.Frame(info_frame, bg='#0d5f0d')
        controls_frame.pack(pady=10)
        
        # Botones de cantidad de apuesta
        tk.Label(controls_frame, text="Cantidad a apostar:", font=('Arial', 12, 'bold'),
                fg='white', bg='#0d5f0d').pack()
        
        bet_amounts_frame = tk.Frame(controls_frame, bg='#0d5f0d')
        bet_amounts_frame.pack(pady=5)
        
        self.cantidad_apuesta = tk.IntVar(value=10)
        bet_amounts = [5, 10, 25, 50, 100]
        for amount in bet_amounts:
            btn = tk.Radiobutton(bet_amounts_frame, text=f"${amount}", variable=self.cantidad_apuesta,
                                value=amount, font=('Arial', 10, 'bold'),
                                bg='#0d5f0d', fg='white', selectcolor='#1a4a1a',
                                relief=tk.RAISED, bd=2)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Botones principales
        main_controls_frame = tk.Frame(controls_frame, bg='#0d5f0d')
        main_controls_frame.pack(pady=10)
        
        clear_btn = tk.Button(main_controls_frame, text="🗑️ LIMPIAR", 
                             command=self.limpiar_apuestas,
                             font=('Arial', 12, 'bold'),
                             bg='#FF6347', fg='white',
                             relief=tk.RAISED, bd=2,
                             width=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(main_controls_frame, text="🔄 RESET", 
                             command=self.reset_juego,
                             font=('Arial', 12, 'bold'),
                             bg='#9C27B0', fg='white',
                             relief=tk.RAISED, bd=2,
                             width=10)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de apuestas actuales
        self.apuestas_frame = tk.Frame(info_frame, bg='#0d5f0d')
        self.apuestas_frame.pack(pady=10)
        
        self.apuestas_label = tk.Label(self.apuestas_frame, text="Apuestas: Ninguna", 
                                      font=('Arial', 12, 'bold'),
                                      fg='yellow', bg='#0d5f0d')
        self.apuestas_label.pack()
        
        self.dibujar_rueda()
        self.actualizar_apuestas_display()
    
    def crear_mesa_apuestas(self, parent):
        """Crea la mesa de apuestas con todos los números y opciones"""
        betting_frame = tk.Frame(parent, bg='#0d5f0d')
        betting_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(betting_frame, text="🎯 MESA DE APUESTAS", font=('Arial', 14, 'bold'),
                fg='white', bg='#0d5f0d').pack(pady=5)
        
        # Crear scroll para la mesa
        canvas_frame = tk.Frame(betting_frame, bg='#0d5f0d')
        canvas_frame.pack()
        
        canvas = tk.Canvas(canvas_frame, width=500, height=400, bg='#0d5f0d')
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#0d5f0d')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mesa principal de números (0-36)
        numbers_frame = tk.Frame(scrollable_frame, bg='#0d5f0d', relief=tk.RAISED, bd=2)
        numbers_frame.pack(pady=5)
        
        tk.Label(numbers_frame, text="NÚMEROS INDIVIDUALES", font=('Arial', 12, 'bold'),
                fg='white', bg='#0d5f0d').pack()
        
        # Crear botones para números 0-36
        numbers_container = tk.Frame(numbers_frame, bg='#0d5f0d')
        numbers_container.pack(pady=5)
        
        # Número 0 especial
        zero_btn = tk.Button(numbers_container, text="0", command=lambda: self.apostar_numero(0),
                            font=('Arial', 10, 'bold'), bg='green', fg='white',
                            width=3, height=1, relief=tk.RAISED, bd=2)
        zero_btn.pack(pady=2)
        
        # Números 1-36 en filas de 12
        for row in range(3):
            row_frame = tk.Frame(numbers_container, bg='#0d5f0d')
            row_frame.pack()
            for col in range(12):
                num = row * 12 + col + 1
                color = 'red' if num in self.numeros_rojos else 'black'
                btn = tk.Button(row_frame, text=str(num), 
                               command=lambda n=num: self.apostar_numero(n),
                               font=('Arial', 10, 'bold'), 
                               bg=color, fg='white',
                               width=3, height=1, relief=tk.RAISED, bd=1)
                btn.pack(side=tk.LEFT, padx=1, pady=1)
        
        # Apuestas especiales
        special_frame = tk.Frame(scrollable_frame, bg='#0d5f0d', relief=tk.RAISED, bd=2)
        special_frame.pack(pady=5)
        
        tk.Label(special_frame, text="APUESTAS ESPECIALES", font=('Arial', 12, 'bold'),
                fg='white', bg='#0d5f0d').pack()
        
        special_bets = [
            ("ROJO", "rojo", "#DC143C"),
            ("NEGRO", "negro", "black"),
            ("PAR", "par", "#4169E1"),
            ("IMPAR", "impar", "#4169E1"),
            ("1-18", "bajo", "#228B22"),
            ("19-36", "alto", "#228B22"),
            ("1er Tercio", "primer_tercio", "#8B008B"),
            ("2do Tercio", "segundo_tercio", "#8B008B"),
            ("3er Tercio", "tercer_tercio", "#8B008B")
        ]
        
        special_container = tk.Frame(special_frame, bg='#0d5f0d')
        special_container.pack(pady=5)
        
        for i, (texto, tipo, color) in enumerate(special_bets):
            if i % 3 == 0:
                row_frame = tk.Frame(special_container, bg='#0d5f0d')
                row_frame.pack()
            
            btn = tk.Button(row_frame, text=texto, 
                           command=lambda t=tipo: self.apostar_especial(t),
                           font=('Arial', 10, 'bold'), 
                           bg=color, fg='white',
                           width=10, height=1, relief=tk.RAISED, bd=2)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def dibujar_rueda(self):
        """Dibuja la rueda de la ruleta"""
        self.wheel_canvas.delete("all")
        center_x, center_y = 175, 175
        radius = 150
        
        # Dibujar el borde exterior
        self.wheel_canvas.create_oval(center_x - radius - 10, center_y - radius - 10,
                                     center_x + radius + 10, center_y + radius + 10,
                                     fill='#8B4513', outline='gold', width=5)
        
        # Calcular ángulo por sección
        angle_per_section = 360 / len(self.orden_rueda)
        
        # Dibujar cada sección
        for i, numero in enumerate(self.orden_rueda):
            start_angle = (i * angle_per_section + self.angulo_rueda) % 360
            
            # Determinar color
            if numero == 0:
                color = 'green'
            elif numero in self.numeros_rojos:
                color = '#DC143C'
            else:
                color = 'black'
            
            # Dibujar sección
            self.wheel_canvas.create_arc(center_x - radius, center_y - radius,
                                       center_x + radius, center_y + radius,
                                       start=start_angle, extent=angle_per_section,
                                       fill=color, outline='gold', width=2)
            
            # Calcular posición para el número
            angle_rad = math.radians(start_angle + angle_per_section / 2)
            text_radius = radius * 0.8
            text_x = center_x + text_radius * math.cos(angle_rad)
            text_y = center_y - text_radius * math.sin(angle_rad)
            
            # Dibujar número
            self.wheel_canvas.create_text(text_x, text_y, text=str(numero),
                                        font=('Arial', 10, 'bold'), fill='white')
        
        # Dibujar centro
        self.wheel_canvas.create_oval(center_x - 20, center_y - 20,
                                    center_x + 20, center_y + 20,
                                    fill='gold', outline='black', width=2)
        
        # Dibujar flecha indicadora
        arrow_points = [center_x, center_y - radius - 15,
                       center_x - 10, center_y - radius - 5,
                       center_x + 10, center_y - radius - 5]
        self.wheel_canvas.create_polygon(arrow_points, fill='gold', outline='black', width=2)
    
    def apostar_numero(self, numero):
        """Apuesta a un número específico"""
        cantidad = self.cantidad_apuesta.get()
        if cantidad > self.dinero:
            messagebox.showwarning("Dinero insuficiente", 
                                 f"No tienes suficiente dinero para apostar ${cantidad}")
            return
        
        if self.girando:
            messagebox.showinfo("Ruleta girando", "Espera a que termine el giro actual")
            return
        
        apuesta_key = f"numero_{numero}"
        if apuesta_key in self.apuestas:
            self.apuestas[apuesta_key] += cantidad
        else:
            self.apuestas[apuesta_key] = cantidad
        
        self.dinero -= cantidad
        self.actualizar_dinero()
        self.actualizar_apuestas_display()
    
    def apostar_especial(self, tipo):
        """Apuesta especial (rojo, negro, par, impar, etc.)"""
        cantidad = self.cantidad_apuesta.get()
        if cantidad > self.dinero:
            messagebox.showwarning("Dinero insuficiente", 
                                 f"No tienes suficiente dinero para apostar ${cantidad}")
            return
        
        if self.girando:
            messagebox.showinfo("Ruleta girando", "Espera a que termine el giro actual")
            return
        
        if tipo in self.apuestas:
            self.apuestas[tipo] += cantidad
        else:
            self.apuestas[tipo] = cantidad
        
        self.dinero -= cantidad
        self.actualizar_dinero()
        self.actualizar_apuestas_display()
    
    def girar_ruleta(self):
        """Gira la ruleta y determina el número ganador"""
        if not self.apuestas:
            messagebox.showinfo("Sin apuestas", "Debes hacer al menos una apuesta")
            return
        
        if self.girando:
            return
        
        self.girando = True
        self.girar_btn.config(state=tk.DISABLED)
        
        # Generar número ganador
        self.numero_ganador = random.choice(self.numeros_ruleta)
        
        # Animación de giro
        self.animar_giro()
    
    def animar_giro(self, vueltas=0):
        """Animación del giro de la ruleta"""
        if vueltas < 30:  # 30 frames de animación
            # Calcular velocidad decreciente
            velocidad = max(1, 20 - vueltas // 2)
            self.angulo_rueda = (self.angulo_rueda + velocidad) % 360
            
            self.dibujar_rueda()
            self.root.after(50, lambda: self.animar_giro(vueltas + 1))
        else:
            # Posicionar en el número ganador
            index_ganador = self.orden_rueda.index(self.numero_ganador)
            angle_per_section = 360 / len(self.orden_rueda)
            self.angulo_rueda = 360 - (index_ganador * angle_per_section)
            
            self.dibujar_rueda()
            self.mostrar_resultado()
    
    def mostrar_resultado(self):
        """Muestra el resultado y calcula ganancias"""
        numero = self.numero_ganador
        
        # Determinar color del número
        if numero == 0:
            color_texto = "VERDE"
            color_bg = 'green'
        elif numero in self.numeros_rojos:
            color_texto = "ROJO"
            color_bg = '#DC143C'
        else:
            color_texto = "NEGRO"
            color_bg = 'black'
        
        # Actualizar display del resultado
        self.resultado_label.config(text=f"¡{numero} {color_texto}!", 
                                   fg='white', bg=color_bg)
        
        # Calcular ganancias
        ganancias_totales = 0
        mensaje_ganancias = []
        
        for apuesta, cantidad in self.apuestas.items():
            ganancia = self.calcular_ganancia(apuesta, cantidad, numero)
            if ganancia > 0:
                ganancias_totales += ganancia
                tipo_apuesta = apuesta.replace('numero_', '').replace('_', ' ').upper()
                mensaje_ganancias.append(f"{tipo_apuesta}: +${ganancia}")
        
        # Actualizar dinero
        self.dinero += ganancias_totales
        self.actualizar_dinero()
        
        # Mostrar mensaje de resultado
        if ganancias_totales > 0:
            mensaje = f"🎉 ¡GANASTE ${ganancias_totales}!\n\n" + "\n".join(mensaje_ganancias)
            messagebox.showinfo("¡Felicitaciones!", mensaje)
        else:
            total_perdido = sum(self.apuestas.values())
            messagebox.showinfo("Mejor suerte la próxima vez", 
                               f"Perdiste ${total_perdido}. ¡Inténtalo de nuevo!")
        
        # Limpiar apuestas y reactivar botón
        self.limpiar_apuestas()
        self.girando = False
        self.girar_btn.config(state=tk.NORMAL)
        
        # Verificar si se quedó sin dinero
        if self.dinero <= 0:
            messagebox.showinfo("Game Over", "¡Te quedaste sin dinero! Usa RESET para empezar de nuevo.")
    
    def calcular_ganancia(self, apuesta, cantidad, numero):
        """Calcula la ganancia para una apuesta específica"""
        # Apuesta a número específico (paga 35:1)
        if apuesta.startswith('numero_'):
            num_apostado = int(apuesta.split('_')[1])
            if num_apostado == numero:
                return cantidad * 35
        
        # Apuestas especiales (pagan 1:1)
        elif apuesta == 'rojo' and numero in self.numeros_rojos:
            return cantidad * 1
        elif apuesta == 'negro' and numero in self.numeros_negros:
            return cantidad * 1
        elif apuesta == 'par' and numero > 0 and numero % 2 == 0:
            return cantidad * 1
        elif apuesta == 'impar' and numero % 2 == 1:
            return cantidad * 1
        elif apuesta == 'bajo' and 1 <= numero <= 18:
            return cantidad * 1
        elif apuesta == 'alto' and 19 <= numero <= 36:
            return cantidad * 1
        elif apuesta == 'primer_tercio' and 1 <= numero <= 12:
            return cantidad * 2
        elif apuesta == 'segundo_tercio' and 13 <= numero <= 24:
            return cantidad * 2
        elif apuesta == 'tercer_tercio' and 25 <= numero <= 36:
            return cantidad * 2
        
        return 0
    
    def actualizar_dinero(self):
        """Actualiza la visualización del dinero"""
        self.dinero_label.config(text=f"💰 Dinero: ${self.dinero}")
    
    def actualizar_apuestas_display(self):
        """Actualiza la visualización de las apuestas actuales"""
        if not self.apuestas:
            self.apuestas_label.config(text="Apuestas: Ninguna")
        else:
            total = sum(self.apuestas.values())
            apuestas_texto = []
            for apuesta, cantidad in self.apuestas.items():
                nombre = apuesta.replace('numero_', '').replace('_', ' ').upper()
                apuestas_texto.append(f"{nombre}: ${cantidad}")
            
            texto = f"Apuestas (Total: ${total}):\n" + " | ".join(apuestas_texto[:5])
            if len(apuestas_texto) > 5:
                texto += f"\n... y {len(apuestas_texto) - 5} más"
            
            self.apuestas_label.config(text=texto)
    
    def limpiar_apuestas(self):
        """Limpia todas las apuestas"""
        if self.girando:
            messagebox.showinfo("Ruleta girando", "No puedes limpiar apuestas mientras gira la ruleta")
            return
        
        # Devolver dinero de las apuestas
        total_devuelto = sum(self.apuestas.values())
        self.dinero += total_devuelto
        
        self.apuestas = {}
        self.actualizar_dinero()
        self.actualizar_apuestas_display()
    
    def reset_juego(self):
        """Reinicia completamente el juego"""
        self.dinero = 1000
        self.apuestas = {}
        self.numero_ganador = None
        self.girando = False
        self.angulo_rueda = 0
        
        self.actualizar_dinero()
        self.actualizar_apuestas_display()
        self.resultado_label.config(text="Resultado: -", fg='white', bg='#0d5f0d')
        self.girar_btn.config(state=tk.NORMAL)
        self.dibujar_rueda()
        
        messagebox.showinfo("Juego reiniciado", "¡Vuelves a empezar con $1000!")

def main():
    root = tk.Tk()
    ruleta = RuletaCasino(root)
    root.mainloop()

if __name__ == "__main__":
    main()
