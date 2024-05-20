import math
print("Abdullah Chouhan: Assignment 1\n\n\n")
while (True):
    task = int(input("Enter corresponding number for task between 1 to 5, any other to exit\n"))
    if task == 1:
        try:
            a, b = map(int, input("Enter two numbers, separated by space: ").split())
            print(f"The product is{a*b}")
        except ValueError:
            print("Invalid input. Please enter two integers.")
    elif task == 2:
        try:
            a, b = map(int, input("Enter two numbers, separated by space: ").split())
            print(f"The sum is {a + b}\nThe difference is {a - b}\nThe product is {a * b}\nThe quotient is {a / b}")
        except ValueError:
            print("Invalid input. Please enter two integers.")
        except ZeroDivisionError:
            print("Cannot divide by zero.")
    elif task == 3:
        try:
            r = int(input("Enter radius: "))
            print(f"The circumference is {2 * math.pi * r}\nThe area is {math.pi * r * r}")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    elif task == 4:
        try:
            a = int(input("Enter a number to check if positive and vice-versa: "))
            if a > 0:
                print("The number is positive")
            elif a == 0:
                print("The number is zero") 
            else:
                print("The number is negative")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    elif task == 5:
        try:
            year = int(input("Enter a year: "))
            print(f"{year} is a leap year") if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else print(f"{year} is not a leap year")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    else:
        print("Exiting...")
        break
    print("\n\n\n")