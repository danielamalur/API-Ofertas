from fastapi import FastAPI

app = FastAPI()

# Datos de prueba con ofertas de supermercados
def obtener_ofertas():
    return [
        {
            "supermercado": "DIA",
            "producto": "Leche Semidesnatada 1L",
            "precioAnterior": 1.20,
            "precioOferta": 0.99,
            "descuento": 17,
            "enlace": "https://www.dia.es/leche-oferta"
        },
        {
            "supermercado": "Carrefour",
            "producto": "Pan de Molde Integral 500g",
            "precioAnterior": 1.50,
            "precioOferta": 1.20,
            "descuento": 20,
            "enlace": "https://www.carrefour.es/pan-oferta"
        },
        {
            "supermercado": "Alcampo",
            "producto": "Aceite de Oliva Virgen Extra 1L",
            "precioAnterior": 6.50,
            "precioOferta": 5.85,
            "descuento": 10,
            "enlace": "https://www.alcampo.es/aceite-oferta"
        }
    ]

@app.get("/ofertas")
def leer_ofertas():
    return obtener_ofertas()
