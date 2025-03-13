import time
import geocoder
import requests


apiKey = ''

print("""
                        xxxxxx             
            xxxxxxxxxxx xxx     xxxx         
            x          xx          xxxxxx    
    xxxxxxxx                       xx  xxx  
    xx                                    xx 
    xx        ┌─────────────────────┐      xx 
    x         │  AirQualityChecker  │      xx 
    xx        └─────────────────────┘        x
    xxx                                     x
      xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \n""")

#print("Enter the coordinates you want to check: \n")

def coordinates():
    """Gets user coordinates based on their choice."""

    while True:
        choice = input("Enter coordinates [1] or Use my location [2]: ")
        if choice == "1":
            try:
                latitude = float(input("Enter latitude: "))
                longitude = float(input("Enter longitude: "))
                print(f"You are checking air quality for the coordinates: {latitude}, {longitude}")
                return latitude, longitude
            except ValueError:
                print("Invalid input. Please enter numeric values for latitude and longitude.")
        elif choice == "2":
            try:
                latitude, longitude = location()
                return latitude, longitude
            except Exception as e:
                print(f"Error getting location: {e}")
                print("Please enter coordinates manually.")
        else:
            print("Invalid choice. Please enter 1 or 2.")


def location():

    #Getting user location based on IP address
    l = geocoder.ip("me")

    global latitide
    global longitude
    latitude = l.lat
    longitude = l.lng
    print(f"You are checking air quality for the coordinates: {latitude}, {longitude}")

    return latitude, longitude


def AirQuality(lat, long):

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={apiKey}"

    #Get response from server
    response = requests.get(url)
    # print(response.url)

    if response.status_code == 200:
        time.sleep(1)

        data = response.json()['list'][0]
        # print(response.url)
        # print(data)

        # Storing API response values in variables
        carbon_monoxide = data['components']['co']
        nitrogen_monoxide = data['components']['no']
        nitrogen_dioxide = data['components']['no2']
        ozone = data['components']['o3']
        sulphur = data['components']['so2']
        ammonia = data['components']['nh3']
        pm25 = data['components']['pm2_5']
        pm10 = data['components']['pm10']
        
        #    print(data)
    else:
        print(f"API is not responding: {response.status_code}")
    
    def categorize(value, thresholds, catgories):
        for i in range(len(thresholds)):
            if value <= thresholds[i]:
                return categories[i]
        return categories[-1]

    def ugm3_to_ppm(ugm3, molecular_weight):
        mgm3 = ugm3 / 1000
        ppm = (24.45 * mgm3) / molecular_weight
        return ppm

    # Carbon Monoxide in ppm calculation
    co_ppm = round(ugm3_to_ppm(carbon_monoxide, 28.01), 2)

    # Ranking basically
    categories = ["Good", "Moderate", "Could be Unhealthy", "Unhealthy", "Very Unhealthy", "Hazardous"]

    # Thresholds for each pollutant based on AQI categories I got from diffrerent sources
    pollutant_thresholds = {
    "carbon_monoxide": [50, 100, 150, 200, 300],
    "nitrogen_monoxide": [40, 80, 180, 280, 565],
    "nitrogen_dioxide": [40, 80, 180, 280, 565],
    "ozone": [50, 100, 168, 208, 748],
    "sulphur": [40, 80, 380, 800, 1600],
    "ammonia": [200, 400, 800, 1200, 1800],
    "pm25": [12, 35.4, 55.4, 150.4, 250.4],
    "pm10": [54, 154, 254, 354, 424],
    }

    # Printing results
    print(f"Carbon Monoxide: {co_ppm} ppm [{categorize(co_ppm, pollutant_thresholds['carbon_monoxide'], categories)}]")
    print(f"Nitrogen Monoxide: {nitrogen_monoxide} µg/m³ [{categorize(nitrogen_monoxide, pollutant_thresholds['nitrogen_monoxide'], categories)}]")
    print(f"Nitrogen Dioxide: {nitrogen_dioxide} µg/m³ [{categorize(nitrogen_dioxide, pollutant_thresholds['nitrogen_dioxide'], categories)}]")
    print(f"Ozone: {ozone} µg/m³ [{categorize(ozone, pollutant_thresholds['ozone'], categories)}]")
    print(f"Sulphur: {sulphur} µg/m³ [{categorize(sulphur, pollutant_thresholds['sulphur'], categories)}]")
    print(f"Ammonia: {ammonia} µg/m³ [{categorize(ammonia, pollutant_thresholds['ammonia'], categories)}]")
    print(f"PM2.5: {pm25} µg/m³ [{categorize(pm25, pollutant_thresholds['pm25'], categories)}]")
    print(f"PM10: {pm10} µg/m³ [{categorize(pm10, pollutant_thresholds['pm10'], categories)}]")

    return 

latitude, longitude = coordinates()

AirQuality(lat=latitude, long=longitude)


