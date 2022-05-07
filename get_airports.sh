#! /bin/bash

# Clean up upstream and temp files
rm -rf airports.sqlite countries.dat custom_airports.dat custom_major_airports.dat custom_country_names.dat custom_major_airports.dat

# Download most recent list
# wget https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat
# wget https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat

# Manually clean up superfluous commas from airport names

# cp countries.dat custom_countries.dat
# Manually clean up custom_countries.dat to keep only the countries we want

# Keep only the names of the countries
cut -d, -f1 custom_countries.dat > custom_country_names.dat

# Keep only the airports from our custom countries list
while read line; do
    grep "$line" airports.dat >> custom_airports.dat
done<custom_country_names.dat

# Keep only the airports with a IATA code
while read line; do
	field=$(echo $line | cut -d, -f5 -)
	if [ $field != 'N' ]; then
		echo $line >> custom_major_airports.dat
	fi
done < custom_airports.dat 

# Remove unwanted fields
cut -d, -f2-5,7,8 custom_major_airports.dat > custom_major_airports_wanted_fields.dat

# Remove upstream and temp files
rm -rf countries.dat custom_airports.dat custom_major_airports.dat custom_country_names.dat custom_major_airports.dat

# Create sqlite db
sqlite3 airports.sqlite "CREATE TABLE airport ( name varchar(100), city varchar(100), country varchar(50), iata varchar(3), lat real, lon real);"
(echo .separator ,; echo .import custom_major_airports_wanted_fields.dat airport) | sqlite3 airports.sqlite
