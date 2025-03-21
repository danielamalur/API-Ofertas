from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI()

def obtener_ofertas_dia():
    url = "https://www.dia.es/ofertas"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.google.com/"
    }
    response = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(response.text, "html.parser")
    
    ofertas = []
    productos = soup.select(".product-card")  # Ajustar según estructura real
    for producto in productos:
        nombre = producto.select_one(".product-title").text.strip()
        precio_anterior = producto.select_one(".old-price").text.strip()
        precio_oferta = producto.select_one(".new-price").text.strip()
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.google.com/"
    }
    response = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(response.text, "html.parser")
    
    ofertas = []
    productos = soup.select(".product-card")  # Ajustar según estructura real
    for producto in productos:
        nombre = producto.select_one(".product-title").text.strip()
        precio_anterior = producto.select_one(".old-price").text.strip()
        precio_oferta = producto.select_one(".new-price").text.strip()
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

import os

@app.get("/test-connection")
def test_connection():
    try:
        dia_response = os.popen("curl -I https://www.dia.es").read()
        carrefour_response = os.popen("curl -I https://www.carrefour.es").read()
        alcampo_response = os.popen("curl -I https://www.alcampo.es").read()

        return {
            "DIA": dia_response,
            "Carrefour": carrefour_response,
            "Alcampo": alcampo_response
        }
    except Exception as e:
        return {"error": str(e)}
