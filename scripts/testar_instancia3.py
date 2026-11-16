import contextlib
import io
import json
import math
import os
from pathlib import Path
from time import perf_counter
import sys

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA / "src"))
os.chdir(PASTA)

from grafo import Grafo
from busca import busca_largura, componentes_conexas, possui_ciclo
from articulacao import encontra_articulacao
from caminhoMinimo import dijkstra
from Euler import ciclo_euleriano
from ArvoreGeradora import prim
from metricasRede import calcular_metricas


def conferir_arvore(n, arestas):
    pai = list(range(n + 1))

    def raiz(v):
        while pai[v] != v:
            pai[v] = pai[pai[v]]
            v = pai[v]
        return v

    assert len(arestas) == n - 1, "Uma árvore geradora possui n-1 arestas"
    for u, v, _ in arestas:
        a, b = raiz(u), raiz(v)
        assert a != b, "Há ciclo na árvore geradora"
        pai[a] = b
    assert len({raiz(v) for v in range(1, n + 1)}) == 1, "AGM desconexa"


def kruskal_teste(grafo):
    n = grafo.ordem()
    pai = list(range(n + 1))
    rank = [0] * (n + 1)

    def raiz(u):
        while pai[u] != u:
            pai[u] = pai[pai[u]]
            u = pai[u]
        return u

    arestas = [
        (grafo.matriz[u][v], u + 1, v + 1)
        for u in range(n)
        for v in range(u + 1, n)
        if grafo.matriz[u][v] > 0
    ]
    custo = 0.0
    escolhidas = 0
    for peso, u, v in sorted(arestas):
        ru, rv = raiz(u), raiz(v)
        if ru == rv:
            continue
        if rank[ru] < rank[rv]:
            ru, rv = rv, ru
        pai[rv] = ru
        if rank[ru] == rank[rv]:
            rank[ru] += 1
        custo += peso
        escolhidas += 1
        if escolhidas == n - 1:
            break
    assert escolhidas == n - 1
    return custo


