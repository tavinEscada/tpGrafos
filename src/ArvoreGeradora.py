from Grafo import Grafo

def prim(grafo):
    n = grafo.ordem()
    matriz = grafo.get_matriz()

    INF = float("inf")
    na_arvore = [False] * n
    custo = [INF] * n
    pai = [None] * n

    custo[0] = 0

    for _ in range(n):
        u = -1
        for v in range(n):
            if not na_arvore[v] and (u == -1 or custo[v] < custo[u]):
                u = v

        na_arvore[u] = True

        for v in range(n):
            peso = matriz[u][v]
            if peso != 0 and not na_arvore[v] and peso < custo[v]:
                custo[v] = peso
                pai[v] = u

    arestas = []
    peso_total = 0
    for v in range(n):
        if pai[v] is not None:
            peso = matriz[pai[v]][v]
            arestas.append((pai[v] + 1, v + 1, peso))
            peso_total += peso

    return arestas, peso_total

def imprime_arvore(arestas, raiz=1):
    filhos = {}
    for pai, filho, peso in arestas:
        filhos.setdefault(pai, []).append((filho, peso))

    def descer(v, prefixo):
        lista = filhos.get(v, [])
        for i, (f, peso) in enumerate(lista):
            ultimo = (i == len(lista) - 1)
            print(prefixo + ("└── " if ultimo else "├── ") + f"{f} ({peso})")
            descer(f, prefixo + ("    " if ultimo else "│   "))

    print(raiz)
    descer(raiz, "")

def arvore(grafo):
    if grafo.e_conexo() == False:
        print("Nao é possivel obter a arvore geradora, pois o grafo nao é conexo")
        return

    arestas, peso_total = prim(grafo)

    print("árvore geradora mínima:")

    imprime_arvore(arestas)

    print(f"peso total: {peso_total}")