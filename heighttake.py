import requests
from googlesearch import search
from bs4 import BeautifulSoup
import re

def google_search(query):
    search_results = []
    for j in search(query, num_results=5):
        search_results.append(j)
    return search_results

def get_average_height(search_results):
    heights = []

    for result in search_results:
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            height_text = soup.get_text()

            
            height_match = re.search(r'\d+(\.\d+)?\s*(meters?|cm|in(ch(es)?)?)', height_text, re.I)
            if height_match:
                height_value = float(height_match.group(0).split()[0])
                unit = height_match.group(0).lower()

                
                if 'in' in unit:
                    height_value *= 2.54  # 1 inch = 2.54 cm

                heights.append(height_value)
        except Exception as e:
            print(f"Error processing {result}: {e}")

    if heights:
        average_height = sum(heights) / len(heights)
        return average_height
    else:
        return None


object_name = input("Enter the object for height estimation: ")


search_query = f"{object_name} average height"
search_results = google_search(search_query)

average_height = get_average_height(search_results)


if average_height is not None:
    print(f"Object: {object_name}")
    print(f"Average Height: {average_height:.2f} centimeters")
else:
    print(f"No information found for {object_name}")
