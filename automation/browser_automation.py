import subprocess

def open_chrome_and_search(query):
    try:
        url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
        subprocess.Popen(['start', url], shell=True)
        return f'Searching Google for: {query}'
    except Exception as e:
        return f'Could not search: {e}'

def open_youtube_and_search(query):
    try:
        url = f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'
        subprocess.Popen(['start', url], shell=True)
        return f'Searching YouTube for: {query}'
    except Exception as e:
        return f'Could not search YouTube: {e}'

def open_url(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        subprocess.Popen(['start', url], shell=True)
        return f'Opened {url}'
    except Exception as e:
        return f'Could not open: {e}'
