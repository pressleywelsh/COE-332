from pydantic import BaseModel

class countryData(BaseModel):
    country: str
    country_code: str
    year: int
    health_exp: float
    life_expect: float
    maternal_mortality: int
    infant_mortality: float
    neonatal_mortality: float
    under_5_mortality: float
    prev_hiv: float
    inci_tuberc: float
    prev_undernourishment: float

