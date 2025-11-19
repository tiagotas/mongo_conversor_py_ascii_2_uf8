import os
from tqdm import tqdm

def remover_aspas_grande(caminho_csv, remover_somente_externas=False):
    """
    Remove aspas de arquivos CSV gigantes sem carregar tudo na memória.
    
    remover_somente_externas = True:
        Remove aspas apenas se a linha inteira começar e terminar com aspas.
    """
    
    nome, ext = os.path.splitext(caminho_csv)
    novo_arquivo = f"{nome}_sem_aspas{ext}"

    tamanho_total = os.path.getsize(caminho_csv)

    with open(caminho_csv, "r", encoding="utf-8", errors="replace") as f_origem, \
         open(novo_arquivo, "w", encoding="utf-8", newline="") as f_destino, \
         tqdm(total=tamanho_total, unit="B", unit_scale=True, desc="Processando", ncols=80) as barra:

        while True:
            linha = f_origem.readline()
            if not linha:
                break

            if remover_somente_externas:
                # Exemplo: "valor1","valor2" -> valor1","valor2
                if linha.startswith('"') and linha.endswith('"'):
                    linha = linha[1:-1]
            else:
                # Remove TODAS as aspas
                linha = linha.replace('"', "")

            f_destino.write(linha)

            barra.update(len(linha.encode("utf-8")))

    print("\n✔ Arquivo processado com sucesso!")
    print(f"➡ Arquivo gerado: {novo_arquivo}")


def main():
    caminho = input("Digite o caminho do arquivo CSV: ").strip()

    if not os.path.isfile(caminho):
        print("Arquivo não encontrado.")
        return

    print("\nComo deseja remover as aspas?")
    print("1 - Remover TODAS as aspas")
    print("2 - Remover apenas se a linha inteira estiver entre aspas (\"linha inteira\")")

    opc = input("Escolha (1/2): ").strip()

    if opc == "1":
        remover_aspas_grande(caminho)
    elif opc == "2":
        remover_aspas_grande(caminho, remover_somente_externas=True)
    else:
        print("Opção inválida.")


if __name__ == "__main__":
    main()
