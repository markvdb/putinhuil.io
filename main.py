from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from math import atan2, cos, pi, sin, sqrt
from typing import Optional
import sqlite3

description = """
![putinhuil.io](https://i.imgur.com/XDQ7DiQ.png)
When I take a European flight, how many euros end up in the pockets of Putin and his cronies? Putinhuil.io tries to answer that question for you.

## Calculation basis
- geo distance. Basic math really.
- [average jet fuel consumption per passenger km](https://en.wikipedia.org/wiki/Fuel_economy_in_aircraft)
- [Amsterdam-Rotterdam-Antwerp petrochemical refinery margins on URALS](https://www.spglobal.com/commodityinsights/en/market-insights/latest-news/oil/040422-refinery-margin-tracker-russian-crude-cargoes-taper-off-as-margins-rise)
- [IATA platts fuel monitor](https://www.iata.org/en/publications/economics/fuel-monitor/)
- [EU Russian oil market share](https://ec.europa.eu/eurostat/cache/infographs/energy/bloc-2c.html)

Note that a number of factors are in flux and/or shady. On one side, we have reports of [falling Russian oil consumption in Europe](https://www.spglobal.com/commodityinsights/en/market-insights/latest-news/oil/040422-crude-oil-prices-jump-amid-expectations-of-more-russian-sanctions). On the other, we have companies like Shell playing the ["Latvian blend"](https://www.washingtonpost.com/business/energy/the-backdoor-that-keeps-russian-oil-flowing-into-europe/2022/04/08/efecb7ce-b701-11ec-8358-20aa16355fb4_story.html) trick. That's why for now, we think it best to stick with the historical Russian oil market share.

## Curious about the name?

"Putin" is obvious. "Huile" is French for oil. ".io" because all cool kids do that. Honestly, I swear.

I know nothing about Slavic languages, especially not about any [rude words](https://en.wikipedia.org/wiki/Putin_khuylo!) Neither does my partner who thanks to previous visit by Russian armies to her country 1940-1941 and 1944-1994 speaks Russian fluently as her fourth language. блять!
"""


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

def moneytorussia(iata1, iata2, iata3 = None, iata4 = None, iata5 = None, passengers=1, returntrip=True):
	iata1 = iata1.upper()
	iata2 = iata2.upper()
	if passengers is None: passengers = 1

	paxkm = distance(get_airport_coordinates(iata1,iata2))
	if iata3 is not None:
		iata3 = iata3.upper()
		paxkm += distance(get_airport_coordinates(iata2,iata3))
		if iata4 is not None:
			iata4 = iata4.upper()
			paxkm += distance(get_airport_coordinates(iata3,iata4))
			if iata5 is not None:
				iata5 = iata5.upper()
				paxkm += distance(get_airport_coordinates(iata4,iata5))
	if passengers > 1: paxkm *= passengers
	if returntrip: paxkm *= 2
	return(round(paxkm * flight_length_compensation_factor * fuel_consumption_per_paxkm * (jet_fuel_price - ara_refining_margin) * russian_oil_market_share, 2))


app = FastAPI(
	title = "Putinhuil.io",
	description = description,
	version = "0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/flight/")
async def flight(
		iata1 : str = Query(
			...,
			title = "departure airport 3 letter IATA code",
			description = "Please use the 3 letter IATA code.",
			min_length = 3,
			max_length = 3),
		iata2 : str = Query(
			...,
			title = "first stop airport 3 letter IATA code",
			description = "For a direct flight, this is your destination airport.",
			min_length = 3,
			max_length = 3),
		iata3 : Optional[str] = Query(
			None,
			title = "second stop airport 3 letter IATA code",
			min_length = 3,
			max_length = 3),
		iata4 : Optional[str] = Query(
			None,
			title = "third stop airport 3 letter IATA code",
			min_length = 3,
			max_length = 3),
		iata5 : Optional[str] = Query(
			None,
			title = "fourth stop airport 3 letter IATA code",
			min_length = 3,
			max_length = 3),
		pax : int = Query(
			None,
			title = "number of passengers"),
		ret : bool = True
	):
	m = moneytorussia(iata1, iata2, iata3, iata4, iata5, pax, ret)
	return {"message": str(m)}
