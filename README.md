# 🐢 Jabuti CRUD API

API RESTful desenvolvida como parte de um desafio técnico, utilizando FastAPI, PostgreSQL e Redis, com arquitetura em camadas e suporte a cache.

---
## 🚀 Tecnologias utilizadas

- Python 3.11 
- FastAPI 
- Alchemy 
- PostgreSQL 
- Redis 
- Docker & Docker Compose 
- Pydantic

---
## 🧠 Arquitetura
```bash
app/
 ├── api/            # Rotas (controllers)
 ├── services/       # Regras de negócio
 ├── repositories/   # Acesso ao banco
 ├── models/         # Modelos ORM (SQLAlchemy)
 ├── schemas/        # Validação e serialização (Pydantic)
 ├── core/           # Configurações e DB
 ├── cache/          # Integração com Redis
```

---
## ⚙️ Como rodar o projeto

### 1. Clone o repositório
```bash
git clone <SEU_REPO>
cd jabuti_startproject
```

### 2. Suba os containers
```bash
docker compose up --build
```

### 3. Acesse a API

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

---
## 📌 Endpoints

### 🔹 Criar usuário
```bash
POST /users/
```
### 🔹 Listar usuários (com paginação)
```bash
GET /users/?limit=10&offset=0
```
### 🔹 Buscar usuário por ID
```bash
GET /users/{id}
```
### 🔹 Atualizar usuário
```bash
PUT /users/{id}
```
### 🔹 Deletar usuário
```bash
DELETE /users/{id}
```

--- 

##  ⚡ Cache com Redis

A API utiliza Redis para otimizar leitura de dados.

### Estratégia adotada:

#### ✅ Cache nos GETs 
- GET /users 
- GET /users/{id}

#### 🔄 Invalidação em escrita 
- POST → invalida listas 
- PUT → invalida usuário e listas 
- DELETE → invalida usuário e listas

### 🔑 Padrão das chaves
```code
user:{id}
users:list:{limit}:{offset}
```

### ⏱ TTL padrão
- 600 segundos (10 minutos)

--- 

## 🧪 Testes

```bash
http://localhost:8000/docs
```

### Fluxo recomendado:

1.	Criar usuário
2.	Listar usuários
3.	Buscar por ID
4.	Atualizar
5.	Deletar
6.	Validar erros (404, 409)

### 🐳 Serviços Docker

O projeto utiliza três serviços:
- app → FastAPI 
- db → PostgreSQL 
- cache → Redis

--- 

### 💡 Observações
- Cada requisição utiliza uma sessão isolada do banco (dependency injection)
- O cache segue padrão “cache-aside” 
- Estrutura preparada para escalar e evoluir

--- 

## 👨‍💻 Autor

Desenvolvido por Vitor Vargas Cardoso 🚀
