import chardet
import os
from tqdm import tqdm

def detectar_codificacao_stream(caminho, amostra=200_000):
    """
    Detecta a codificação lendo apenas os primeiros bytes (amostra).
    Ideal para arquivos grandes.
    """
    with open(caminho, "rb") as f:
        dados = f.read(amostra)
    
    resultado = chardet.detect(dados)
    return resultado["encoding"], resultado["confidence"]


def converter_grande_para_utf8(caminho_csv, codificacao_origem):
    """
    Converte arquivos gigantes sem usar muita memória.
    Inclui barra de progresso baseada em bytes processados.
    """
    nome, ext = os.path.splitext(caminho_csv)
    novo_arquivo = f"{nome}_utf8{ext}"

    tamanho_total = os.path.getsize(caminho_csv)

    with open(caminho_csv, "r", encoding=codificacao_origem, errors="replace") as f_origem, \
         open(novo_arquivo, "w", encoding="utf-8", newline="") as f_destino, \
         tqdm(total=tamanho_total, unit="B", unit_scale=True, desc="Convertendo", ncols=80) as barra:

        while True:
            linha = f_origem.readline()
            if not linha:
                break

            f_destino.write(linha)

            # Atualiza a barra com o número de bytes lidos
            barra.update(len(linha.encode(codificacao_origem, errors="replace")))

    print("\n✔ Conversão concluída!")
    print(f"➡ Arquivo gerado: {novo_arquivo}")


def main():
    caminho = input("Digite o caminho do arquivo CSV: ").strip()

    if not os.path.isfile(caminho):
        print("Arquivo não encontrado.")
        return

    print("\nDetectando codificação (amostragem)...")
    codificacao, confianca = detectar_codificacao_stream(caminho)

    print(f"\n📌 Codificação detectada (estimada): {codificacao}")
    print(f"📈 Confiança: {confianca*100:.2f}%\n")

    if codificacao is None:
        print("Não foi possível detectar a codificação.")
        return

    if codificacao.lower() in ["utf-8", "utf_8", "utf8"]:
        print("✔ O arquivo já está em UTF-8.")
    else:
        print("⚠ O arquivo NÃO está em UTF-8.")
        opcao = input("Deseja converter para UTF-8? (s/n): ").lower()
        if opcao == "s":
            converter_grande_para_utf8(caminho, codificacao)
        else:
            print("Conversão cancelada.")


if __name__ == "__main__":
    main()
