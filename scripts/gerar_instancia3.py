import argparse
import random
from pathlib import Path

PASTA = Path(__file__).resolve().parents[1]
SAIDA = PASTA / "testes" / "instancia3.txt"


def gerar(vertices=120, arestas=200, semente=2026):
    if not 50 <= vertices <= 200:
        raise ValueError("A Instância 3 deve ter entre 50 e 200 vértices.")

    limite = (vertices - 1) * (vertices - 2) // 2 + 1
    if not vertices - 1 <= arestas <= limite:
        raise ValueError(f"Escolha entre {vertices - 1} e {limite} arestas.")

    aleatorio = random.Random(semente)
    nums = list(range(1, vertices))
    aleatorio.shuffle(nums)
    ligacoes = set()

    for i in range(1, len(nums)):
        a = nums[i]
        b = aleatorio.choice(nums[:i])
        ligacoes.add(tuple(sorted((a, b))))

    ligacoes.add(tuple(sorted((vertices, aleatorio.choice(nums)))))

    disponiveis = []
    for a in range(1, vertices):
        for b in range(a + 1, vertices):
            if (a, b) not in ligacoes:
                disponiveis.append((a, b))

    aleatorio.shuffle(disponiveis)
    faltam = arestas - len(ligacoes)
    ligacoes.update(disponiveis[:faltam])

    lista = []
    for a, b in sorted(ligacoes):
        peso = round(aleatorio.uniform(0.5, 15.0), 2)
        lista.append((a, b, peso))

    return lista


def salvar(destino=SAIDA, vertices=120, arestas=200, semente=2026):
    lista = gerar(vertices, arestas, semente)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with destino.open("w", encoding="utf-8") as arq:
        arq.write(f"{vertices}\n")
        for a, b, peso in lista:
            arq.write(f"{a} {b} {peso:.2f}\n")

    return destino


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=120)
    parser.add_argument("--arestas", type=int, default=200)
    parser.add_argument("--semente", type=int, default=2026)
    parser.add_argument("--saida", type=Path, default=SAIDA)
    args = parser.parse_args()

    caminho = salvar(args.saida, args.vertices, args.arestas, args.semente)
    densidade = 2 * args.arestas / (args.vertices * (args.vertices - 1))
    print(f"Arquivo: {caminho}")
    print(f"Vértices: {args.vertices}; arestas: {args.arestas}; densidade: {densidade:.4%}")
    print("Conexo por construção; último vértice é folha; pesos positivos.")
