import copy, random, time

def minimax(tablero, profundidad, es_turno_max):

    if profundidad == 0 or tablero.es_juego_terminado():
        puntuacion = tablero.evaluar()

        if abs(puntuacion) == 1000:
            return puntuacion - profundidad
        return puntuacion

    if not es_turno_max: 
        mejor_valor = float('inf') 
        movimientos_gato = tablero.obtener_movimientos_validos(tablero.pos_gato)

        for movimiento in movimientos_gato:
            nuevo_tablero = tablero.simular_movimiento('gato', movimiento)
            valor = minimax(nuevo_tablero,profundidad - 1, True)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor
    else: 
        mejor_valor = float('-inf') 
        movimientos_raton = tablero.obtener_movimientos_validos(tablero.pos_raton)

        for movimiento in movimientos_raton:
            nuevo_tablero = tablero.simular_movimiento('raton', movimiento)
            valor = minimax(nuevo_tablero,profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
        
class Tablero:
    def __init__(self, tamanho=5, grid=None, pos_gato=None, pos_raton=None):
        self.tamanho = tamanho
        self.SIMBOLO_GATO = '😼'
        self.SIMBOLO_RATON = '🐭'
        
        if grid is not None:
            self.grid = grid
            self.pos_gato = pos_gato
            self.pos_raton = pos_raton
        else:
            self.grid = [['🧱'] * tamanho for _ in range(tamanho)]
            self.pos_gato = (0,0)
            self.pos_raton = (tamanho - 1, tamanho - 1)
            
            self.grid[self.pos_gato[0]][self.pos_gato[1]] = self.SIMBOLO_GATO 
            self.grid[self.pos_raton[0]][self.pos_raton[1]] = self.SIMBOLO_RATON
    
    def imprimir(self):
        for fila in self.grid:
            print(*fila, sep=" ")

    def obtener_movimientos_validos(self,posicion): 
        fila,col = posicion
        movimientos = []
        cambios = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        # cambios = [
        #     (-1, 0), (1, 0), (0, -1), (0, 1), # Ortogonales
        #     (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
        # ]   
                       
        for cambio_fila, cambio_col in cambios:
            nueva_fila = fila + cambio_fila
            nueva_col = col + cambio_col            
          
            if 0 <= nueva_fila < self.tamanho and 0 <= nueva_col < self.tamanho:
                movimientos.append((nueva_fila,nueva_col))         
        # print(f"DEBUG: Movimientos válidos para la posición {posicion} son: {movimientos}")
        return movimientos

    def simular_movimiento(self, jugador, movimiento):
        if jugador == 'gato':
           simbolo = self.SIMBOLO_GATO
           pos_actual = self.pos_gato
        else:
            simbolo = self.SIMBOLO_RATON
            pos_actual = self.pos_raton
      
        tablero_copia = copy.deepcopy(self.grid)
        # Se guardan las posiciones actuales para el tablero copia
        pos_gato_nueva, pos_raton_nueva = self.pos_gato, self.pos_raton
        # 3. Limpiar la posición anterior y mover al jugador en la copia
        if jugador == 'gato':
            tablero_copia[pos_actual[0]][pos_actual[1]] = '🧱'
            tablero_copia[movimiento[0]][movimiento[1]] = simbolo
            pos_gato_nueva = movimiento  # Actualizar la nueva posición del gato
        else: 
            tablero_copia[pos_actual[0]][pos_actual[1]] = '🧱'
            tablero_copia[movimiento[0]][movimiento[1]] = simbolo
            pos_raton_nueva = movimiento # Actualizar la nueva posición del ratón
        # Devolvemos el tablero modificado
        return Tablero(self.tamanho, tablero_copia, pos_gato_nueva, pos_raton_nueva)

    def evaluar(self):   
        if self.pos_gato == self.pos_raton:
            return -1000   
        # Distancia 1
        # puntuacion = abs(self.pos_raton[0] - self.pos_gato[0]) + abs(self.pos_raton[1] - self.pos_gato[1])
        # Distancia 2 
        # puntuacion = ((self.pos_raton[0] - self.pos_gato[0])**2 + (self.pos_raton[1] - self.pos_gato[1])**2)**1/2
        # Distancia 3
        puntuacion = max(abs(self.pos_raton[0] - self.pos_gato[0]), abs(self.pos_raton[1] - self.pos_gato[1]))       
        #print(f"DEBUG: Gato en {self.pos_gato}, Ratón en {self.pos_raton} -> Puntuacion Chebyshev: {puntuacion}")
        
        return puntuacion    
    
    def mover_raton(self, movimiento):
        self.grid[self.pos_raton[0]][self.pos_raton[1]] = '🧱'
        self.pos_raton = movimiento
        self.grid[self.pos_raton[0]][self.pos_raton[1]] = self.SIMBOLO_RATON
    
    def mover_gato(self, movimiento):
        self.grid[self.pos_gato[0]][self.pos_gato[1]] = '🧱'
        self.pos_gato = movimiento        
        self.grid[self.pos_gato[0]][self.pos_gato[1]] = self.SIMBOLO_GATO
      
    def es_juego_terminado(self):
        return self.pos_gato == self.pos_raton 

class Gato:
    def __init__(self, pos, profundidad_busqueda=4):
        self.pos = pos
        self.profundidad_busqueda = profundidad_busqueda
    
    def decidir_movimiento(self, tablero):
        mejor_movimiento = None
        mejor_valor = float('inf')
        movimientos_gatos = tablero.obtener_movimientos_validos(tablero.pos_gato)
      
        for movimiento in movimientos_gatos:
            nuevo_tablero = tablero.simular_movimiento('gato',movimiento)
            #Llamada al algoritmo minimax
            valor = minimax(nuevo_tablero,self.profundidad_busqueda, es_turno_max=True)
            
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento

        return mejor_movimiento 
        
class Raton:
    def __init__(self, pos, profundidad_busqueda=4):
        self.pos = pos
        self.profundidad_busqueda = profundidad_busqueda
        self.modo_inteligente = False

    def decidir_movimiento(self, tablero):

        if not self.modo_inteligente:
            movimientos_posibles = tablero.obtener_movimientos_validos(tablero.pos_raton)
            return random.choice(movimientos_posibles)
        else: 
            mejor_movimiento = None
            mejor_valor = float('-inf')            
            movimientos_raton = tablero.obtener_movimientos_validos(tablero.pos_raton)
            
            for movimiento in movimientos_raton:
                nuevo_tablero = tablero.simular_movimiento('raton',movimiento)                
                valor = minimax(nuevo_tablero,self.profundidad_busqueda, es_turno_max=False)

                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento

        return mejor_movimiento
          
class Juego:
    def __init__(self,tamanho=5):
        self.tablero = Tablero(tamanho)
        self.turno_actual = 'raton' 
        self.turno_restantes = 15
        
        while True:

            opcion = input("Elige el nivel de dificultad para el ratón( 1 = facil, 2 = normal, 3 = difícil): ")
            try:   
                dificultad = int(opcion)
                if dificultad == 1:
                    profundidad_ia = 2
                    break
                elif dificultad == 2:
                    profundidad_ia = 4
                    break
                elif dificultad == 3:
                    profundidad_ia = 6
                    break
                else:
                    print('Elegir un número de dificultad valida (1, 2 o 3)')
            except ValueError:
                print('Error: Debes ingresar solo un número.')
            
        print(f"Dificultad seleccionada: {dificultad} (profundidad de búsqueda: {profundidad_ia})")

        self.gato = Gato(self.tablero.pos_gato, profundidad_busqueda=profundidad_ia)
        self.raton = Raton(self.tablero.pos_raton)

    def jugar(self):
        turnos_jugados = 0
        while not self.tablero.es_juego_terminado() and self.turno_restantes > 0:
            
            print(f'\n--- Turno {turnos_jugados + 1} ')
            self.tablero.imprimir()

            if self.turno_actual == 'raton':        
                if turnos_jugados >=3:
                    self.raton.modo_inteligente = True

                movimiento = self.raton.decidir_movimiento(self.tablero)
                self.tablero.mover_raton(movimiento)
                self.turno_actual = 'gato'  
            else:
                movimiento = self.gato.decidir_movimiento(self.tablero)
                self.tablero.mover_gato(movimiento)
                self.turno_actual = 'raton'

            turnos_jugados += 1
            self.turno_restantes -= 1

            # time.sleep(0.5)
        
        self.imprimir_resultado()

    def imprimir_resultado(self):
        if self.tablero.pos_gato == self.tablero.pos_raton:
            print('\nEl Gato le comió al ratón! Ganó Tom')
            pos_final = self.tablero.pos_gato
            self.tablero.grid[pos_final[0]][pos_final[1]] = self.tablero.SIMBOLO_GATO
        else:
            print('\nEl ratón se escapó! Gano Jerry')
        
        self.tablero.imprimir()

if __name__ == "__main__":
    juego  = Juego(tamanho=5)
    juego.jugar()