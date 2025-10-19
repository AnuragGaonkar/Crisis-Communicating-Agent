from transformers import pipeline

class MisinformationDetector:
    def __init__(self):
        try:
            self.classifier = pipeline("text-classification", 
                                      model="hamzab/roberta-fake-news-classification")
            self.model_ready = True
        except:
            self.model_ready = False
            print("Misinformation model not available, using fallback")
    
    def predict(self, text):
        if not self.model_ready:
            keywords = ['heard', 'rumor', 'unconfirmed', 'allegedly', 'supposedly']
            return 1 if any(k in text.lower() for k in keywords) else 0
        
        result = self.classifier(text)[0]
        return 1 if result['label'] == 'FAKE' else 0
    
    def predict_proba(self, text):
        if not self.model_ready:
            keywords = ['heard', 'rumor', 'unconfirmed', 'allegedly', 'supposedly']
            score = sum(1 for k in keywords if k in text.lower()) / len(keywords)
            return [1-score, score]
        
        result = self.classifier(text)[0]
        confidence = result['score']
        if result['label'] == 'FAKE':
            return [1-confidence, confidence]
        else:
            return [confidence, 1-confidence]
