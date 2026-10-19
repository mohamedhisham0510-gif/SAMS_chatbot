# SAMS Chatbot: Beginner Guide

Everything here uses only: variables, lists, dictionaries, `if`, `for` loops and functions. No classes, no AI libraries.

You type four files, in this order:

1. `knowledge_base.py` : the data (what the bot knows)
2. `chatbot_engine.py` : the logic (how it picks an answer)
3. `app.py` : the screen (what the student sees)
4. `requirements.txt` : one line, the library to install

## 0. Setup and run

Install Python 3.9 or newer, then in a terminal inside the `sams_chatbot` folder:

```
python -m venv venv
venv\Scripts\activate            (Windows)   or   source venv/bin/activate   (Mac/Linux)
pip install -r requirements.txt
streamlit run app.py
```

- `python -m venv venv` makes a private space for this project's libraries.
- `pip install -r requirements.txt` installs whatever is listed in the file.
- `streamlit run app.py` starts the website on your own computer.

## 1. The big idea (say this to your lecturer first)

The bot does NOT use AI. It does 3 things:

1. **Clean** the student's sentence: lowercase, remove punctuation, split into words.
2. **Score** each topic: every keyword of that topic found in the sentence gives points.
3. **Answer** with the highest-scoring topic. If no topic scores enough, say sorry and suggest topics.

This is called **rule-based keyword matching**. Its answers are fully predictable, because a person wrote every rule and every answer.

Why 3 files?

- `knowledge_base.py` = data only. To add a topic, edit only this file.
- `chatbot_engine.py` = thinking only. It knows nothing about the screen.
- `app.py` = display only. It knows nothing about how matching works.

---

## 2. `requirements.txt`

```
streamlit>=1.30
```

Streamlit is the library that turns Python code into a web page. `>=1.30` means "version 1.30 or newer".

---

## 3. `knowledge_base.py`

This file has no logic. It is only data.

### Python ideas you need

- A **list** is items in square brackets: `["a", "b", "c"]`
- A **dictionary** is labelled boxes in curly brackets: `{"name": "Ali", "age": 20}`. You read a box with `person["name"]`.
- A **string** is text in quotes.
- `#` starts a comment. Python ignores it.
- Text in triple quotes `""" ... """` at the top of a file is a note describing the file.

### What one topic looks like

```python
{
    "id": "attendance_bar",
    "title": "Barred due to attendance",
    "keywords": ["barred", "attendance", "attendance bar"],
    "answer": ( "line one\n" "line two\n" ),
    "follow_ups": ["appeal", "retake"],
},
```

| Box | Meaning |
|---|---|
| `id` | Short unique name the code uses to find the topic. |
| `title` | The nice label printed on buttons. |
| `keywords` | Words or phrases that mean "this topic". |
| `answer` | The reply text. `**bold**` and numbered lists work (Markdown). |
| `follow_ups` | Ids of related topics, shown as buttons under the answer. |

### Notes

- `TOPICS = [ {...}, {...}, ... ]` is a **list of dictionaries**: one dictionary per topic.
- Two strings next to each other inside `( )` are joined into one. That is just a way to split a long answer over several lines.
- `\n` means "new line". `\n\n` leaves a blank line (Markdown needs it for lists).
- `SMALL_TALK` has the same idea for greetings, thanks and goodbye. No title or follow-ups.
- `FALLBACK_MESSAGE` is what the bot says when it does not understand.
- **Every comma matters.** A missing comma between items is the most common error.
- **Replace the sample answers** with the real UNITAR rules before submitting.

---

## 4. `chatbot_engine.py`

### Top of the file

```python
from knowledge_base import TOPICS, SMALL_TALK, FALLBACK_MESSAGE
```

Brings in the data from the other file. Both files must be in the same folder.

```python
MIN_SCORE = 2
WORD_POINTS = 2
PHRASE_WORD_POINTS = 2
```

Three settings, written in capitals because they are fixed numbers.

- `MIN_SCORE`: a topic needs at least 2 points to be chosen. This stops one random word from triggering an answer.
- `WORD_POINTS`: points for one matching word.
- `PHRASE_WORD_POINTS`: points for each word of a matching phrase. A 2-word phrase gives 4 points, so phrases beat single words.

### Function 1: `remove_plural(word)`

```python
def remove_plural(word):
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        word = word[:-1]
    return word
```

