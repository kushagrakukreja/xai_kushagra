# multiplication_table.py

def testing_function_1(number,config="none"):
    for i in range(1, 11):
        print(f"{number} x {i} = {number * i}")

if __name__ == "__main__":
    try:
        num = int(input("Enter a number: "))
        testing_function_1(num)
    except ValueError:
        print("That's not a number. Please try again with a valid integer.")