import pandas as pd

# Load the first dataset
csv_url_1 = 'https://drive.google.com/uc?id=10vuvzzDJ_Bypyt7XJVeHVgzeXolcDyCL'
recipes_df_1 = pd.read_csv(csv_url_1)

# Load the second dataset from local file in chunks
chunk_size = 1000
chunks = []
for chunk in pd.read_csv('recipes_data.csv', chunksize=chunk_size, on_bad_lines='skip'):
    chunks.append(chunk)
recipes_df_2 = pd.concat(chunks, ignore_index=True)

# Load the third dataset
csv_url_3 = 'https://drive.google.com/uc?id=13apn07VxfvJKbNVogjL2ATJ93I20Oo9D'
recipes_df_3 = pd.read_csv(csv_url_3)

# Clean column names to avoid any leading/trailing spaces
recipes_df_1.columns = recipes_df_1.columns.str.strip()
recipes_df_2.columns = recipes_df_2.columns.str.strip()
recipes_df_3.columns = recipes_df_3.columns.str.strip()

# Rename columns to standardize (adjust as necessary)
recipes_df_1.rename(columns={
    'Unnamed: 0': 'Index',
    'Title': 'RecipeName',
    'Ingredients': 'Ingredients',
    'Instructions': 'Instructions',
    'Image_Name': 'ImageURL',
    'Cleaned_Ingredients': 'CleanedIngredients'
}, inplace=True)

# Adjust the following according to the actual column names in the second dataset
recipes_df_2.rename(columns={
    # Example mapping (adjust based on your dataset)
    'OriginalRecipeName': 'RecipeName',
    'SomeIngredients': 'CleanedIngredients',  # Replace with actual name
    'SomeInstructions': 'Instructions'         # Replace with actual name
}, inplace=True)

recipes_df_3.rename(columns={
    'TranslatedRecipeName': 'RecipeName',
    'TranslatedIngredients': 'CleanedIngredients',
    'TranslatedInstructions': 'Instructions',
    'image-url': 'ImageURL'
}, inplace=True)

# Print columns of each dataset
print("Columns in Dataset 1:")
print(recipes_df_1.columns.tolist())
print("\nColumns in Dataset 2:")
print(recipes_df_2.columns.tolist())
print("\nColumns in Dataset 3:")
print(recipes_df_3.columns.tolist())

# Combine the datasets
combined_recipes_df = pd.concat([
    recipes_df_1[['RecipeName', 'CleanedIngredients', 'Instructions', 'ImageURL']],
    recipes_df_2[['RecipeName', 'CleanedIngredients', 'Instructions']],
    recipes_df_3[['RecipeName', 'CleanedIngredients', 'Instructions', 'ImageURL']]
], ignore_index=True)

# Function to find recipes based on available ingredients
def find_recipes(available_ingredients):
    matched_recipes = []
    for index, row in combined_recipes_df.iterrows():
        recipe_ingredients = [ingredient.strip().lower() for ingredient in row['CleanedIngredients'].split(',')]
        if all(item in recipe_ingredients for item in available_ingredients):
            matched_recipes.append(row['RecipeName'])
    return matched_recipes

# User input for available ingredients
user_input = input("Enter excess food items you have (comma-separated): ")
available_ingredients = [ingredient.strip().lower() for ingredient in user_input.split(',')]

# Find suggested recipes
suggested_recipes = find_recipes(available_ingredients)

# Output the results
if suggested_recipes:
    print("Here are some recipes you can make with your excess food:")
    for recipe in suggested_recipes:
        print(f"- {recipe}")
else:
    print("Sorry, no matching recipes found.")
