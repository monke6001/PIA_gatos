import json
import os
from collections import Counter

def load_json_data(filename):
    """Carga y valida los datos desde un archivo JSON."""
    if not os.path.exists(filename):
        print(f"❌ El archivo {filename} no existe.")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Archivo '{filename}' cargado con éxito. Total registros: {len(data)}")
        return data
    except json.JSONDecodeError:
        print("❌ Error al decodificar el archivo JSON.")
        return []

def show_full_data(data):
    """Muestra todos los datos disponibles por cada gato."""
    if not data:
        print("⚠️ No hay datos para mostrar.")
        return

    print("\n📋 Mostrando todos los gatos disponibles:\n")
    for idx, cat in enumerate(data, start=1):
        print(f"Gato #{idx}")
        print(f"• URL         : {cat.get('url', 'N/A')}")
        print(f"• Raza        : {cat.get('breed', 'N/A')}")
        print(f"• Origen      : {cat.get('origin', 'N/A')}")
        print(f"• Temperamento: {cat.get('temperament', 'N/A')}")
        print("-" * 50)

def show_summary(data):
    """Resumen por raza y origen."""
    breeds = [item["breed"] for item in data]
    origins = [item["origin"] for item in data]

    print("\n📊 Razas más comunes:")
    for breed, count in Counter(breeds).most_common():
        print(f"• {breed}: {count}")

    print("\n🌍 Orígenes más comunes:")
    for origin, count in Counter(origins).most_common():
        print(f"• {origin}: {count}")

def filter_by_origin(data, origin_name):
    """Filtra y muestra los gatos de un origen específico con todos sus datos."""
    filtered = [item for item in data if item["origin"].lower() == origin_name.lower()]
    if not filtered:
        print(f"⚠️ No se encontraron gatos del origen '{origin_name}'.")
    else:
        print(f"\n🐾 Gatos del origen '{origin_name}':")
        for idx, cat in enumerate(filtered, start=1):
            print(f"\nGato #{idx}")
            print(f"• URL         : {cat['url']}")
            print(f"• Raza        : {cat['breed']}")
            print(f"• Origen      : {cat['origin']}")
            print(f"• Temperamento: {cat['temperament']}")
            print("-" * 50)

if __name__ == "__main__":
    print("📂 Analizador de Datos de Gatos (desde JSON)")
    data = load_json_data("cat_data_clean.json")

    if data:
        show_full_data(data)
        show_summary(data)

        origin_input = input("\n🔍 Filtrar por país de origen (opcional): ").strip()
        if origin_input:
            filter_by_origin(data, origin_input)
