from transformers import pipeline
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class SemanticAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.ner_ready = True
        except:
            self.ner_ready = False
        
        try:
            self.classifier = pipeline("zero-shot-classification",
                                      model="facebook/bart-large-mnli")
            self.classifier_ready = True
        except:
            self.classifier_ready = False
    
    def analyze_semantics(self, text):
        entities = []
        topics = []
        
        if self.ner_ready:
            doc = self.nlp(text)
            entities = [ent.text for ent in doc.ents]
            topics = [chunk.text for chunk in doc.noun_chunks][:5]

        text_lower = text.lower()

        high_urgency = ["emergency", "immediately", "help", "urgent", "deadly", "panic", 
                       "danger", "critical", "life-threatening", "evacuate", "dying",
                       "attack", "disaster", "tsunami", "earthquake", "fire"]

        medium_urgency = ["worried", "scared", "anxious", "concerned", "confused", 
                         "should i", "what should", "don't know what to do"]

        low_indicators = ["is it true", "did", "was", "were", "has", "have", "when did",
                         "i heard", "i read", "someone said"]

        if any(word in text_lower for word in high_urgency):
            urgency = "High"
            
        elif any(phrase in text_lower for phrase in medium_urgency):
            urgency = "Medium"

        elif any(phrase in text_lower for phrase in low_indicators):
            urgency = "Low"
        else:
            urgency = "Low" 
        
        return {
            "entities": entities,
            "topics": topics,
            "urgency": urgency
        }
