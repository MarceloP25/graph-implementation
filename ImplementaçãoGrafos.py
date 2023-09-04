'''
Dupla: Marcelo e Eduardo
Trabalho final de implementação de grafos buscando implementar a lógica de rotas aéreas de voos internacionais na América do Sul,
implantando uma fórmula simples, não condizendo totalmente com a realidade, apenas para ilustrar uma representação do cálculo real.
calcCusto = (tempoVoo * 0.5) + (turbulencia * 0.1) + ((taxaVoo * horaVooTrecho) * 0.3) + (milha * 0.1)
'''
class Grafo:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adjacencia = [[] for _ in range(num_vertices)]
        self.pesos = [[0] * num_vertices for _ in range(num_vertices)]
        self.milhas = [[[] for _ in range(num_vertices)] for _ in range(num_vertices)]
        self.tempo_voo_ = [[[] for _ in range(num_vertices)] for _ in range(num_vertices)]

    def adicionar_aresta(self, origem, destino, peso, milha, tempo_voo):
        if destino not in self.adjacencia[origem]:
            self.adjacencia[origem].append(destino)
            self.adjacencia[destino].append(origem)
            self.pesos[origem][destino] = peso
            self.pesos[destino][origem] = peso
            self.tempo_voo_[origem][destino] = tempo_voo
            self.tempo_voo_[destino][origem] = tempo_voo
            self.milhas[origem][destino] = milha
            self.milhas[destino][origem] = milha
        else:
            print("Essa ligação já existe.")

    def mostrar_grafo(self):
        for vertice in range(self.num_vertices):
            print(f"Vértice {vertice}: ", end="")
            print(*self.adjacencia[vertice])

    def mostrar_pesos(self):
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.pesos[i][j] != 0:
                    print(f"Peso entre os vértices {i} e {j}: {self.pesos[i][j]}")

    def mostrar_tabela_ligacoes(self):
        print("Tabela de Ligações:")
        print("Vértice de Origem  |  Peso da Aresta  |  Milhas  |  Tempo de Voo  |  Vértice de Destino")
        print("------------------+-----------------+---------+---------------+-------------------")
        for origem in range(self.num_vertices):
            for destino in self.adjacencia[origem]:
                peso = self.pesos[origem][destino]
                milhas = self.milhas[origem][destino]
                tempo_voo = self.tempo_voo_[origem][destino]
                print(f"       {origem}       |       {peso}      |   {milhas}   |    {tempo_voo}    |        {destino}")

    def encontrar_caminho_menor_peso(self, origem, destino):
        caminhos = [[] for _ in range(self.num_vertices)]
        menor_peso = float('inf')
        self.dfs(origem, destino, [], caminhos)

        tabela_caminhos = []
        for caminho in caminhos:
            if caminho:
                peso_total = self.calcular_peso_caminho(caminho)
                if peso_total < menor_peso:
                    menor_peso = peso_total

                tempo_voo_total = self.calcular_tempo_voo_total(caminho)
                tabela_caminhos.append((caminho, peso_total, tempo_voo_total))

        print("Caminhos encontrados:")
        print("Caminho        |    Peso Total  |   Milhas Totais  |  Tempo de Voo Total")
        print("----------------+--------------+-----------------+---------------------")
        for caminho, peso_total, tempo_voo_total in tabela_caminhos:
            milhas_totais = self.calcular_milhas_totais(caminho)
            print(f"{caminho}    |    {peso_total}    |    {milhas_totais}    |    {tempo_voo_total}")

        print(f"\nCaminho com menor peso total: {tabela_caminhos[0][0]} (Peso: {menor_peso})")

    def dfs(self, vertice_atual, destino, caminho_atual, caminhos):
        caminho_atual.append(vertice_atual)

        if vertice_atual == destino:
            caminhos[vertice_atual - 1] = caminho_atual.copy()
        else:
            for vizinho in self.adjacencia[vertice_atual]:
                if vizinho not in caminho_atual:
                    self.dfs(vizinho, destino, caminho_atual, caminhos)

        caminho_atual.pop()

    def calcular_peso_caminho(self, caminho):
        peso_total = 0
        for i in range(len(caminho) - 1):
            origem = caminho[i]
            destino = caminho[i + 1]
            peso_total += self.pesos[origem][destino]

        return peso_total

    def calcular_milhas_totais(self, caminho):
        milhas_totais = 0
        for i in range(len(caminho) - 1):
            origem = caminho[i]
            destino = caminho[i + 1]
            milhas_totais += self.milhas[origem][destino]

        return milhas_totais

    def calcular_tempo_voo_total(self, caminho):
        tempo_voo_total = 0
        for i in range(len(caminho) - 1):
            origem = caminho[i]
            destino = caminho[i + 1]
            tempo_voo_total += self.tempo_voo_[origem][destino]

        return tempo_voo_total


# Solicitar o número de vértices e arestas ao usuário
num_vertices = int(input("Digite o número de vértices do grafo: "))
num_arestas = int(input("Digite o número de arestas do grafo: "))

grafo = Grafo(num_vertices)

# Solicitar as ligações entre vértices e pesos
for i in range(num_arestas):
    print(f"\nLigação {i + 1}:")
    origem = int(input("Digite a origem da aresta: "))
    destino = int(input("Digite o destino da aresta: "))
    tempo_voo = float(input("Digite o tempo de voo (em horas): "))
    turbulencia = float(input("Digite o valor de turbulência: "))
    taxa_voo = 800
    milha = float(input("Digite o valor da milha: "))

    custo = (tempo_voo * 0.5) + (turbulencia * 0.1) + ((taxa_voo * tempo_voo) * 0.3) + (milha * 0.1)

    grafo.adicionar_aresta(origem, destino, custo, milha, tempo_voo)

# Mostrar o grafo, os pesos das arestas e a tabela de ligações
print("\nGrafo:")
grafo.mostrar_grafo()

print("\nPesos das Arestas:")
grafo.mostrar_pesos()

print("\nTabela de Ligações:")
grafo.mostrar_tabela_ligacoes()

# Realizar busca pelos caminhos com menor peso
origem = int(input("\nDigite o vértice de origem: "))
destino = int(input("Digite o vértice de destino: "))
grafo.encontrar_caminho_menor_peso(origem, destino)