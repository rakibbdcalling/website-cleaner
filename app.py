import os
from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Function to process URLs based on the button clicked
def modify_urls(urls, action):
    modified_urls = []
    
    def clean_url(url):
        url = url.replace("https://", "").replace("http://", "").replace("www.", "")
        match = re.match(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', url)
        return match.group(0) if match else None

    for url in urls:
        cleaned_url = url.strip()
        
        if cleaned_url:
            cleaned_url = clean_url(cleaned_url)
            if cleaned_url is None:
                modified_urls.append(url.strip())
                continue
        
        if action == "add_https":
            if cleaned_url and not cleaned_url.startswith("https://"):
                cleaned_url = "https://" + cleaned_url
        elif action == "add_http":
            if cleaned_url and not cleaned_url.startswith("http://"):
                cleaned_url = "http://" + cleaned_url
        elif action == "add_https_www":
            if cleaned_url and not cleaned_url.startswith("https://www."):
                cleaned_url = "https://www." + cleaned_url
        elif action == "add_http_www":
            if cleaned_url and not cleaned_url.startswith("http://www."):
                cleaned_url = "http://www." + cleaned_url
        
        if action in ["add_https", "add_http", "add_https_www", "add_http_www"]:
            if cleaned_url and not cleaned_url.endswith("/"):
                cleaned_url += "/"
        
        modified_urls.append(cleaned_url if cleaned_url else url.strip())

    return modified_urls

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    if request.method == "POST":
        urls = request.form["urls"].split("\n")
        action = request.form["action"]
        result = modify_urls(urls, action)

    input_urls = request.form.get("urls", "")
    return render_template("index.html", result="\n".join(result), input_urls=input_urls)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway-assigned port
    app.run(debug=False, host="0.0.0.0", port=port)
