import os
import pickle
import pandas as pd
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import numpy as np

@csrf_exempt
def sentiment_page(request):
    return render(request, 'index.html')


def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  
    text = re.sub(r'[^A-Za-z\s]', '', text)  
    return text.strip()  


model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

@csrf_exempt
def predict_sentiment(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text')
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)

          
            preprocessed_text = preprocess_text(text)

          
            prediction = model.predict([preprocessed_text])[0]
            prediction = str(prediction)  

         
            sentiment_percentages = {}
            if hasattr(model, 'predict_proba'):
                sentiment_probabilities = model.predict_proba([preprocessed_text])[0]

                
                sentiment_labels = ['Negative', 'Positive', 'Neutral']
                sentiment_percentages = {
                    label: float(prob) * 100 for label, prob in zip(sentiment_labels, sentiment_probabilities)
                }

        
            return JsonResponse({
                'prediction': prediction,
                'sentiment_percentages': sentiment_percentages
            })

        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
