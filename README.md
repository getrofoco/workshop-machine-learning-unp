# Minicurso: Machine Learning na Prática até o Deploy

Este repositório contém o material do minicurso "Machine Learning na Prática".
O objetivo deste projeto é fornecer uma implementação completa, demonstrando as etapas necessárias para treinar um modelo preditivo e implantá-lo em ambiente de produção utilizando **Google Cloud Run**, **FastAPI**, **Docker** e **uv**.

## Estrutura do Projeto

* `data/`: Contém os scripts de pré-processamento e o conjunto de dados (`houses.csv`).
* `notebooks/`: Contém os experimentos e a rotina de treinamento dos modelos (`01_modelagem.ipynb`).
* `models/`: Diretório destinado ao armazenamento do modelo treinado serializado no formato `.pkl`.
* `api/`: Implementação do backend em FastAPI e esquemas de validação de dados via Pydantic.
* `Dockerfile`: Especificação para a construção da imagem de contêiner.
* `pyproject.toml`: Configuração e gerenciamento das dependências do projeto através da ferramenta `uv`.

---

## Execução do Projeto Localmente

### 1. Preparação do Ambiente com `uv`
O projeto utiliza o `uv` como gerenciador de dependências, devido à sua eficiência na resolução e instalação de pacotes.
* **Instalação do uv**: 
  * Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  * Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Após a instalação, abra o terminal no diretório raiz do projeto e instale as dependências executando o comando a seguir:
```bash
uv sync
```

### 2. Dados
Conjunto de dados `houses.csv` sintético com 5.000 amostras com características não-lineares, focadas no mercado imobiliário de alto padrão.

### 3. Modelagem e Treinamento
Para iniciar o ambiente Jupyter e visualizar o processo de treinamento:
```bash
uv run jupyter lab
```
Navegue até o diretório `notebooks/` e abra o arquivo `01_modelagem.ipynb`.
Ao executar as células do notebook, será possível analisar a comparação de desempenho entre um modelo de Regressão Linear e um modelo Random Forest otimizado via `GridSearchCV`. A execução final do notebook persistirá o modelo otimizado no diretório `models/`.

### 4. Inicialização da API
Com o modelo treinado, é possível iniciar o servidor da API para disponibilizar o serviço de inferência:
```bash
uv run uvicorn api.main:app --reload
```

O serviço estará acessível através do seguinte endereço:
- **Documentação da API (Swagger/OpenAPI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Teste de Inferência via Terminal (cURL)

A API processa requisições HTTP do tipo POST contendo objetos JSON na rota `/predict`. Para testar a inferência diretamente pelo terminal, utilize os exemplos abaixo:

**No Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -ContentType "application/json" -Body '{"area_m2": 260, "quartos": 4, "banheiros": 4, "vagas": 3, "idade_anos": 10}'
```

**No Linux/Mac/Git Bash:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "area_m2": 260,
  "quartos": 4,
  "banheiros": 4,
  "vagas": 3,
  "idade_anos": 10
}'
```

A resposta conterá o valor predito e o intervalo de confiança sugerido para a estimativa.

---

## Empacotamento da Aplicação com Docker

Para assegurar a reprodutibilidade e portabilidade do projeto, a aplicação foi configurada para ser encapsulada utilizando Docker.
*(Requisito: Docker instalado e configurado no ambiente local)*

```bash
# Construção da imagem Docker
docker build -t previsao-imoveis .

# Execução do contêiner com mapeamento da porta 8080
docker run -p 8080:8080 previsao-imoveis
```
O serviço estará disponível em `http://localhost:8080`.

---