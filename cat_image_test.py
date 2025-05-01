import json
import urllib.parse
import urllib.request
import webbrowser

# URL base de The Cat API y clave de API
API_URL = "https://api.thecatapi.com/v1/images/search"
API_KEY = "live_HX2npF4yOZ0p0smEfsW3INtqQGdzBF1882OZP7bNbu0jnDqKEAyXCQVE6s9SwzyC"

def fetch_cat_images(params):
    # Codificar parámetros en la URL
    query_string = urllib.parse.urlencode(params)
    full_url = f"{API_URL}?{query_string}"

    # Preparar la solicitud con la clave de API en los encabezados
    req = urllib.request.Request(full_url)
    req.add_header("x-api-key", API_KEY)

    try:
        # Realizar la solicitud y analizar el JSON
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())

        if not data:
            print("No se encontraron imágenes con estos filtros.")
        else:
            print(f"\nAbriendo {len(data)} imagen(es) de gato...")
            for item in data:
                image_url = item.get("url")
                if image_url:
                    print("URL de la imagen:", image_url)
                    webbrowser.open(image_url)
    except Exception as e:
        print("Error al obtener imagen(es) de gato:", e)

def basic_filters():
    # Filtros básicos (cuántas, raza, categoría)
    limit = input("¿Cuántas imágenes quieres? (1–100): ").strip()
    breed_ids = input("Ingresa ID(s) de raza, separadas por comas (o deja en blanco): ").strip()
    category_ids = input("Ingresa ID(s) de categoría, separadas por comas (o deja en blanco): ").strip()

    params = {
        "limit": limit or "1",  # Valor predeterminado: 1 imagen si no se ingresa nada
    }

    # Agregar filtros de raza y categoría si se proporcionan
    if breed_ids:
        params["breed_ids"] = breed_ids
    if category_ids:
        params["category_ids"] = category_ids

    fetch_cat_images(params)

def advanced_filters():
    # Filtros avanzados (todas las opciones disponibles)
    limit = input("¿Cuántas imágenes quieres? (1–100): ").strip()
    page = input("¿Qué página de imágenes quieres? (0-n): ").strip()
    order = input("Orden (ASC/DESC/RAND): ").strip().upper()
    has_breeds = input("¿Mostrar solo imágenes con información de raza? (1 para Sí, 0 para No): ").strip()
    breed_ids = input("Ingresa ID(s) de raza, separadas por comas (o deja en blanco): ").strip()
    category_ids = input("Ingresa ID(s) de categoría, separadas por comas (o deja en blanco): ").strip()
    sub_id = input("Ingresa sub_id si quieres filtrar por sub_id (o deja en blanco): ").strip()

    # Establecer valores predeterminados si no se ingresan datos
    params = {
        "limit": limit or "1",  # Valor predeterminado: 1 imagen
        "page": page or "0",    # Página predeterminada: 0
        "order": order or "RAND", # Orden predeterminado: aleatorio
        "has_breeds": has_breeds or "0",  # Mostrar imágenes sin información de raza por defecto
    }

    # Agregar filtros si se proporcionan
    if breed_ids:
        params["breed_ids"] = breed_ids
    if category_ids:
        params["category_ids"] = category_ids
    if sub_id:
        params["sub_id"] = sub_id

    fetch_cat_images(params)

# Menú principal
print("Selecciona opción de filtro:")
print("1. Filtros básicos (Cuántas, Raza, Categoría)")
print("2. Filtros avanzados (Todas las opciones disponibles)")

choice = input("Ingresa 1 o 2: ").strip()

if choice == "1":
    basic_filters()
elif choice == "2":
    advanced_filters()
else:
    print("¡Opción inválida! Por favor selecciona 1 o 2.")
