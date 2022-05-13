#! /bin/bash

echo "airport,iata"> iata_mappings.dat
cut -d, -f1,4 custom_major_airports_wanted_fields.dat >> iata_mappings.dat
csvjson iata_mappings.dat | sed -e 's/\"airport\"/airport/g' -e 's/\"iata\"/iata/g' > iata_mappings.jsobject
