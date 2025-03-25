import requests
from flask import jsonify

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



