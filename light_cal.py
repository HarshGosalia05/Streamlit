import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Workshop"]
collection = db["profile"]



Name = input("Enter Your Name : ")
Age = int(input("Enter Your Age : "))
City = input("Enter Your City : ")
Area = input("Enter Your Area : ")

data = {
    "name": Name,
    "age": Age,
    "city": City,
    "area": Area,
}

collection.insert_one(data)

cal_energy=0
light=TV=Fans=Ac=Fridge=Wm=0

light = int(input("How many lights : "))
Fans = int(input("How many Fans : "))
TV = int(input("How many T.V. : "))

que = input("You have an Air Conditioner? Yes or No : ").lower()
if que == "yes":
    Ac = int(input("How many Air Conditioner : "))

que = input("You have an Refrigerator? Yes or No : ").lower()
if que == "yes":
    Fridge = int(input("How many Fridge : "))


que = input("You have an Washing Machine? Yes or No : ").lower()
if que == "yes":
    Wm = int(input("How many Washing Machine : "))





if light>=0 :
    cal_energy += light * 0.2
if Fans>=0 :
    cal_energy += Fans * 0.2
if TV>=0 :
    cal_energy += TV * 0.3
if Ac>=0 :
    cal_energy += Ac * 3.00
if Fridge>=0 :
    cal_energy += Fridge * 3.1
if Wm>=0 :
    cal_energy += Wm * 2.8

print("Total Energy : ",cal_energy)
rate_per_unit = 8  # ₹ per kWh
totalvalue = round(cal_energy * rate_per_unit, 2)



print("\n------------------------------------------")
print("Energy Consumption Details : ")
print("------------------------------------------")
print(f"Name     : {Name}")
print(f"City     : {City}")
print(f"Area     : {Area}")
print(f"Age      : {Age}\n")
print("Appliances Used:")
print(f"Light            : {light}")
print(f"Fans             : {Fans}")
print(f"TV               : {TV}")
print(f"Air Conditioner  : {Ac}")
print(f"Refrigerator     : {Fridge}")
print(f"Washing Machine  : {Wm}")
print("------------------------------------------")
print(f"🔋 Total Energy Consumption  : {cal_energy:.2f} kWh")
print(f"💰 Estimated Daily Cost      : ₹{totalvalue}")
print("------------------------------------------\n")

data = {
    "name": Name,
    "age": Age,
    "city": City,
    "area": Area,
}

collection.insert_one(data)

# Fetch and print all documents
for doc in collection.find():
    print(doc)