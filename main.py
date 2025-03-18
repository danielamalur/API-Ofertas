from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def obtener_ofertas_dia():
    url = "https://www.dia.es/ofertas"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    ofertas = []
    productos = soup.select(".product-card")  # Ajustar según estructura real
    for producto in productos:
        nombre = producto.select_one(".product-title").text.strip()
        precio_anterior = producto.select_one(".old-price").text.strip()
        precio_oferta = producto.select_one(".new-price").text.strip()
        enlace = producto.select_one("a")["href"]
        ofertas.append({
            "supermercado": "DIA",
            "producto": nombre,
            "precioAnterior": precio_anterior,
            "precioOferta": precio_oferta,
            "descuento": calcular_descuento(precio_anterior, precio_oferta),
            "enlace": f"https://www.dia.es{enlace}"
        })
    return ofertas

def obtener_ofertas_carrefour():
    url = "https://www.carrefour.es/supermercado/ofertas"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    ofertas = []
    productos = soup.select(".offer-card")  # Ajustar según estructura real
    for producto in productos:
        nombre = producto.select_one(".product-name").text.strip()
        precio_anterior = producto.select_one(".original-price").text.strip()
        precio_oferta = producto.select_one(".current-price").text.strip()
        enlace = producto.select_one("a")["href"]
        ofertas.append({
            "supermercado": "Carrefour",
            "producto": nombre,
            "precioAnterior": precio_anterior,
            "precioOferta": precio_oferta,
            "descuento": calcular_descuento(precio_anterior, precio_oferta),
            "enlace": f"https://www.carrefour.es{enlace}"
        })
    return ofertas

def obtener_ofertas_alcampo():
    url = "https://www.alcampo.es/compra-online/ofertas"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    ofertas = []
    productos = soup.select(".product-item")  # Ajustar según estructura real
    for producto in productos:
        nombre = producto.select_one(".product-title").text.strip()
        precio_anterior = producto.select_one(".price-old").text.strip()
        precio_oferta = producto.select_one(".price-new").text.strip()
        enlace = producto.select_one("a")["href"]
        ofertas.append({
            "supermercado": "Alcampo",
            "producto": nombre,
            "precioAnterior": precio_anterior,
            "precioOferta": precio_oferta,
            "descuento": calcular_descuento(precio_anterior, precio_oferta),
            "enlace": f"https://www.alcampo.es{enlace}"
        })
    return ofertas

def calcular_descuento(precio_anterior, precio_oferta):
    try:
        precio_anterior = float(precio_anterior.replace("€", "").replace(",", "."))
        precio_oferta = float(precio_oferta.replace("€", "").replace(",", "."))
        return round((1 - (precio_oferta / precio_anterior)) * 100, 2)
    except:
        return 0

@app.get("/ofertas")
def leer_ofertas():
    ofertas = []
    ofertas.extend(obtener_ofertas_dia())
    ofertas.extend(obtener_ofertas_carrefour())
    ofertas.extend(obtener_ofertas_alcampo())
    return ofertas
