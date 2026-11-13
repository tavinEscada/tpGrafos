from Busca import componentes_conexas

def ciclo_euleriano(grafo):

    if len(componentes_conexas(grafo)) != 1:
        #nao é conexo
        print("o grafo não possui ciclo euleriano, pois nao é conexo")
        return

    n_vertices_impares = 0

    for i in range(1, grafo.ordem() + 1):
        if grafo.grau(i) % 2 != 0:
            n_vertices_impares += 1

    if n_vertices_impares == 2:
        print("o grafo é semi-euleriano e possui somente o circuito euleriano:")
        #printar o ciclo
        return

    elif n_vertices_impares == 0:
        #printar o ciclo
        print("o grafo possui o ciclo euleriano:")

        return

    else:
        print("o grafo não possui ciclo euleriano, pois tem", n_vertices_impares, "vertices de grau impar")

    return

