# ====================================================
# Exportar dados do SQL Server para Excel + Validação CNAM
# Autor: João Mocambite
# Objetivo: 
#   1) Conectar ao banco SQL Server e buscar dados de clientes
#   2) Exportar todos os registros para Excel
#   3) Validar até 100 números de telefone usando a API freecnam.org
#   4) Exportar os resultados da validação para outra planilha Excel
# ====================================================

# Bibliotecas necessárias
import pyodbc          # Conexão com SQL Server
import pandas as pd    # Manipulação de dados (DataFrame)
from dotenv import load_dotenv  # Carregar variáveis de ambiente (.env)
import os              # Manipular pastas e caminhos
import requests        # Fazer requisições HTTP (chamada na API freecnam)
import time            # Usado para dar pausas entre chamadas da API

# -----------------------------
# 1) Carregar variáveis do arquivo .env
# -----------------------------
# O arquivo .env guarda informações sensíveis (como servidor e banco de dados)
load_dotenv()
server = os.getenv("DB_SERVER")      # Nome do servidor SQL
database = os.getenv("DB_DATABASE")  # Nome do banco de dados

# -----------------------------
# 2) Definir pasta onde os relatórios serão salvos
# -----------------------------
pasta_destino = "automacao_relatorio\\Report_number_whatsapp"
os.makedirs(pasta_destino, exist_ok=True)  # Cria a pasta caso não exista

# -----------------------------
# 3) Conectar ao SQL Server
# -----------------------------
# Aqui usamos autenticação do Windows (Trusted_Connection=yes)
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

# -----------------------------
# 4) Criar a consulta SQL
# -----------------------------
# DISTINCT([Pessoa_Cpf]) -> remove CPFs duplicados
query = """
SELECT DISTINCT([Pessoa_Cpf]), [Telefone_Celular]
FROM [CAMCAP_LEBES].[dbo].[CAMCAP_LEBES_CDC]
"""

# -----------------------------
# 5) Ler dados da consulta para um DataFrame (pandas)
# -----------------------------
df = pd.read_sql(query, conn)

# -----------------------------
# 6) Limpar registros inválidos (sem número)
# -----------------------------
df = df[df["Telefone_Celular"].notna()]  # remove valores nulos
df = df[df["Telefone_Celular"].astype(str).str.strip() != ""]  # remove strings vazias

# -----------------------------
# 7) Validar até 100 números de telefone com a API freecnam.org
# -----------------------------
resultados = []
numeros_validar = df["Telefone_Celular"].head(100)  # pega só os 100 primeiros números

for numero in numeros_validar:
    try:
        url = f"https://freecnam.org/dip?q={numero}"
        r = requests.get(url, timeout=5)  # timeout=5 segundos para não travar
        if r.status_code == 200:
            resultados.append(r.text.strip())  # resposta da API
        else:
            resultados.append("Erro API")      # caso a API não responda corretamente
    except:
        resultados.append("Erro conexão")      # erro de internet ou outro
    time.sleep(1)  # pausa de 1s para não sobrecarregar a API gratuita

# -----------------------------
# 8) Criar DataFrame com os 100 números validados
# -----------------------------
df_validacao = pd.DataFrame({
    "Telefone_Celular": numeros_validar.values,
    "CNAM_Info": resultados
})

# -----------------------------
# 9) Exportar dados para Excel
# -----------------------------
# a) Todos os dados
caminho_excel = os.path.join(pasta_destino, "dados_clientes.xlsx")
df.to_excel(caminho_excel, index=False)

# b) Apenas os 100 validados
caminho_validacao = os.path.join(pasta_destino, "validacao_cnam.xlsx")
df_validacao.to_excel(caminho_validacao, index=False)

# -----------------------------
# 10) Mensagem final
# -----------------------------
print("✅ Dados exportados com sucesso!")
print(f"📂 Arquivos salvos em: {pasta_destino}")

# -----------------------------
# 11) Fechar conexão
# -----------------------------
conn.close()
