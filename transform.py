import pandas as pd
import numpy as np
import json

results = {"translatedText": [], "detectedSourceLanguage": []}
data = json.load(open("data.json", "r"))["results"]
_data = np.hstack([d["data"]["translations"] for d in data]).tolist()
for item in _data:
    results["translatedText"].append(item["translatedText"])
    results["detectedSourceLanguage"].append(item["detectedSourceLanguage"])
df = pd.DataFrame(results)

print(df.head())