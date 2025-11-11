"""
EJERCICIO 2: Agente de Información de Países con API Pública - SOLUCIÓN

Este agente inteligente:
1. Recibe consultas en lenguaje natural sobre países
2. Usa LLM para extraer el país de la consulta
3. Consulta la API REST Countries para obtener datos reales
4. Usa LLM para formatear la respuesta de forma conversacional
"""

import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extraer_pais(consulta_usuario):
    """
    Usa el LLM para extraer el nombre del país de la consulta del usuario.
    
    Args:
        consulta_usuario: La pregunta del usuario en lenguaje natural
    
    Returns:
        El nombre del país en inglés (para la API)
    """
    prompt = f"""Extrae el nombre del país de la siguiente consulta del usuario.
Responde ÚNICAMENTE con el nombre del país en inglés, sin ninguna explicación adicional.
Si no hay un país mencionado, responde "NONE".

Consulta del usuario: "{consulta_usuario}"

Nombre del país en inglés:"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=50
    )
    
    pais = response.choices[0].message.content.strip()
    return None if pais == "NONE" else pais


def consultar_api_paises(nombre_pais):
    """
    Consulta la API de REST Countries para obtener información del país.
    
    Args:
        nombre_pais: Nombre del país en inglés
    
    Returns:
        Diccionario con los datos del país o None si hay error
    """
    url = f"https://restcountries.com/v3.1/name/{nombre_pais}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            datos = response.json()
            # La API devuelve una lista, tomamos el primer resultado
            return datos[0]
        else:
            print(f"Error: La API respondió con código {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None


def formatear_respuesta(consulta_usuario, datos_pais):
    """
    Usa el LLM para formatear los datos del país en una respuesta natural.
    
    Args:
        consulta_usuario: La pregunta original del usuario
        datos_pais: Diccionario con los datos del país de la API
    
    Returns:
        Respuesta formateada en lenguaje natural
    """
    # Extraer información relevante de los datos del país
    nombre = datos_pais.get('name', {}).get('common', 'N/A')
    capital = datos_pais.get('capital', ['N/A'])[0] if datos_pais.get('capital') else 'N/A'
    poblacion = datos_pais.get('population', 'N/A')
    region = datos_pais.get('region', 'N/A')
    subregion = datos_pais.get('subregion', 'N/A')
    area = datos_pais.get('area', 'N/A')
    bandera = datos_pais.get('flag', '')
    
    # Formatear idiomas
    idiomas = datos_pais.get('languages', {})
    idiomas_str = ', '.join(idiomas.values()) if idiomas else 'N/A'
    
    # Formatear monedas
    monedas = datos_pais.get('currencies', {})
    monedas_list = []
    for codigo, info in monedas.items():
        nombre_moneda = info.get('name', codigo)
        simbolo = info.get('symbol', '')
        monedas_list.append(f"{nombre_moneda} ({simbolo})" if simbolo else nombre_moneda)
    monedas_str = ', '.join(monedas_list) if monedas_list else 'N/A'
    
    # Crear información estructurada para el LLM
    info_pais = f"""
Información del país:
- Nombre: {nombre} {bandera}
- Capital: {capital}
- Población: {poblacion:,} habitantes
- Región: {region}
- Subregión: {subregion}
- Área: {area:,} km²
- Idiomas: {idiomas_str}
- Monedas: {monedas_str}
"""
    
    # Crear el prompt para el LLM
    prompt = f"""Eres un asistente útil que responde preguntas sobre países.

Consulta del usuario: "{consulta_usuario}"

{info_pais}

Instrucciones:
1. Responde específicamente a lo que el usuario preguntó
2. Usa un tono conversacional y amigable
3. Incluye solo la información relevante para su pregunta
4. Si pregunta por algo específico, enfócate en eso
5. Puedes agregar un dato interesante adicional si es relevante

Respuesta:"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    
    return response.choices[0].message.content.strip()


def agente_paises(consulta_usuario):
    """
    Función principal del agente que orquesta todo el flujo.
    
    Args:
        consulta_usuario: La pregunta del usuario
    
    Returns:
        Respuesta final del agente
    """
    print(f"\n🤖 Agente: Procesando tu consulta...\n")
    
    # PASO 1: Extraer el país de la consulta
    print("📍 Paso 1: Identificando el país...")
    pais = extraer_pais(consulta_usuario)
    
    if not pais:
        return "❌ No pude identificar el país en tu consulta. ¿Podrías reformularla?"
    
    print(f"   ✓ País identificado: {pais}")
    
    # PASO 2: Consultar la API
    print("🌍 Paso 2: Consultando información del país...")
    datos = consultar_api_paises(pais)
    
    if not datos:
        return f"❌ No encontré información sobre '{pais}'. Verifica el nombre del país."
    
    print(f"   ✓ Datos obtenidos de la API")
    
    # PASO 3: Formatear la respuesta
    print("💬 Paso 3: Generando respuesta natural...\n")
    respuesta = formatear_respuesta(consulta_usuario, datos)
    
    return respuesta


def main():
    print("=" * 80)
    print("🌎 AGENTE DE INFORMACIÓN DE PAÍSES")
    print("=" * 80)
    print("\nEste agente puede responder preguntas sobre países del mundo.")
    print("Ejemplos:")
    print("  - ¿Cuál es la capital de Francia?")
    print("  - Dime la población de Japón")
    print("  - ¿Qué moneda usa Argentina?")
    print("  - Información sobre Italia")
    print("  - ¿Qué idiomas se hablan en Suiza?")
    print("\nEscribe 'salir' para terminar.")
    print("=" * 80)
    
    while True:
        consulta = input("\n👤 Tu consulta: ").strip()
        
        if consulta.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 ¡Hasta luego!")
            break
        
        if not consulta:
            print("⚠️  Por favor, escribe una consulta.")
            continue
        
        # Llamar al agente con la consulta
        respuesta = agente_paises(consulta)
        
        # Mostrar la respuesta
        print(f"\n🤖 Agente: {respuesta}")
        print("\n" + "-" * 80)


if __name__ == "__main__":
    main()
