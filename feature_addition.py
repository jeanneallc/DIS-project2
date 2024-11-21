import pandas as pd
import requests
import json

def fetch_book_data(isbn):
    """Fetches book data from Open Library API using ISBN."""
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        book_key = f"ISBN:{isbn}"
        if book_key in data:
            book_info = data[book_key]
            return {
                "title": book_info.get("title", None),
                "authors": ", ".join([author.get("name") for author in book_info.get("authors", [])]),
                "number_of_pages": book_info.get("number_of_pages", None),
                "publish_date": book_info.get("publish_date", None)
            }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for ISBN {isbn}: {e}")
    return {"title": None, "authors": None, "number_of_pages": None, "publish_date": None}

def enrich_books_data(input_file, output_file):
    """Reads a books.csv file, fetches additional metadata using the Open Library API, and saves the enriched data."""
    # Read the input CSV
    books_df = pd.read_csv(input_file)
    
    # Initialize new columns
    books_df["title"] = None
    books_df["authors"] = None
    books_df["number_of_pages"] = None
    books_df["publish_date"] = None

    # Fetch data for each ISBN
    for idx, row in books_df.iterrows():
        isbn = row["ISBN"]
        print(f"Fetching data for ISBN: {isbn}")
        book_data = fetch_book_data(isbn)
        books_df.at[idx, "title"] = book_data["title"]
        books_df.at[idx, "authors"] = book_data["authors"]
        books_df.at[idx, "number_of_pages"] = book_data["number_of_pages"]
        books_df.at[idx, "publish_date"] = book_data["publish_date"]
    
    # Save the enriched data to a new CSV file
    books_df.to_csv(output_file, index=False)
    print(f"Enriched data saved to {output_file}")

# Use the function
input_csv = "books.csv"  # Input file path
output_csv = "enriched_books.csv"  # Output file path
enrich_books_data(input_csv, output_csv)
