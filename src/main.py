import time
from caminhoMinimo import dijkstra
from grafo import Grafo
from articulacao import encontra_articulacao, eh_articulacao
from busca import busca_largura, componentes_conexas, possui_ciclo
from Euler import ciclo_euleriano
from ArvoreGeradora import arvore
from metricasRede import imprimir_metricas
from cobertura import cobertura_gulosa, cobertura_heuristica, validar_cobertura

def menu():

    print("========================================")
    print("         ANÁLISE DE REDE SOCIAL")
    print("========================================")
    print("1 - Informar ordem do grafo")
    print("2 - Informar tamanho do grafo")
    print("3 - Calcular densidade")
    print("4 - Informar vizinhos de um vértice")
    print("5 - Informar grau de um vértice")
    print("6 - Verificar se um vértice é articulação")
    print("7 - Executar busca em largura")
    print("8 - Identificar componentes conexas")
    print("9 - Verificar existência de ciclos")
    print("10 - Calcular caminhos mínimos")
    print("11 - Análise euleriana")
    print("12 - Arvore geradora minima")
    print("13 - Cobertura mínima gulosa")
    print("14 - Cobertura mínima heurística")
    print("15 - Comparar algoritmos")
    print("16 - Métricas da rede")
    print("0 - Sair")
    print("========================================")


arquivo = input("Digite o nome do arquivo do grafo: ")

grafo = Grafo(arquivo)

while True:

    menu()

    opcao = input("Digite a opção: ")

    if opcao == "1":

        print("Ordem do grafo:", grafo.ordem())

    elif opcao == "2":

        print("Tamanho do grafo:", grafo.tamanho())

    elif opcao == "3":

        print("Densidade do grafo:", grafo.densidade())

    elif opcao == "4":

        vertice = int(input("Digite o vértice: "))

        print("Vizinhos:", grafo.vizinhos(vertice))

    elif opcao == "5":

        vertice = int(input("Digite o vértice: "))

        print("Grau:", grafo.grau(vertice))

    elif opcao == "6":

        vertice = int(input("Digite o vértice: "))

        if eh_articulacao(grafo, vertice):
            print("O vértice", vertice, "é articulação.")
        else:
            print("O vértice", vertice, "não é articulação.")

    elif opcao == "7":

        vertice = int(input("Digite o vértice inicial da busca: "))

        ordem, fora_arvore = busca_largura(grafo, vertice)

        print("Sequência da busca:", ordem)

        if len(fora_arvore) == 0:
            print("Não existem arestas fora da árvore BFS.")
        else:
            print("Arestas fora da árvore BFS:", fora_arvore)

    elif opcao == "8":

        componentes = componentes_conexas(grafo)

        print("Número de componentes conexas:", len(componentes))

        for i in range(len(componentes)):
            print("Componente", i + 1, ":", componentes[i])

    elif opcao == "9":

        if possui_ciclo(grafo):
            print("O grafo possui ciclo.")
        else:
            print("O grafo não possui ciclo.")

    elif opcao == "10":
        origem = int(input("Digite o vertice de origem: "))
        dist, caminhos = dijkstra(grafo, origem)

        for i in range(1, grafo.ordem() + 1):
                d = dist[i]

                if d == float('inf'):
                    dStr = "Inalcançável"

                else:
                    dStr = f"{d:.1f}"

                print(f" para o vertice", i,  ": distancia =", dStr, "| caminho =", caminhos[i])

        print()

    elif opcao == "11":
        ciclo_euleriano(grafo)

    elif opcao == "12":
        arvore(grafo)

    elif opcao == "13":
        resultado = cobertura_gulosa(grafo)
        print("Cobertura mínima gulosa:", resultado)
        print("Quantidade de vértices:", len(resultado))

    elif opcao == "14":
        cobertura = cobertura_heuristica(grafo)
        print("Cobertura heurística:", cobertura)
        print("Quantidade de vértices:", len(cobertura))

    elif opcao == "15":

        inicio = time.perf_counter()
        cobertura_g = cobertura_gulosa(grafo)
        tempo_guloso = time.perf_counter() - inicio

        inicio = time.perf_counter()
        cobertura_h = cobertura_heuristica(grafo)
        tempo_heuristica = time.perf_counter() - inicio

        print("\n===== COMPARAÇÃO DOS ALGORITMOS =====")

        print("\nAlgoritmo Guloso:")
        print("Cobertura:", cobertura_g)
        print("Quantidade de vértices:", len(cobertura_g))
        print("Tempo de execução:", tempo_guloso, "segundos")

        print("\nAlgoritmo Heurístico:")
        print("Cobertura:", cobertura_h)
        print("Quantidade de vértices:", len(cobertura_h))
        print("Tempo de execução:", tempo_heuristica, "segundos")
        print("\nValidação das coberturas:")
        print("Guloso:", "Válida" if validar_cobertura(grafo, cobertura_g) else "Inválida")
        print("Heurístico:", "Válida" if validar_cobertura(grafo, cobertura_h) else "Inválida")

    elif opcao == "16":

        imprimir_metricas(grafo)
    
    elif opcao == "0":

        print("Programa encerrado.")
        break

    else:

        print("Opção inválida.")