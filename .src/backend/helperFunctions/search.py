import requests
from flask import jsonify
from math import radians, sin, cos, sqrt, atan2
import csv

#general purpose searchQuery
def searchRequest(searchVal,token):
    try:
        url = "https://www.onemap.gov.sg/api/common/elastic/search?"
        params = {
            "searchVal": f"{searchVal}",
            "returnGeom": "Y",
            "getAddrDetails": "Y",
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
        url,
        params=params,
        headers=headers
        )
        data = response.json()
        data["results"] = data.get("results", [])[:5]
        print(data)
        return jsonify(data)
        
    except Exception as e:
        return jsonify({'error':'internal server error'})
    

#function to find and return name,latitude and longitude from giving searchVal        
def searchAndReturnLL(searchVal,token):
    try:
        url = "https://www.onemap.gov.sg/api/common/elastic/search?"
        params = {
            "searchVal": f"{searchVal}",
            "returnGeom": "Y",
            "getAddrDetails": "Y",
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
        url,
        params=params,
        headers=headers
        )
        data = response.json()
        data["results"] = data.get("results", [])[:1]
        if data.get("results"):
            first = data["results"][0]
            extracted = {
            "address": first.get("ADDRESS"),
            "latitude": first.get("LATITUDE"),
            "longitude": first.get("LONGITUDE")
        }
        else:
            print("No results found.")    
        
        return jsonify(extracted)
        
    except Exception as e:
        return jsonify({'error':'internal server error'})
    

#function to query OneMap API for routing information using the combined_address
def getRouting(combined_address,token):

    fromAddress = combined_address["from"]
    destAddress = combined_address["destination"]
    start_coords = f"{fromAddress['latitude']},{fromAddress['longitude']}"
    end_coords = f"{destAddress['latitude']},{destAddress['longitude']}"

    url="https://www.onemap.gov.sg/api/public/routingsvc/route"
    params={
        "start": f"{start_coords}",
        "end": f"{end_coords}",
        "routeType":"cycle"
    }
    headers ={
        "Authorization": f"{token}"
    }

    response = requests.get(url,params=params,headers=headers)
    data = response.json()
    return data

def haversine(lat1, lon1, lat2, lon2):
    """Calculate Haversine distance between two lat/lng points in kilometers."""
    R = 6371  # Earth radius in km
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def findWaterPoints(route_points, csv_path='waterpoints.csv', radius_km=0.5):
    """
    Load waterpoints from a CSV and return those within radius_km of any route point.

    Args:
        route_points: List of (lat, lng) tuples.
        csv_path: Path to the waterpoints CSV file.
        radius_km: Proximity threshold in kilometers.

    Returns:
        List of waterpoint dicts within range.
    """
    nearby = []
    seen = set()

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                wp_name = row["Name"]
                wp_lat = float(row["Latitude"])
                wp_lng = float(row["Longitude"])
                #wp_description = row.get("Description", "")
                #wp_type = row.get("Type", "")

                for lat, lng in route_points:
                    distance = haversine(lat, lng, wp_lat, wp_lng)
                    if distance <= radius_km:
                        key = (wp_name, wp_lat, wp_lng)
                        if key not in seen:
                            seen.add(key)
                            nearby.append({
                                "name": wp_name,
                                "lat": wp_lat,
                                "lng": wp_lng,
                                #"description": wp_description,
                                #"type": wp_type,
                                "distance_km": round(distance, 3),
                            })
                        break  # No need to check more route points for this wp
            except (ValueError, KeyError):
                continue  # Skip invalid rows

    return nearby
    