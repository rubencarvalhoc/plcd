import json

# Two dictionaries
dict1 = {"name": "Alice", "age": 30, "city": "Lisbon"}
dict2 = {"name": "Bob", "age": 25, "city": "Porto"}

# Combine them into a single JSON object
combined_data = {
    "person1": dict1,
    "person2": dict2
}

# Convert to JSON string
json_data = json.dumps(combined_data, indent=4)
print(json_data)
