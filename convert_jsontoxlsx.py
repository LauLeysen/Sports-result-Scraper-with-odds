import pandas as pd
import json

# Assuming you have the JSON data loaded into a variable named `data`
# Replace 'your_json_file.json' with the path to your JSON file
with open('matches_data_MLB.json', 'r') as file:
    data = json.load(file)

# Flatten the list if your JSON structure is nested lists
flat_list = [item for sublist in data for item in sublist]

# Convert the flat list to a DataFrame
df = pd.DataFrame(flat_list)

# Save the DataFrame to an Excel file
df.to_excel('mlb_matches22.xlsx', index=False)
