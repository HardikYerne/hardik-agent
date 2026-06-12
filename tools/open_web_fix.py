def open_website(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        import subprocess
        chrome_paths = [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        ]
        for path in chrome_paths:
            import os
            if os.path.exists(path):
                subprocess.Popen([path, url])
                return f'Opening {url} in Chrome'
        subprocess.Popen(['start', url], shell=True)
        return f'Opening {url}'
    except Exception as e:
        return f'Could not open: {e}'
