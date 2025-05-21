# multiplication_table.py

def testing_function_1(number, config="none"):
    output = []
    for i in range(1, 11):
        result = number * i  # Proper math, not string multiplication
        output.append(f"{number} x {i} = {result}")
    return "\n".join(output)

if __name__ == "__main__":
    try:
        num = int(input("Enter a number: "))
        result = testing_function_1(num)
        print(result)
    except ValueError:
        print("That's not a number. Please try again with a valid integer.")