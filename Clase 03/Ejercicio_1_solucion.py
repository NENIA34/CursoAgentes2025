"""
Ejercicio 1: Sistema de 3 llamadas secuenciales al LLM
1. Elegir un área de negocio para IA con Agentic
2. Presentar un problema en esa industria
3. Proponer una solución de IA con Agentic
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llamar_llm(prompt, contexto_previo=None):
    """
    Función para hacer una llamada al LLM de OpenAI
    
    Args:
        prompt: El prompt a enviar al LLM
        contexto_previo: Contexto de llamadas anteriores (opcional)
    
    Returns:
        La respuesta del LLM
    """
    mensajes = []
    
    # Si hay contexto previo, agregarlo
    if contexto_previo:
        mensajes.extend(contexto_previo)
    
    # Agregar el nuevo prompt
    mensajes.append({"role": "user", "content": prompt})
    
    # Hacer la llamada al LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=mensajes,
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def main():
    print("=" * 80)
    print("EJERCICIO 1: Sistema de IA con Agentic - 3 Llamadas Secuenciales")
    print("=" * 80)
    
    # Mantener el historial de conversación
    historial = []
    
    # PASO 1: Elegir un área de negocio
    print("\n[PASO 1] Pidiendo al LLM que elija un área de negocio...\n")
    prompt_1 = """Elige un área de negocio específica que sea prometedora para implementar 
una solución de IA con Agentic (sistemas de IA que pueden actuar de forma autónoma). 
Responde de forma concisa indicando solo el área de negocio y una breve justificación 
de por qué es prometedora."""
    
    respuesta_1 = llamar_llm(prompt_1)
    print(f"Respuesta: {respuesta_1}")
    
    # Agregar al historial
    historial.append({"role": "user", "content": prompt_1})
    historial.append({"role": "assistant", "content": respuesta_1})
    
    # PASO 2: Presentar un problema en esa industria
    print("\n" + "-" * 80)
    print("[PASO 2] Pidiendo al LLM que presente un problema en esa industria...\n")
    prompt_2 = """Basándote en el área de negocio que mencionaste, describe un problema 
específico y desafiante que enfrenta esa industria actualmente. El problema debe ser 
algo que pueda beneficiarse de una solución de IA con Agentic. Sé específico y detallado."""
    
    respuesta_2 = llamar_llm(prompt_2, historial)
    print(f"Respuesta: {respuesta_2}")
    
    # Agregar al historial
    historial.append({"role": "user", "content": prompt_2})
    historial.append({"role": "assistant", "content": respuesta_2})
    
    # PASO 3: Proponer la solución de IA con Agentic
    print("\n" + "-" * 80)
    print("[PASO 3] Pidiendo al LLM que proponga una solución de IA con Agentic...\n")
    prompt_3 = """Ahora propón una solución detallada de IA con Agentic para resolver 
el problema que describiste. Explica:
1. Cómo funcionaría el sistema agéntico
2. Qué agentes específicos se necesitarían
3. Cómo estos agentes trabajarían de forma autónoma
4. Qué beneficios concretos traería esta solución"""
    
    respuesta_3 = llamar_llm(prompt_3, historial)
    print(f"Respuesta: {respuesta_3}")
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DEL EJERCICIO COMPLETADO")
    print("=" * 80)
    print(f"\n✓ Área de negocio identificada")
    print(f"✓ Problema específico descrito")
    print(f"✓ Solución de IA con Agentic propuesta")
    print("\nEjercicio completado exitosamente!")

if __name__ == "__main__":
    main()