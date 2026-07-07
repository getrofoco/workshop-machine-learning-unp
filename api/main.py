import os
import pickle
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ImovelInput, ImovelOutput

# Dicionário global para armazenar o modelo carregado
ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Este código roda uma vez quando a API sobe
    # Carregamos o modelo para a memória aqui para evitar ler do disco a cada requisição
    caminho_modelo = os.path.join(
        os.path.dirname(__file__), "..", "models", "modelo_imoveis.pkl"
    )
    # DESAFIO 6: Descomente o bloco abaixo para carregar o modelo treinado na inicialização da API
    try:
        with open(caminho_modelo, "rb") as f:
            ml_models["modelo_imoveis"] = pickle.load(f)

        print(f"Modelo carregado com sucesso de {caminho_modelo}")
    except FileNotFoundError:
        print(
            f"AVISO: Modelo não encontrado em {caminho_modelo}. Execute o notebook de treinamento primeiro!"
        )

    yield  # O aplicativo serve requisições aqui

    # Limpeza se necessário
    ml_models.clear()


# Inicializando a aplicação FastAPI
app = FastAPI(
    title="API Previsão de Preços de Imóveis",
    description="API construída no Workshop de Machine Learning para prever preços de imóveis usando Random Forest.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configurando para permitir requisições de outras origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    """
    Rota principal de health check da API.
    """
    return {
        "message": "API de Previsão de Imóveis em execução. Acesse /docs para a documentação."
    }


@app.post("/predict", response_model=ImovelOutput)
async def predict_price(imovel: ImovelInput):
    """
    Recebe os dados do imóvel, formata para o modelo e retorna o preço previsto.
    """
    # 1. Recuperamos o dicionário do modelo carregado no startup
    modelo_dict = ml_models.get("modelo_imoveis")

    if not modelo_dict:
        # Se o modelo não estiver carregado, retornamos 0 para não quebrar o frontend/schema
        return ImovelOutput(preco_sugerido=0, preco_minimo=0, preco_maximo=0)

    # DESAFIO 7: Descomente as linhas abaixo para extrair o modelo e as features
    rf_model = modelo_dict["model"]
    features_esperadas = modelo_dict["features"]
    rmse = modelo_dict["rmse_teste"]

    features_esperadas = ["area_m2", "quartos", "banheiros", "vagas", "idade_anos"]

    # 2. Preparamos os dados de entrada no formato (DataFrame) que o scikit-learn espera
    # O pydantic garante que recebemos exatamente o que o schema define.
    input_df = pd.DataFrame(
        [
            {
                "area_m2": imovel.area_m2,
                "quartos": imovel.quartos,
                "banheiros": imovel.banheiros,
                "vagas": imovel.vagas,
                "idade_anos": imovel.idade_anos,
            }
        ]
    )

    # Garantindo a ordem correta das colunas (mesmas do treinamento)
    # DESAFIO 8: Descomente a linha abaixo para alinhar as colunas com as que o modelo espera
    input_df = input_df[features_esperadas]

    # 3. Fazendo a previsão
    # DESAFIO 9: Descomente as linhas abaixo para fazer a previsão com o modelo
    preco_previsto = rf_model.predict(input_df)[0]
    preco_minimo = max(0, preco_previsto - rmse)
    preco_maximo = preco_previsto + rmse

    # Valores temporários enquanto o desafio não for feito
    preco_previsto = 0
    preco_minimo = 0
    preco_maximo = 0

    return ImovelOutput(
        preco_sugerido=round(preco_previsto, 2),
        preco_minimo=round(preco_minimo, 2),
        preco_maximo=round(preco_maximo, 2),
    )
