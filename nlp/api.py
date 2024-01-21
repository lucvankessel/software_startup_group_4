from bottle import route, run, request, post, response
import json
from nlp import classify_sentence  # Make sure to import the function correctly


@post('/classify')
def classify_text():
    print("NLP classify_text running", flush=True)
    try:
        # Parse input data
        data = request.json
        text = data.get('text')
        if not text:
            raise ValueError("No text provided.")

        # Use the NLP function to classify the text
        result = classify_sentence(text)

        # Prepare the response
        return json.dumps({'classification': result})
    except Exception as e:
        response.status = 400
        return json.dumps({'error': str(e)})


run(host='0.0.0.0', port=8081, debug=True, reloader=True)
