# Order Management API

API desenvolvida em **Python** com **FastAPI**, para gerenciamento de pedidos com autenticação de usuários via **JWT**.  
O projeto inclui criação de contas, login, refresh de token, além de CRUD de pedidos e itens relacionados.  

---

## 🚀 Tecnologias utilizadas
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web rápido e moderno
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para banco de dados
- [Passlib (bcrypt)](https://passlib.readthedocs.io/en/stable/) - Criptografia de senhas
- [Python-Jose](https://python-jose.readthedocs.io/en/latest/) - Geração e validação de JWT
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para rodar a API
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Migrações de banco de dados
- [Requests](https://docs.python-requests.org/en/master/) - Testes e consumo da API
- [Python-dotenv](https://pypi.org/project/python-dotenv/) - Gerenciamento de variáveis de ambiente

---

## 📂 Estrutura do projeto
```
.
├── main.py              # Arquivo principal da aplicação
├── auth_routes.py       # Rotas de autenticação
├── order_routes.py      # Rotas de pedidos
├── models.py            # Modelos do banco de dados
├── schemas.py           # Schemas Pydantic
├── testes.py            # Exemplo de requisições à API
├── requirements.txt     # Dependências do projeto
└── database/            # Banco SQLite
```

---

## ⚙️ Como rodar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/DanielMaffi/Fastapi-orders.git
cd order-management-api
```

### 2. Criar e ativar um ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente  
Crie um arquivo `.env` na raiz com os valores:

```env
SECRET_KEY=chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Rodar as migrações do banco
```bash
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```

### 6. Iniciar o servidor
```bash
uvicorn main:app --reload
```

Normalmente a API ficará disponível em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

---

## 🔑 Endpoints principais

### Autenticação
- `POST /auth/criar_conta` → Criar novo usuário  
- `POST /auth/login` → Login com e-mail e senha  
- `POST /auth/login-form` → Login com formulário OAuth2  
- `GET /auth/refresh` → Gera novo token de acesso  

### Pedidos
- `POST /order/pedido` → Criar pedido  
- `POST /order/pedido/cancelar/{id}` → Cancelar pedido  
- `POST /order/pedido/adicionar-item/{id}` → Adicionar item ao pedido  
- `POST /order/pedido/remover-item/{id}` → Remover item do pedido  
- `POST /order/pedido/finalizar/{id}` → Finalizar pedido  
- `GET /order/pedido/{id}` → Detalhar pedido  
- `GET /order/listar` → Listar todos pedidos (apenas admin)  
- `GET /order/listar/pedidos-usuario` → Listar pedidos do usuário logado  

---

## 👤 Autor
Desenvolvido por **DanielMaffi**