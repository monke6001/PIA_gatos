import json
import urllib.parse
import urllib.request
import webbrowser
import os  # Importar el módulo os para abrir archivos con las aplicaciones predeterminadas

# URL base de The Cat API y clave de API
API_URL = "https://api.thecatapi.com/v1/images/search"
API_KEY = "live_HX2npF4yOZ0p0smEfsW3INtqQGdzBF1882OZP7bNbu0jnDqKEAyXCQVE6s9SwzyC"

def clean_cat_data(item):
    """Toma un objeto JSON de The Cat API y retorna un diccionario con campos relevantes limpios."""
    cleaned = {}
    url = item.get("url", "").strip()
    if not url.startswith("http"):
        return None  # descartar entradas con URL inválida
    cleaned["url"] = url

    breeds = item.get("breeds", [])
    if breeds:
        breed = breeds[0]
        cleaned["breed_name"]  = breed.get("name", "Desconocida").strip().title()
        cleaned["origin"]      = breed.get("origin", "Desconocido").strip().title()
        cleaned["temperament"] = breed.get("temperament", "N/A").strip().capitalize()
    else:
        cleaned["breed_name"]  = "Desconocida"
        cleaned["origin"]      = "Desconocido"
        cleaned["temperament"] = "N/A"

    return cleaned

def fetch_cat_images(params):
    query_string = urllib.parse.urlencode(params)
    full_url = f"{API_URL}?{query_string}"

    req = urllib.request.Request(full_url)
    req.add_header("x-api-key", API_KEY)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())

        if not data:
            print("No se encontraron imágenes con estos filtros.")
            return

        # Nueva estructura de datos para análisis
        cat_data_analysis = []

        for item in data:
            cleaned = clean_cat_data(item)
            if cleaned:
                cat_data_analysis.append({
                    "url": cleaned["url"],
                    "breed": cleaned["breed_name"],
                    "origin": cleaned["origin"],
                    "temperament": cleaned["temperament"]
                })

        if not cat_data_analysis:
            print("No hay datos válidos después de la limpieza.")
            return

        # Mostrar resultados y abrir en navegador
        print(f"\nAbriendo {len(cat_data_analysis)} imagen(es) de gato limpias:")
        for info in cat_data_analysis:
            print(f"- URL: {info['url']}")
            print(f"  • Raza: {info['breed']}")
            print(f"  • Origen: {info['origin']}")
            print(f"  • Temperamento: {info['temperament']}\n")
            webbrowser.open(info["url"])

        # Guardar en archivo JSON
        with open("cat_data_clean.json", "w", encoding="utf-8") as f_json:
            json.dump(cat_data_analysis, f_json, ensure_ascii=False, indent=4)

        # Guardar en archivo TXT
        with open("cat_data_clean.txt", "w", encoding="utf-8") as f_txt:
            for cat in cat_data_analysis:
                f_txt.write(f"URL: {cat['url']}\n")
                f_txt.write(f"Raza: {cat['breed']}\n")
                f_txt.write(f"Origen: {cat['origin']}\n")
                f_txt.write(f"Temperamento: {cat['temperament']}\n")
                f_txt.write("-" * 40 + "\n")

        print("✅ Datos guardados en 'cat_data_clean.json' y 'cat_data_clean.txt'.")

    except Exception as e:
        print("Error al obtener o procesar datos de gato:", e)

def basic_filters():
    limit = input("¿Cuántas imágenes quieres? (1–100): ").strip() or "1"
    breed_ids = input("ID(s) de raza, separadas por comas (o deja en blanco): ").strip()
    category_ids = input("ID(s) de categoría, separadas por comas (o deja en blanco): ").strip()

    params = {"limit": limit}
    if breed_ids:
        params["breed_ids"] = breed_ids
    if category_ids:
        params["category_ids"] = category_ids

    fetch_cat_images(params)

def advanced_filters():
    limit       = input("¿Cuántas imágenes quieres? (1–100): ").strip() or "1"
    page        = input("¿Qué página? (0-n): ").strip() or "0"
    order       = input("Orden (ASC/DESC/RAND): ").strip().upper() or "RAND"
    has_breeds  = input("¿Solo con raza? (1 Sí, 0 No): ").strip() or "0"
    breed_ids   = input("ID(s) de raza, separadas por comas: ").strip()
    category_ids= input("ID(s) de categoría, separadas por comas: ").strip()
    sub_id      = input("sub_id (o deja en blanco): ").strip()

    params = {
        "limit": limit,
        "page": page,
        "order": order,
        "has_breeds": has_breeds,
    }
    if breed_ids:
        params["breed_ids"] = breed_ids
    if category_ids:
        params["category_ids"] = category_ids
    if sub_id:
        params["sub_id"] = sub_id

    fetch_cat_images(params)

def view_saved_data():
    """Permite al usuario abrir los archivos JSON y TXT con las aplicaciones predeterminadas."""
    print("\n1. Abrir datos en formato JSON")
    print("2. Abrir datos en formato TXT")
    choice = input("Selecciona el formato a abrir (1 o 2): ").strip()

    if choice == "1":
        try:
            # Abre el archivo JSON con la aplicación predeterminada del sistema
            os.system("start cat_data_clean.json")
        except FileNotFoundError:
            print("El archivo JSON no se encuentra. Asegúrate de haber guardado datos previamente.")
    elif choice == "2":
        try:
            # Abre el archivo TXT con la aplicación predeterminada del sistema
            os.system("start cat_data_clean.txt")
        except FileNotFoundError:
            print("El archivo TXT no se encuentra. Asegúrate de haber guardado datos previamente.")
    else:
        print("Opción inválida.")

if __name__ == "__main__":
    print("Selecciona opción de filtro:")
    print("1. Filtros básicos (Cuántas, Raza, Categoría)")
    print("2. Filtros avanzados (Todas las opciones)")
    print("3. Ver datos guardados")
    choice = input("Ingresa 1, 2 o 3: ").strip()

    if choice == "1":
        basic_filters()
    elif choice == "2":
        advanced_filters()
    elif choice == "3":
        view_saved_data()
    else:
        print("¡Opción inválida! Selecciona 1, 2 o 3.")
