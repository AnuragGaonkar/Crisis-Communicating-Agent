### Agentic AI Crisis Communication System
    A powerful AI-driven assistant designed to provide real-time crisis communication support by verifying claims, detecting language, analyzing sentiment, and delivering human-like verified responses.

### Features
- Real-time web claim verification

- Multi-language detection with language name display

- Sentiment and emotion analysis

- Crisis urgency detection

- Official source verification and citations

- Human-like AI responses using Google Gemini Pro

- User login/signup with futuristic robotic-themed UI

- Multiple conversations per user with chat history management

- Interactive and expandable detailed analysis reports

### Installation
   - Clone or download the repository.

   - Create a virtual environment (recommended):
        ```sh python -m venv venv ```

   - Activate it:

       - Windows: ```sh venv\Scripts\activate ```

   - Install dependencies:
        ```sh pip install -r requirements.txt ```


   - Run the app with:
        ```sh streamlit run app.py ```

### Usage:
- Launch and login or signup with a creative robot-themed page.

- Start new conversations or resume existing ones from the sidebar.

- Ask about crisis situations, facts, or news.

- View an expandable analysis report including language, sentiment, and source verification.

- Manage multiple chat sessions and clear history as needed.

- Logout securely when finished.

### Architecture
- Streamlit for frontend UI and session management

- Google Gemini Pro for AI chat responses

- DuckDuckGo based web search agent for fact verification

- Langdetect and Langcodes libraries for language identification

- Semantic and sentiment modules for input analysis

- Session-based state storage for users and conversations

### Future Plans
- Enhanced login and signup with database-backed user persistence.

- Multi-modal inputs (images, audio) for richer queries.

- Collaboration features and role-based permissions.

- Improved AI response customization and alerts.

### Contributing
- Contributions welcome! Please fork the repo and submit pull requests for improvements or features.

