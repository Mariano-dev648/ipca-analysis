import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Configuracao visual global
sns.set_theme(style='darkgrid')
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 12

def conectar():
    return sqlite3.connect('database/ipca.db')

def carregar_dados(conn):
    df = pd.read_sql('SELECT * FROM ipca ORDER BY data', conn)
    df['data'] = pd.to_datetime(df['data'])
    return df

# ---- GRAFICO 1: Evolucao mensal do IPCA ----
def grafico_evolucao(df):
    fig, ax = plt.subplots()
    ax.plot(df['data'], df['variacao_pct'], color='steelblue', linewidth=1.5)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax.set_title('Evolucao Mensal do IPCA (2015-2024)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Data')
    ax.set_ylabel('Variacao (%)')
    plt.tight_layout()
    plt.savefig('outputs/graficos/evolucao_mensal.png', dpi=150)
    print("Grafico 1 salvo!")
    plt.close()

# ---- GRAFICO 2: Inflacao acumulada por ano ----
def grafico_anual(conn):
    query = '''
        SELECT SUBSTR(data, 1, 4) AS ano,
               ROUND(SUM(variacao_pct), 2) AS total
        FROM ipca
        GROUP BY ano
        ORDER BY ano
    '''
    df = pd.read_sql(query, conn)
    fig, ax = plt.subplots()
    bars = ax.bar(df['ano'], df['total'], color='steelblue', edgecolor='white')
    ax.bar_label(bars, fmt='%.1f%%', padding=3, fontsize=10)
    ax.set_title('Inflacao Acumulada por Ano (IPCA)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Inflacao Acumulada (%)')
    plt.tight_layout()
    plt.savefig('outputs/graficos/inflacao_anual.png', dpi=150)
    print("Grafico 2 salvo!")
    plt.close()

# ---- GRAFICO 3: Media historica por mes ----
def grafico_media_mes(conn):
    ordem = ['janeiro','fevereiro','marco','abril','maio','junho',
             'julho','agosto','setembro','outubro','novembro','dezembro']
    query = '''
        SELECT SUBSTR(mes_ano, 1, INSTR(mes_ano, ' ') - 1) AS mes,
               ROUND(AVG(variacao_pct), 2) AS media
        FROM ipca
        GROUP BY mes
    '''
    df = pd.read_sql(query, conn)
    df['mes'] = df['mes'].str.replace('março', 'marco')
    df['ordem'] = df['mes'].apply(lambda x: ordem.index(x) if x in ordem else 99)
    df = df.sort_values('ordem')
    fig, ax = plt.subplots()
    bars = ax.bar(df['mes'], df['media'], color='coral', edgecolor='white')
    ax.bar_label(bars, fmt='%.2f%%', padding=3, fontsize=10)
    ax.set_title('Media Historica do IPCA por Mes (2015-2024)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Media (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/graficos/media_por_mes.png', dpi=150)
    print("Grafico 3 salvo!")
    plt.close()

if __name__ == '__main__':
    conn = conectar()
    df = carregar_dados(conn)
    grafico_evolucao(df)
    grafico_anual(conn)
    grafico_media_mes(conn)
    conn.close()
    print("\nTodos os graficos salvos em outputs/graficos/")