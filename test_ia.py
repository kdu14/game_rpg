import markovify
import os

print("--- Iniciando Teste de Diagnóstico da IA ---")
print(f"Executando a partir da pasta: {os.getcwd()}")
print("-" * 20)

arquivos_corpus = [
    "corpus.txt",
    "corpus_atq_jogador.txt",
    "corpus_atq_inimigo.txt",
    "corpus_vitoria.txt"
]

todos_carregados = True

for nome_arquivo in arquivos_corpus:
    print(f"Tentando carregar '{nome_arquivo}'...")
    try:
        with open(nome_arquivo, encoding="utf-8") as f:
            texto = f.read()
        
        modelo = markovify.Text(texto)
        frase = modelo.make_sentence(tries=100)
        
        if frase:
            print(f"  [SUCESSO] Arquivo carregado e frase gerada: '{frase}'")
        else:
            print(f"  [AVISO] Arquivo carregado, mas não foi possível gerar uma frase. O corpus pode ser muito pequeno.")
            todos_carregados = False

    except FileNotFoundError:
        print(f"  [ERRO GRAVE] O arquivo '{nome_arquivo}' NÃO FOI ENCONTRADO!")
        print(f"  Verifique se o arquivo está na mesma pasta que este script e se o nome está correto.")
        todos_carregados = False
    except Exception as e:
        print(f"  [ERRO] Ocorreu um problema inesperado com '{nome_arquivo}': {e}")
        todos_carregados = False
    
    print("-" * 20)

if todos_carregados:
    print("\nDiagnóstico final: Todos os arquivos parecem estar funcionando corretamente!")
else:
    print("\nDiagnóstico final: Um ou mais arquivos apresentaram problemas. Verifique as mensagens de erro acima.")