name = input("Enter Your Name : ")
# City = input("Enter Your City : ")

# d = { "Name" : name, "Age : " : Age,"City" : City}
# print(d)

while 1 :
    print("IF YOU ENTER 0 THEN EXIT.")
    Age = int(input("Enter Your Age : "))

    if Age == 0 :
        break 
    elif Age >= 18 :
        print("1. You Drink ice Tea")
        print("2. You Drink Ginger Tea")
        print("3. You Drink Fudina Tea")
        print("4. You Drink Suger Free Tea")
        no = int(input("Enter Number For Order Tea : "))      
        if no == 1 :
            print("1. You Ordered ice Tea")
        elif no == 2:
            print("2. You Ordered Ginger Tea")
        elif no == 3:
            print("3. You Ordered Fudina Tea")
        elif no == 4:
            print("4. You Ordered Suger Free Tea")
        else :
            print("You Order Normal suger Tea")
        print()


    elif Age <18 :
        print("You Drink Coffie")
        print("1. You Drink Capicino")
        print("2. You Drink Black coffie")
        print("3. You Drink Americano Coffie")
        no = int(input("Enter Number For Order Tea : "))      
        if no == 1 :
            print("1. You Ordered Capicino")
        elif no == 2:
            print("2. You Ordered Black coffie")
        elif no == 3:
            print("3. You Ordered Americano Coffie")
        else :
            print("You Order Normal suger Tea")
    
    else :
        print("You Drink Tea")