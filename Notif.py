import requests
import schedule as schedule

import Settings



def Send(message):
    payload = {
    "app_key": "qCMgVPeA5cBXRuWjnICu",
    "app_secret": "HblMYLMoDd4OyCXbkSwiLG3Tu0iGbKzFEZdcnDpcFNAJw9HFw38qCkrjrh8ANCBc",
    "target_type": "app",
    "content": message
    }

    r = requests.post("https://api.pushed.co/1/push", data=payload)
    print(r.text)

