l = ["Morning","Afternoon","Evening","Night"]
day_choice = []
for i in range(len(l)):
    print(f"{i+1}. You Are in {l[i]} Mood")
    
no = int(input("Enter the Number : "))


if no == 1 :
    print(f"Now, You Are in {l[no]} Mood")
    choice = ["Tea","Coffie","Milk"]
    print(choice)
    no1 = int(input("Enter the Number : "))

    if no1 == 1 :
        # print("1. Simple Tea")
        # print("2. Suger Free Tea")
        # print("3. Lemon Tea")
        # print("4. Ice Tea")
        tea = input("Please enter your chai option \n 1) Ginger chai ,\n  2)suger free chai  , \n 3)fudina chai ,\n 4) iced tea ")

        # no2 = int(input("Enter the Number : "))
        day_choice.append(l[i] + tea)



    elif no1 == 2:
        print("1. Simple Coffie")
        print("2. Black(Dark) Coffie")
        print("3. Capicino Coffie")
        print("4. Palang Tod Coffie")
        no1 = int(input("Enter the Number : "))

    elif no1 == 3 :
        print("1. Turmeric Milk")
        print("2. Gulab MilkShek")
        print("3. Mango MilkShek")
        print("4. ")
    



elif no == 2 :
    print(f"Now, You Are in {l[no]} Mood")
    print("1. Tea")    
    print("2. Coffie")
    print("3. Milk")


elif no == 3 :
    print(f"Now, You Are in {l[no]} Mood")
    print("1. Tea")    
    print("2. Coffie")
    print("3. Milk")


elif no == 4 :
    print(f"Now, You Are in {l[no]} Mood")
    print("1. Tea")    
    print("2. Coffie")
    print("3. Milk")


    
print(choice)