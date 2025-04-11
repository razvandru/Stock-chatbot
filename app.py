from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Object to store the tree structure for exchange options
stockTree = {
    "LSE": {
        "name": "London Stock Exchange",
        "stocks": {
            "CRDA": ("CRODA INTERNATIONAL PLC", 4807.00),
            "GSK": ("GSK PLC", 1574.80),
            "ANTO": ("ANTOFAGASTA PLC", 1746.00),
            "FLTR": ("FLUTTER ENTERTAINMENT PLC", 16340.00),
            "BDEV": ("BARRATT DEVELOPMENTS PLC", 542.60)
        }
    },
    "NYSE": {
        "name": "New York Stock Exchange",
        "stocks": {
            "AHT": ("Ashford Hospitality Trust", 1.72),
            "KUKE": ("Kuke Music Holding Ltd", 1.20),
            "ASH": ("Ashland Inc.", 93.42),
            "NMR": ("Nomura Holdings Inc.", 5.84),
            "LC": ("LendingClub Corp", 9.71)
        }
    },
    "NASDAQ": {
        "name": "Nasdaq",
        "stocks": {
            "AMD": ("Advanced Micro Devices, Inc.", 164.21),
            "TSLA": ("Tesla, Inc.", 190.35),
            "SOFI": ("SoFi Technologies, Inc.", 8.24),
            "PARA": ("Paramount Global", 14.92),
            "GOOGL": ("Alphabet Inc.", 141.91)
        }
    }
}

# POST call from frontend
@app.route('/trade', methods=['POST'])

# Parse user input for current selection and decide what to send to frontend
def parse_current_Selection():
    print(request)
    userInput = request.get_json()
    if not userInput:
        return jsonify({"error": "Invalid JSON"}), 400 # if data is not received, return error
    currentStep = userInput.get('step')
    currentSelection = userInput.get('selection')

    if currentStep == "start": # current step is at the beginning
        return jsonify({
            "message": "Please select a Stock Exchange:",
            "options": [{"label": value["name"], "value": index} for index, value in stockTree.items()], # return first stock options
            "next_step": "exchange"
        })

    elif currentStep == "exchange": # current step is at the first level in the stock tree
        exchangeOptions = stockTree.get(currentSelection)
        if not exchangeOptions:
            return jsonify({"message": "Invalid exchange."}) # if user input is not received, return error
        return jsonify({
            "message": f"Please select a stock:",
            "options": [{"label": name, "value": stockOptions} for stockOptions, (name, _) in exchangeOptions["stocks"].items()], # return second stock options
            "next_step": "stock",
            "context": currentSelection
        })

    elif currentStep == "stock": # current step is at the second level in the stock tree
        exchangeCode = userInput.get("context")
        exchange = stockTree.get(exchangeCode)
        if not exchange:
            return jsonify({"message": "Invalid exchange context."}) # if user input is not received, return error
        stock = exchange["stocks"].get(currentSelection)
        if not stock:
            return jsonify({"message": "Invalid stock selection."}) # if user input is not received, return error
        name, price = stock
        return jsonify({
            "message": f"Stock Price of {name} is {price}", # return selected stock price
            "options": [
                {"label": "Main menu", "value": "main"},
                {"label": "Go Back", "value": "back"}
            ],
            "next_step": "main_menu",
            "context": exchangeCode
        })

    elif currentStep == "main_menu":
        if currentSelection == "main":
            return jsonify({
                "message": "Please select a Stock Exchange:",
                "options": [{"label": value["name"], "value": index} for index, value in stockTree.items()],
                # return first stock options
                "next_step": "exchange"
            })
        elif currentSelection == "back":
            return previous_step(userInput.get("context")) # return to the previous step
        else:
            return jsonify({"message": "Unknown navigation command."}) # if user input is not received, return error

    else:
        return jsonify({"message": "Unknown step."}) # default error in case of invalid step

# Parse user input and display options for previous step
def previous_step(exchangeCode):
    exchange = stockTree.get(exchangeCode)
    if not exchange:
        return jsonify({"message": "Invalid exchange."})
    return jsonify({
        "message": f"Please select a stock from {exchange['name']}:",
        "options": [{"label": name, "value": code} for code, (name, _) in exchange["stocks"].items()],
        "next_step": "stock",
        "context": exchangeCode
    })

# Main method with default path
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()