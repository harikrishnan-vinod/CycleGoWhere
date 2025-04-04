from flask import Blueprint, request, jsonify
import requests
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
    print("Finding bicycle park points")
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
    print("Finding bicycle points")
    result = MainPageController.findBikeShops(points)
    return result 