class Filters:
    def __init__(self, water_coolers=False, bike_repair=False, bike_park=False):
        self.water_coolers = water_coolers
        self.bike_repair = bike_repair
        self.bike_park = bike_park
    
    def to_dict(self):
        return {
            "water_coolers": self.water_coolers,
            "bike_repair": self.bike_repair,
            "bike_park": self.bike_park
        }
    
    @staticmethod
    def from_dict(data):
        return Filters(
            water_coolers=data.get("water_coolers", False),
            bike_repair=data.get("bike_repair", False),
            bike_park=data.get("bike_park", False)
        )