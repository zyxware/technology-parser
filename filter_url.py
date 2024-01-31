import sys

# Check if the input file argument is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

# Define the keywords to filter out
keywords = ['mail', 'image', 'login', 'autodiscover', 'microsoft', 'googleapis', 'google', 'amazon', 'cdn', 'vpn', 'cisco', 'mx', 'spam','aws', 'idp', 'smtp', 'cloud', 'stage','dev']

# Function to check if any keyword is in the URL
def contains_keyword(url, keywords):
    return any(keyword in url for keyword in keywords)

# Read URLs from the input file
try:
    with open(input_file, 'r') as file:
        urls = file.readlines()
except FileNotFoundError:
    print(f"File not found: {input_file}")
    sys.exit(1)

# Filter URLs
filtered_urls = [url for url in urls if not contains_keyword(url, keywords)]

# Output filtered URLs to stdout
for url in filtered_urls:
    sys.stdout.write(url)

