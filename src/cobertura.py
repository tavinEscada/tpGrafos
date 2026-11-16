def cobertura_gulosa(grafo):

    n = grafo.ordem()
    matriz = grafo.get_matriz()

    arestas = set()

    for i in range(n):
        for j in range(i + 1, n):
            if matriz[i][j] != 0:
                arestas.add((i, j))

    incidentes = [[] for _ in range(n)]

    for u, v in arestas:
        incidentes[u].append((u, v))
        incidentes[v].append((u, v))

    cobertura = set()
    nao_cobertas = arestas.copy()

    while nao_cobertas:

        melhor_vertice = -1
        maior_quantidade = 0

        for v in range(n):

            if v not in cobertura:

                quantidade = sum(
                    1 for aresta in incidentes[v]
                    if aresta in nao_cobertas
                )

                if quantidade > maior_quantidade:
                    maior_quantidade = quantidade
                    melhor_vertice = v

        if melhor_vertice == -1:
            break

        cobertura.add(melhor_vertice)

        for aresta in incidentes[melhor_vertice]:
            nao_cobertas.discard(aresta)

    return sorted(v + 1 for v in cobertura)


def cobertura_heuristica(grafo):

    n = grafo.ordem()
    matriz = grafo.get_matriz()

    nao_cobertas = set()

    for i in range(n):
        for j in range(i + 1, n):
            if matriz[i][j] != 0:
                nao_cobertas.add((i, j))

    cobertura = set()

    while nao_cobertas:

        u, v = next(iter(nao_cobertas))

        cobertura.add(u)
        cobertura.add(v)

        nao_cobertas = {
            (a, b) for a, b in nao_cobertas
            if a != u and a != v and b != u and b != v
        }

    return sorted(vertice + 1 for vertice in cobertura)


def validar_cobertura(grafo, cobertura):

    matriz = grafo.get_matriz()
    n = grafo.ordem()

    cobertura = set(cobertura)

    for i in range(n):
        for j in range(i + 1, n):

            if matriz[i][j] != 0:

                if (i + 1) not in cobertura and (j + 1) not in cobertura:
                    return False

    return True

