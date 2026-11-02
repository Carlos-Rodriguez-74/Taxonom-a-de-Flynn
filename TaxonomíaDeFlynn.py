import time
from concurrent.futures import ThreadPoolExecutor


class SimuladorFlynn:

  def __init__(self, datos):
    self.datos = datos

  # ----------------------------------------------------
  # 1. SISD (Single Instruction, Single Data)
  # ----------------------------------------------------
  def ejecutar_sisd(self):
    print("\n[SISD] Ejecutando operación secuencial (Un flujo de instrucción y datos)...")
    inicio = time.time()
    
    resultado = []
    for x in self.datos:
      # Una sola instrucción aplicada secuencialmente elemento por elemento.
      res = (x ** 2) + 5
      resultado.append(res)
      
    fin = time.time()
    print(f"   -> Resultado: {resultado[:5]}...")
    print(f"   -> Tiempo SISD: {fin - inicio:.6f} segundos")
    return resultado

  # ----------------------------------------------------
  # 2. SIMD (Single Instruction, Multiple Data)
  # ----------------------------------------------------
  def ejecutar_simd(self):
    print("\n[SIMD] Ejecutando operación paralela (Una instrucción, múltiples datos)...")
    inicio = time.time()

    # La instrucción opera de forma uniforme sobre el conjunto completo de datos.
    resultado = [(x ** 2) + 5 for x in self.datos]
    
    fin = time.time()
    print(f"   -> Resultado: {resultado[:5]}...")
    print(f"   -> Tiempo SIMD: {fin - inicio:.6f} segundos")
    return resultado

  # ----------------------------------------------------
  # 3. MIMD (Multiple Instruction, Multiple Data)
  # ----------------------------------------------------
  def _op_cuadrado(self, subdatos):
    return [x ** 2 for x in subdatos]

  def _op_multiplicar(self, subdatos):
    return [x * 10 for x in subdatos]

  def _op_cubo(self, subdatos):
    return [x ** 3 for x in subdatos]

  def ejecutar_mimd(self):
    print("\n[MIMD] Ejecutando múltiples instrucciones sobre múltiples datos en paralelo...")
    inicio = time.time()
    
    # Se dividen los datos en 3 subconjuntos para aplicarles operaciones diferentes concurrentemente.
    tamanio = len(self.datos) // 3
    sub1 = self.datos[:tamanio]
    sub2 = self.datos[tamanio:tamanio * 2]
    sub3 = self.datos[tamanio * 2:]

    with ThreadPoolExecutor(max_workers=3) as executor:
      # Cada hilo ejecuta una instrucción distinta sobre un subconjunto de datos distinto.
      f1 = executor.submit(self._op_cuadrado, sub1)
      f2 = executor.submit(self._op_multiplicar, sub2)
      f3 = executor.submit(self._op_cubo, sub3)

      res1 = f1.result()
      res2 = f2.result()
      res3 = f3.result()

    fin = time.time()
    print(f"   -> Subconjunto 1 (Al cuadrado): {res1[:3]}...")
    print(f"   -> Subconjunto 2 (Multiplicar x10): {res2[:3]}...")
    print(f"   -> Subconjunto 3 (Al cubo): {res3[:3]}...")
    print(f"   -> Tiempo MIMD: {fin - inicio:.6f} segundos")
    return res1 + res2 + res3


# --- Programa Principal ---
if __name__ == "__main__":
  # Generamos un conjunto de datos grande para notar el comportamiento de cada modelo.
  datos_prueba = list(range(1, 500001))
  
  print(f"=== INICIANDO SIMULACIÓN TAXONOMÍA DE FLYNN ({len(datos_prueba)} elementos) ===")
  
  simulador = SimuladorFlynn(datos_prueba)
  simulador.ejecutar_sisd()
  simulador.ejecutar_simd()
  simulador.ejecutar_mimd()