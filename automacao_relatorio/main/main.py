# ====================================================
# Exportar dados do SQL Server para Excel + Validação WhatsApp (API Meta)
# Autor: João Mocambite
# Objetivo: 
#   1) Conectar ao banco SQL Server e buscar dados de clientes
#   2) Exportar todos os registros para Excel
#   3) Validar até 100 números de telefone usando a API oficial da Meta (WhatsApp Cloud API)
#   4) Exportar os resultados da validação para outra planilha Excel
# ====================================================

# Bibliotecas necessárias
import pyodbc          # Conexão com SQL Server
import pandas as pd    # Manipulação de dados (DataFrame)
from dotenv import load_dotenv  # Carregar variáveis de ambiente (.env)
import os              # Manipular pastas e caminhos
import requests        # Fazer requisições HTTP (chamada na API Meta)
import time            # Usado para dar pausas entre chamadas da API

# -----------------------------
# 1) Carregar variáveis do arquivo .env
# -----------------------------
# O arquivo .env guarda informações sensíveis (como servidor e banco de dados)
load_dotenv()
server = os.getenv("DB_SERVER")        # Nome do servidor SQL
database = os.getenv("DB_DATABASE")    # Nome do banco de dados
access_token = os.getenv("META_TOKEN") # Token de acesso da API Meta
phone_number_id = os.getenv("META_PHONE_ID")  # ID do número do WhatsApp Business

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
# 7) Validar até 100 números de telefone com a API Meta (WhatsApp Cloud API)
# -----------------------------
# Endpoint oficial da Meta: POST /{Phone-Number-ID}/contacts
# Doc: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/contacts
# Obs: Necessário token válido e ID do número configurados no .env
resultados = []
numeros_validar = df["Telefone_Celular"].head(100)  # pega só os 100 primeiros números

url = f"https://graph.facebook.com/v20.0/{phone_number_id}/contacts"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

for numero in numeros_validar:
    try:
        payload = {
            "blocking": "wait",
            "contacts": [str(numero)],
            "force_check": True
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            data = r.json()
            # Se o número é válido no WhatsApp
            if "contacts" in data and data["contacts"]:
                resultados.append(data["contacts"][0].get("status", "desconhecido"))
            else:
                resultados.append("não encontrado")
        else:
            resultados.append(f"Erro API ({r.status_code})")
    except Exception as e:
        resultados.append("Erro conexão")
    time.sleep(1)  # pausa de 1s para não sobrecarregar a API

# -----------------------------
# 8) Criar DataFrame com os 100 números validados
# -----------------------------
df_validacao = pd.DataFrame({
    "Telefone_Celular": numeros_validar.values,
    "WhatsApp_Status": resultados
})

# -----------------------------
# 9) Exportar dados para Excel
# -----------------------------
# a) Todos os dados
caminho_excel = os.path.join(pasta_destino, "dados_clientes.xlsx")
df.to_excel(caminho_excel, index=False)

# b) Apenas os 100 validados
caminho_validacao = os.path.join(pasta_destino, "validacao_whatsapp.xlsx")
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
