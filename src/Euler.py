from Busca import componentes_conexas

def hierholzer(grafo, vertice_inicio):
    n = grafo.ordem()

    adj = {}

    for vertice in range(1, n + 1):
        adj[vertice] = set(grafo.vizinhos(vertice))

    pilha = [vertice_inicio]
    percurso = []

    while pilha:
        i = pilha[-1]
        if adj[i]:
            j = adj[i].pop()
            adj[j].remove(i)
            pilha.append(j)
        else:
            percurso.append(pilha.pop())

    return percurso

def ciclo_euleriano(grafo):

    if len(componentes_conexas(grafo)) != 1:
        #nao é conexo
        print("o grafo não possui ciclo euleriano, pois nao é conexo")
        return

    lista_vertices_impares = []

    for i in range(1, grafo.ordem() + 1):
        if grafo.grau(i) % 2 != 0:
            lista_vertices_impares.append(i)
            
    if len(lista_vertices_impares) == 2:
        print("o grafo é semi-euleriano e possui o caminho euleriano:")
        #printar o caminho
        print(hierholzer(grafo, lista_vertices_impares[0]))
        return

    elif len(lista_vertices_impares) == 0:
        #printar o ciclo
        print("o grafo possui o ciclo euleriano:")
        print(hierholzer(grafo, 1))

        return

    else:
        print("o grafo não possui ciclo euleriano, pois tem", len(lista_vertices_impares), "vertices de grau impar")

    return
