# multiplication_table.py

def print_multiplication_table(number):
    for i in range(1, 11):
        print(f"{number} x {i} = {number * i}")

if __name__ == "__main__":
    try:
        num = int(input("Enter a number: "))
        print_multiplication_table(num)
    except ValueError:
        print("That's not a number. Try again with a valid integer.")