# Dashboard Interativo – Yelp Analytics

Este dashboard foi desenvolvido com **Dash** para visualização interativa e inferência em tempo real dos modelos de Machine Learning treinados a partir dos dados do Yelp.
O funcionamento do dashboard depende de um **backend em FastAPI**, responsável por expor os modelos de inferência via API REST.

## Funcionalidades

- Classificação de sentimento de avaliações textuais
- Predição do cluster de um estabelecimento
- Interface amigável e responsiva
- Integração direta com a API FastAPI

## Estrutura

- `app.py`: aplicação principal do Dash
- `pages/`: páginas do dashboard
- `data/`: dados auxiliares para visualização
- `assets/`: arquivos de estilo
- `backend/`: API FastAPI responsável pelas inferências
- `backend/models`: modelos treinados e pipelines utilizados pelo backend
- `requirements.txt/`: pacotes necessários para a aplicação

## Backend (FastAPI)

O backend é responsável por:
- Carregar os modelos treinados (`.pkl`)
- Executar a inferência de sentimento e clusterização
- Disponibilizar os resultados via endpoints REST

## Executar o Dashboard

### 1. Iniciar o Backend

A partir da raiz do projeto:

```bash
uvicorn backend.backend:app --reload
```

O backend ficará disponível em:

```bash
http://127.0.0.1:8000
```

### 2. Iniciar o dashboard

Em outro terminal, na pasta dashboard/:

```bash
python app.py
```

O dashboard será carregado automaticamente no navegador.

## Integração com o Backend

O dashboard consome os endpoints:

```bash
/predict/sentiment

/predict/cluster
```

via requisições HTTP utilizando a biblioteca requests.

## Integração Dashboard ↔ Backend

O dashboard consome os endpoints do backend por meio de requisições HTTP utilizando a biblioteca requests.

Exemplos:

- Classificação de sentimento de avaliações textuais
- Predição do cluster de um estabelecimento

Essa separação permite escalabilidade, reutilização da API e facilidade de deploy em ambientes de produção.


