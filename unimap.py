import pandas as pd
from fuzzywuzzy import process, fuzz

def preprocess_name(name):
    """
    Basic preprocessing of university names.
    """
    # Convert to lowercase
    name = name.lower()
    # Replace common university terms for standardization
    name = name.replace('university', 'uni').replace('institute', 'inst').replace('college', 'coll')
    # Additional preprocessing can be added here
    return name

def match_universities(base_file, url_file, output_file, threshold=85):
    # Load the datasets
    base_df = pd.read_csv(base_file)
    url_df = pd.read_csv(url_file)

    # Preprocess university names and store in a new column
    base_df['processed_uniname'] = base_df['uniname'].apply(preprocess_name)
    url_df['processed_uniname'] = url_df['uniname'].apply(preprocess_name)

    # Create a mapping of processed university names to URLs
    uni_to_url = dict(zip(url_df['processed_uniname'], url_df['url']))

    # Function to find best match with a threshold
    def find_best_match(name):
        best_match, score = process.extractOne(name, uni_to_url.keys(), scorer=fuzz.token_sort_ratio)
        return uni_to_url[best_match] if score >= threshold else None

    # Applying the function to each processed university name in the base dataset
    base_df['matched_url'] = base_df['processed_uniname'].apply(find_best_match)

    # Dropping the processed names column before saving
    base_df.drop(columns=['processed_uniname'], inplace=True)

    # Saving the merged dataset
    base_df.to_csv(output_file, index=False)
    print(f"Output file '{output_file}' created successfully.")

    # Returning unmatched or low confidence matches for manual review
    return base_df[base_df['matched_url'].isnull()]

unmatched = match_universities('uni-rank.csv', 'uni-url.csv', 'merged_universities.csv')
print("Universities that need manual review:")
print(unmatched)

