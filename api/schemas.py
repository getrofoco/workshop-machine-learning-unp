from pydantic import BaseModel, Field

class ImovelInput(BaseModel):
    area_m2: float = Field(..., title="Área do Imóvel em m²", gt=0, example=150)
    quartos: int = Field(..., title="Quantidade de Quartos", ge=1, example=3)
    banheiros: int = Field(..., title="Quantidade de Banheiros", ge=1, example=2)
    vagas: int = Field(..., title="Vagas de Garagem", ge=0, example=2)
    idade_anos: int = Field(..., title="Idade do Imóvel em anos", ge=0, example=5)

class ImovelOutput(BaseModel):
    preco_sugerido: float = Field(..., title="Preço Sugerido (R$)")
    preco_minimo: float = Field(..., title="Preço Mínimo (Intervalo)")
    preco_maximo: float = Field(..., title="Preço Máximo (Intervalo)")