- `def` makes a function: a named block of code you can reuse.
- `len(word)` is the number of letters.
- `word.endswith("s")` is True if the word ends with "s".
- `word[:-1]` means "the word without its last letter".
- So `fees` becomes `fee`, and `class` stays `class` (it ends in "ss").
- `return` sends the answer back to whoever called the function.

Why? So "fee" and "fees" both match the same keyword.

### Function 2: `clean_text(text)`

```python
def clean_text(text):
    text = text.lower()
    for symbol in "?!.,;:'\"()-/":
        text = text.replace(symbol, " ")
    words = text.split()
    cleaned_words = []
    for word in words:
        cleaned_words.append(remove_plural(word))
    return cleaned_words
```

Line by line:

1. `text.lower()` makes everything lowercase, so "Barred" equals "barred".
2. The `for` loop goes through each punctuation symbol and `.replace(symbol, " ")` swaps it for a space.
3. `text.split()` cuts the sentence into a list of words.
4. `cleaned_words = []` makes an empty list.
5. The second `for` loop runs `remove_plural` on each word and `.append(...)` adds it to the list.
6. `return` gives back the finished list.

Example: `"I'm BARRED!!"` becomes `["i", "m", "barred"]`.

### Function 3: `phrase_is_in_message(message_words, phrase_words)`

Checks if a phrase like `["attendance", "bar"]` appears in the message **with the words side by side**.

```python
phrase_length = len(phrase_words)
last_start = len(message_words) - phrase_length

for start in range(last_start + 1):
    piece = message_words[start:start + phrase_length]
    if piece == phrase_words:
        return True
return False
```

- `phrase_length` is how many words the phrase has.
- `last_start` is the last position where the phrase could still fit.
- `range(n)` counts 0, 1, 2 ... n-1.
- `message_words[start:start + phrase_length]` is a **slice**: a piece of the list.
- If the piece equals the phrase, we found it, so `return True` and stop.
- If the loop ends with no match, `return False`.

Example: message `["i","am","barred","from","exam"]`, phrase `["barred","from"]`. At `start = 2` the piece is `["barred","from"]`, so it is True.

### Function 4: `score_topic(message_words, topic)`

The heart of the bot.

```python
score = 0
for keyword in topic["keywords"]:
    keyword_words = clean_text(keyword)
    if len(keyword_words) == 1:
        if keyword_words[0] in message_words:
            score = score + WORD_POINTS
    else:
        if phrase_is_in_message(message_words, keyword_words):
            score = score + PHRASE_WORD_POINTS * len(keyword_words)
return score
```

- Start at 0 points.
- Loop over every keyword of the topic.
- Clean the keyword the same way as the message, so they can match.
- **One word keyword:** if it is in the message, add 2 points. (`in` checks if something is inside a list.)
- **Phrase keyword:** if the words appear side by side, add 2 points per word.
- Return the total.

Example, message "i am barred because of low attendance", topic attendance_bar:
`barred` +2, `attendance` +2 = **4 points** (more if a phrase matches too).

### Function 5: `find_best_topic(message_words)`

```python
best_topic = None
best_score = 0
for topic in TOPICS:
    score = score_topic(message_words, topic)
    if score > best_score:
        best_score = score
        best_topic = topic
return best_topic, best_score
```

This is the classic "find the maximum" pattern. Remember the best so far; whenever a topic beats it, replace it. `None` means "nothing yet". It returns two values at once.

### Function 6: `find_small_talk(message_words)`

Loops through the greeting, thanks, goodbye and about entries. If any keyword is in the message, it returns that reply. If nothing matches, it returns `None`.

### Functions 7, 8, 9: lookup helpers

- `get_topic_by_id(topic_id)` loops through `TOPICS` until one has the matching `"id"`, and returns it.
- `get_title(topic_id)` returns that topic's `"title"` (used for button labels).
- `get_topic_reply(topic_id)` returns a small dictionary: the topic's answer text and its follow-up ids.

### Function 10: `get_response(message)`

The only function the screen calls. It returns a dictionary with `"text"` (what the bot says) and `"suggestions"` (topic ids for buttons).

The order of decisions:

1. Clean the message into words. If there are none, ask the student to type something.
2. Find the best topic. If its score is at least `MIN_SCORE`, answer it.
3. Otherwise check for small talk (hello, thanks).
4. Otherwise say sorry (`FALLBACK_MESSAGE`) and suggest popular topics.

Topics are checked before small talk so that "hi, I'm barred" gets the barred answer, not just a greeting.

