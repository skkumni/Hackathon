
class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        result = ''
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-002',
                           headers=headers, json=completion_request, stream=True) as r:
            response_text=r.text
            lines = response_text.strip().split('\n\n')

            for line in lines:
                if line.find('event:result') != -1:
                    line_dict = json.loads(line.split('data:', 1)[1])
                    result = line_dict['message']['content']
        
        return result


def clova(prompt):
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='',
        api_key_primary_val='HolL48sNDJV2GluXorHDVnS36TEx5OmJ7K9um5pP',
        request_id='b50adfab61354b31a9a4469f563fe7e1'
    )

    preset_text = [{"role":"user","content":prompt}]
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 256,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True
    }

    return completion_executor.execute(request_data)