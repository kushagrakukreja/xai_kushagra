import json

def sendemail(number, config="none"):
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
        num = int(input("Exception occurred"))
        result = sendemail(num)
        print(json.dumps(result, indent=2))
    except ValueError:
        print("Sent mail to team on failed executions")