import os
import csv
import requests

csv_filename = "bicycle_parking.csv"
if not os.path.isfile(csv_filename):
    # Create the file if it doesn't exist
    print("Creating CSV file...")
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # writer.writerow(["Name", "Latitude", "Longitude", "Description", "Type"])

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