import requests
def translate(src_lang="en",dest_lang="hi",text="") : 
    json_data = {
        'controlConfig': {
            'dataTracking': True,
        },
        'input': [
            {
                'source': text ,
            },
        ],
        'config': {
            'serviceId': '',
            'language': {
                'sourceLanguage': src_lang,
                'targetLanguage': dest_lang,
                'targetScriptCode': None,
                'sourceScriptCode': None,
            },
        },
    }
    
    response = requests.post('https://demo-api.models.ai4bharat.org/inference/translation/v2', json=json_data)
    translated_txt = response.json()["output"][0]["target"]
    return translated_txt
 
#trail translate :: 
#print( translate("en","ta","You dont need pan card to open income tax account") )

