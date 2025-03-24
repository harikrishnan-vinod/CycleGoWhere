class Location:
    def __init__(self, name=None, latitude=0, longitude=0, address=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
    
    def to_dict(self):
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address
        }
    
    @staticmethod
    def from_dict(data):
        return Location(
            name=data.get("name"),
            latitude=data.get("latitude", 0),
            longitude=data.get("longitude", 0),
            address=data.get("address")
        )