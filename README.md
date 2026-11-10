# Store API

API REST para gerenciamento de produtos, desenvolvida com **FastAPI**, **MongoDB** e testes automatizados com **Pytest**.

O projeto nasceu de um desafio educacional da [Digital Innovation One (DIO)](https://www.dio.me/) para praticar **TDD — desenvolvimento orientado por testes** — em uma aplicação Python assíncrona.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Execução local](#execução-local)
- [Endpoints e exemplos de uso](#endpoints-e-exemplos-de-uso)
- [Testes](#testes)
- [Próximos passos](#próximos-passos)

## Funcionalidades

- Cadastro de produtos com nome, quantidade, preço e status.
- Consulta de um produto por identificador UUID.
- Listagem de produtos com filtros opcionais de preço mínimo e máximo.
- Consulta de produtos com preço entre 5.000 e 8.000, com limites exclusivos.
- Atualização parcial de quantidade, preço e status, com registro automático de `updated_at`.
- Exclusão de produtos.
- Validação dos dados de entrada e respostas HTTP para produtos não encontrados.
- Documentação interativa gerada pelo FastAPI.

## Tecnologias

| Tecnologia | Papel no projeto |
| --- | --- |
| Python 3.12 | Versão de referência definida em `.python-version` |
| FastAPI e Uvicorn | Definição das rotas HTTP e execução da API |
| Pydantic e Pydantic Settings | Validação de dados e leitura das configurações |
| MongoDB e Motor | Persistência e acesso assíncrono ao banco de dados |
| Pytest, pytest-asyncio e HTTPX | Testes de schemas, casos de uso e endpoints |
| Poetry | Gerenciamento de dependências e ambiente Python |
| Docker Compose | Execução local do MongoDB |
| pre-commit, Ruff e Black | Verificações e formatação configuradas para o desenvolvimento |

As dependências e suas restrições de versão estão em [`app/pyproject.toml`](app/pyproject.toml); as versões resolvidas estão em [`app/poetry.lock`](app/poetry.lock).

## Estrutura do projeto

```text
store_api/
├── README.md
├── .python-version
└── app/
    ├── docker-compose.yml      # Serviço local do MongoDB
    ├── Makefile                # Atalhos para execução e testes
    ├── pyproject.toml          # Dependências e configuração do Pytest
    ├── poetry.lock
    ├── store/
    │   ├── main.py             # Criação da aplicação FastAPI
    │   ├── routers.py          # Registro das rotas
    │   ├── controllers/        # Endpoints e respostas HTTP
    │   ├── core/               # Configurações e exceções
    │   ├── db/                 # Conexão com o MongoDB
    │   ├── models/             # Modelos usados na persistência
    │   ├── schemas/            # Contratos de entrada e saída
    │   └── usecases/           # Operações de negócio e acesso aos produtos
    └── tests/
        ├── controllers/        # Testes dos endpoints HTTP
        ├── schemas/            # Testes de validação dos dados
        ├── usecases/           # Testes dos casos de uso
        ├── conftest.py         # Preparação e limpeza do ambiente de testes
        └── factories.py        # Dados de exemplo para os testes
```

As requisições passam pelos controllers, que recebem e respondem às chamadas HTTP, e pelos casos de uso, que executam as operações sobre os produtos. Os schemas definem os dados aceitos e retornados pela API.

## Execução local

### Pré-requisitos

- Python **3.12**, conforme a versão de referência do projeto.
- Poetry instalado.
- Docker com Docker Compose, ou uma instância local de MongoDB acessível.
- Git para clonar o repositório.

### 1. Clone o repositório e instale as dependências

```bash
git clone https://github.com/FilipeMadeira13/store_api.git
cd store_api/app
poetry install --no-root
```

A opção `--no-root` instala as dependências sem instalar o próprio projeto como um pacote Python. Execute os próximos comandos a partir da pasta **`app/`**.

### 2. Configure as variáveis de ambiente

Edite o arquivo **`app/.env`**, localizado na pasta da aplicação. Para desenvolvimento local, utilize:

```dotenv
DATABASE_URL=mongodb://localhost:27017/store?uuidRepresentation=standard
PROJECT_NAME="Store API"
ROOT_PATH=/
```

| Variável | Descrição | Obrigatória | Valor padrão |
| --- | --- | --- | --- |
| `DATABASE_URL` | URI de conexão, incluindo o nome do banco de dados | Sim | Sem padrão |
| `PROJECT_NAME` | Título exibido na documentação da API | Não | `Store API` |
| `ROOT_PATH` | Prefixo da aplicação ao executá-la atrás de um proxy | Não | `/` |

Na URI de exemplo, `store` é o banco de desenvolvimento. A opção `uuidRepresentation=standard` configura a representação dos identificadores UUID no MongoDB. Variáveis definidas no ambiente têm prioridade sobre o arquivo `.env`.

### 3. Inicie o MongoDB

```bash
docker compose up -d db
```

O arquivo Compose do projeto inicia o MongoDB na porta **27017**. Se você já utiliza outra instância, ajuste `DATABASE_URL` e siga para a próxima etapa.

### 4. Inicie a API

```bash
poetry run uvicorn store.main:app --reload
```

Com o Make instalado, você também pode usar `make run`.

Após iniciar a aplicação, acesse:

| Recurso | Endereço |
| --- | --- |
| Swagger UI — documentação para explorar e testar as rotas | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| ReDoc — documentação de referência | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |
| Especificação OpenAPI em JSON | [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json) |

## Endpoints e exemplos de uso

Todas as rotas de produtos utilizam o prefixo **`/products`**.

| Método | Rota | Operação | Resposta de sucesso |
| --- | --- | --- | --- |
| `POST` | `/products/` | Cadastrar um produto | `201 Created` |
| `GET` | `/products/` | Listar produtos, com filtros opcionais `min_price` e `max_price` | `200 OK` |
| `GET` | `/products/{id}` | Consultar um produto por UUID | `200 OK` |
| `GET` | `/products/filter/price` | Listar produtos com `5000 < price < 8000` | `200 OK` |
| `PATCH` | `/products/{id}` | Atualizar parcialmente um produto | `200 OK` |
| `DELETE` | `/products/{id}` | Excluir um produto | `204 No Content` |

As operações de consulta por ID, atualização e exclusão retornam `404 Not Found` quando o produto não existe. Dados incompatíveis com os schemas retornam `422 Unprocessable Entity`.

### Cadastrar um produto

```bash
curl -X POST 'http://127.0.0.1:8000/products/' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Iphone 14 Pro Max",
    "quantity": 10,
    "price": "7500.00",
    "status": true
  }'
```

Os quatro campos são obrigatórios no cadastro. A resposta inclui os dados do produto e os campos gerados `id`, `created_at` e `updated_at`. O preço é tratado como decimal e serializado como texto no JSON de resposta.

### Filtrar produtos por preço

```bash
curl 'http://127.0.0.1:8000/products/?min_price=5000&max_price=8000'
```

Os parâmetros são opcionais e podem ser usados separadamente. Os limites são **exclusivos**: nesse exemplo, produtos com preço exatamente igual a 5.000 ou 8.000 ficam fora do resultado.

O mesmo intervalo está disponível na rota dedicada:

```bash
curl 'http://127.0.0.1:8000/products/filter/price'
```

### Atualizar um produto

Substitua `<id>` pelo UUID retornado no cadastro:

```bash
curl -X PATCH 'http://127.0.0.1:8000/products/<id>' \
  -H 'Content-Type: application/json' \
  -d '{
    "quantity": 5,
    "price": "7200.00",
    "status": true
  }'
```

O `PATCH` aceita os campos opcionais `quantity`, `price` e `status`. O campo `updated_at` recebe automaticamente o horário da atualização.

## Testes

A suíte utiliza Pytest com suporte a funções assíncronas e está organizada em três grupos:

| Grupo | O que verifica |
| --- | --- |
| `tests/schemas/` | Validação dos dados de entrada |
| `tests/usecases/` | Operações sobre os produtos e interação com o MongoDB |
| `tests/controllers/` | Respostas HTTP, validação e cenários de produto não encontrado |

> **Use um banco exclusivo para testes.** A fixture de limpeza em `tests/conftest.py` apaga os documentos de todas as coleções que não começam com `system` no banco configurado após cada teste. O comando abaixo seleciona `store_test`, separado do banco de desenvolvimento.

Com o MongoDB disponível, execute na pasta `app/`:

```bash
DATABASE_URL='mongodb://localhost:27017/store_test?uuidRepresentation=standard' \
  poetry run pytest
```

Para executar apenas os testes dos endpoints com saída detalhada:

```bash
DATABASE_URL='mongodb://localhost:27017/store_test?uuidRepresentation=standard' \
  poetry run pytest tests/controllers/ -v
```

O MongoDB também é necessário ao executar somente os testes de schemas, pois a fixture de limpeza é aplicada automaticamente a todos os testes.

## Próximos passos

Como continuidade do desafio original:

- Mapear falhas de inserção no MongoDB para exceções tratadas pelo controller de cadastro.
- Permitir informar `updated_at` na atualização, mantendo o horário atual como padrão quando o campo não for enviado.
- Adicionar testes para os limites exclusivos dos filtros de preço.
