#Importar librerias
from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import uvicorn

#Crear una instancia de la aplicación FastAPI
app = FastAPI()

#Descargar datos historicos
tickers_sec = ["XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLK", "XLU", "XLB", "XLC"]
data_sect_total = yf.download(tickers_sec, start="2000-01-01", end="2023-06-01")

@app.get("/calcular_roi_sectores/{inversion_inicial}")
async def calcular_roi_sectores_endpoint(inversion_inicial: float):
    result = []
    for sector in tickers_sec:
        #Obtener el precio de cierre ajustado más reciente
        precio_actual = data_sect_total["Adj Close"].tail(1)[sector]
        # Calcular el precio de cierre ajustado hace 1 año
        precio_hace_un_anio = data_sect_total.shift(252)["Adj Close"].shift(252).dropna()[sector][0]
        # Calcular el ROI para el último año
        ganancia = precio_actual - precio_hace_un_anio
        roi = (ganancia / precio_hace_un_anio) * 100
        # Calcular el valor de la inversión después de 1 año
        valor_final = inversion_inicial * (1 + roi / 100)

        #Retornar resultados para cada sector
        sector_result = {
            "sector": sector,
            "inversion_inicial": inversion_inicial,
            "roi_ultimo_anio": round(roi, 2),
            "valor_final_anio": round(valor_final, 2)
        }
        result.append(sector_result)

    return result


#Ejecuta la aplicación FastAPI:
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)


