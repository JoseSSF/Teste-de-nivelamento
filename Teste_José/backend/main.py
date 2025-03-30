from fastapi import FastAPI, Query
import pandas as pd
import os

app = FastAPI()

# Caminho do CSV
base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, "backend", "arquivosBaixados", "operadoras", "Relatorio_cadop.csv")

if os.path.exists(csv_path):
    print("Arquivo encontrado:", csv_path)
else:
    print("Arquivo não encontrado:", csv_path)

# Carregar dados do CSV
df = pd.read_csv(csv_path, encoding="utf-8")

@app.get("/buscar")
def buscar_operadora(termo: str = Query(..., min_length=2)):
    """Busca operadoras no CSV com base no termo"""
    resultados = df[df.apply(lambda row: row.astype(str).str.contains(termo, case=False, na=False).any(), axis=1)]
    return resultados.to_dict(orient="records")
