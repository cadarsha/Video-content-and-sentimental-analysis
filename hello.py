import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from io import StringIO

# Example URL to scrape
url = 'https://dsproj.ccbp.tech/'

# Fetch webpage content
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the script tag containing CSV URL
    script_tag = soup.find('script', string=lambda text: text and 'fetch(' in text)

    if script_tag:
        # Extract the URL of the CSV file from JavaScript code
        js_code = script_tag.string
        csv_url = js_code.split("fetch('")[1].split("')")[0]

        # Fetch CSV data
        csv_response = requests.get(csv_url)

        if csv_response.status_code == 200:
            # Read CSV data into pandas DataFrame
            csv_data = csv_response.content.decode('utf-8')
            df = pd.read_csv(StringIO(csv_data))

            # Display the loaded data
            print("Video Data:")
            print(df)

            # Plotting video metrics
            plt.figure(figsize=(14, 8))

            # Define bar width and positions
            bar_width = 0.2
            index = range(len(df))

            # Plot bars for likes, shares, comments, and views
            plt.bar(index, df['likes'], width=bar_width, label='Likes', color='blue')
            plt.bar([i + bar_width for i in index], df['shares'], width=bar_width, label='Shares', color='green')
            plt.bar([i + 2 * bar_width for i in index], df['comments'], width=bar_width, label='Comments', color='orange')
            plt.bar([i + 3 * bar_width for i in index], df['views'], width=bar_width, label='Views', color='red')

            # Labeling the plot
            plt.xlabel('Videos')
            plt.ylabel('Count')
            plt.title('Video Content Analysis')
            plt.xticks(index, df['description'], rotation=45, ha='right')
            plt.legend()

            # Ensure a tight layout
            plt.tight_layout()
            plt.show()

        else:
            print(f"Failed to retrieve CSV data from {csv_url}. Status code: {csv_response.status_code}")

    else:
        print(f"No JavaScript code found with CSV fetch URL on {url}")

else:
    print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")