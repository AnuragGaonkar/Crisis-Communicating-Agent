from transformers import pipeline
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        try:
            # Multi-emotion classifier
            self.emotion_classifier = pipeline("text-classification",
                                              model="j-hartmann/emotion-english-distilroberta-base",
                                              return_all_scores=False)
            self.model_ready = True
        except:
            self.model_ready = False
    
    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if self.model_ready:
            emotion_result = self.emotion_classifier(text)[0]
            emotion = emotion_result['label']
            emotion_score = emotion_result['score']
        else:
            # Fallback
            if polarity < -0.3:
                emotion = "sadness"
            elif polarity > 0.3:
                emotion = "joy"
            else:
                emotion = "neutral"
            emotion_score = abs(polarity)
        
        sentiment = 'positive' if polarity > 0.05 else 'negative' if polarity < -0.05 else 'neutral'
        
        return {
            "sentiment": sentiment,
            "polarity": polarity,
            "emotion": emotion,
            "emotion_confidence": emotion_score
        }
