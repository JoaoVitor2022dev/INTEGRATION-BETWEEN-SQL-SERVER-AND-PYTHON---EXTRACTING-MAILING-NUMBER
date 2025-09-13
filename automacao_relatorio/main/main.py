# ====================================================
# Projeto: Exportar dados do SQL Server para CSV/Excel
# Autor: João Mocambite
# Objetivo: Aprender Python + SQL + pandas
# ====================================================

import pyodbc       # Biblioteca para conectar ao SQL Server
import pandas as pd # Biblioteca para manipular dados em DataFrame
from dotenv import load_dotenv # Biblioteca para ler arquivo .env
import os            # Para acessar variáveis de ambiente

# -----------------------------
# 1) Carregar variáveis do .env
# -----------------------------
load_dotenv()  # Lê o arquivo .env e carrega as variáveis
server = os.getenv("DB_SERVER")      # Nome do servidor SQL
database = os.getenv("DB_DATABASE")  # Nome do banco de dados
user = os.getenv("DB_USER")          # Usuário SQL (se usar SQL Authentication)
password = os.getenv("DB_PASSWORD")  # Senha SQL (se usar SQL Authentication)

# -----------------------------
# 2) Conexão com SQL Server
# -----------------------------
# Usando autenticação do Windows (Trusted Connection)
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

# Se quiser usar SQL Authentication, use essa linha em vez da acima:
# conn = pyodbc.connect(
#     f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#     f"SERVER={server};"
#     f"DATABASE={database};"
#     f"UID={user};PWD={password}"
# )

# -----------------------------
# 3) Consulta SQL
# -----------------------------
query = """
SELECT DISTINCT([Pessoa_Cpf]), [Telefone_Celular]
FROM [CAMCAP_LEBES].[dbo].[CAMCAP_LEBES_CDC]
"""
# SELECT DISTINCT -> retorna apenas valores únicos
# [Pessoa_Cpf], [Telefone_Celular] -> colunas que queremos
# [CAMCAP_LEBES].[dbo].[CAMCAP_LEBES_CDC] -> tabela completa com schema dbo

# -----------------------------
# 4) Ler dados da tabela
# -----------------------------
df = pd.read_sql(query, conn)
# pd.read_sql -> executa a query e retorna um DataFrame do pandas
# DataFrame é uma tabela em memória fácil de manipular

# -----------------------------
# 5) Salvar os dados em CSV
# -----------------------------
df.to_csv("dados_clientes.csv", index=False, encoding="utf-8-sig")
# index=False -> não salva o índice do DataFrame
# encoding="utf-8-sig" -> compatível com Excel, mantém acentos

# -----------------------------
# 6) Salvar os dados em Excel
# -----------------------------
df.to_excel("dados_clientes.xlsx", index=False)
# Salva os dados também em Excel, útil para abrir diretamente no programa

# -----------------------------
# 7) Mensagem de sucesso
# -----------------------------
print("✅ Dados exportados com sucesso!")

# -----------------------------
# 8) Fechar a conexão
# -----------------------------
conn.close()
# Sempre feche a conexão para liberar recursos do SQL Server
