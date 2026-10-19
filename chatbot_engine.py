"""
chatbot_engine.py
-----------------
The "brain" of SAMS. It has NO screen code and NO AI model.

How it works in 3 steps:
  1. Clean the student's message (lowercase, no punctuation, split into words).
  2. Give every topic points for each of its keywords found in the message.
  3. Reply with the topic that has the most points.
"""

from knowledge_base import TOPICS, SMALL_TALK, FALLBACK_MESSAGE

# ---------- Settings (change these to tune the bot) ----------
MIN_SCORE = 2         # a topic needs at least this many points to be chosen
WORD_POINTS = 2       # points for one matching word, e.g. "attendance"
PHRASE_WORD_POINTS = 2  # points per word for a matching phrase, e.g. "attendance bar"


# ---------- Step 1: clean the message ----------
def remove_plural(word):
    """Turn 'fees' into 'fee' so singular and plural match."""
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        word = word[:-1]          # cut off the last letter
    return word


def clean_text(text):
    """Turn 'I'm BARRED!!' into the list ['i', 'm', 'barred']."""
    text = text.lower()

    # Replace punctuation with a space
    for symbol in "?!.,;:'\"()-/":
        text = text.replace(symbol, " ")

    words = text.split()          # cut the sentence into words

    cleaned_words = []
    for word in words:
        cleaned_words.append(remove_plural(word))
    return cleaned_words


# ---------- Step 2: score the topics ----------
def phrase_is_in_message(message_words, phrase_words):
    """Check if the phrase appears in the message, words side by side."""
    phrase_length = len(phrase_words)
    last_start = len(message_words) - phrase_length

    for start in range(last_start + 1):
        piece = message_words[start:start + phrase_length]
        if piece == phrase_words:
            return True
    return False


def score_topic(message_words, topic):
    """Count the points one topic earns for this message."""
    score = 0

    for keyword in topic["keywords"]:
        keyword_words = clean_text(keyword)

        if len(keyword_words) == 1:
            # A single word keyword
            if keyword_words[0] in message_words:
                score = score + WORD_POINTS
        else:
            # A keyword made of several words (a phrase)
            if phrase_is_in_message(message_words, keyword_words):
                score = score + PHRASE_WORD_POINTS * len(keyword_words)

    return score


def find_best_topic(message_words):
    """Return the topic with the highest score, and that score."""
    best_topic = None
    best_score = 0

    for topic in TOPICS:
        score = score_topic(message_words, topic)
        if score > best_score:
            best_score = score
            best_topic = topic

    return best_topic, best_score


def find_small_talk(message_words):
    """Look for greetings, thanks, etc. Returns the reply text or None."""
    for item in SMALL_TALK:
        for keyword in item["keywords"]:
            keyword_words = clean_text(keyword)
            if phrase_is_in_message(message_words, keyword_words):
                return item["answer"]
    return None


# ---------- Step 3: build the reply ----------
def get_topic_by_id(topic_id):
    """Find a topic using its id."""
    for topic in TOPICS:
        if topic["id"] == topic_id:
            return topic
    return None


def get_title(topic_id):
    """Get the button label of a topic."""
    return get_topic_by_id(topic_id)["title"]


def get_topic_reply(topic_id):
    """The reply for a chosen topic (used by the buttons too)."""
    topic = get_topic_by_id(topic_id)
    return {
        "text": topic["answer"],
        "suggestions": topic["follow_ups"],
    }


def get_response(message):
    """The ONE function the screen calls. Returns a dictionary:
         "text"        -> what the bot says
         "suggestions" -> list of topic ids to show as buttons
    """
    message_words = clean_text(message)

    # Nothing typed
    if len(message_words) == 0:
        return {
            "text": "Please type your question and I'll help.",
            "suggestions": ["attendance_bar", "appeal", "fees", "exam_deferment"],
        }

    # 1) Does the message match a topic well enough?
    best_topic, best_score = find_best_topic(message_words)
    if best_topic is not None and best_score >= MIN_SCORE:
        return get_topic_reply(best_topic["id"])

    # 2) Is it a greeting or thanks?
    small_talk_reply = find_small_talk(message_words)
    if small_talk_reply is not None:
        return {
            "text": small_talk_reply,
            "suggestions": ["attendance_bar", "appeal", "fees", "exam_deferment"],
        }

    # 3) Not understood: say sorry and suggest popular topics
    return {
        "text": FALLBACK_MESSAGE,
        "suggestions": ["attendance_bar", "appeal", "fees"],
    }
