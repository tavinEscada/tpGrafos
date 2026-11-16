import math
from pathlib import Path
import sys
import tempfile
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA / "src"))
from metricasRede import calcular_metricas, distancias_todos_pares
from gerar_instancia3 import salvar


class GrafoSimples:
    def __init__(self, n, arestas):
        self.matriz = [[0] * n for _ in range(n)]
        for a, b, peso in arestas:
            self.matriz[a - 1][b - 1] = peso
            self.matriz[b - 1][a - 1] = peso

    def ordem(self):
        return len(self.matriz)

    def get_matriz(self):
        return self.matriz


class TesteMetricas(unittest.TestCase):
    def test_caminho_ponderado(self):
        g = GrafoSimples(4, [(1, 2, 2.0), (2, 3, 3.0), (3, 4, 4.0), (1, 4, 20.0)])
        r = calcular_metricas(g)
        self.assertEqual(r["diametro"], 9)
        self.assertEqual(r["raio"], 5)
        self.assertEqual(r["centros"], [3])
        self.assertEqual(r["perifericos"], [1, 4])
        self.assertEqual(r["excentricidades"], {1: 9, 2: 7, 3: 5, 4: 9})
        self.assertEqual(r["distancias"][0][3], 9)

    def test_pesos_reais_e_caminho_indireto(self):
        g = GrafoSimples(3, [(1, 2, 0.1), (2, 3, 0.2), (1, 3, 0.4)])
        r = calcular_metricas(g)
        self.assertTrue(math.isclose(r["distancias"][0][2], 0.3))
        self.assertEqual(r["centros"], [2])
        self.assertEqual(r["perifericos"], [1, 3])

    def test_desconexo(self):
        g = GrafoSimples(3, [(1, 2, 1.0)])
        self.assertTrue(math.isinf(distancias_todos_pares(g)[0][2]))
        with self.assertRaisesRegex(ValueError, "conexo"):
            calcular_metricas(g)

    def test_peso_negativo(self):
        with self.assertRaisesRegex(ValueError, "positivos"):
            distancias_todos_pares(GrafoSimples(2, [(1, 2, -1.0)]))

    def test_laco_positivo_nao_altera_distancias(self):
        g = GrafoSimples(2, [(1, 1, 5.0), (1, 2, 2.0)])
        r = calcular_metricas(g)
        self.assertEqual(r["diametro"], 2)
        self.assertEqual(r["raio"], 2)

    def test_gerador_reprodutivel(self):
        with tempfile.TemporaryDirectory() as pasta:
            a = Path(pasta) / "a.txt"
            b = Path(pasta) / "b.txt"
            salvar(a)
            salvar(b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(len(a.read_text().splitlines()), 201)


if __name__ == "__main__":
    unittest.main(verbosity=2)
