import sys
import io
import random
import unittest
from game import Game
from game_old import GameOld

class TriviaGoldenMasterTest(unittest.TestCase):
    def test_golden_master_10k_runs(self):
        # Ejecutamos 10,000 pruebas simuladas para cumplir con el Golden Master
        for run in range(10000):
            # Fijamos la semilla usando el número de corrida para que ambas ejecuciones reciban lo mismo
            seed = run
            
            # 1. Capturar salida del código viejo (Oráculo)
            output_old = self._simulate_game(GameOld(), seed)
            
            # 2. Capturar salida del código refactorizado (Tu versión limpia)
            output_new = self._simulate_game(Game(), seed)
            
            # 3. Comparación estricta del Golden Master
            if output_old != output_new:
                self.fail(f"¡El Golden Master falló en la corrida {run}! Las salidas no coinciden.")

    def _simulate_game(self, game_instance, seed):
        random.seed(seed)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            game_instance.add('Chet')
            game_instance.add('Pat')
            game_instance.add('Sue')
            
            while True:
                game_instance.roll(random.randrange(5) + 1)
                
                if random.randrange(9) == 7:
                    not_a_winner = game_instance.wrong_answer()
                else:
                    not_a_winner = game_instance.was_correctly_answered()
                    
                if not not_a_winner:
                    break
        finally:
            sys.stdout = sys.__stdout__
            
        return captured_output.getvalue()

if __name__ == '__main__':
    unittest.main()