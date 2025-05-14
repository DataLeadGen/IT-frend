import trafilatura
import json
import sys

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    """
    # Send a request to the website
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        content = get_website_text_content(url)
        if content:
            print(json.dumps({"url": url, "content": content}))
        else:
            print(json.dumps({"url": url, "error": "No content extracted"}))
    else:
        print("Please provide a URL as a command-line argument.")