from flask import Flask, render_template, request, jsonify
import requests
import polyline

app = Flask(__name__)

# Replace these with your actual API keys
GOOGLE_API_KEY = "AIzaSyCXOPeQJ_nH8RK8UiXHxXGjXlrVcTZLZ4o"
WEATHER_API_KEY = "4fd9d6c533bd8c49390df3cf96288689"



def get_location(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"
    response = requests.get(url).json()
    if response['status'] == 'OK':
        loc = response['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    return None, None


def get_temperature(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}"
    response = requests.get(url).json()
    if "main" in response:
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return temp, desc
    return None, None


def get_nearest_hospitals(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&type=hospital&key={GOOGLE_API_KEY}"
    response = requests.get(url).json()
    hospitals = []
    for place in response.get("results", [])[:5]:
        name = place["name"]
        dest_lat = place["geometry"]["location"]["lat"]
        dest_lon = place["geometry"]["location"]["lng"]

        dist_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={lat},{lon}&destination={dest_lat},{dest_lon}&departure_time=now&traffic_model=best_guess&key={GOOGLE_API_KEY}"
        dist_response = requests.get(dist_url).json()
        if dist_response.get("routes"):
            leg = dist_response["routes"][0]["legs"][0]
            distance = leg["distance"]["text"]
            duration = leg["duration_in_traffic"]["text"]
            hospitals.append({
                "name": name,
                "lat": dest_lat,
                "lon": dest_lon,
                "distance": distance,
                "duration": duration
            })
    return hospitals


def get_route_and_heatmap(start_lat, start_lon, dest_lat, dest_lon):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_lat},{start_lon}&destination={dest_lat},{dest_lon}&departure_time=now&traffic_model=best_guess&key={GOOGLE_API_KEY}"
    response = requests.get(url).json()
    if not response.get("routes"):
        return None
    polyline_points = polyline.decode(response["routes"][0]["overview_polyline"]["points"])
    heatmap = [pt for i, pt in enumerate(polyline_points) if i % 5 == 0]
    return {
        "route": polyline_points,
        "heatmap": heatmap
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.get_json()
    address = data.get("location")
    lat, lon = get_location(address)
    if lat is None:
        return jsonify({"error": "Invalid location"})

    temp, desc = get_temperature(lat, lon)
    hospitals = get_nearest_hospitals(lat, lon)
    if not hospitals:
        return jsonify({"error": "No hospitals found nearby"})

    return jsonify({
        "lat": lat,
        "lon": lon,
        "temperature": temp,
        "description": desc,
        "hospitals": hospitals
    })


@app.route("/get_route", methods=["POST"])
def get_route():
    data = request.get_json()
    start_lat, start_lon = data["start"]
    dest_lat, dest_lon = data["dest"]
    route = get_route_and_heatmap(start_lat, start_lon, dest_lat, dest_lon)
    if not route:
        return jsonify({"error": "No route found"})
    return jsonify(route)


@app.route("/live_eta", methods=["POST"])
def live_eta():
    data = request.get_json()
    user_lat, user_lon = data["start"]
    hospital_lat, hospital_lon = data["hospital"]

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={user_lat},{user_lon}&destination={hospital_lat},{hospital_lon}&departure_time=now&traffic_model=best_guess&key={GOOGLE_API_KEY}"
    response = requests.get(url).json()
    if not response.get("routes"):
        return jsonify({"error": "No route found"})

    leg = response["routes"][0]["legs"][0]
    eta = leg["duration_in_traffic"]["text"]
    distance = leg["distance"]["text"]
    traffic_level = get_traffic_level(leg["duration_in_traffic"]["value"], leg["duration"]["value"])

    return jsonify({"eta": eta, "distance": distance, "traffic_level": traffic_level})


def get_traffic_level(current_duration, normal_duration):
    ratio = current_duration / normal_duration
    if ratio > 1.5:
        return "red"
    elif ratio > 1.2:
        return "yellow"
    else:
        return "green"


if __name__ == "__main__":
    app.run(debug=True)
