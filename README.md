# 📄 README – Automação de Exportação SQL Server + Validação WhatsApp (Meta API)

## 🚀 Visão Geral
Este projeto automatiza a extração de dados de clientes de um banco **SQL Server**, exporta os resultados para planilhas **Excel** e valida até **100 números de telefone** usando a **API oficial da Meta (WhatsApp Cloud API)**.

## 🔧 Funcionalidades
- Conectar ao banco de dados SQL Server  
- Extrair dados de **CPF e Telefone** de clientes  
- Limpar registros inválidos (nulos ou vazios)  
- Exportar todos os dados para **Excel**  
- Validar até 100 números de telefone com a API oficial da Meta  
- Exportar os resultados da validação para outra planilha  

---

## 📂 Estrutura de Pastas
```
automacao_relatorio/
│
├── Report_number_whatsapp/     # Saída dos relatórios em Excel
│   ├── dados_clientes.xlsx     # Todos os clientes exportados
│   ├── validacao_whatsapp.xlsx # Resultados da validação
│
├── .env                        # Variáveis de ambiente (não versionar no Git)
├── requirements.txt            # Dependências do projeto
├── automacao_whatsapp.py       # Script principal
└── README.md                   # Documentação
```

---

## ⚙️ Configuração do Ambiente

### 1. Clonar o projeto
```bash
git clone https://github.com/seu-repositorio/automacao-whatsapp.git
cd automacao-whatsapp
```

### 2. Criar ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

**requirements.txt**
```
pyodbc
pandas
python-dotenv
openpyxl
requests
```

---

## 🔑 Configuração do `.env`
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```ini
# Conexão com SQL Server
DB_SERVER=SEU_SERVIDOR_SQL
DB_DATABASE=SEU_BANCO_SQL

# Credenciais da API Meta (WhatsApp Cloud API)
META_TOKEN=seu_token_de_acesso
META_PHONE_ID=seu_phone_number_id
```

- **META_TOKEN** → Gere no [Meta for Developers](https://developers.facebook.com/).  
- **META_PHONE_ID** → ID do número registrado no WhatsApp Business.  

---

## ▶️ Como Executar
```bash
python automacao_whatsapp.py
```

### Saída esperada no terminal:
```
✅ Dados exportados com sucesso!
📂 Arquivos salvos em: automacao_relatorio\Report_number_whatsapp
```

---

## 📊 Resultados
- **dados_clientes.xlsx** → Todos os clientes exportados do SQL Server.  
- **validacao_whatsapp.xlsx** → Até 100 números com status de validação (`valid`, `invalid`, `erro API`).  

---

## 📚 Referências
- [Documentação oficial WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)  
- [Biblioteca Requests](https://requests.readthedocs.io/)  
- [pandas](https://pandas.pydata.org/)  
