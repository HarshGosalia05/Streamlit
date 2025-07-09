# Name = input("Enter Your Name : ")
# Age = int(input("Enter Your Age : "))
# City = input("Enter Your City : ")
# Area = input("Enter Your Area : ")

data = []
BHK = ["1BHK","2BHK","3BHK"]
cal_enrgy =0
print("1. Flat")
print("2. Tenament ( House )")
s1 = int(input("Enter Number : ")) 

if s1 == 1 :
    bhk = int(input("1BHK,2BHK,3BHK"))
    if bhk == 1 :
        cal_enrgy += 2*0.4 + 2*0.8
        
    elif bhk == 2 :
        cal_enrgy += 2 * .4 + 2 * .8

    elif bhk == 3 :
        cal_enrgy += 2 * .4 + 2 * .8


ac = input("You Have a Ac? Yes or No\n").lower()
if ac == "yes":
    cal_enrgy+=3

fridge = input("You Have a Fridge? Yes or No\n").lower()
if fridge == "yes":
    cal_enrgy+=3

wm = input("You Have a Washing Machine? Yes or No\n").lower()
if wm == "yes":
    cal_enrgy+=3

print("Total Energy : ",cal_enrgy)


        

# name - input
# age
# city
# area

# flat/house(Tenament)

# 1 2 3 Bhk

# 1bhk -> (2 light ) * 0.8kw ,2 * 0.8kg fan
#                 0.8 + 1.6 
#                 =   2.6

# 2BHK -> 3 light + 3 fan =?
# 3BHK -> 3 light + 3 fan =?

# Do you have

# Ac + 3
# Fridge +4
# wm + 2
