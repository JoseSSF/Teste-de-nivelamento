import os
import pdfplumber
import pandas as pd
import zipfile

pdf_anexo = "downloads/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_arquivo = "Procedimentos.csv"
zip_arquivo = "Teste_Jose.zip"

SUBSTITUICAO = {
    "OD": "Procedimentos Odontológicos",
    "AMB": "Procedimentos Ambulatoriais"
}

def extrair_tabela_pdf(caminho_pdf):
    """Extrai a tabela do PDF e retorna como lista de dicionários"""
    dados_extraidos = []
    
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                cabecalho = tabela[0]
                for linha in tabela[1:]:
                    dados_extraidos.append(dict(zip(cabecalho, linha)))
    
    return dados_extraidos

def salvar_csv(dados, caminho_csv):
    df = pd.DataFrame(dados)
    
    # Substitui abreviações
    df.replace(SUBSTITUICAO, inplace=True)
    
    df.to_csv(caminho_csv, index=False, encoding="utf-8")
    print(f"CSV salvo em: {caminho_csv}")

def compactar_arquivo(caminho_arquivo, caminho_zip):

    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(caminho_arquivo, os.path.basename(caminho_arquivo))
    
    print(f"Arquivo ZIP criado: {caminho_zip}")

if os.path.exists(pdf_anexo):
    dados = extrair_tabela_pdf(pdf_anexo)
    if dados:
        salvar_csv(dados, csv_arquivo)
        compactar_arquivo(csv_arquivo, zip_arquivo)
    else:
        print("Nenhuma tabela encontrada no PDF.")
else:
    print(f"Arquivo {pdf_anexo} não encontrado.")
