class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word_count = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if not node.is_end_of_word:
            self.total_words += 1
            node.word_count += 1
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root

        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        return self._get_all_words_from_node(node, prefix)

    def _get_all_words_from_node(self, node, current_prefix):
        words = []

        if node.is_end_of_word:
            words.append(current_prefix)

        for char, child_node in node.children.items():
            words.extend(self._get_all_words_from_node(child_node, current_prefix + char))

        return words

    def count_words(self):
        return self.total_words

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word


def carregar_palavras_do_arquivo(nome_arquivo):
    palavras = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                palavra = linha.strip()
                if palavra:
                    palavras.append(palavra)
        return palavras
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []


def teste_basico():
    print("=== TESTE BÁSICO ===")
    trie = Trie()
    palavras = ["apple", "banana", "apricot", "app", "appetizer", "bat", "ball", "batman"]

    for palavra in palavras:
        trie.insert(palavra)

    print("Número total de palavras na Trie:", trie.count_words())

    prefixo = "app"
    sugestoes = trie.search_prefix(prefixo)
    print(f"Palavras que começam com '{prefixo}': {sugestoes}")

    print(f"\nTestes adicionais:")
    print(f"Existe 'apple'? {trie.search('apple')}")
    print(f"Existe 'appl'? {trie.search('appl')}")
    print(f"Existe palavra com prefixo 'ba'? {trie.starts_with('ba')}")
    print(f"Palavras com prefixo 'ba': {trie.search_prefix('ba')}")


def teste_com_arquivo():
    print("\n=== TESTE COM ARQUIVO GRANDE ===")

    nome_arquivo = "outputTP1"
    palavras = carregar_palavras_do_arquivo(nome_arquivo)

    if not palavras:
        print("Nenhuma palavra carregada. Verifique o arquivo.")
        return

    print(f"Carregadas {len(palavras)} palavras do arquivo.")

    trie = Trie()

    print("Inserindo palavras na Trie...")
    for i, palavra in enumerate(palavras):
        trie.insert(palavra)
        if (i + 1) % 1000 == 0:  # Progresso a cada 1000 palavras
            print(f"Inseridas {i + 1} palavras...")

    print(f"\nNúmero total de palavras na Trie: {trie.count_words()}")

    while True:
        print("\n--- SISTEMA DE AUTOCOMPLETE ---")
        prefixo = input("Digite um prefixo para buscar (ou 'sair' para terminar): ").strip().lower()

        if prefixo == 'sair':
            break

        if not prefixo:
            continue

        sugestoes = trie.search_prefix(prefixo)
        print(f"\nPalavras que começam com '{prefixo}':")
        print(f"Encontradas {len(sugestoes)} sugestões:")

        for i, palavra in enumerate(sugestoes[:20]):
            print(f"  {i + 1}. {palavra}")

        if len(sugestoes) > 20:
            print(f"  ... e mais {len(sugestoes) - 20} palavras")


def teste_performance(trie, prefixos_teste):
    print("\n=== TESTE DE PERFORMANCE ===")
    import time

    for prefixo in prefixos_teste:
        inicio = time.time()
        sugestoes = trie.search_prefix(prefixo)
        fim = time.time()

        print(f"Prefix: '{prefixo}' -> {len(sugestoes)} resultados em {fim - inicio:.6f} segundos")
        if sugestoes:
            print(f"  Exemplos: {sugestoes[:3]}")


if __name__ == "__main__":
    teste_basico()
    teste_com_arquivo()

