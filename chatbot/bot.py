import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web_search.search import WebSearchAgent
import google.generativeai as genai

class CrisisChatbot:
    def __init__(self):
        try:
            if "GENIE_API_KEY" in st.secrets:
                api_key = st.secrets["GENIE_API_KEY"]
            else:
                load_dotenv()
                api_key = os.getenv("GENIE_API_KEY")
            genai.configure(api_key=api_key)  
            self.model = genai.GenerativeModel("gemini-2.5-pro")
            self.search_agent = WebSearchAgent()
            self.model_ready = True
            self.conversation_history = []
            print("Chatbot with web search loaded successfully")
        except Exception as e:
            self.model_ready = False
            print(f"Failed to initialize: {e}")

    def needs_clarification(self, user_input):
        """Check if question needs clarification"""
        vague_terms = ['all banks', 'the bank', 'hospitals', 'government', 'they', 'everywhere']
        locations = ['india', 'us', 'uk', 'country', 'city', 'world']
        
        user_lower = user_input.lower()
        has_vague = any(term in user_lower for term in vague_terms)
        has_location = any(loc in user_lower for loc in locations)
        
        if has_vague and not has_location and len(self.conversation_history) < 2:
            return True, "which country, region, or specific location you're asking about"
        
        return False, None

    def get_response(self, user_input, analysis_results=None, history=None):
        """Generate human-like response with web search powered by Gemini Pro"""
        
        if not self.model_ready:
            return "System temporarily unavailable."

        if history is not None and not self.conversation_history:
            self.conversation_history = history.copy()
        
        self.conversation_history.append({"role": "user", "content": user_input})
        
        needs_clarif, clarif_question = self.needs_clarification(user_input)
        if needs_clarif:
            response = f"To provide accurate verified information, could you please specify {clarif_question}?"
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        verification = self.search_agent.verify_claim(user_input)

        search_summary = f"Web search found {len(verification['sources'])} sources:\n\n"
        
        if verification['sources']:
            for idx, source in enumerate(verification['sources'][:3], 1):
                search_summary += f"{idx}. {source['title']}\n"
                search_summary += f"   Source: {source['source']}\n"
                search_summary += f"   Content: {source['snippet'][:150]}...\n\n"
            
            search_summary += f"Official sources found: {len(verification.get('verified_sources', []))}\n\n"
        else:
            search_summary += "No sources found for this claim.\n\n"

        prompt = (
            "You are a crisis communication AI assistant for government agencies.\n\n"
            "Your role:\n"
            "- Provide factual, calm responses based on web search results\n"
            "- If search shows no confirmation, clearly state that\n"
            "- Direct users to official channels\n"
            "- Be empathetic and professional\n"
            "- Cite sources you reference\n\n"
            "CRITICAL: Base your response ONLY on the search results provided. Do not make up information.\n\n"
            f"{search_summary}User question: {user_input}\n"
            "Based on the search results above, provide a helpful response that:\n"
            "1. States if the claim is verified, unverified, or denied by sources\n"
            "2. References specific sources\n"
            "3. Advises checking official channels\n"
            "4. Maintains empathetic, professional tone\n"
            "Keep response under 150 words."
        )
        
        try:
            result = self.model.generate_content(prompt)
            ai_response = result.text.strip()
        except Exception as e:
            print(f"API Error: {e}")
            if verification.get('verified_sources'):
                fallback = (
                    f"Based on {len(verification['sources'])} sources checked, "
                    f"including {len(verification['verified_sources'])} official sources, "
                )
                snippets = ' '.join([s['snippet'].lower() for s in verification['sources'][:3]])
                if 'no evidence' in snippets or 'false' in snippets or 'unverified' in snippets:
                    fallback += "there is NO official confirmation of this claim. "
                else:
                    fallback += "this information is supported by official sources. "
            else:
                fallback = (
                    f"Searched {len(verification['sources'])} sources but found no official confirmation. "
                )
            fallback += "Check official government websites for verified information.\n\nSources: "
            fallback += ", ".join([s['source'] for s in verification['sources'][:3]])
            ai_response = fallback

        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
