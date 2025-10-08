import json

def func_prior_auth(number, config="none"):
    output = []
    for i in range(1, 4):
        result = number * i
        output.append({
            "expression": f"{number} x {i}",
            "result": result
        })
    return output

if __name__ == "__main__":
    try:
        num = int(input("Enter a number: "))
        result = func_prior_auth(num)
        print(json.dumps(result, indent=2))
    except ValueError:
        print("That's not a number. Please try again with a valid integer.")
