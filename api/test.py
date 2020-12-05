import requests

BASE = "http://127.0.0.1:5000/"


response = requests.put(BASE + "user/0",{
	"last_name" : "Brault",
	"first_name" : "Henri",
	"date_of_birth" : "15/04/1999"})
print(response.json())

response = requests.put(BASE + "user/1",{
	"last_name" : "Zidane",
	"first_name" : "Zinédine",
	"date_of_birth" : "23/06/1972"})
print(response.json())

response = requests.put(BASE + "user/2",{
	"last_name" : "Liotard",
	"first_name" : "Loreena",
	"date_of_birth" : "22/02/1999"})
print(response.json())

input("Users all set, press any key")
#----------------------------------------------------------------------------
response = requests.put(BASE + "user/0/0",{
	"name" : "coloc de charme",
	"location" : "Caen"
	})
print(response.json())

response = requests.put(BASE + "user/2/2",{
	"name" : "petit appartement nul",
	"location" : "Caen"
	})
print(response.json())

response = requests.put(BASE + "user/1/1",{
	"name" : "Villa tres chere",
	"location" : "Madrid"
	})
print(response.json())

input("Houses all set, press any key")
#----------------------------------------------------------------------------

response = requests.get(BASE + "browse/Caen")
print(response.json())