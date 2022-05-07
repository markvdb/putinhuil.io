from math import atan2, cos, pi, sin, sqrt
import sqlite3

# Global constants. Dirty, but it works
earth_radius = 6371
flight_length_compensation_factor = 1.08
fuel_consumption_per_paxkm = 0.035
radials_per_degree = pi / 180
russian_oil_market_share = .27
jet_fuel_price = 0.85
ara_refining_margin = 0.3039

def distance(coordinates):
	delta_lat_radials = (coordinates["lat0"] - coordinates["lat1"]) * radials_per_degree
	delta_lon_radials = (coordinates["lon0"] - coordinates["lon1"]) * radials_per_degree

	lat0_radials = coordinates["lat0"] * radials_per_degree
	lat1_radials = coordinates["lat1"] * radials_per_degree

	sin_delta_lat = sin(delta_lat_radials/2) 
	sin_delta_lon = sin(delta_lon_radials/2)

	a = sin_delta_lat * sin_delta_lat + cos(lat0_radials) * cos(lat1_radials) * sin_delta_lon * sin_delta_lon
	c = 2 * atan2(sqrt(a), sqrt(1-a));

	return(earth_radius * c)

def get_airport_coordinates(iata1, iata2):
	query= "SELECT lat, lon FROM airport WHERE iata IN('" + iata1 + "','" + iata2 +"')"
	connection = sqlite3.connect('airports.sqlite')
	cursor = connection.cursor()
	cursor.execute(query)
	c = cursor.fetchall()
	coordinates = {
		"lat0": c[0][0],
		"lon0": c[0][1],
		"lat1": c[1][0],
		"lon1": c[1][1]
	}
	return(coordinates)

def moneytorussia(iata1, iata2, passengers=1, returntrip=True):
	paxkm = distance(get_airport_coordinates(iata1,iata2))
	if passengers > 1: paxkm *= passengers
	if returntrip: paxkm *= 2
	return(round(paxkm * flight_length_compensation_factor * fuel_consumption_per_paxkm * (jet_fuel_price - ara_refining_margin) * russian_oil_market_share),2)
