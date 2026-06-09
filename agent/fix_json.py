def extract_json(text):
    try:
        text = text.strip()
        # remove all extra closing braces
        while text.endswith('}}'):
            text = text[:-1]
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            return json.loads(json_str)
    except Exception as e:
        print(f'JSON error: {e}')
    return {'action': 'talk', 'value': 'I could not process that command.'}
