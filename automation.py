import requests
import pandas as pd
from google.colab import files

# Upload your CSV file containing domain names
uploaded = files.upload()
file_name = list(uploaded.keys())[0]

# Read domains from the uploaded file
domains_df = pd.read_csv(file_name)
domains = domains_df['Domain'].tolist()

# Replace this with your Ahrefs API token
API_TOKEN = "YOUR_API_TOKEN"

# Base URL for Ahrefs API
API_URL = "https://apiv2.ahrefs.com/"

# Function to fetch Ahrefs data for a domain
def fetch_ahrefs_data(domain, token):
    params = {
        'token': token,
        'from': 'domain',
        'target': domain,
        'output': 'json'
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {domain}: {response.status_code}")
        return None

# Iterate over domains and fetch data
results = []
for domain in domains:
    print(f"Crawling domain: {domain}")
    data = fetch_ahrefs_data(domain, API_TOKEN)
    if data:
        results.append({
            'Domain': domain,
            'Data': data
        })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save results to a CSV file
output_file = "ahrefs_crawl_results.csv"
results_df.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")

# Download the results
files.download(output_file)
