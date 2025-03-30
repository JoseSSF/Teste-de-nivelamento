import mysql.connector
import os
from etapa3_config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def importar_dados():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            allow_local_infile=True
        )
        cursor = conn.cursor()

        cursor.execute("SET GLOBAL local_infile = 1;")

        base_path = os.path.dirname(os.path.abspath(__file__))
        path_operadoras = os.path.join(base_path, "arquivosBaixados", "operadoras")
        path_demonstracoes = os.path.join(base_path, "arquivosBaixados", "demonstracoes")

        # Verifica se as pastas existem antes de tentar ler arquivos
        if not os.path.exists(path_operadoras):
            print(f"❌ ERRO: Pasta não encontrada: {path_operadoras}")
            return
        if not os.path.exists(path_demonstracoes):
            print(f"❌ ERRO: Pasta não encontrada: {path_demonstracoes}")
            return

        # Importar arquivos da pasta operadoras
        for file in os.listdir(path_operadoras):
            if file.endswith(".csv"):
                full_path = os.path.join(path_operadoras, file).replace("\\", "/")
                query_operadoras = f"""
                LOAD DATA LOCAL INFILE '{full_path}'
                INTO TABLE operadoras_de_plano_de_saude_ativas
                FIELDS TERMINATED BY ';' ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
                (CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero, Complemento, Bairro, 
                Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico, Representante, Cargo_Representante, 
                Regiao_de_Comercializacao, @Data_Registro_ANS)
                SET Data_Registro_ANS = STR_TO_DATE(@Data_Registro_ANS, '%d/%m/%Y');
                """
                cursor.execute(query_operadoras)
                print(f"✅ Importado: {file}")

        # Importar arquivos da pasta demonstracoes
        for file in os.listdir(path_demonstracoes):
            if file.endswith(".csv"):
                full_path = os.path.join(path_demonstracoes, file).replace("\\", "/")
                query_demonstracoes = f"""
                LOAD DATA LOCAL INFILE '{full_path}'
                INTO TABLE demonstracoes_contabeis
                FIELDS TERMINATED BY ';' ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
                (DATA_MOV, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
                """
                cursor.execute(query_demonstracoes)
                print(f"✅ Importado: {file}")

        conn.commit()
        cursor.close()
        conn.close()
        print("🚀 Importação concluída com sucesso!")

    except mysql.connector.Error as err:
        print(f"❌ Erro ao importar dados: {err}")

if __name__ == "__main__":
    importar_dados()
