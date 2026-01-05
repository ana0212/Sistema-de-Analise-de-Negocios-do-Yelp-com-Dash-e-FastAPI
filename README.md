# Sistema de Análise de Negócios do Yelp com Dash e FastAPI

Este projeto apresenta um sistema completo de análise de dados do Yelp, integrando **Machine Learning**, **API REST** e **Dashboard interativo** para apoio à tomada de decisão em negócios locais.

A solução permite:
- Classificação automática de sentimento de avaliações textuais
- Clusterização de estabelecimentos com base em métricas de desempenho
- Visualização interativa e inferência em tempo real via dashboard web

## Objetivo Profissional

Este projeto foi desenvolvido com foco em Data Science aplicada, engenharia de modelos e deploy de aplicações analíticas, sendo ideal para demonstração em portfólio profissional.

## Arquitetura do Projeto

O sistema é dividido em três camadas principais:

- **Notebooks**: análise exploratória, segmentação dos estabelecimentos (análise de cluster) e treinamento dos modelos de análise de sentimento
- **Backend (FastAPI)**: disponibiliza os modelos treinados via endpoints REST
- **Dashboard (Dash)**: interface interativa para visualização e inferência

## Demonstração
- [Acesse o app online](https://yelp-dashboard.onrender.com/)

## Resultados Principais

### Classificação de Sentimento

Modelo supervisionado treinado a partir de avaliações textuais do Yelp.

**Métricas de desempenho:**
- **Acurácia:** 86,56%
- **AUC-ROC:** 0,943
- **Recall (classe negativa):** 0,869
- **Recall (classe positiva):** 0,864

Esses resultados indicam bom equilíbrio entre classes, alta capacidade discriminativa e robustez na identificação de sentimentos positivos e negativos.

### Clusterização de Negócios

Os estabelecimentos foram segmentados com base em:
- Média de estrelas
- Número de avaliações

**Interpretação dos clusters:**

- **Cluster 0 — Baixa avaliação e baixo engajamento**  
  Negócios que podem ser priorizados em iniciativas de melhoria da experiência do cliente, revisão de processos operacionais e capacitação, reduzindo riscos de churn e avaliações negativas.

- **Cluster 1 — Alta avaliação e baixo engajamento**  
  Representam oportunidades estratégicas para ações de marketing, aumento de visibilidade na plataforma e estímulo à geração de avaliações, ampliando alcance sem comprometer a percepção de qualidade.

- **Cluster 2 — Boa avaliação e alto engajamento**  
  Segmento mais consolidado, no qual estratégias de retenção, fidelização e consistência da experiência tendem a gerar maior retorno.

## Funcionalidades

- Classificação de sentimento de avaliações (positivo / negativo)
- Predição do cluster de um estabelecimento com base em:
  - Média de estrelas
  - Número de avaliações
- Dashboard interativo com múltiplas páginas
- Inferência em tempo real via API

## Tecnologias Utilizadas

- Python
- Pandas, NumPy
- Scikit-learn
- NLTK / SpaCy
- FastAPI
- Dash & Dash Bootstrap Components
- Plotly
- Joblib
- Uvicorn

## Execução Local

### 1. Backend (API)
```bash
uvicorn backend.backend:app --reload
```

### 2. Dashboard
```bash
python dashboard/app.py
```

A aplicação ficará disponível localmente no navegador.

## Endpoints da API
```bash
POST /predict/sentiment

POST /predict/cluster
```

## Observações sobre os Dados

Os datasets completos não estão versionados no repositório devido a limitações de tamanho.
O projeto utiliza versões processadas e modelos previamente treinados para inferência.





