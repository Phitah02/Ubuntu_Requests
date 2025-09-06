import requests
import os
from urllib.parse import urlparse

def is_valid_image_url(url):
    """
    Basic validation to check if the URL is a valid HTTP/HTTPS URL.
    """
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and '.' in parsed.netloc

def get_filename_from_url(url):
    """
    Extract filename from URL or generate a default one.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        filename = "downloaded_image.jpg"
    return filename

def download_image(url, directory):
    """
    Download and save an image from the given URL with precautions.
    """
    try:
        # Fetch the image with user-agent header for respect
        headers = {'User-Agent': 'Ubuntu-Image-Fetcher/1.0'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Check important HTTP headers
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            raise ValueError(f"Invalid content type: {content_type}. Only images are allowed.")
        
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            raise ValueError("File too large (>10MB). Download aborted for safety.")
        
        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(directory, filename)
        
        # Prevent downloading duplicate images by checking if file exists
        if os.path.exists(filepath):
            print(f"✗ Image already exists: {filename}. Skipping to avoid duplicates.")
            return
        
        # Save the image in binary mode
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except ValueError as e:
        print(f"✗ Validation error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    """
    Main function to handle user interaction and image fetching.
    """
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("Enter image URLs one by one. Press Enter without input to finish.\n")
    
    # Create directory if it doesn't exist
    directory = "Fetched_Images"
    os.makedirs(directory, exist_ok=True)
    
    while True:
        url = input("Please enter the image URL (or press Enter to finish): ").strip()
        if not url:
            break
        
        if not is_valid_image_url(url):
            print("✗ Invalid URL. Please enter a valid HTTP/HTTPS URL.")
            continue
        
        download_image(url, directory)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
