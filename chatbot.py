import streamlit as st
import google.generativeai as genai
import datetime
from google.cloud import firestore
from config import generation_config
from config import api_key

genai.configure(api_key=api_key)

# Initialize session state for storing chat history and session ID
def initialise():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = "session_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    if "selected_session_id" not in st.session_state:
        st.session_state["selected_session_id"] = None

# Initialize Firestore client
db = firestore.Client()


# Function to fetch all session IDs from Firestore for the current user
def get_all_session_ids(user_id):
    try:
        # Query to get all session documents for the user in the "chat_sessions" subcollection
        sessions = db.collection("users").document(user_id).collection("chat_sessions").stream()
        session_ids = [session.id for session in sessions]
        return session_ids
    except Exception as e:
        st.error(f"Error fetching session IDs from Firestore: {str(e)}")
        return []

# Function to load a specific session's chat history from Firestore for the current user
def load_chat_history_from_firestore(user_id, session_id):
    try:
        # Reference to the document for the session
        doc_ref = db.collection("users").document(user_id).collection("chat_sessions").document(session_id)
        doc = doc_ref.get()

        if doc.exists:
            chat_data = doc.to_dict().get("history", [])
            return chat_data
        else:
            st.warning("No chat history found for the selected session.")
            return []
    except Exception as e:
        st.error(f"Error loading chat history from Firestore: {str(e)}")
        return []

# Function to update chat history in Firestore for the current user
def update_chat_history_in_firestore(user_id, session_id, chat_history):
    try:
        # Reference to the document for the session
        doc_ref = db.collection("users").document(user_id).collection("chat_sessions").document(session_id)

        # Convert chat history to a format suitable for Firestore
        chat_history_dict = {
            "history": chat_history,
            "last_updated": datetime.datetime.now(datetime.timezone.utc)
        }

        # Set the document data (creates a new document if it doesn't exist)
        doc_ref.set(chat_history_dict, merge=True)
        st.success("Chat history updated in Firestore.")
    except Exception as e:
        st.error(f"Error updating chat history in Firestore: {str(e)}")

def chatbot():
    # Custom CSS styling
    st.markdown("""
        <style>
            body { background-color: #2D2F33; color: #FFFFFF; }
            .block-container { padding-top: 2rem; padding-bottom: 2rem; }
            
            .left-panel, .right-panel {
                background-color: #1E1E2F;
                padding: 1rem;
                border-radius: 10px;
            }
            .chat-bubble {
                max-width: 80%;
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                color: #FFFFFF;
                font-size: 1rem;
            }
            .user-bubble { background-color: #4A90E2; align-self: flex-end; }
            .bot-bubble { background-color: #3E3E5E; align-self: flex-start; }
            
            .sidebar {
                background-color: #1E1E2F;
                color: #FFFFFF;
                padding: 1rem;
            }
            .search-bar {
                padding: 0.5rem;
                background-color: #2E2E4E;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                width: 100%;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Get the user ID from session state
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("User not logged in.")
        return

    # Sidebar for chat history (left panel)
    with st.sidebar:
        st.markdown("### Previous Chat Sessions")

        # Get all previous session IDs for the current user
        all_session_ids = get_all_session_ids(user_id)

        # Allow the user to select a session to view its chat history
        selected_session = st.selectbox("Select a session", all_session_ids, index=0 if all_session_ids else -1)

        # Load the selected session's chat history when a new session is selected
        if "selected_session_id" in st.session_state and selected_session and selected_session != st.session_state["selected_session_id"]:
            st.session_state["selected_session_id"] = selected_session
            previous_chat_history = load_chat_history_from_firestore(user_id, selected_session)
        else:
            previous_chat_history = []

        # Display the chat history for the selected session in the sidebar
        st.markdown("### Chat History")
        if previous_chat_history:
            for entry in previous_chat_history:
                st.write(f"{entry['role'].capitalize()}: {entry['text']}")
        else:
            st.write("No chat history for this session.")

    # Chat interface (right panel)
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FFFFFF'>Chat with ELITH</h3>", unsafe_allow_html=True)

    # Function to get chatbot response
    def get_response(user_input):
        try:
            # Initialize the model and get the response
            model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
            response = model.start_chat().send_message(user_input)
            
            # If response is valid, return the text
            if hasattr(response, 'text') and response.text:
                return response.text
            else:
                return "I'm here to help!"
        except Exception as e:
            return f"Error: {str(e)}"

    # Display chat history with styled chat bubbles (for the current session only)
    initialise()

    for chat in st.session_state["chat_history"]:
        bubble_class = "user-bubble" if chat["role"] == "user" else "bot-bubble"
        st.markdown(f"<div class='chat-bubble {bubble_class}'>{chat['text']}</div>", unsafe_allow_html=True)

    # Placeholder for input field at the bottom of the chat window
    if user_input := st.chat_input("Type your message here..."):

        initialise()

        # Append user message to chat history
        st.session_state["chat_history"].append({"role": "user", "text": user_input})
        st.markdown(f"<div class='chat-bubble user-bubble'>{user_input}</div>", unsafe_allow_html=True)

        # Get the bot's response and add it to the chat history
        bot_response = get_response(user_input)
        st.session_state["chat_history"].append({"role": "bot", "text": bot_response})
        st.markdown(f"<div class='chat-bubble bot-bubble'>{bot_response}</div>", unsafe_allow_html=True)

        # Update chat history in Firestore for the current user
        update_chat_history_in_firestore(user_id, st.session_state["session_id"], st.session_state["chat_history"])

    st.markdown("</div>", unsafe_allow_html=True)