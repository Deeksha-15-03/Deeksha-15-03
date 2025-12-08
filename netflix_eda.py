import pandas as pd

# ------------------------------
# 1. Upload the file in Colab
# ------------------------------
from google.colab import files
uploaded = files.upload()     # Upload netflix_titles.csv

df = pd.read_csv("netflix_titles.csv")
print("Dataset Loaded Successfully!")
print("Initial shape:", df.shape)

# ------------------------------
# 2. Handle Missing Values
# ------------------------------
# Fill categorical columns with mode
categorical_cols = ['country', 'rating']
for col in categorical_cols:
    if col in df.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

# Remove rows where title or type is missing
df.dropna(subset=['title', 'type'], inplace=True)

print("Missing values handled.")

# ------------------------------
# 3. Remove Duplicate Rows
# ------------------------------
df.drop_duplicates(inplace=True)
print("Duplicates removed.")

# ------------------------------
# 4. Standardize Text Columns
# ------------------------------
text_cols = df.select_dtypes(include='object').columns

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.lower()

# Standardize type values
df['type'] = df['type'].replace({
    'movie': 'movie',
    'tv show': 'tv show',
    'tvshow': 'tv show'
})

print("Text columns standardized.")

# ------------------------------
# 5. Clean Column Names
# ------------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Column names cleaned.")

# ------------------------------
# 6. Convert date_added to datetime
# ------------------------------
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

print("Date formats fixed.")

# ------------------------------
# 7. Clean Duration Column
# ------------------------------
def split_duration(value):
    value = str(value)
    parts = value.split()
    if len(parts) == 2:
        try:
            return int(parts[0]), parts[1]
        except:
            return None, None
    return None, None

df['duration_value'], df['duration_type'] = zip(*df['duration'].apply(split_duration))

df.drop(columns=['duration'], inplace=True)

print("Duration column cleaned.")

# ------------------------------
# 8. Export cleaned file
# ------------------------------
df.to_csv("netflix_cleaned.csv", index=False)
print("Final cleaned file saved as netflix_cleaned.csv")

# Download the cleaned file
files.download("netflix_cleaned.csv")

print("Cleaning Completed Successfully!")
