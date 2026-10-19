"""
app.py
------
The screen of SAMS, made with Streamlit.
Run it with:   streamlit run app.py

IMPORTANT Streamlit rule: every time the user clicks or types,
Streamlit runs this whole file again from the top.
So anything we want to remember (the chat) is saved in st.session_state.
"""

import streamlit as st

from chatbot_engine import get_response, get_topic_reply, get_title
from knowledge_base import TOPICS

# Must be the first Streamlit command
st.set_page_config(page_title="SAMS | Student Assistant", page_icon="🎓")

# ---------- Design (4 colours: navy, teal, light grey-blue, white) ----------
STYLE = """
<style>
.stApp { background-color: #F4F7FA; }

.header-box {
    background: linear-gradient(90deg, #1F3A5F, #2A9D8F);
    color: #FFFFFF;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 16px;
}
.header-box h1 { color: #FFFFFF; margin: 0; font-size: 28px; }
.header-box p  { margin: 4px 0 0 0; }

[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 12px;
}

.stButton > button {
    border: 1px solid #2A9D8F;
    color: #1F3A5F;
    background-color: #FFFFFF;
    border-radius: 20px;
}
.stButton > button:hover {
    background-color: #2A9D8F;
    color: #FFFFFF;
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

WELCOME = (
    "Hi! I'm **SAMS**, your Student Assistant. 👋\n\n"
    "Tell me what you want to know, for example *\"I'm barred because of attendance\"*, "
    "or tap a topic below."
)


# ---------- Memory of the app ----------
def setup_memory():
    """Create the chat history the first time the app opens."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME,
                "suggestions": ["attendance_bar", "appeal", "fees", "exam_deferment"],
            }
        ]
    if "queued" not in st.session_state:
        st.session_state.queued = None   # None means "no button waiting"


def clear_chat():
    """Runs when the Clear chat button is clicked."""
    del st.session_state["messages"]
    st.session_state.queued = None


def queue_topic(topic_id):
    """Runs when ANY topic button is clicked. It only saves which topic."""
    st.session_state.queued = topic_id


# ---------- Adding messages to the chat ----------
def add_user_message(text):
    st.session_state.messages.append({"role": "user", "content": text})


def add_bot_message(reply):
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply["text"],
            "suggestions": reply["suggestions"],
        }
    )


# ---------- Drawing the screen ----------
def show_header():
    st.markdown(
        """
        <div class="header-box">
            <h1>🎓 SAMS</h1>
            <p>Student Assistant Management System: step-by-step help for university processes</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_sidebar():
    with st.sidebar:
        st.markdown("### 📚 Quick topics")
        for topic in TOPICS:
            st.button(
                topic["title"],
                key="side_" + topic["id"],
                on_click=queue_topic,
                args=(topic["id"],),
                use_container_width=True,
            )
        st.divider()
        st.button("🗑️ Clear chat", on_click=clear_chat, use_container_width=True)
        st.caption("SAMS uses keyword matching only. No AI model or external API.")


def show_messages():
    messages = st.session_state.messages
    last_number = len(messages) - 1

    for number in range(len(messages)):
        message = messages[number]

        if message["role"] == "user":
            avatar = "🧑‍🎓"
        else:
            avatar = "🎓"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

            # Only the newest bot message shows the suggestion buttons
            if message["role"] == "assistant" and number == last_number:
                ids = message["suggestions"]
                if len(ids) > 0:
                    st.caption("You might also want to know:")
                    columns = st.columns(len(ids))
                    for position in range(len(ids)):
                        topic_id = ids[position]
                        with columns[position]:
                            st.button(
                                get_title(topic_id),
                                key="suggest_" + str(number) + "_" + topic_id,
                                on_click=queue_topic,
                                args=(topic_id,),
                                use_container_width=True,
                            )


# ---------- Main program ----------
def main():
    setup_memory()
    show_header()
    show_sidebar()

    typed_text = st.chat_input("Type your question here...")

    if typed_text:
        # The student typed a question
        add_user_message(typed_text)
        add_bot_message(get_response(typed_text))

    elif st.session_state.queued is not None:
        # The student clicked a topic button
        topic_id = st.session_state.queued
        st.session_state.queued = None
        add_user_message(get_title(topic_id))
        add_bot_message(get_topic_reply(topic_id))

    show_messages()


main()