### Test the engine before building the screen

Make `try_it.py` in the same folder:

```python
from chatbot_engine import get_response

while True:
    message = input("You: ")
    if message == "quit":
        break
    print("SAMS:", get_response(message)["text"])
```

Run `python try_it.py` and chat in the terminal. If the answers are right here, any later bug is in the screen, not the logic.

---

## 5. `app.py`

### The one rule you must understand

Streamlit **re-runs the whole file from the top** every time the student types or clicks. So normal variables are forgotten each time. To remember the chat, we store it in `st.session_state`, which survives between runs.

### Imports and setup

```python
import streamlit as st
from chatbot_engine import get_response, get_topic_reply, get_title
from knowledge_base import TOPICS
st.set_page_config(page_title="SAMS | Student Assistant", page_icon="🎓")
```

- `as st` is a nickname so we type `st.` instead of `streamlit.`.
- `set_page_config` sets the browser tab title and icon. It must be the **first** Streamlit command.

### The design (CSS)

```python
STYLE = """ <style> ... </style> """
st.markdown(STYLE, unsafe_allow_html=True)
```

CSS is the language that controls how a web page looks. We keep it in one text variable and give it to `st.markdown`. `unsafe_allow_html=True` means "let me use real HTML/CSS". (It is only risky with text typed by strangers. This is our own CSS.)

The four colours are navy `#1F3A5F`, teal `#2A9D8F`, light grey-blue `#F4F7FA` and white `#FFFFFF`. What the rules do:

- `.stApp`: page background colour.
- `.header-box`: the banner at the top, with a navy-to-teal gradient and rounded corners (`border-radius`).
- `[data-testid="stChatMessage"]`: makes chat bubbles white and rounded.
- `.stButton > button`: topic buttons become white pills with a teal border.
- `.stButton > button:hover`: when the mouse is over a button, it turns teal.

### `setup_memory()`

```python
if "messages" not in st.session_state:
    st.session_state.messages = [ {...welcome message...} ]
if "queued" not in st.session_state:
    st.session_state.queued = None
```

- The `if ... not in` check means "only do this the first time". Without it the chat would reset on every click.
- `messages` is a list of dictionaries. Each has a `"role"` (`"user"` or `"assistant"`, the exact words Streamlit expects), the `"content"` text, and for bot messages `"suggestions"`.
- `queued` remembers a button that was clicked. `None` means no button is waiting.

### `clear_chat()` and `queue_topic(topic_id)`

- `clear_chat` deletes the saved messages. On the next run `setup_memory` builds a fresh chat.
- `queue_topic` only saves which topic was clicked. It is a **callback**: a function Streamlit runs when a button is clicked, before it re-runs the page.

### `add_user_message(text)` and `add_bot_message(reply)`

Both use `.append(...)` to add one dictionary to the end of the `messages` list. The bot version copies `"text"` and `"suggestions"` from the engine's reply.

### `show_header()`

Draws the banner using a small piece of HTML and the `header-box` class from the CSS.

### `show_sidebar()`

```python
with st.sidebar:
    for topic in TOPICS:
        st.button(topic["title"], key="side_" + topic["id"],
                  on_click=queue_topic, args=(topic["id"],), use_container_width=True)
```

- `with st.sidebar:` puts everything indented into the side panel.
- The `for` loop makes one button per topic automatically. Add a topic to the knowledge base and its button appears with no extra work.
- `key` must be unique for every button, so we join "side_" to the topic id.
- `on_click=queue_topic` says which function to run; `args=(...)` is what to pass into it. (The comma in `(topic["id"],)` is needed so Python reads it as a tuple.)
- `use_container_width=True` stretches the button to full width.
- `st.divider()` draws a line and `st.caption()` prints small grey text.

### `show_messages()`

```python
for number in range(len(messages)):
    message = messages[number]
    if message["role"] == "user":
        avatar = "🧑‍🎓"
    else:
        avatar = "🎓"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        ...
```

- Loop through every saved message in order.
- Pick an avatar depending on who sent it.
- `st.chat_message(...)` draws a chat bubble; the indented lines go inside it.
- `st.markdown(...)` shows the text, turning `**bold**` and lists into formatting.

The suggestion buttons:

```python
if message["role"] == "assistant" and number == last_number:
    ids = message["suggestions"]
    if len(ids) > 0:
        columns = st.columns(len(ids))
        for position in range(len(ids)):
            topic_id = ids[position]
            with columns[position]:
                st.button(get_title(topic_id), key=..., on_click=queue_topic, args=(topic_id,))
```

