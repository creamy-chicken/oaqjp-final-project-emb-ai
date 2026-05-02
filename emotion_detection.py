
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def emotion_detector(text_to_analyze):
    try:
        url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

        headers = {
            "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
            "Content-Type": "application/json"
        }

        input_json = {
            "raw_document": {"text": text_to_analyze}
        }

        response = requests.post(url, headers=headers, json=input_json, timeout=5)
        return response.json()

    except Exception as e:
        return {
            "error": "Emotion service unavailable",
            "details": str(e)
        }

@app.route('/emotion', methods=['POST'])
def analyze_emotion():
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "Please provide 'text' in request body"}), 400
    
    result = emotion_detector(data["text"])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)