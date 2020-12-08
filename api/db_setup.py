import requests


BASE = "http://127.0.0.1:5000/"


response = requests.put(BASE + "user/0",{
	"last_name" : "Brault",
	"first_name" : "Henri",
	"date_of_birth" : "15/04/1999"})
print(response.json())



response = requests.put(BASE + "user/1",{
	"last_name" : "Liotard",
	"first_name" : "Loreena",
	"date_of_birth" : "22/02/1999"})
print(response.json())

input("Users all set, press any key")
#----------------------------------------------------------------------------
response = requests.put(BASE + "user/0/0",{
	"name" : "coloc de charme",
	"location" : "Caen",
	"description" : "colocation pour 3 personnes",
	"house_type" : 1
	})
print(response.json())

response = requests.put(BASE + "user/0/2",{
	"name" : "maison familiale",
	"location" : "Magne",
	"description" : "grande maison",
	"house_type" : 0
	})
print(response.json())


response = requests.put(BASE + "user/1/1",{
	"name" : "petit appartement",
	"location" : "Caen",
	"description" : "9m2",
	"house_type" : 1
	})
print(response.json())


input("Houses all set, press any key")
#----------------------------------------------------------------------------

response = requests.put(BASE + "user/1/1/0",{
	"name" : "salon",
	"surface_area" : 9
	})
print(response.json())

response = requests.put(BASE + "user/0/0/1",{
	"name" : "entrée",
	"surface_area" : 14
	})
print(response.json())

response = requests.put(BASE + "user/0/0/2",{
	"name" : "chambre",
	"surface_area" : 8
})
print(response.json())



input("Rooms all set, press any key")