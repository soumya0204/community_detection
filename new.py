import requests
import csv
# Replace 'YOUR_RAPID_API_KEY' with your actual RapidAPI key
RAPID_API_KEY = '85dc4ce6d4msh05ce4244d60e23dp11a174jsn304c23d2c333'

# Instagram endpoint URL
url = "https://instagram-data1.p.rapidapi.com/followers"

# Specify the Instagram username you want to retrieve data for
username = "vellore_vit"

# Set up the headers with the RapidAPI key
headers = {
    'X-RapidAPI-Host': "instagram-data1.p.rapidapi.com",
    'X-RapidAPI-Key': RAPID_API_KEY
}

# Set up the query parameters
params = {
    'username': username
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse and print the response JSON data
    data = response.json()
    print(data)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")

csv_file_path = "followers_data.csv"

# Extracting collectors data
collectors = data.get("collector", [])

# Extracting column headers
headers = ["id", "username", "full_name", "profile_pic_url", "is_private", "is_verified"]

# Writing to CSV
with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    
    # Write header
    writer.writeheader()
    
    # Write data rows
    for collector in collectors:
        writer.writerow(collector)

print(f"CSV data has been written to: {csv_file_path}")