- Buttons only appear under the **newest** bot message (`number == last_number`), so old messages stay clean.
- `st.columns(n)` splits the width into `n` side-by-side columns.
- Each button goes in its own column, labelled with `get_title(topic_id)`.
- The key joins the message number and topic id, so it is always unique.

### `main()`

```python
setup_memory()
show_header()
show_sidebar()

typed_text = st.chat_input("Type your question here...")

if typed_text:
    add_user_message(typed_text)
    add_bot_message(get_response(typed_text))
elif st.session_state.queued is not None:
    topic_id = st.session_state.queued
    st.session_state.queued = None
    add_user_message(get_title(topic_id))
    add_bot_message(get_topic_reply(topic_id))

show_messages()
```

Read it in order:

1. Make sure the chat memory exists, then draw the banner and sidebar.
2. `st.chat_input` draws the text box at the bottom and returns what the student typed (or nothing).
3. **If they typed:** save their message, get the engine's reply, save the reply.
4. **Else if a button was clicked:** read which topic, set `queued` back to `None` (so it is not processed twice), save the topic title as the student's message, then save that topic's reply.
5. `show_messages()` runs **last**, so it draws everything including the newest messages.
6. The very last line, `main()`, starts it all. Defining a function does nothing until you call it.

---

## 6. Questions your lecturer might ask (with simple answers)

**Q: Is this AI?**
No. It is a rule-based system. It follows rules a person wrote: if a keyword is in the message, give points to its topic. It cannot learn or understand meaning.

**Q: Why not use ChatGPT or machine learning?**
Cost (no API fees), privacy (nothing is sent to outside companies), and predictability (it can only say what we wrote, so it cannot give wrong or invented university rules).

**Q: How does it choose an answer?**
It cleans the message into words, adds up points for each keyword found, and picks the topic with the highest score. It needs at least `MIN_SCORE` (2) points, otherwise it says it doesn't understand.

**Q: Why do phrases give more points than words?**
A phrase like "attendance bar" is more specific than the word "attendance", so it is stronger evidence.

**Q: What is `MIN_SCORE` for?**
A safety limit, so a single weak match doesn't trigger a wrong answer.

**Q: What if the student makes a spelling mistake?**
The bot will not match that word. It falls back to suggesting topics. (Extension: add typo tolerance with Python's `difflib`.)

**Q: What if the question is not about any topic?**
It gives the fallback message and suggests the most popular topics, so the student is never stuck.

**Q: Why three separate files?**
Data, logic and display are kept apart. A new topic needs only a change in `knowledge_base.py`. Anyone can test the logic without the website.

**Q: Why is `st.session_state` needed?**
Streamlit re-runs the file on every click. Session state is the only place that remembers the chat between runs.

**Q: What are the limitations?**
It only knows what is written in the knowledge base. It cannot understand meaning, remember earlier questions, or handle very different wording. The answers also need to be kept up to date manually.

**Q: How did you test it?**
I typed sample questions for each topic, plus greetings, an empty message, and an unrelated question, and checked that each gave the expected reply. (Make a table of these for your report.)

**Q: How would you improve it?**
Typo tolerance, remembering the last topic, a "was this helpful?" button, logging unanswered questions to find missing topics, and a Bahasa Malaysia keyword list.

---

## 7. Common errors

| Error | Fix |
|---|---|
| `ModuleNotFoundError: streamlit` | Activate the venv, then run `pip install -r requirements.txt`. |
| `ModuleNotFoundError: knowledge_base` | You are in the wrong folder. `cd sams_chatbot` first. |
| `SyntaxError` in the knowledge base | A missing comma or bracket between topics. |
| `StreamlitDuplicateElementKey` | Two buttons have the same `key`. |
| `set_page_config` error | It must be the first Streamlit command. |
| Bot always says "not sure" | Add more keywords to that topic. Test the engine with `try_it.py`. |
| `KeyError: 'messages'` | You cleared the chat but `setup_memory()` was not called first in `main()`. |

## 8. Ideas to extend it

1. **Add a topic:** copy one dictionary in `TOPICS`, change its `id`, `title`, `keywords`, `answer`, `follow_ups`.
2. **Change `MIN_SCORE`** to 3 and see which test questions stop working. Write that in your report as testing.
3. **Log unanswered questions** to a text file inside the fallback branch of `get_response`.
