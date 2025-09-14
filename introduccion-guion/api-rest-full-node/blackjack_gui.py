import tkinter as tk
from tkinter import ttk, messagebox
import random

class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor
    
    def __str__(self):
        return f"{self.valor}{self.get_palo_symbol()}"
    
    def get_palo_symbol(self):
        symbols = {'Corazones': '♥', 'Diamantes': '♦', 'Tréboles': '♣', 'Picas': '♠'}
        return symbols.get(self.palo, self.palo)
    
    def get_color(self):
        return 'red' if self.palo in ['Corazones', 'Diamantes'] else 'black'
    
    def valor_numerico(self):
        if self.valor in ['J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 11
        else:
            return int(self.valor)

class Mazo:
    def __init__(self):
        self.cartas = []
        self.crear_mazo()
        self.mezclar()
    
    def crear_mazo(self):
        palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        for palo in palos:
            for valor in valores:
                self.cartas.append(Carta(palo, valor))
    
    def mezclar(self):
        random.shuffle(self.cartas)
    
    def repartir_carta(self):
        if len(self.cartas) == 0:
            self.crear_mazo()
            self.mezclar()
        return self.cartas.pop()

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🃏 Blackjack Casino 🃏")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0d5f0d')  # Verde casino
        self.root.resizable(False, False)
        
        # Variables del juego
        self.mazo = Mazo()
        self.mano_jugador = []
        self.mano_dealer = []
        self.dinero = 1000
        self.apuesta_actual = 0
        self.juego_activo = False
        self.dealer_oculta = True
        
        self.crear_interfaz()
        self.actualizar_dinero()
    
    def crear_interfaz(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#0d5f0d')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="🃏 BLACKJACK CASINO 🃏", 
                              font=('Arial', 24, 'bold'), 
                              fg='gold', bg='#0d5f0d')
        title_label.pack()
        
        # Frame del dealer
        dealer_frame = tk.LabelFrame(self.root, text="🎩 DEALER", 
                                    font=('Arial', 14, 'bold'),
                                    fg='white', bg='#0d5f0d', 
                                    relief=tk.RAISED, bd=3)
        dealer_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.dealer_cards_frame = tk.Frame(dealer_frame, bg='#0d5f0d')
        self.dealer_cards_frame.pack(pady=10)
        
        self.dealer_value_label = tk.Label(dealer_frame, text="Valor: ?", 
                                          font=('Arial', 12, 'bold'),
                                          fg='white', bg='#0d5f0d')
        self.dealer_value_label.pack()
        
        # Frame del jugador
        player_frame = tk.LabelFrame(self.root, text="🎲 JUGADOR", 
                                    font=('Arial', 14, 'bold'),
                                    fg='white', bg='#0d5f0d',
                                    relief=tk.RAISED, bd=3)
        player_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.player_cards_frame = tk.Frame(player_frame, bg='#0d5f0d')
        self.player_cards_frame.pack(pady=10)
        
        self.player_value_label = tk.Label(player_frame, text="Valor: 0", 
                                          font=('Arial', 12, 'bold'),
                                          fg='white', bg='#0d5f0d')
        self.player_value_label.pack()
        
        # Frame de información y apuestas
        info_frame = tk.Frame(self.root, bg='#0d5f0d')
        info_frame.pack(pady=10)
        
        # Dinero y apuesta
        money_frame = tk.Frame(info_frame, bg='#0d5f0d')
        money_frame.pack(side=tk.LEFT, padx=20)
        
        self.dinero_label = tk.Label(money_frame, text=f"💰 Dinero: ${self.dinero}", 
                                    font=('Arial', 14, 'bold'),
                                    fg='gold', bg='#0d5f0d')
        self.dinero_label.pack()
        
        self.apuesta_label = tk.Label(money_frame, text="🎯 Apuesta: $0", 
                                     font=('Arial', 12, 'bold'),
                                     fg='white', bg='#0d5f0d')
        self.apuesta_label.pack()
        
        # Frame de apuestas
        bet_frame = tk.Frame(info_frame, bg='#0d5f0d')
        bet_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(bet_frame, text="Apostar:", font=('Arial', 12, 'bold'),
                fg='white', bg='#0d5f0d').pack()
        
        bet_buttons_frame = tk.Frame(bet_frame, bg='#0d5f0d')
        bet_buttons_frame.pack()
        
        bet_amounts = [10, 25, 50, 100, 250]
        for amount in bet_amounts:
            btn = tk.Button(bet_buttons_frame, text=f"${amount}", 
                           command=lambda a=amount: self.apostar(a),
                           font=('Arial', 10, 'bold'),
                           bg='#1a4a1a', fg='white', 
                           relief=tk.RAISED, bd=2,
                           width=6, height=1)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Botón apostar todo
        all_in_btn = tk.Button(bet_buttons_frame, text="TODO", 
                              command=self.apostar_todo,
                              font=('Arial', 10, 'bold'),
                              bg='#8b0000', fg='white', 
                              relief=tk.RAISED, bd=2,
                              width=6, height=1)
        all_in_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame de controles del juego
        controls_frame = tk.Frame(self.root, bg='#0d5f0d')
        controls_frame.pack(pady=20)
        
        # Botones principales
        self.nuevo_juego_btn = tk.Button(controls_frame, text="🃏 NUEVO JUEGO", 
                                        command=self.nuevo_juego,
                                        font=('Arial', 14, 'bold'),
                                        bg='#4CAF50', fg='white',
                                        relief=tk.RAISED, bd=3,
                                        width=12, height=2)
        self.nuevo_juego_btn.pack(side=tk.LEFT, padx=10)
        
        self.hit_btn = tk.Button(controls_frame, text="🎯 HIT", 
                                command=self.hit,
                                font=('Arial', 14, 'bold'),
                                bg='#2196F3', fg='white',
                                relief=tk.RAISED, bd=3,
                                width=8, height=2,
                                state=tk.DISABLED)
        self.hit_btn.pack(side=tk.LEFT, padx=10)
        
        self.stand_btn = tk.Button(controls_frame, text="✋ STAND", 
                                  command=self.stand,
                                  font=('Arial', 14, 'bold'),
                                  bg='#FF9800', fg='white',
                                  relief=tk.RAISED, bd=3,
                                  width=8, height=2,
                                  state=tk.DISABLED)
        self.stand_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_btn = tk.Button(controls_frame, text="🔄 RESET", 
                                  command=self.reset_juego,
                                  font=('Arial', 14, 'bold'),
                                  bg='#9C27B0', fg='white',
                                  relief=tk.RAISED, bd=3,
                                  width=8, height=2)
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
        # Frame de mensajes
        self.mensaje_frame = tk.Frame(self.root, bg='#0d5f0d')
        self.mensaje_frame.pack(pady=10)
        
        self.mensaje_label = tk.Label(self.mensaje_frame, text="¡Haz una apuesta para comenzar!", 
                                     font=('Arial', 16, 'bold'),
                                     fg='yellow', bg='#0d5f0d')
        self.mensaje_label.pack()
    
    def crear_carta_visual(self, carta, oculta=False):
        """Crea una representación visual de una carta"""
        canvas = tk.Canvas(self.root, width=80, height=110, 
                          bg='white', relief=tk.RAISED, bd=2)
        
        if oculta:
            # Carta oculta (dorso)
            canvas.create_rectangle(5, 5, 75, 105, fill='#0d47a1', outline='black', width=2)
            canvas.create_text(40, 55, text="🃏", font=('Arial', 20), fill='white')
        else:
            # Carta visible
            color = carta.get_color()
            canvas.create_rectangle(5, 5, 75, 105, fill='white', outline='black', width=2)
            
            # Valor en la esquina superior izquierda
            canvas.create_text(15, 20, text=carta.valor, font=('Arial', 12, 'bold'), fill=color)
            canvas.create_text(15, 35, text=carta.get_palo_symbol(), font=('Arial', 12), fill=color)
            
            # Símbolo grande en el centro
            canvas.create_text(40, 55, text=carta.get_palo_symbol(), font=('Arial', 24), fill=color)
            
            # Valor en la esquina inferior derecha (invertido)
            canvas.create_text(65, 90, text=carta.valor, font=('Arial', 12, 'bold'), fill=color, angle=180)
            canvas.create_text(65, 75, text=carta.get_palo_symbol(), font=('Arial', 12), fill=color, angle=180)
        
        return canvas
    
    def calcular_valor_mano(self, mano):
        """Calcula el valor de una mano considerando los ases"""
        valor = 0
        ases = 0
        
        for carta in mano:
            if carta.valor == 'A':
                ases += 1
                valor += 11
            else:
                valor += carta.valor_numerico()
        
        while valor > 21 and ases > 0:
            valor -= 10
            ases -= 1
        
        return valor
    
    def tiene_blackjack(self, mano):
        """Verifica si una mano tiene blackjack"""
        return len(mano) == 2 and self.calcular_valor_mano(mano) == 21
    
    def apostar(self, cantidad):
        """Realiza una apuesta"""
        if cantidad > self.dinero:
            messagebox.showwarning("Dinero insuficiente", 
                                 f"No tienes suficiente dinero para apostar ${cantidad}")
            return
        
        if self.juego_activo:
            messagebox.showinfo("Juego en curso", "Termina la ronda actual antes de cambiar la apuesta")
            return
        
        self.apuesta_actual = cantidad
        self.actualizar_apuesta()
        self.mensaje_label.config(text=f"Apuesta: ${cantidad}. ¡Presiona 'NUEVO JUEGO' para comenzar!")
    
    def apostar_todo(self):
        """Apuesta todo el dinero disponible"""
        self.apostar(self.dinero)
    
    def actualizar_dinero(self):
        """Actualiza la visualización del dinero"""
        self.dinero_label.config(text=f"💰 Dinero: ${self.dinero}")
    
    def actualizar_apuesta(self):
        """Actualiza la visualización de la apuesta"""
        self.apuesta_label.config(text=f"🎯 Apuesta: ${self.apuesta_actual}")
    
    def limpiar_cartas(self):
        """Limpia las cartas de la mesa"""
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
    
    def mostrar_cartas_jugador(self):
        """Muestra las cartas del jugador"""
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        for i, carta in enumerate(self.mano_jugador):
            carta_canvas = self.crear_carta_visual(carta)
            carta_canvas.pack(side=tk.LEFT, padx=2)
            carta_canvas.master = self.player_cards_frame
        
        valor = self.calcular_valor_mano(self.mano_jugador)
        self.player_value_label.config(text=f"Valor: {valor}")
    
    def mostrar_cartas_dealer(self):
        """Muestra las cartas del dealer"""
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        
        for i, carta in enumerate(self.mano_dealer):
            # Primera carta oculta si el juego está activo
            oculta = i == 0 and self.dealer_oculta and self.juego_activo
            carta_canvas = self.crear_carta_visual(carta, oculta)
            carta_canvas.pack(side=tk.LEFT, padx=2)
            carta_canvas.master = self.dealer_cards_frame
        
        if self.dealer_oculta and self.juego_activo:
            self.dealer_value_label.config(text="Valor: ?")
        else:
            valor = self.calcular_valor_mano(self.mano_dealer)
            self.dealer_value_label.config(text=f"Valor: {valor}")
    
    def nuevo_juego(self):
        """Inicia un nuevo juego"""
        if self.apuesta_actual == 0:
            messagebox.showwarning("Sin apuesta", "Debes hacer una apuesta antes de comenzar")
            return
        
        if self.dinero < self.apuesta_actual:
            messagebox.showwarning("Dinero insuficiente", "No tienes suficiente dinero para esta apuesta")
            return
        
        # Reiniciar variables
        self.mano_jugador = []
        self.mano_dealer = []
        self.juego_activo = True
        self.dealer_oculta = True
        
        # Repartir cartas iniciales
        for _ in range(2):
            self.mano_jugador.append(self.mazo.repartir_carta())
            self.mano_dealer.append(self.mazo.repartir_carta())
        
        self.mostrar_cartas_jugador()
        self.mostrar_cartas_dealer()
        
        # Verificar blackjack inmediato
        if self.tiene_blackjack(self.mano_jugador):
            if self.tiene_blackjack(self.mano_dealer):
                self.terminar_juego("¡Ambos tienen Blackjack! Empate 🤝", "empate")
            else:
                self.terminar_juego("¡BLACKJACK! Ganaste 🎉", "blackjack")
        elif self.tiene_blackjack(self.mano_dealer):
            self.revelar_cartas_dealer()
            self.terminar_juego("El dealer tiene Blackjack. Perdiste 😞", "dealer")
        else:
            # Activar botones de juego
            self.hit_btn.config(state=tk.NORMAL)
            self.stand_btn.config(state=tk.NORMAL)
            self.nuevo_juego_btn.config(state=tk.DISABLED)
            self.mensaje_label.config(text="¡Tu turno! Elige HIT o STAND")
    
    def hit(self):
        """Pide una carta"""
        if not self.juego_activo:
            return
        
        carta = self.mazo.repartir_carta()
        self.mano_jugador.append(carta)
        self.mostrar_cartas_jugador()
        
        valor = self.calcular_valor_mano(self.mano_jugador)
        if valor > 21:
            self.terminar_juego("¡Te pasaste de 21! Perdiste 😞", "bust")
        elif valor == 21:
            self.stand()  # Automáticamente se planta con 21
    
    def stand(self):
        """El jugador se planta"""
        if not self.juego_activo:
            return
        
        # Revelar carta oculta del dealer
        self.revelar_cartas_dealer()
        
        # Turno del dealer
        self.root.after(1000, self.turno_dealer)
    
    def revelar_cartas_dealer(self):
        """Revela todas las cartas del dealer"""
        self.dealer_oculta = False
        self.mostrar_cartas_dealer()
    
    def turno_dealer(self):
        """Ejecuta el turno del dealer"""
        valor_dealer = self.calcular_valor_mano(self.mano_dealer)
        
        if valor_dealer < 17:
            # Dealer debe tomar carta
            carta = self.mazo.repartir_carta()
            self.mano_dealer.append(carta)
            self.mostrar_cartas_dealer()
            
            # Continuar después de 1 segundo
            self.root.after(1000, self.turno_dealer)
        else:
            # Dealer se planta, determinar ganador
            self.determinar_ganador()
    
    def determinar_ganador(self):
        """Determina el ganador final"""
        valor_jugador = self.calcular_valor_mano(self.mano_jugador)
        valor_dealer = self.calcular_valor_mano(self.mano_dealer)
        
        if valor_dealer > 21:
            self.terminar_juego("¡El dealer se pasó de 21! Ganaste 🎉", "jugador")
        elif valor_jugador > valor_dealer:
            self.terminar_juego("¡Tu mano es mejor! Ganaste 🎉", "jugador")
        elif valor_dealer > valor_jugador:
            self.terminar_juego("La mano del dealer es mejor. Perdiste 😞", "dealer")
        else:
            self.terminar_juego("¡Empate! 🤝", "empate")
    
    def terminar_juego(self, mensaje, resultado):
        """Termina el juego y actualiza el dinero"""
        self.juego_activo = False
        
        # Actualizar dinero según el resultado
        if resultado == "jugador":
            self.dinero += self.apuesta_actual
        elif resultado == "blackjack":
            ganancia = int(self.apuesta_actual * 1.5)
            self.dinero += ganancia
            mensaje += f" (Ganaste ${ganancia})"
        elif resultado == "dealer" or resultado == "bust":
            self.dinero -= self.apuesta_actual
            mensaje += f" (Perdiste ${self.apuesta_actual})"
        
        self.actualizar_dinero()
        self.mensaje_label.config(text=mensaje)
        
        # Desactivar botones de juego
        self.hit_btn.config(state=tk.DISABLED)
        self.stand_btn.config(state=tk.DISABLED)
        self.nuevo_juego_btn.config(state=tk.NORMAL)
        
        # Verificar si se quedó sin dinero
        if self.dinero <= 0:
            messagebox.showinfo("Game Over", "¡Te quedaste sin dinero! Usa RESET para empezar de nuevo.")
    
    def reset_juego(self):
        """Reinicia completamente el juego"""
        self.dinero = 1000
        self.apuesta_actual = 0
        self.juego_activo = False
        self.mano_jugador = []
        self.mano_dealer = []
        self.dealer_oculta = True
        
        self.limpiar_cartas()
        self.actualizar_dinero()
        self.actualizar_apuesta()
        
        self.player_value_label.config(text="Valor: 0")
        self.dealer_value_label.config(text="Valor: ?")
        
        self.hit_btn.config(state=tk.DISABLED)
        self.stand_btn.config(state=tk.DISABLED)
        self.nuevo_juego_btn.config(state=tk.NORMAL)
        
        self.mensaje_label.config(text="¡Juego reiniciado! Haz una apuesta para comenzar.")

def main():
    root = tk.Tk()
    juego = BlackjackGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
