# carrega e salva no banco
import sqlite3
import pandas as pd

def criar_banco():
        # Conecta ao banco (cria o arquivo se não existir)
    conn = sqlite3.connect('database/ipca.db')
    cursor = conn.cursor()

        # Cria a tabela
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS ipca (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   mes_ano TEXT NOT NULL,
                   data TEXT NOT NULL
                   )
                   ''')
    conn.commit()
    print("banco criado com sucesso!")
    return conn

def inserir_dados(conn):
        # Carrega o CSV limpo
    df = pd.read_csv('data/processed/ipca_limpo.csv')

        # Insere no banco
    df.to_sql('ipca', conn, if_exists='replace', index=False)

    print(f"Dados inseridos com sucesso! Total: {len(df)} registros")

def verificar_dados(conn):
    df = pd.read_sql('SELECT * FROM ipca LIMIT 5', conn)
    print(df)

if __name__ == '__main__':
    conn = criar_banco()
    inserir_dados(conn)
    verificar_dados(conn)
    conn.close()
    print("concluirdo!")
