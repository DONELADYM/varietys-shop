import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    info = cargar_info_negocio()
    return {
        "horario": info.get("negocio", {}).get("horario", "Lunes a Domingo 7am-10pm"),
        "esta_abierto": True,
    }


def obtener_catalogo() -> list:
    info = cargar_info_negocio()
    return info.get("productos", [])


def buscar_producto(consulta: str) -> list:
    productos = obtener_catalogo()
    consulta_lower = consulta.lower()
    return [
        p for p in productos
        if consulta_lower in p.get("nombre", "").lower()
        or consulta_lower in p.get("notas", "").lower()
    ]


def calcular_envio(total: float) -> str:
    if total >= 50:
        return "¡Envío GRATIS! Tu pedido supera los $50."
    return f"El envío tiene un costo adicional. Agrega más productos para llegar a $50 y obtener envío gratis."


def buscar_en_knowledge(consulta: str) -> str:
    resultados = []
    knowledge_dir = "knowledge"
    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."
    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue
    if resultados:
        return "\n---\n".join(resultados)
    return "No encontré información específica sobre eso en mis archivos."
