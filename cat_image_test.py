import json
import urllib.parse
import urllib.request
import webbrowser

# The Cat API base URL and API key
API_URL = "https://api.thecatapi.com/v1/images/search"
API_KEY = "live_HX2npF4yOZ0p0smEfsW3INtqQGdzBF1882OZP7bNbu0jnDqKEAyXCQVE6s9SwzyC"

def fetch_cat_images(params):
    # Encode parameters into the URL
    query_string = urllib.parse.urlencode(params)
    full_url = f"{API_URL}?{query_string}"

    # Prepare the request with API key in headers
    req = urllib.request.Request(full_url)
    req.add_header("x-api-key", API_KEY)

    try:
        # Perform the request and parse JSON
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())

        if not data:
            print("No images found with these filters.")
        else:
            print(f"\nOpening {len(data)} cat image(s)...")
            for item in data:
                image_url = item.get("url")
                if image_url:
                    print("Image URL:", image_url)
                    webbrowser.open(image_url)
    except Exception as e:
        print("Error fetching cat image(s):", e)

def basic_filters():
    # Basic filters (how many, breed, category)
    limit = input("How many images do you want? (1–100): ").strip()
    breed_ids = input("Enter breed ID(s), comma-separated (or leave blank): ").strip()
    category_ids = input("Enter category ID(s), comma-separated (or leave blank): ").strip()

    params = {
        "limit": limit or "1",  # Default to 1 image if no input
    }

    # Add breed and category filters if provided
    if breed_ids:
        params["breed_ids"] = breed_ids
    if category_ids:
        params["category_ids"] = category_ids

    fetch_cat_images(params)

def advanced_filters():
    # Advanced filters (all available options)
    limit = input("How many images do you want? (1–100): ").strip()
    page = input("Which page of images do you want? (0-n): ").strip()
    order = input("Order (ASC/DESC/RAND): ").strip().upper()
    has_breeds = input("Only show images with breed info? (1 for Yes, 0 for No): ").strip()
    breed_ids = input("Enter breed ID(s), comma-separated (or leave blank): ").strip()
    category_ids = input("Enter category ID(s), comma-separated (or leave blank): ").strip()
    sub_id = input("Enter sub_id if you want to filter by sub_id (or leave blank): ").strip()

    # Set defaults if empty inputs
    params = {
        "limit": limit or "1",  # Default to 1 image if no input
        "page": page or "0",    # Default to page 0
        "order": order or "RAND", # Default to random order
        "has_breeds": has_breeds or "0",  # Default to showing images without breed info
    }

    # Add filters if provided
    if breed_ids:
        params["breed_ids"] = breed_ids
    if category_ids:
        params["category_ids"] = category_ids
    if sub_id:
        params["sub_id"] = sub_id

    fetch_cat_images(params)

# Main menu
print("Select filter option:")
print("1. Basic Filters (How many, Breed, Category)")
print("2. Advanced Filters (All available options)")

choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    basic_filters()
elif choice == "2":
    advanced_filters()
else:
    print("Invalid choice! Please select 1 or 2.")
