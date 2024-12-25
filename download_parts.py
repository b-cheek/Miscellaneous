import os
import requests

# Base URL with placeholders for the number
# base_url = "https://archives.nyphil.org/index.php/jp2/|MP|2|2729-113|MP_2729-113_{:03d}.jp2/portrait/600"
base_url = "https://archives.nyphil.org/index.php/jp2/|MP|2|2729-113|MP_2729-113_{:03d}.jp2/portrait/1200"

# Directory to save the images
output_dir = "nyphil_images"
os.makedirs(output_dir, exist_ok=True)

# Range of numbers to iterate through
start_num = 1
end_num = 17

# Loop through the range and download each image
for num in range(start_num, end_num + 1):
    # Format the URL with the current number
    url = base_url.format(num)
    print(f"Processing: {url}")
    
    try:
        # Fetch the image
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for failed requests
        
        # Save the image to the output directory
        file_name = os.path.join(output_dir, f"MP_2729-113_{num:03d}.jpg")
        with open(file_name, "wb") as file:
            file.write(response.content)
            print(f"Downloaded: {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

