from lang_detection.detect import detect_language
from sentiment_analysis.analyze import SentimentAnalyzer
from semantic_analysis.analyze import SemanticAnalyzer
from update_generation.generate import UpdateGenerator
from dissemination.distribute import DisseminationSystem
from chatbot.bot import CrisisChatbot
from web_search.search import WebSearchAgent


def main():
    print("Loading Agentic AI Crisis Communication System with Web Search...")
    
    sentiment_analyzer = SentimentAnalyzer()
    semantic_analyzer = SemanticAnalyzer()
    update_generator = UpdateGenerator()
    dissemination_system = DisseminationSystem()
    chatbot = CrisisChatbot()
    web_search = WebSearchAgent()
    
    print("\nAgentic AI Ready - Real-time Web Verification Enabled\n")
    print("="*60)

    while True:
        user_input = input("\nEnter message (or 'exit'): ")
        if user_input.lower() == 'exit':
            break
        
        print("\n" + "="*60)
        print("ANALYSIS REPORT")
        print("="*60)

        lang = detect_language(user_input)
        print(f"\nLanguage: {lang}")

        semantic = semantic_analyzer.analyze_semantics(user_input)
        print("\nSemantic Analysis:")
        print(f"   Topics: {', '.join(semantic['topics'][:3]) if semantic['topics'] else 'None'}")
        print(f"   Entities: {', '.join(semantic['entities'][:3]) if semantic['entities'] else 'None'}")
        print(f"   Urgency Level: {semantic['urgency']}")

        print("\nVerification (Web Search Based):")
        try:
            verification = web_search.verify_claim(user_input)
            
            if verification['sources']:
                if verification['verified_sources']:
                    status = "✓ Verified by Official Sources"
                    confidence = verification['confidence']
                else:
                    status = "⚠ Unverified - No Official Sources Found"
                    confidence = 1 - verification['confidence']
            else:
                status = "✗ Cannot Verify - No Sources Found"
                confidence = 0.0
            
            print(f"   Status: {status}")
            print(f"   Confidence: {confidence:.2%}")
            print(f"   Total Sources: {len(verification['sources'])}")
            print(f"   Official/Trusted Sources: {len(verification.get('verified_sources', []))}")
            
            if verification.get('verified_sources'):
                print(f"   Top Official Source: {verification['verified_sources'][0]['source']}")
        except Exception as e:
            print(f"   Status: Verification system error: {e}")

        sentiment = sentiment_analyzer.analyze_sentiment(user_input)
        print(f"\nSentiment: {sentiment['sentiment'].title()}")
        print(f"   Emotion: {sentiment['emotion'].title()} ({sentiment.get('emotion_confidence', 0):.2%})")

        update = update_generator.generate_update(user_input)
        adapted = update_generator.cultural_adapt(update, "Global")
        print(f"\nOfficial Update:\n   {adapted}")

        dissemination_result = dissemination_system.distribute(adapted, "email")
        print(f"\n{dissemination_result}")

        print("\nAgentic Response:")
        bot_response = chatbot.get_response(user_input)
        print(f"   {bot_response}")
        print("\n" + "="*60)


if __name__ == "__main__":
    main()
