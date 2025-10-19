import streamlit as st
from lang_detection.detect import detect_language
from sentiment_analysis.analyze import SentimentAnalyzer
from semantic_analysis.analyze import SemanticAnalyzer
from update_generation.generate import UpdateGenerator
from chatbot.bot import CrisisChatbot
from web_search.search import WebSearchAgent
from langcodes import Language


st.set_page_config(
    page_title="Crisis AI Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .verified {
        color: #00C853;
        font-weight: bold;
    }
    .unverified {
        color: #FF6D00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'analyzers_loaded' not in st.session_state:
    with st.spinner("Loading AI models..."):
        st.session_state.sentiment_analyzer = SentimentAnalyzer()
        st.session_state.semantic_analyzer = SemanticAnalyzer()
        st.session_state.update_generator = UpdateGenerator()
        st.session_state.chatbot = CrisisChatbot()
        st.session_state.web_search = WebSearchAgent()
        st.session_state.analyzers_loaded = True

st.markdown('<p class="main-header">Agentic AI Crisis Communication System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time verification • Multi-language support • Sentiment analysis</p>', unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=100)
    st.title("System Info")
    st.markdown("---")
    st.markdown("### Chat History")

    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages[::-1]):
            role = "User" if msg['role'] == 'user' else "AI"
            with st.expander(f"{role} - {msg['content'][:50]}..."):
                st.write(msg['content'])
    else:
        st.info("No messages yet")


st.markdown("###Chat with Crisis AI")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if 'sample_query' in st.session_state:
    user_input = st.session_state.sample_query
    del st.session_state.sample_query
else:
    user_input = st.chat_input("Ask about any crisis situation, news, or fact...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing and verifying..."):

            lang = detect_language(user_input)

            semantic = st.session_state.semantic_analyzer.analyze_semantics(user_input)

            sentiment = st.session_state.sentiment_analyzer.analyze_sentiment(user_input)

            verification = st.session_state.web_search.verify_claim(user_input)

            response_container = st.container()

            with response_container:
                with st.expander("Analysis Report", expanded=False):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        try:
                            lang_full = Language.get(lang).display_name().capitalize()
                        except:
                            lang_full = lang.upper()
                        st.metric("Language", lang_full)
                        st.metric("Urgency", semantic['urgency'])

                    with col2:
                        st.metric("Sentiment", sentiment['sentiment'].title())
                        st.metric("Emotion", sentiment['emotion'].title())

                    with col3:
                        if verification['verified']:
                            st.markdown(f"<p class='verified'>✓ VERIFIED</p>", unsafe_allow_html=True)
                            st.metric("Confidence", f"{verification['confidence']*100:.0f}%")
                        else:
                            st.markdown(f"<p class='unverified'>⚠ UNVERIFIED</p>", unsafe_allow_html=True)
                            st.metric("Sources Found", len(verification['sources']))

                    if verification['sources']:
                        st.markdown("**Sources Checked:**")
                        for idx, source in enumerate(verification['sources'][:3], 1):
                            st.markdown(f"{idx}. [{source['source']}]({source['url']})")
                            st.caption(source['title'][:80] + "...")

                bot_response = st.session_state.chatbot.get_response(user_input)

                st.markdown("### Response:")
                with st.chat_message("assistant"):
                    st.markdown(bot_response)

                if verification['verified']:
                    st.success(f"Verified by {len(verification['verified_sources'])} official sources")
                elif verification['sources']:
                    st.warning(f"Found {len(verification['sources'])} sources but none from official channels")
                else:
                    st.error("Could not find sources to verify this claim")

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Messages", len(st.session_state.messages) // 2)
with col2:
    st.metric("Status", "Online")
with col3:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
