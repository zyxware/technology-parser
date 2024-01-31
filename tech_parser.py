import json
import csv
import os
import pandas as pd

def read_base_domains(filename):
    """Reads the base domains from a file."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def remove_url_parameters(url):
    if "?" not in url:
        return url
    return url.split('?')[0]

def get_cms_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading JSON from {filename}: {e}")
        return ["File Error", "File Error", "File Error"]

    url = ''
    cms_name = ''
    cms_version = ''
    
    if not data:
        return ["0", "0", "0"]
    
    for url_data, status in data["urls"].items():
        url_data = remove_url_parameters(url_data)
        if status['status'] == 200:
            url = url_data
            break
        elif status['status'] == 0:
            url = url_data
            return [url, "0", "0"]
            
    if url:
        for technology in data['technologies']:
            for category in technology['categories']:
                if category['name'] == 'CMS':
                    cms_name = technology['name']
                    cms_version = technology['version']
                    break
                    
    if not cms_name:
        cms_name = 'Not Detected'
        cms_version = '0'
        
    if not cms_version:
        cms_version = '0'
        
    return [url, cms_name, cms_version]

def load_tranco_data(filename):
    df = pd.read_csv(filename, header=None, names=['TrancoRank', 'Domain'])
    tranco_series = pd.Series(df.TrancoRank.values, index=df.Domain)
    return tranco_series

def find_tranco_rank(full_domain, tranco_series):
    return tranco_series.get(full_domain, '0')

def create_csv(base_domains_file, folder):
    base_domains = read_base_domains(base_domains_file)
    tranco_series = load_tranco_data('tranco_Z25PG.csv')
    domains_data = {}

    for filename in os.scandir(folder):
        if filename.is_file():
            for base_domain in base_domains:
                if filename.name.endswith(f"{base_domain}.json"):
                    full_domain = filename.name.split('.json')[0][5:]  # Removes 'tech_' prefix
                    domains_data.setdefault(base_domain, []).append((full_domain, filename.name))

    with open('domains.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['BaseDomain', 'FullDomain', 'URL', 'CMS', 'Version', 'TrancoRank'])

        for base_domain, files in domains_data.items():
            for full_domain, filename in files:
                full_path = os.path.join(folder, filename)
                if os.path.exists(full_path):
                    cms_data = get_cms_data(full_path)
                    tranco_rank = find_tranco_rank(full_domain, tranco_series)
                    writer.writerow([base_domain, full_domain] + cms_data + [tranco_rank])
                else:
                    writer.writerow([base_domain, full_domain, 'File Not Found', 'File Not Found'])

# File containing the base domains
base_domains_file = "uni_list.txt"

# Folder containing the technology files
folder = "technology"

# Create the CSV
create_csv(base_domains_file, folder)
