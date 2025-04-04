from flask import Blueprint, request, jsonify
import requests
import polyline
import traceback
import time
import os
from Controllers.MainPageController import MainPageController

search_bp = Blueprint("search",__name__)

auth_token = {
    "token": None,
    "expires_at": 0
}

def get_onemap_token():
    current_time = time.time()
    if auth_token["token"] and current_time < auth_token["expires_at"]:
        return auth_token["token"]

    url = "https://www.onemap.gov.sg/api/auth/post/getToken"
    payload = {
        "email": os.environ["ONEMAP_EMAIL"],
        "password": os.environ["ONEMAP_EMAIL_PASSWORD"]
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    token = response.json()["access_token"]
    auth_token["token"] = token
    auth_token["expires_at"] = current_time + 86400
    return token


@search_bp.route('/search')
def searchaddressUpdateList():
    fromAddress = request.args.get("fromAddress")
    destAddress = request.args.get("destAddress")
    token = get_onemap_token()

    
    if fromAddress:
        try:
            data = MainPageController.searchRequest(fromAddress,token)
            return data

        except Exception as e:
            return jsonify({'error':'internal server error'}) 

        
    if destAddress:
        try:
            data = MainPageController.searchRequest(destAddress,token)
            return data

        except Exception as e:
            return jsonify({'error':'internal server error'}) 
        
@search_bp.route('/route')
def handlerouting():

    fromAddress = request.args.get("fromAddress")
    destAddress = request.args.get("destAddress")
    token = get_onemap_token()
    #get latitude and longitude from onemap api
    
    try:
        data_fromAddress = MainPageController.searchAndReturnLL(fromAddress,token).get_json()
        data_destAddress = MainPageController.searchAndReturnLL(destAddress,token).get_json()
        
        combined_address = {
            "from": data_fromAddress,
            "destination": data_destAddress
        }
        
        return MainPageController.getRouting(combined_address,token)

    
    except Exception as e:
        return jsonify({'error':'internal server error'})
    

@search_bp.route('/fetchWaterPoint', methods=["POST"])
def getWaterPoint():
    data = request.json
    instructions = data.get("routeInstructions", [])

    points = []
    for step in instructions:
        latlng_str = step[3]
        if latlng_str:
            try:
                lat_str, lng_str = latlng_str.split(",")
                lat, lng = float(lat_str), float(lng_str)
                points.append((lat, lng))  # ✅ now a list of (lat, lng) tuples
            except ValueError:
                continue 
    print("Finding Water points")
    result = MainPageController.findWaterPoints(points)
    return result

@search_bp.route('/fetchBicyclePark', methods=["POST"])
def getBicyclePark():
    data = request.json
    instructions = data.get("routeInstructions", [])

    points = []
    for step in instructions:
        latlng_str = step[3]
        if latlng_str:
            try:
                lat_str, lng_str = latlng_str.split(",")
                lat, lng = float(lat_str), float(lng_str)
                points.append((lat, lng))  # ✅ now a list of (lat, lng) tuples
            except ValueError:
                continue 
    print("Finding Bicycle parkings")
    result = MainPageController.findBikeParking(points)
    return result

@search_bp.route('/fetchBicycleShop', methods=["POST"])
def getBicycleShop():
    data = request.json
    instructions = data.get("routeInstructions", [])

    points = []
    for step in instructions:
        latlng_str = step[3]
        if latlng_str:
            try:
                lat_str, lng_str = latlng_str.split(",")
                lat, lng = float(lat_str), float(lng_str)
                points.append((lat, lng))  # ✅ now a list of (lat, lng) tuples
            except ValueError:
                continue 
    print("Finding Bicycle Shops")
    result = MainPageController.findBikeShops(points)
    return result

@search_bp.route("/save-activity", methods=["POST"])
def save_activity():
    data = request.get_json()
    user_uid = data.get("userUID")
    activity_data = data.get("activityData")
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

    try:
        decoded_points = polyline.decode(activity_data["route_geometry"], 5)
        geo_points = [firestore.GeoPoint(lat, lng) for lat, lng in decoded_points]

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
                    "distance": row[5],
                    "latLng": row[3]
                })

        doc_data = {
            "activityName": activity_data["activityName"],
            "notes": activity_data["notes"],
            "distance": activity_data["distance"],
            "startPostal": activity_data["startPostal"],
            "endPostal": activity_data["endPostal"],
            "duration": activity_data["timeTaken"],
            "routePath": geo_points,
            "startTime": start_time,
            "instructions": instructions_converted,
            "startLocation": firestore.GeoPoint(*decoded_points[0]),
            "endLocation": firestore.GeoPoint(*decoded_points[-1]),
            "createdAt": firestore.SERVER_TIMESTAMP
        }

        db.collection("users").document(user_uid).collection("activities").add(doc_data)
        return jsonify({"message": "Activity saved"}), 200
    
    except Exception as e:
        print("Error saving activity:", e)
        traceback.print_exc()
        return jsonify({"message": "Failed to save activity"}), 500