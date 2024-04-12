import json
import math
import requests


def get_location_with_tiles(keyword, zoom):
    base_url = "https://geoapi.heartrails.com/api/json?method=suggest&keyword="
    response = requests.get(f"{base_url}{keyword}&matching=like")
    data = response.json()
    if "location" in data["response"]:
        locations = data["response"]["location"]
        for location in locations:
            lat = float(location["y"])
            lon = float(location["x"])
            x_tile, y_tile = lat_lon_to_tile_coords(lat, lon, zoom)
            location["tile"] = {}
            location["tile"]["x"] = x_tile
            location["tile"]["y"] = y_tile
            location["tile"]["z"] = zoom
        return locations
    else:
        return "No locations found"


def lat_lon_to_tile_coords(latitude, longitude, zoom):
    lat_rad = math.radians(latitude)
    x_pixel = (longitude + 180) / 360 * (2**zoom) * 256
    x_tile = int(x_pixel // 256)
    y_pixel = (
        (1 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)
        / 2
        * (2**zoom)
        * 256
    )
    y_tile = int(y_pixel // 256)
    return x_tile, y_tile


def run(keyword, zoom):
    results = {}
    locations_with_tiles = get_location_with_tiles(keyword, zoom)
    results["locations"] = locations_with_tiles
    return json.dumps(results, ensure_ascii=False)


if __name__ == "__main__":
    print(run("品川区", zoom=13))
