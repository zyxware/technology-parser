import asyncio
import os
import argparse

async def run_wappalyzer(url, semaphore):
    async with semaphore:
        try:
            print(f"Starting Wappalyzer for: {url}")
            # Run Wappalyzer on the URL
            # Remove 'https://' from the URL to create the filename
            fname = url.replace('https://', '')
            command = f"../wappalyzer/cli.js {url} > technology/tech_{fname}.json"
            file_path = f'technology/tech_{fname}.json'
            
            # Check if the file already exists
            if os.path.exists(file_path):
              print(f"Result already available for: {url}. Skipping Wappalyzer.")
              return None
            
            # Launch subprocess without waiting for its output
            proc = await asyncio.create_subprocess_shell(command, shell=True )

            # Wait for the process to complete and return its exit status
            await proc.wait()
            if proc.returncode == 0:
                print(f"Wappalyzer completed successfully for: {url}")
                return url
            else:
                print(f"Wappalyzer encountered an error for: {url}")
                return None

        except Exception as e:
            print(f"Error running Wappalyzer for {url}: {e}")
            return None

async def main(input_file):
    processed_urls_file = 'processed_urls.txt'
    processed_urls = set()

    if os.path.exists(processed_urls_file):
        with open(processed_urls_file, 'r') as file:
            processed_urls = set(line.strip() for line in file)

    urls = []
    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file if line.strip() not in processed_urls]

    # Ensure the technology directory exists
    if not os.path.exists('technology'):
        os.makedirs('technology')

    # Semaphore to limit concurrent subprocesses
    max_concurrent_subprocesses = 20
    semaphore = asyncio.Semaphore(max_concurrent_subprocesses)

    tasks = [run_wappalyzer(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)

    #with open(processed_urls_file, 'a') as file:
    #    for result in results:
    #        if result:
    #            file.write(result + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Wappalyzer on a list of URLs")
    parser.add_argument('input_file', help="File containing list of URLs")
    args = parser.parse_args()
    asyncio.run(main(args.input_file))
