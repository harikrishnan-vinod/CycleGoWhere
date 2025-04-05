from flask import jsonify
import requests
from math import radians, sin, cos, sqrt, atan2
import csv
from Entities.DatabaseController import DatabaseController
from Entities.Activity import Activity
from Entities.Route import Route
from routes.services import db, firestore_module as firestore
import os
import datetime
import polyline

def haversine(lat1, lon1, lat2, lon2):
    """Calculate Haversine distance between two lat/lng points in kilometers."""
    R = 6371  # Earth radius in km
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

class MainPageController:
    def __init__(self):
        self.db_controller = DatabaseController()
    
    @staticmethod
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
    @staticmethod      
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
    @staticmethod
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

    @staticmethod
    def findWaterPoints(route_points,radius_km=0.5):
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

        with open("./Controllers/ParkData/verified_points.csv", newline='', encoding='utf-8') as csvfile:
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
    
    @staticmethod
    def findBikeParking(route_points,radius_km=0.5):
        nearby = []
        seen = set()
        # Define CSV file name
        csv_filename = "./Controllers/ParkData/bicycle_parking.csv"
        if not os.path.isfile(csv_filename):
            # Create the file if it doesn't exist
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

        with open(csv_filename, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader, None)  # Skip header row
            if headers is None:
                # Only fetch from API if "Bicycle Parking" is NOT in CSV
                
                print("Fetching bicycle parking data from API...")

                # Define Overpass API Query for Bicycle Parking
                query = """
                [out:json];
                area["name"="Singapore"]->.searchArea;
                (
                node["amenity"="bicycle_parking"](area.searchArea);
                way["amenity"="bicycle_parking"](area.searchArea);
                relation["amenity"="bicycle_parking"](area.searchArea);
                );
                out center;
                """

                # Send request to Overpass API
                url = "https://overpass-api.de/api/interpreter"
                response = requests.get(url, params={"data": query})
                data = response.json()

                # Extract relevant information
                bicycle_parking_spots = []
                for element in data["elements"]:
                    name = element["tags"].get("name", "Unnamed Bicycle Parking")
                    lat = element.get("lat", element["center"]["lat"] if "center" in element else None)
                    lon = element.get("lon", element["center"]["lon"] if "center" in element else None)
                    capacity = element["tags"].get("capacity", "Unknown Capacity")
                    covered = element["tags"].get("covered", "Unknown")

                    # Create description field
                    description = f"Capacity: {capacity}, Covered: {covered}"

                    # Append to list
                    bicycle_parking_spots.append([name, lat, lon, description, "Bicycle Parking"])

                # Append data to CSV
                with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
                    print("Writing rows...")
                    writer = csv.writer(file)

                    # Write headers only if file does not exist
                    if not os.path.isfile(csv_filename) or os.stat(csv_filename).st_size == 0:
                        writer.writerow(["Name", "Latitude", "Longitude", "Description", "Type"])

                    writer.writerows(bicycle_parking_spots)

                # print(f"Successfully appended {len(bicycle_parking_spots)} bicycle parking locations to {csv_filename}")

            else:
                print("Bicycle Parking data already exists in the CSV. Skipping API request.")

        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    bp_name = row["Name"]
                    bp_lat = float(row["Latitude"])
                    bp_lng = float(row["Longitude"])
                    #wp_description = row.get("Description", "")
                    #wp_type = row.get("Type", "")

                    for lat, lng in route_points:
                        distance = haversine(lat, lng, bp_lat, bp_lng)
                        if distance <= radius_km:
                            key = (bp_name, bp_lat, bp_lng)
                            if key not in seen:
                                seen.add(key)
                                nearby.append({
                                    "name": bp_name,
                                    "lat": bp_lat,
                                    "lng": bp_lng,
                                    #"description": wp_description,
                                    #"type": wp_type,
                                    "distance_km": round(distance, 3),
                                })
                            break  # No need to check more route points for this wp
                except (ValueError, KeyError):
                    continue  # Skip invalid rows

        return nearby
    
    @staticmethod
    def findBikeShops(route_points, radius_km=0.5):
        """
        Load bike shop data from a CSV and return shops near the route.

        Args:
            route_points (list): List of (lat, lon) tuples representing the route.
            radius_km (float): Radius to consider a shop as "nearby".

        Returns:
            List of nearby bike shops.
        """
        nearby = []
        seen = set()
        csv_filename = "./Controllers/ParkData/bicycle_shops.csv"
        
        if not os.path.isfile(csv_filename):
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Latitude", "Longitude", "Description", "Type"])
        
        # Check if bicycle shop data already exists in CSV
        with open(csv_filename, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            if headers and any(row[4] == "Bicycle Shop" for row in reader):
                print("Bicycle Shop data already exists in the CSV. Skipping API request.")
            else:
                print("Fetching bicycle shop data from API...")
                
                # Overpass API query for bicycle shops
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
                
                url = "https://overpass-api.de/api/interpreter"
                response = requests.get(url, params={"data": query})
                data = response.json()
                
                bicycle_shops = []
                for element in data["elements"]:
                    name = element["tags"].get("name", "Unnamed Bicycle Shop")
                    lat = element.get("lat", element["center"]["lat"] if "center" in element else None)
                    lon = element.get("lon", element["center"]["lon"] if "center" in element else None)
                    street = element["tags"].get("addr:street", "Unknown Street")
                    housenumber = element["tags"].get("addr:housenumber", "Unknown Number")
                    
                    description = f"Address: {housenumber} {street}"
                    bicycle_shops.append([name, lat, lon, description, "Bicycle Shop"])
                
                # Append data to CSV
                with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(bicycle_shops)
                
                # print(f"Successfully appended {len(bicycle_shops)} bicycle shop locations to {csv_filename}")
        
        # Load bicycle shop data and find nearby shops
        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    shop_name = row["Name"]
                    shop_lat = float(row["Latitude"])
                    shop_lng = float(row["Longitude"])
                    
                    for lat, lng in route_points:
                        distance = haversine(lat, lng, shop_lat, shop_lng)
                        if distance <= radius_km:
                            key = (shop_name, shop_lat, shop_lng)
                            if key not in seen:
                                seen.add(key)
                                nearby.append({
                                    "name": shop_name,
                                    "lat": shop_lat,
                                    "lng": shop_lng,
                                    "distance_km": round(distance, 3),
                                })
                            break  # No need to check more route points for this shop
                except (ValueError, KeyError):
                    continue  # Skip invalid rows
        
        return nearby
    
    def saveActivity(self, user_uid, activity_data):
        decoded_points = polyline.decode(activity_data["route_geometry"], 5)
        geo_points = [firestore.GeoPoint(lat, lng) for lat, lng in decoded_points]

        start_time_str = activity_data.get("startTime")
        start_time = None

        if start_time_str:
            try:
                # Try full ISO 8601 with microseconds
                start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                try:
                    # Fallback without microseconds
                    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
                except Exception as e:
                    print("Invalid startTime format fallback:", e)
        
        instructions_converted = []
        for row in activity_data["route_instructions"]:
            if isinstance(row, dict):
                instructions_converted.append({
                    "direction": row.get("direction"),
                    "road": row.get("road"),
                    "distance": row.get("distance"),
                    "latLng": row.get("latLng")
                })
            elif isinstance(row, list):
                instructions_converted.append({
                    "direction": row[0],
                    "road": row[1],
                    "distance": row[2],
                    "latLng": row[3]
                })

        route = Route(
            start_location=firestore.GeoPoint(*decoded_points[0]),
            end_location=firestore.GeoPoint(*decoded_points[-1]),
            distance=activity_data["distance"],
            route_path=geo_points,
            instructions=instructions_converted,
            start_postal=activity_data["startPostal"],
            end_postal=activity_data["endPostal"]
        )
        activity = Activity(user_uid=user_uid,
                            activity_name=activity_data["activityName"],
                            notes=activity_data["notes"],
                            duration=activity_data["timeTaken"],
                            start_time=start_time,
                            route=route,
                            created_at=firestore.SERVER_TIMESTAMP)

        self.db_controller.save_activity(activity)
        return jsonify({"message": "Activity saved"}), 200