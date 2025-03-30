import mysql.connector
from etapa3_config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def executar_consultas():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()

        consulta_trimestre = """
        SELECT 
            o.Nome_Fantasia AS nome_operadora,
            d.DATA_MOV,
            d.VL_SALDO_FINAL AS despesas_eventos
        FROM demonstracoes_contabeis d
        JOIN operadoras_de_plano_de_saude_ativas o ON d.REG_ANS = o.CNPJ
        WHERE d.DATA_MOV > DATE_SUB((SELECT MAX(d.DATA_MOV) FROM demonstracoes_contabeis), INTERVAL 3 MONTH)
        ORDER BY d.VL_SALDO_FINAL DESC
        LIMIT 10;
        """
        cursor.execute(consulta_trimestre)
        print("\n Top 10 operadoras com maiores despesas no último trimestre:")
        for row in cursor.fetchall():
            print(row)

        consulta_ano = """
        SELECT 
            o.Nome_Fantasia AS nome_operadora,
            YEAR(d.DATA_MOV) AS ano,
            SUM(d.VL_SALDO_FINAL) AS total_despesas
        FROM demonstracoes_contabeis d
        JOIN operadoras_de_plano_de_saude_ativas o ON d.REG_ANS = o.CNPJ
        WHERE YEAR(d.DATA_MOV) = YEAR((SELECT MAX(d.DATA_MOV) FROM demonstracoes_contabeis)) 
        GROUP BY o.Nome_Fantasia, YEAR(d.DATA_MOV)
        ORDER BY total_despesas DESC
        LIMIT 10;
        """
        cursor.execute(consulta_ano)
        print("\n Top 10 operadoras com maiores despesas no último ano:")
        for row in cursor.fetchall():
            print(row)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f" Erro ao executar consultas: {err}")

if __name__ == "__main__":
    executar_consultas()
