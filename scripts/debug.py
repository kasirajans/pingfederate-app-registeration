import json

data = {"key": "value"}
# First serialization
json_data = json.dumps(data)

# Second serialization (this is where the problem occurs)
output = json.dumps({"resources": json_data})

print(output)