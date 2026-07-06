# Usar imagem oficial baseada no Debian slim para tamanho reduzido
FROM python:3.13-slim

# Copiar o binário pré-compilado do uv diretamente da imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Variáveis de ambiente para o uv e Python
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1

# Configurar diretório de trabalho
WORKDIR /app

# Primeiro, instalamos as dependências para aproveitar o cache de camadas do Docker
COPY pyproject.toml .
# Instalar apenas as dependências principais de produção sem criar ambiente virtual (.venv) dentro do container (usando sistema do container)
RUN uv pip install --system fastapi uvicorn scikit-learn pandas numpy pydantic

# Copiar o restante do código
COPY . .

# A porta que o Cloud Run espera por padrão é 8080
ENV PORT=8080
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
