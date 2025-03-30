import os
import requests
import zipfile
from bs4 import BeautifulSoup
from tqdm import tqdm

URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
PASTA = "downloads"
os.makedirs(PASTA, exist_ok=True)

def pega_links():
    r = requests.get(URL)
    if r.status_code != 200:
        print("Erro ao acessar site")
        return []
    
    soup = BeautifulSoup(r.text, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        if ("Anexo I" in a.text or "Anexo II" in a.text) and a['href'].lower().endswith(".pdf"):
            links.append(a['href'])
    
    return links

def baixa_pdf(url):
    nome = url.split("/")[-1]
    caminho = os.path.join(PASTA, nome)
    r = requests.get(url, stream=True)
    tamanho = int(r.headers.get('content-length', 0))
    
    with open(caminho, 'wb') as f, tqdm(desc=nome, total=tamanho, unit='B', unit_scale=True) as barra:
        for chunk in r.iter_content(1024):
            f.write(chunk)
            barra.update(len(chunk))
    
    return caminho

def zipa_arquivos(lista):
    with zipfile.ZipFile("arquivos_zipados.zip", 'w', zipfile.ZIP_DEFLATED) as z:
        for arq in lista:
            z.write(arq, os.path.basename(arq))
    print("ZIP criado: arquivos_zipados.zip")

links = pega_links()
if links:
    print("Baixando PDFs...")
    arquivos = [baixa_pdf(link) for link in links]
    zipa_arquivos(arquivos)
else:
    print("Nenhum PDF encontrado.")
