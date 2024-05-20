import math
import numpy as np

def area(rlen, width = 0):
    if width == 0:
        return math.pi * rlen * rlen
    else:
        return rlen * width
    
def tempconv(temp, flag):
    if flag == "C":
        return (temp - 32) * 5/9
    elif flag == "F":
        return (temp * 9/5) + 32

print("Abdullah Chouhan: Assignment 2\n\n\n")
while (True):
    task = int(input("Enter corresponding number for task between 1 to 10, any other to exit\n"))
    if task == 1:
        light = input("Enter \"red\", \"yellow\" or \"green\": ")
        print("The light says: ", end = "")
        if light == "red":
            print("Stop")
        elif light == "yellow":
            print("Caution")
        elif light == "green":
            print("Go")
        else:
            print("Invalid input. Please enter \"red\", \"yellow\" or \"green\"")
    elif task == 2:
        try:
            a = int(input("Enter a number to check if odd or even: "))
            print("The number is odd") if a % 2 != 0 else print("The number is even")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    elif task == 3:
        try:
            total = 0
            while (True):
                i = int(input("Enter any number to add to sum, 0 to exit: "))
                if i == 0:
                    break
                else:
                    total += i
            print(f"The sum is {total}")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    elif task == 4:
        print("Outputting first 10 natural even numbers...")
        for i in range(2, 21, 2):
            print(i)
    elif task == 5:
        try:
            r = float(input("Enter radius: "))
            print(f"The area is {area(r)}")
            l, w = map(int, input("Enter length and width, separated by space: ").split())
            print(f"The area is {area(l, w)}")
        except ValueError:
            print("Invalid input. Please enter an integer(s).")
    elif task == 6:
        try:
            t = int(input("Enter temperature: "))
            while (True):
                f = input("Enter \"C\" for Celsius or \"F\" for Fahrenheit to convert temperature into: ")
                if f == "C" or f == "F":
                    break
                else:
                    print("Invalid input. Please enter \"C\" or \"F\".")
            print(f"The temperature in {f} is {tempconv(t, f)}")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    elif task == 7:
        try:
            list1 = [int(num) for num in input("Enter numbers separated by space: ").split()]
            maxnum, minnum = -math.inf, math.inf
            for i in list1:
                if i > maxnum:
                    maxnum = i
                if i < minnum:
                    minnum = i
            print(f"The maximum number is {maxnum}\nThe minimum number is {minnum}")
        except ValueError:
            print("Invalid input. Please enter numbers.")
    elif task == 8:
        list1 = ["albatross", "cricket", "butterfly", "dragonfly", "flyingfish"]
        print("Initial list: ", list1)
        list1.append("goose")
        print("List after appending 'goose': ", list1)
        list1.insert(3, "hummingbird")
        print("List after inserting 'hummingbird' at index 3: ", list1)
        list1.remove("cricket")
        print("List after removing 'cricket': ", list1)
        list1.sort()
        print("List after sorting: ", list1)
    elif task == 9:
        arr = np.arange(1, 11)
        print(f"Initial array: {arr}\nShape of the array: {arr.shape}\nData type of the array: {arr.dtype}\nMean of the array: {arr.mean()}")
        arr = np.append(arr, 11)
        print(f"Array after adding 11: {arr}")
        arr = np.delete(arr, 0)
        print(f"Array after removing the first element: {arr}")
    elif task == 10:
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([4, 5, 6])
        print(f"Initial arrays of compatible dimensions: {arr1} and {arr2}\nAddition: {np.add(arr1, arr2)}\nSubtraction: {np.subtract(arr1, arr2)}\nMultiplication: {np.multiply(arr1, arr2)}\nDot product: {np.dot(arr1, arr2)}\nMatrix multiplication: {np.matmul(arr1, arr2)}")
    else:
        print("Exiting...")
        break
    print("\n")