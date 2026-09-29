# StockMaster - Back-End

API Back-End desenvolvida para o sistema **StockMaster**, projeto acadêmico voltado ao gerenciamento e controle de estoque.

## 📌 Sobre o projeto

O StockMaster é um sistema web de controle de estoque destinado a pequenos negócios. O Back-End é responsável pelo gerenciamento dos dados e pelas regras de negócio utilizadas pelo sistema.

## 🚀 Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Swagger / OpenAPI

## ⚙️ Funcionalidades

A API possui recursos para:

- Cadastro, consulta, atualização e exclusão de produtos
- Consulta de produtos e inventário
- Registro de entrada de estoque
- Registro de saída de estoque
- Histórico de movimentações
- Alerta de estoque mínimo
- Alerta de produtos próximos da validade ou vencidos
- Gerenciamento de usuários
- Autenticação de usuários
- Perfis de Administrador e Operador

## 📂 Estrutura do projeto

```text
stockmaster-backend/
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── alertas.py
│   │   ├── movimentacoes.py
│   │   ├── produtos.py
│   │   └── usuarios.py
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── requirements.txt
└── README.md
```

## ▶️ Executando o projeto

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

Após iniciar, a documentação interativa estará disponível no Swagger:

```text
http://127.0.0.1:8000/docs
```

## 📚 Documentação da API

O FastAPI gera automaticamente a documentação da API utilizando o padrão OpenAPI.

Principais grupos de endpoints:

- Produtos
- Movimentações
- Alertas
- Usuários

## 👥 Projeto acadêmico

Projeto desenvolvido na disciplina de Projeto Integrador do curso de Sistemas para Internet - UAPI/UESPI.

### Equipe Alpha

- Daniel Rufino
- Francisco Igor
- Lucas Passos
- Maria Geane
- Maria Gerlane
- Naiara Souza da Silva 