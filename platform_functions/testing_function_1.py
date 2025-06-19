import json

def testing_function_1(number, config="none"):
    output = []
    for i in range(1, 11):
        result = number * i
        output.append({
            "expression": f"{number} x {i}",
            "result": result
        })
    return output

if __name__ == "__main__":
    try:
        num = int(input("Enter 
        result = testing_function_1(num)
        print(json.dumps(result, indent=2))
    except ValueError:
        print("That's not a number. Please try again ssswith a valid integergggs")