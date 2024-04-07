import requests


class Line:
    def __init__(self, tokens):
        self.tokens = tokens
        self.headers_tpl = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer {token}'
        }
        self.url = 'https://notify-api.line.me/api/notify'

    def send(self, message, token):
        print(f"Sending message: {message}")
        headers = self.headers_tpl
        headers['Authorization'] = headers['Authorization'].format(token=token)
        payload = {
            'message': f"\n{message}"
        }
        response = requests.post(self.url, headers=headers, data=payload)
        print(response.text)
        return response

    def send_all(self, message):
        responses = []
        for token in self.tokens:
            response = self.send(message, token)
            responses.append(response)
        return responses