def executar():
    grafo = Grafo("instancia3.txt")
    n = grafo.ordem()
    m = grafo.tamanho()
    densidade = grafo.densidade()
    assert 50 <= n <= 200
    assert n - 1 <= m < n * (n - 1) // 2
    assert densidade < 0.05, "Foi escolhido o limite de teste de 5% para este gerador"
    assert all(
        grafo.matriz[u][v] == grafo.matriz[v][u]
        for u in range(n) for v in range(n)
    ), "Matriz não simétrica"
    assert all(
        grafo.matriz[u][v] > 0
        for u in range(n) for v in range(u + 1, n)
        if grafo.matriz[u][v] != 0
    ), "Peso não positivo"
    assert all(grafo.matriz[u][u] == 0 for u in range(n))

    inicio = perf_counter()
    componentes = componentes_conexas(grafo)
    ordem_bfs, fora_arvore = busca_largura(grafo, 1)
    articulacoes = encontra_articulacao(grafo)
    ciclo = possui_ciclo(grafo)
    tempo_estrutura = perf_counter() - inicio
    assert len(componentes) == 1 and len(componentes[0]) == n, "Grafo desconexo"
    assert len(ordem_bfs) == n, "BFS não alcançou todos"
    assert ciclo, "Com 200 arestas e 120 vértices deve existir ciclo"

    impares = [v for v in range(1, n + 1) if grafo.grau(v) % 2 == 1]
    assert grafo.grau(n) == 1, "Vértice n deve ser folha no gerador"
    assert len(impares) >= 2
    euler_saida = io.StringIO()
    inicio = perf_counter()
    with contextlib.redirect_stdout(euler_saida):
        ciclo_euleriano(grafo)
    tempo_euler = perf_counter() - inicio
    assert "não possui ciclo euleriano" in euler_saida.getvalue()

    inicio = perf_counter()
    arestas_agm, custo_agm = prim(grafo)
    tempo_agm = perf_counter() - inicio
    conferir_arvore(n, arestas_agm)
    assert math.isclose(custo_agm, kruskal_teste(grafo), rel_tol=1e-10)

    inicio = perf_counter()
    metricas = calcular_metricas(grafo)
    tempo_distancias = perf_counter() - inicio
    dist = metricas["distancias"]
    for u in range(n):
        assert math.isclose(dist[u][u], 0, abs_tol=1e-9)
        assert math.isclose(max(dist[u]), metricas["excentricidades"][u + 1], abs_tol=1e-9)
        for v in range(n):
            assert math.isfinite(dist[u][v])
            assert math.isclose(dist[u][v], dist[v][u], abs_tol=1e-7)

    inicio = perf_counter()
    for origem in range(1, n + 1):
        dist_origem, _ = dijkstra(grafo, origem)
        for destino in range(1, n + 1):
            assert math.isclose(
                dist[origem - 1][destino - 1], dist_origem[destino], abs_tol=1e-7
            ), f"Erro na distância {origem} -> {destino}"
    tempo_conferencia = perf_counter() - inicio

    grau_min = min(grafo.grau(v) for v in range(1, n + 1))
    grau_max = max(grafo.grau(v) for v in range(1, n + 1))
    resultados = {
        "instancia": "instancia3.txt",
        "vertices": n,
        "arestas": m,
        "arestas_maximas": n * (n - 1) // 2,
        "densidade": densidade,
        "grau_medio": 2 * m / n,
        "grau_minimo": grau_min,
        "grau_maximo": grau_max,
        "conexo": len(componentes) == 1,
        "possui_ciclo": ciclo,
        "euleriano": len(impares) == 0,
        "vertices_impares": impares,
        "pontos_articulacao": sorted(articulacoes),
        "bfs_arestas_fora_arvore": len(fora_arvore),
        "agm_custo_total": custo_agm,
        "agm_arestas": [list(item) for item in arestas_agm],
        "diametro": metricas["diametro"],
        "raio": metricas["raio"],
        "vertices_perifericos": metricas["perifericos"],
        "vertices_centrais": metricas["centros"],
        "excentricidades": metricas["excentricidades"],
        "tempos_segundos": {
            "estrutura_bfs_articulacoes": tempo_estrutura,
            "euler": tempo_euler,
            "agm_prim": tempo_agm,
            "metricas_todos_pares": tempo_distancias,
            "dijkstra_tp1_120_origens_conferencia": tempo_conferencia,
        },
        "cobertura_vertices": "PENDENTE: implementação não presente no ZIP original",
        "validacoes": "PASSOU: conexão, pesos, Euler, AGM com Kruskal, distâncias com Dijkstra TP1, simetria e excentricidade",
    }
    pasta_saida = PASTA / "resultados"
    pasta_saida.mkdir(exist_ok=True)
    (pasta_saida / "instancia3_dados.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    resumo = [
        "INSTÂNCIA 3 — RELATÓRIO DE TESTES",
        f"Vértices: {n} | arestas: {m} / {n*(n-1)//2} | densidade: {densidade:.4%}",
        f"Conexo: sim | grau médio: {2*m/n:.4f} | graus mín/máx: {grau_min}/{grau_max}",
        f"Possui ciclo comum: {'sim' if ciclo else 'não'}",
        f"Euleriano: não | vértices ímpares: {len(impares)}",
        f"Pontos de articulação: {sorted(articulacoes)}",
        f"Árvore geradora mínima: {len(arestas_agm)} arestas | custo: {custo_agm:.2f}",
        f"Diâmetro: {metricas['diametro']:.2f} | periféricos: {metricas['perifericos']}",
        f"Raio: {metricas['raio']:.2f} | centrais: {metricas['centros']}",
        f"Tempo da análise de métricas: {tempo_distancias:.6f} s (máquina atual)",
        f"Tempo de Dijkstra TP1 em {n} origens (inclui caminhos): {tempo_conferencia:.6f} s",
        "Cobertura gulosa / heurística: NÃO TESTADAS (código ainda ausente no repositório)",
        "Validações: APROVADAS (pesos, conectividade, Prim/Kruskal, Dijkstra referência, simetria)",
        "\nEXCENTRICIDADES (vértice: distância):",
    ]
    resumo += [f"{v}: {exc:.2f}" for v, exc in metricas["excentricidades"].items()]
    resumo += ["\nARESTAS DA AGM (origem destino peso):"]
    resumo += [f"{u} {v} {peso:.2f}" for u, v, peso in arestas_agm]
    texto = "\n".join(resumo) + "\n"
    (pasta_saida / "instancia3_resumo.txt").write_text(texto, encoding="utf-8")
    print("\n".join(resumo[:11]))
    print("\nArquivos detalhados: resultados/instancia3_resumo.txt e instancia3_dados.json")
    return resultados


if __name__ == "__main__":
    executar()
