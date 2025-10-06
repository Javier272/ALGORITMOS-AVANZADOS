class NodoTrie:
    def __init__(self):
        self.hijos = {}
        self.es_fin_palabra = False


class Trie:
    def __init__(self):
        self.raiz = NodoTrie()

    def insertar(self, palabra):
        nodo = self.raiz
        for caracter in palabra:
            if caracter not in nodo.hijos:
                nodo.hijos[caracter] = NodoTrie()
            nodo = nodo.hijos[caracter]
        nodo.es_fin_palabra = True

    def buscar(self, palabra):
        nodo = self.raiz
        for caracter in palabra:
            if caracter not in nodo.hijos:
                return False
            nodo = nodo.hijos[caracter]
        return nodo.es_fin_palabra

    def dfs(self, nodo=None, prefijo="", resultado=None):
        if resultado is None:
            resultado = []
        if nodo is None:
            nodo = self.raiz

        if nodo.es_fin_palabra:
            resultado.append(prefijo)

        for caracter in sorted(nodo.hijos.keys()):
            self.dfs(nodo.hijos[caracter], prefijo + caracter, resultado)
        return resultado

trie = Trie()
N = int(input().strip())
for _ in range(N):
    palabra = input().strip()
    trie.insertar(palabra)

M = int(input().strip())
palabras_buscar = [input().strip() for _ in range(M)]

recorrido = trie.dfs()
print(" ".join(recorrido))

for palabra in palabras_buscar:
    print(str(trie.buscar(palabra)).lower()) 
