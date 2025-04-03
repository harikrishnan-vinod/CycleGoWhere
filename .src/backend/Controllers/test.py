import requests
import json

# Define Overpass API Query
query = """
[out:json];
area["name"="Singapore"]->.searchArea;
(
  node["shop"="bicycle"](area.searchArea);
  way["shop"="bicycle"](area.searchArea);
  relation["shop"="bicycle"](area.searchArea);
);
out center;
"""

# Send request to Overpass API
url = "https://overpass-api.de/api/interpreter"
response = requests.get(url, params={"data": query})
data = response.json()

# Extract relevant information
bicycle_shops = []
for element in data["elements"]:
    shop_info = {
        "id": element["id"],
        "lat": element.get("lat", element["center"]["lat"] if "center" in element else None),
        "lon": element.get("lon", element["center"]["lon"] if "center" in element else None),
        "name": element["tags"].get("name", "Unknown Bicycle Shop"),
        "address": element["tags"].get("addr:street", "Unknown Street"),
        "postcode": element["tags"].get("addr:postcode", "Unknown Postcode"),
    }
    bicycle_shops.append(shop_info)

# Print results
for shop in bicycle_shops:
    print(f"{shop['name']} - {shop['address']} ({shop['lat']}, {shop['lon']}) - {shop['postcode']}")
