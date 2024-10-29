from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize a dictionary to store counts for various items
counts = {"bottle": 0, "utensil": 0}

@app.route('/update_counter', methods=['POST'])
def update_counter():
    """
    Update the counts of items based on the incoming form data.
    """
    # Loop through incoming data and update counts
    for item, value in request.form.items():
        try:
            value = int(value)  # Convert value to integer
            if item in counts:
                counts[item] += value  # Increment existing item count
            else:
                counts[item] = value  # Initialize new item type if not in dictionary
            print(f"Updated {item} count: {counts[item]}")  # Log the updated count
        except ValueError:
            return jsonify({"success": False, "error": f"Invalid value for {item}. Must be an integer."}), 400

    return jsonify({"success": True, "counts": counts})

@app.route('/get_count', methods=['GET'])
def get_count():
    """
    Retrieve the current counts of items.
    """
    return jsonify(counts)

@app.route('/reset_counter', methods=['POST'])
def reset_counter():
    """
    Reset counts for a specific item or all items if no specific item is provided.
    """
    item = request.form.get("item")  # Get the item to reset from the request
    if item:
        if item in counts:
            counts[item] = 0  # Reset specified item count to 0
            return jsonify({"success": True, "message": f"{item.capitalize()} count reset to 0", "counts": counts})
        else:
            return jsonify({"success": False, "error": f"Item '{item}' not found"}), 404
    else:
        # Reset all counts if no item specified
        for key in counts.keys():
            counts[key] = 0
        return jsonify({"success": True, "message": "All counts reset to 0", "counts": counts})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Accessible on the local network
