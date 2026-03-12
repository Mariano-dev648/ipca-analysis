# consultas SQL
import sqlite3
import pandas as pd

def conectar():
    return sqlite3.connect('database/ipca.db')

# QUERY 1: Mês com maior inflação no período

def maior_inflacao(conn):
    query = '''
    SELECT mes_ano, variacao_pct
    FROM ipca
    ORDER BY variacao_pct DESC
    LIMIT 5
    '''
    df = pd.read_sql(query, conn)
    print("\n🔴 top 5 meses com  MAIOR inflacao:")
    print(df.to_string(index=False))

# QUERY 2: Mês com menor inflação (deflação)
def menor_inflacao(conn):
    query ='''
    SELECT mes_ano, variacao_pct
    FROM ipca
    ORDER BY variacao_pct ASC
    LIMIT 5
    '''
    df = pd.read_sql(query, conn)
    print("\n🟢 Top 5 meses com MENOR inflacao:")
    print(df.to_string(index=False))

# QUERY 3: Inflação acumulada por ano

def inflacao_por_ano(conn):
    query = '''
    SELECT
    SUBSTR(data, 1, 4) AS ano,
    ROUND(SUM(variacao_pct), 2) AS inflacao_acumulada
    FROM ipca
    GROUP BY ano
    ORDER BY ano
    '''
    df = pd.read_sql(query, conn)
    print("\n📅 Inflacao acumulada por ano:")
    print(df.to_string(index=False))

# QUERY 4: Média histórica por mês do ano

def media_por_mes(conn):
    query = '''
    SELECT
    SUBSTR(mes_ano, 1, INSTR(mes_ano, ' ') - 1) AS mes,
            ROUND(AVG(variacao_pct), 2) AS media_historica
        FROM ipca
        GROUP BY mes
        ORDER BY AVG(variacao_pct) DESC
    '''
    df = pd.read_sql(query, conn)
    print("\n📊 Média histórica de inflacao por mês:")
    print(df.to_string(index=False))

if __name__ == '__main__':
    conn = conectar()
    maior_inflacao(conn)
    menor_inflacao(conn)
    inflacao_por_ano(conn)
    media_por_mes(conn)
    conn.close()
