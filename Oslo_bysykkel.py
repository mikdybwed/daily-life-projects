#imports
import pandas as pd
import json
import urllib.request, urllib.response
from urllib.error import HTTPError, URLError


#funksjon for ekstrahering av data ifra json
def get_json(url):
  try:
    with urllib.request.urlopen(url) as response:
      return json.load(response)
  
  #basic feilhåndtering
  except HTTPError as e:
    print("error code: ", e.code)
  except URLError as e:
    print("reason: ", e.reason)


#henter filene som innholder henholdsvis navn og tilgjengelighet på sykkelstasjonene
station_information = get_json("https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json")
station_status = get_json("https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json")


#konverterer sykkelstasjondataen i filene til pandas dataframes
status = pd.DataFrame(station_status["data"]["stations"])
information = pd.DataFrame(station_information["data"]["stations"])


#merger til en dataframe med all informasjon
availability = pd.merge(status, information, on="station_id")


#ekstraherer kun de ønskede variablene navn, tlgjengelige sykler og tilgjengelige låser
availability = availability.filter(["name","num_bikes_available", "num_docks_available"])


#putter for ordens skyld stasjonsnavn som index
availability.set_index("name", inplace=True)
del availability.index.name


#Lager den endelige oversikten
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(availability)