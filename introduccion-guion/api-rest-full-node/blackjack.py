import random

class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor
    
    def __str__(self):
        return f"{self.valor} de {self.palo}"
    
    def valor_numerico(self):
        """Devuelve el valor numérico de la carta"""
        if self.valor in ['J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 11  # El As se manejará como 11 o 1 según convenga
        else:
            return int(self.valor)

class Mazo:
    def __init__(self):
        self.cartas = []
        self.crear_mazo()
        self.mezclar()
    
    def crear_mazo(self):
        """Crea un mazo completo de 52 cartas"""
        palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        for palo in palos:
            for valor in valores:
                self.cartas.append(Carta(palo, valor))
    
    def mezclar(self):
        """Mezcla las cartas del mazo"""
        random.shuffle(self.cartas)
    
    def repartir_carta(self):
        """Reparte una carta del mazo"""
        if len(self.cartas) == 0:
            print("El mazo está vacío, creando uno nuevo...")
            self.crear_mazo()
            self.mezclar()
        return self.cartas.pop()

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.dinero = 1000  # Dinero inicial
    
    def recibir_carta(self, carta):
        """Añade una carta a la mano del jugador"""
        self.mano.append(carta)
    
    def mostrar_mano(self, ocultar_primera=False):
        """Muestra las cartas de la mano"""
        if ocultar_primera and len(self.mano) > 1:
            print(f"{self.nombre}: [OCULTA], {', '.join(str(carta) for carta in self.mano[1:])}")
        else:
            print(f"{self.nombre}: {', '.join(str(carta) for carta in self.mano)}")
    
    def calcular_valor_mano(self):
        """Calcula el valor total de la mano"""
        valor = 0
        ases = 0
        
        for carta in self.mano:
            if carta.valor == 'A':
                ases += 1
                valor += 11
            else:
                valor += carta.valor_numerico()
        
        # Ajustar el valor de los ases si es necesario
        while valor > 21 and ases > 0:
            valor -= 10
            ases -= 1
        
        return valor
    
    def tiene_blackjack(self):
        """Verifica si el jugador tiene blackjack (21 con 2 cartas)"""
        return len(self.mano) == 2 and self.calcular_valor_mano() == 21
    
    def limpiar_mano(self):
        """Limpia la mano del jugador"""
        self.mano = []

class BlackjackGame:
    def __init__(self):
        self.mazo = Mazo()
        self.jugador = Jugador("Jugador")
        self.dealer = Jugador("Dealer")
        self.apuesta_actual = 0
    
    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida"""
        print("=" * 50)
        print("🃏 BIENVENIDO AL BLACKJACK 🃏")
        print("=" * 50)
        print(f"Tienes ${self.jugador.dinero} para apostar")
        print("¡Buena suerte!")
        print()
    
    def realizar_apuesta(self):
        """Permite al jugador realizar una apuesta"""
        while True:
            try:
                print(f"Dinero disponible: ${self.jugador.dinero}")
                apuesta = input("¿Cuánto quieres apostar? (o 'salir' para terminar): ")
                
                if apuesta.lower() == 'salir':
                    return False
                
                apuesta = int(apuesta)
                
                if apuesta <= 0:
                    print("La apuesta debe ser mayor a 0")
                    continue
                
                if apuesta > self.jugador.dinero:
                    print("No tienes suficiente dinero")
                    continue
                
                self.apuesta_actual = apuesta
                return True
                
            except ValueError:
                print("Por favor ingresa un número válido")
    
    def repartir_cartas_iniciales(self):
        """Reparte las cartas iniciales"""
        # Dar 2 cartas al jugador y 2 al dealer
        for _ in range(2):
            self.jugador.recibir_carta(self.mazo.repartir_carta())
            self.dealer.recibir_carta(self.mazo.repartir_carta())
    
    def mostrar_manos(self, ocultar_dealer=True):
        """Muestra las manos de ambos jugadores"""
        print("\n" + "=" * 30)
        self.jugador.mostrar_mano()
        print(f"Valor de tu mano: {self.jugador.calcular_valor_mano()}")
        print()
        self.dealer.mostrar_mano(ocultar_primera=ocultar_dealer)
        if not ocultar_dealer:
            print(f"Valor de la mano del dealer: {self.dealer.calcular_valor_mano()}")
        print("=" * 30)
    
    def turno_jugador(self):
        """Maneja el turno del jugador"""
        while True:
            valor_mano = self.jugador.calcular_valor_mano()
            
            if valor_mano > 21:
                print("\n¡Te pasaste de 21! Perdiste 😞")
                return False
            
            if valor_mano == 21:
                print("\n¡Tienes 21! 🎉")
                return True
            
            accion = input("\n¿Qué quieres hacer? (h)it para pedir carta, (s)tand para plantarse: ").lower()
            
            if accion == 'h' or accion == 'hit':
                carta = self.mazo.repartir_carta()
                self.jugador.recibir_carta(carta)
                print(f"Recibiste: {carta}")
                self.mostrar_manos()
            elif accion == 's' or accion == 'stand':
                return True
            else:
                print("Opción no válida. Usa 'h' para hit o 's' para stand")
    
    def turno_dealer(self):
        """Maneja el turno del dealer"""
        print("\n¡Turno del dealer!")
        self.mostrar_manos(ocultar_dealer=False)
        
        while self.dealer.calcular_valor_mano() < 17:
            carta = self.mazo.repartir_carta()
            self.dealer.recibir_carta(carta)
            print(f"El dealer recibe: {carta}")
            self.mostrar_manos(ocultar_dealer=False)
            input("Presiona Enter para continuar...")
        
        valor_dealer = self.dealer.calcular_valor_mano()
        if valor_dealer > 21:
            print("¡El dealer se pasó de 21!")
            return False
        
        return True
    
    def determinar_ganador(self):
        """Determina el ganador de la ronda"""
        valor_jugador = self.jugador.calcular_valor_mano()
        valor_dealer = self.dealer.calcular_valor_mano()
        
        print(f"\nTu mano: {valor_jugador}")
        print(f"Mano del dealer: {valor_dealer}")
        
        # Verificar blackjack
        jugador_blackjack = self.jugador.tiene_blackjack()
        dealer_blackjack = self.dealer.tiene_blackjack()
        
        if jugador_blackjack and dealer_blackjack:
            print("¡Ambos tienen Blackjack! Es un empate 🤝")
            return "empate"
        elif jugador_blackjack:
            print("¡BLACKJACK! Ganaste 🎉")
            ganancia = int(self.apuesta_actual * 1.5)
            self.jugador.dinero += ganancia
            print(f"Ganaste ${ganancia}")
            return "jugador"
        elif dealer_blackjack:
            print("El dealer tiene Blackjack. Perdiste 😞")
            self.jugador.dinero -= self.apuesta_actual
            print(f"Perdiste ${self.apuesta_actual}")
            return "dealer"
        
        # Comparar valores normales
        if valor_jugador > 21:
            print("Te pasaste de 21. Perdiste 😞")
            self.jugador.dinero -= self.apuesta_actual
            print(f"Perdiste ${self.apuesta_actual}")
            return "dealer"
        elif valor_dealer > 21:
            print("El dealer se pasó de 21. ¡Ganaste! 🎉")
            self.jugador.dinero += self.apuesta_actual
            print(f"Ganaste ${self.apuesta_actual}")
            return "jugador"
        elif valor_jugador > valor_dealer:
            print("¡Tu mano es mejor! Ganaste 🎉")
            self.jugador.dinero += self.apuesta_actual
            print(f"Ganaste ${self.apuesta_actual}")
            return "jugador"
        elif valor_dealer > valor_jugador:
            print("La mano del dealer es mejor. Perdiste 😞")
            self.jugador.dinero -= self.apuesta_actual
            print(f"Perdiste ${self.apuesta_actual}")
            return "dealer"
        else:
            print("¡Es un empate! 🤝")
            return "empate"
    
    def jugar_ronda(self):
        """Juega una ronda completa"""
        # Realizar apuesta
        if not self.realizar_apuesta():
            return False
        
        # Limpiar manos previas
        self.jugador.limpiar_mano()
        self.dealer.limpiar_mano()
        
        # Repartir cartas iniciales
        self.repartir_cartas_iniciales()
        self.mostrar_manos()
        
        # Verificar blackjack inmediato
        if self.jugador.tiene_blackjack() or self.dealer.tiene_blackjack():
            self.mostrar_manos(ocultar_dealer=False)
            self.determinar_ganador()
            return True
        
        # Turno del jugador
        if not self.turno_jugador():
            self.determinar_ganador()
            return True
        
        # Turno del dealer
        self.turno_dealer()
        
        # Determinar ganador
        self.determinar_ganador()
        
        return True
    
    def jugar(self):
        """Función principal del juego"""
        self.mostrar_bienvenida()
        
        while self.jugador.dinero > 0:
            print(f"\n💰 Dinero actual: ${self.jugador.dinero}")
            
            if not self.jugar_ronda():
                break
            
            if self.jugador.dinero <= 0:
                print("\n💸 Te quedaste sin dinero. ¡Fin del juego!")
                break
            
            jugar_otra = input("\n¿Quieres jugar otra ronda? (s/n): ").lower()
            if jugar_otra != 's' and jugar_otra != 'si' and jugar_otra != 'sí':
                break
        
        print(f"\n🎮 Gracias por jugar! Terminaste con ${self.jugador.dinero}")
        if self.jugador.dinero > 1000:
            print("¡Felicidades! Ganaste dinero 🎉")
        elif self.jugador.dinero < 1000:
            print("Mejor suerte la próxima vez 😊")
        else:
            print("¡Terminaste igual que empezaste! 😄")

# Ejecutar el juego
if __name__ == "__main__":
    juego = BlackjackGame()
    juego.jugar()
