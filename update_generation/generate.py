from transformers import pipeline

class UpdateGenerator:
    def __init__(self):
        try:
            self.generator = pipeline("summarization", model="facebook/bart-large-cnn")
            self.model_ready = True
        except:
            self.model_ready = False
    
    def generate_update(self, input_text):
        if not self.model_ready or len(input_text.split()) < 30:
            # For short text, create manual verified update
            return "Official advisory: Please await verified updates from authorities. Unconfirmed information should not be acted upon."
        
        try:
            summary = self.generator(input_text, max_length=80, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except:
            return "Advisory: Verify all information through official government channels before taking action."
    
    def cultural_adapt(self, text, culture_info):
        return f"[{culture_info} Public Advisory] {text}"
    