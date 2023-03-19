from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Create a geolocator object
geolocator = Nominatim(user_agent='myapplication')

# Get the user input address
address = input('Enter an address: ')

try:
    # Use the geolocator to get the latitude and longitude
    location = geolocator.geocode(address, exactly_one=False)

    # Check if the location was found
    if location is not None:
        # Print a list of possible locations
        print('Found', len(location), 'possible locations:')
        for i, loc in enumerate(location):
            print(f"{i+1}. {loc.address}")
        
        # Ask the user to choose a location
        index = int(input('Enter the index of the location you want: ')) - 1
        selected_location = location[index]
        
        # Get the latitude and longitude of the selected location
        latitude, longitude = selected_location.latitude, selected_location.longitude
        print('Latitude:', latitude)
        print('Longitude:', longitude)
    else:
        print('Location not found')
except (GeocoderTimedOut, GeocoderUnavailable) as e:
    print('Error: Unable to connect to the geolocation service. Please check your internet connection and try again.')
