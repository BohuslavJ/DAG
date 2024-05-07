import requests


def get_json_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None


def print_docs_author_jrr_tolkien(json_data):
    name_of_author = input("give me name you are looking for: ")
    if "docs" in json_data:
        print(f"Data for {name_of_author}:")
        for item in json_data["docs"]:
            if "author_name" in item and name_of_author in item["author_name"]:
                    print(item)

# Example usage:
api_url = 'https://openlibrary.org/search.json?q=the+lord+of+the+rings'  # Replace with your API URL
json_data = get_json_data(api_url)

if json_data:
    print_docs_author_jrr_tolkien(json_data)
