import heapq
import math


def _lista_adjacencia(grafo):
    n = grafo.ordem()
    mat = grafo.get_matriz()
    adj = [[] for _ in range(n)]

    for i in range(n):
        if len(mat[i]) != n:
            raise ValueError("A matriz de adjacência deve ser quadrada.")
        if mat[i][i] != 0 and (not math.isfinite(mat[i][i]) or mat[i][i] < 0):
            raise ValueError("Um laço deve ter peso real positivo e finito.")

        for j in range(i + 1, n):
            peso = mat[i][j]
            if peso != mat[j][i]:
                raise ValueError("O grafo deve ser não direcionado (matriz simétrica).")
            if peso == 0:
                continue
            if not math.isfinite(peso) or peso < 0:
                raise ValueError("As arestas devem ter pesos reais positivos e finitos.")
            adj[i].append((j, peso))
            adj[j].append((i, peso))

    return adj


def _dijkstra(adj, inicio):
    n = len(adj)
    dist = [math.inf] * n
    dist[inicio] = 0
    fila = [(0, inicio)]

    while fila:
        valor, atual = heapq.heappop(fila)
        if valor > dist[atual]:
            continue

        for viz, peso in adj[atual]:
            novo = valor + peso
            if novo < dist[viz]:
                dist[viz] = novo
                heapq.heappush(fila, (novo, viz))

    return dist


def distancias_todos_pares(grafo):
    adj = _lista_adjacencia(grafo)
    distancias = []
    for i in range(len(adj)):
        distancias.append(_dijkstra(adj, i))
    return distancias


def calcular_metricas(grafo):
    distancias = distancias_todos_pares(grafo)

    if not distancias:
        raise ValueError("O grafo deve ter pelo menos um vértice.")
    for linha in distancias:
        if math.inf in linha:
            raise ValueError("Métricas de distância exigem um grafo conexo.")

    exc = {}
    for i, linha in enumerate(distancias):
        exc[i + 1] = max(linha)

    diametro = max(exc.values())
    raio = min(exc.values())
    centros = []
    perifericos = []

    for v, valor in exc.items():
        if math.isclose(valor, raio, rel_tol=1e-9, abs_tol=1e-9):
            centros.append(v)
        if math.isclose(valor, diametro, rel_tol=1e-9, abs_tol=1e-9):
            perifericos.append(v)

    return {
        "distancias": distancias,
        "excentricidades": exc,
        "diametro": diametro,
        "raio": raio,
        "centros": centros,
        "perifericos": perifericos,
    }


def imprimir_metricas(grafo):
    try:
        dados = calcular_metricas(grafo)
    except ValueError as erro:
        print("Não foi possível calcular as métricas:", erro)
        return

    print("\nMÉTRICAS DE DISTÂNCIA (pesos das arestas)")
    for v, valor in dados["excentricidades"].items():
        print(f"Excentricidade de {v}: {valor:.2f}")
    print(f"Diâmetro: {dados['diametro']:.2f}")
    print(f"Vértices periféricos: {dados['perifericos']}")
    print(f"Raio: {dados['raio']:.2f}")
    print(f"Vértices centrais: {dados['centros']}")
