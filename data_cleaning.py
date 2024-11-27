import pandas as pd

# Load the books.csv file
books_file = "books.csv" 
books_df = pd.read_csv(books_file)

# Check for missing or incomplete ISBN values
print("Before cleaning:")
print(f"Total rows: {len(books_df)}")
print(f"Rows with missing ISBN: {books_df['ISBN'].isna().sum()}")

# Remove rows with missing or empty ISBN
cleaned_books_df = books_df.dropna(subset=['ISBN'])

# Save the cleaned data to a new file
cleaned_books_file = "cleaned_books.csv"
cleaned_books_df.to_csv(cleaned_books_file, index=False)

print("After cleaning:")
print(f"Total rows: {len(cleaned_books_df)}")
print(f"Cleaned data saved to: {cleaned_books_file}")
