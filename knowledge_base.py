"""
knowledge_base.py
-----------------
All the chatbot's "knowledge" lives here as plain Python data.
The engine reads this list; it never has to be edited to add a new topic.

NOTE: The answers below are general sample guidance. Before you submit,
replace the details (percentages, offices, deadlines) with the official
UNITAR rules so every statement in your report is verifiable.
"""

# Each topic is a dictionary with these keys:
#   id        - a short unique name
#   title     - label shown on buttons and in suggestions
#   keywords  - words/phrases that point to this topic
#               (multi-word phrases score higher than single words)
#   answer    - what the bot replies (Markdown is allowed)
#   follow_ups- ids of related topics offered as quick buttons

TOPICS = [
    {
        "id": "attendance_bar",
        "title": "Barred due to attendance",
        "keywords": [
            "barred", "bar", "attendance", "absent", "absence", "banned",
            "attendance bar", "barred from exam", "low attendance",
            "not allowed exam", "cannot sit exam", "miss class",
        ],
        "answer": (
            "**If you are barred because of low attendance, do this:**\n\n"
            "1. **Check your attendance record** on the student portal and confirm the exact percentage.\n"
            "2. **Collect proof** for any absence that was valid (medical certificate, official letter).\n"
            "3. **Meet your lecturer or academic advisor** as early as possible and explain your situation.\n"
            "4. **Submit an appeal** to the Faculty / Academic Office with your proof, before the appeal deadline.\n"
            "5. **Wait for the decision.** If the appeal fails, you will normally need to retake the subject.\n\n"
            "_Tip: appeals made early are handled more smoothly than last-minute ones._"
        ),
        "follow_ups": ["appeal", "retake", "medical_leave"],
    },
    {
        "id": "appeal",
        "title": "How to submit an appeal",
        "keywords": [
            "appeal", "appeals", "reconsider", "petition", "objection",
            "submit appeal", "write appeal", "appeal letter",
        ],
        "answer": (
            "**How to submit an appeal:**\n\n"
            "1. Get the **appeal form** from the Academic Office or the student portal.\n"
            "2. Write a short, honest explanation of what happened.\n"
            "3. Attach **supporting documents** (medical certificate, letters, screenshots).\n"
            "4. Get any required signature (e.g. academic advisor).\n"
            "5. Submit **before the deadline** and keep a copy or receipt.\n\n"
            "_Late appeals are often rejected, so do not wait._"
        ),
        "follow_ups": ["attendance_bar", "exam_deferment", "result_review"],
    },
    {
        "id": "retake",
        "title": "Retaking or repeating a subject",
        "keywords": [
            "retake", "repeat", "resit", "re-sit", "failed", "fail",
            "repeat subject", "retake subject", "redo subject", "retake exam",
        ],
        "answer": (
            "**To retake or repeat a subject:**\n\n"
            "1. Confirm in your academic record that the subject needs to be repeated.\n"
            "2. **Register for it again** in the next available semester.\n"
            "3. Check whether an **extra retake fee** applies and pay it by the due date.\n"
            "4. Speak to your advisor so the subject fits your timetable and graduation plan.\n\n"
            "_Repeating a subject can delay graduation, so plan your remaining semesters early._"
        ),
        "follow_ups": ["add_drop", "fees", "graduation"],
    },
    {
        "id": "add_drop",
        "title": "Adding or dropping a subject",
        "keywords": [
            "add", "drop", "withdraw", "withdrawal", "add subject",
            "drop subject", "add drop", "change subject", "register subject",
            "course registration", "register course", "registration",
        ],
        "answer": (
            "**Adding or dropping a subject:**\n\n"
            "1. Find the **add/drop period** in the academic calendar. It is short.\n"
            "2. Log in to the student portal and open course registration.\n"
            "3. Choose the subject to add or drop and confirm.\n"
            "4. Check your updated timetable and fee statement.\n\n"
            "_Dropping after the period ends may appear on your transcript as a withdrawal._"
        ),
        "follow_ups": ["timetable", "fees", "retake"],
    },
    {
        "id": "exam_deferment",
        "title": "Deferring or missing an exam",
        "keywords": [
            "defer", "deferment", "postpone", "missed exam", "miss exam",
            "sick during exam", "cannot attend exam", "exam deferment",
            "defer exam", "special exam", "emergency exam",
        ],
        "answer": (
            "**If you cannot sit for an exam:**\n\n"
            "1. **Inform the Academic Office immediately**, ideally before the exam.\n"
            "2. Provide **valid proof** (medical certificate, official letter).\n"
            "3. Fill in the **exam deferment form** and submit it within the allowed days.\n"
            "4. Wait for approval and the date of the deferred exam.\n\n"
            "_Without approval, a missed exam is usually graded as zero._"
        ),
        "follow_ups": ["medical_leave", "appeal", "result_review"],
    },
    {
        "id": "result_review",
        "title": "Disagree with my result",
        "keywords": [
            "result", "results", "grade", "grades", "marks", "gpa", "cgpa",
            "recheck", "remark", "re-mark", "review result", "wrong grade",
            "result review", "check result", "exam result",
        ],
        "answer": (
            "**If you think your result is wrong:**\n\n"
            "1. Check the **official result slip** on the student portal.\n"
            "2. Apply for a **result review / recheck** within the stated period.\n"
            "3. Pay the review fee if one applies.\n"
            "4. Wait for the outcome. The grade may stay the same, go up, or occasionally go down.\n\n"
            "_Ask your lecturer first, as a small recording mistake can be fixed quickly._"
        ),
        "follow_ups": ["appeal", "retake"],
    },
    {
        "id": "medical_leave",
        "title": "Medical leave and sickness",
        "keywords": [
            "sick", "ill", "illness", "medical", "mc", "doctor", "hospital",
            "medical leave", "medical certificate", "unwell", "not feeling well",
        ],
        "answer": (
            "**If you are sick or on medical leave:**\n\n"
            "1. See a doctor and **get a medical certificate (MC)**.\n"
            "2. **Inform your lecturers** and the Academic Office as soon as you can.\n"
            "3. **Submit the MC** through the required channel within the allowed days.\n"
            "4. Ask about **make-up work or exams** for what you missed.\n\n"
            "_Your health comes first. Do not hide a serious problem._"
        ),
        "follow_ups": ["attendance_bar", "exam_deferment"],
    },
    {
        "id": "fees",
        "title": "Fees and payment",
        "keywords": [
            "fee", "fees", "pay", "payment", "tuition", "installment",
            "instalment", "bill", "invoice", "outstanding", "owe",
            "pay fees", "payment plan", "fee statement", "cannot pay",
        ],
        "answer": (
            "**About fees and payment:**\n\n"
            "1. Check your **fee statement** on the student portal.\n"
            "2. Pay through the **approved payment channels** before the due date.\n"
            "3. If you struggle to pay, **contact the Finance Office early** to ask about an instalment plan.\n"
            "4. Keep your **payment receipt**.\n\n"
            "_Unpaid fees can block exam slips or results, so do not ignore them._"
        ),
        "follow_ups": ["scholarship", "retake", "add_drop"],
    },
    {
        "id": "scholarship",
        "title": "Scholarships and financial aid",
        "keywords": [
            "scholarship", "scholarships", "loan", "ptptn", "financial aid",
            "bursary", "funding", "sponsor", "financial help", "study loan",
        ],
        "answer": (
            "**Scholarships and financial aid:**\n\n"
            "1. Ask the **Student Affairs / Finance Office** which schemes are open now.\n"
            "2. Check the **eligibility rules** (CGPA, income, programme).\n"
            "3. Prepare your documents: ID, results, income proof, offer letter.\n"
            "4. Apply **before the closing date**.\n\n"
            "_Some aid requires you to keep a minimum CGPA every semester._"
        ),
        "follow_ups": ["fees", "result_review"],
    },
    {
        "id": "timetable",
        "title": "Timetable and class schedule",
        "keywords": [
            "timetable", "schedule", "class time", "classes", "clash",
            "class clash", "lecture time", "when is class", "my timetable",
        ],
        "answer": (
            "**Finding or fixing your timetable:**\n\n"
            "1. Open the **student portal** and go to your timetable.\n"
            "2. If two classes **clash**, contact the Academic Office to change your section.\n"
            "3. Check for **online class links** or room changes in your announcements.\n\n"
            "_Timetables can change at the start of the semester, so recheck weekly._"
        ),
        "follow_ups": ["add_drop", "student_id"],
    },
    {
        "id": "student_id",
        "title": "Student ID card and portal login",
        "keywords": [
            "id card", "student card", "lost card", "matric", "matric number",
            "password", "login", "log in", "portal", "forgot password",
            "cannot login", "reset password", "student id",
        ],
        "answer": (
            "**Student ID or portal problems:**\n\n"
            "1. **Lost ID card:** report it and request a replacement from the Student Services counter (a fee may apply).\n"
            "2. **Forgot password:** use the *Forgot password* link, or ask the IT Helpdesk to reset it.\n"
            "3. Bring a **photo ID** so staff can verify who you are.\n\n"
            "_Never share your password with anyone._"
        ),
        "follow_ups": ["contact", "timetable"],
    },
    {
        "id": "change_programme",
        "title": "Changing or deferring my programme",
        "keywords": [
            "change programme", "change program", "change course",
            "transfer", "switch", "defer study", "quit", "leave university",
            "withdraw from university", "stop study", "take a break",
            "change major", "change programme",
        ],
        "answer": (
            "**Changing programme or taking a break:**\n\n"
            "1. Talk to your **academic advisor** about your reasons and options.\n"
            "2. Get the **correct form** from the Academic Office (change of programme or study deferment).\n"
            "3. Check how your **completed credits** will be carried over.\n"
            "4. Submit the form with approvals before the deadline.\n\n"
            "_Fees and graduation timeline can change, so confirm both before you decide._"
        ),
        "follow_ups": ["fees", "graduation"],
    },
    {
        "id": "graduation",
        "title": "Graduation requirements",
        "keywords": [
            "graduate", "graduation", "convocation", "degree", "transcript",
            "certificate", "credit hours", "complete degree", "graduation requirements",
            "final semester",
        ],
        "answer": (
            "**Preparing to graduate:**\n\n"
            "1. Check your **programme structure** to see all required credits are done.\n"
            "2. Clear **outstanding fees** and library items.\n"
            "3. Apply for **graduation** within the announced window.\n"
            "4. Request your **transcript and certificate** from the Academic Office.\n\n"
            "_Failed or repeated subjects may push your graduation to a later semester._"
        ),
        "follow_ups": ["retake", "fees"],
    },
    {
        "id": "contact",
        "title": "Who to contact",
        "keywords": [
            "contact", "office", "helpdesk", "help desk", "email", "phone",
            "who to ask", "who do i ask", "counter", "advisor", "adviser",
            "counsellor", "counselor", "support",
        ],
        "answer": (
            "**Who to contact:**\n\n"
            "- **Academic matters** (attendance, exams, appeals): Academic Office / your advisor\n"
            "- **Fees and aid:** Finance Office\n"
            "- **Login and Wi-Fi:** IT Helpdesk\n"
            "- **ID card, welfare, wellbeing:** Student Services / Student Affairs\n\n"
            "_Add the real office names, emails and phone numbers here once you verify them._"
        ),
        "follow_ups": ["attendance_bar", "fees", "student_id"],
    },
]

# Small talk is kept separate. These have no follow-ups and short replies.
SMALL_TALK = [
    {
        "id": "greeting",
        "keywords": ["hi", "hello", "hey", "hai", "good morning", "good afternoon",
                     "good evening", "salam", "assalamualaikum"],
        "answer": (
            "Hello! I'm **SAMS**, the Student Assistant. "
            "Ask me what to do about attendance bars, appeals, fees, exams and more."
        ),
    },
    {
        "id": "thanks",
        "keywords": ["thanks", "thank you", "thank", "tq", "terima kasih", "cheers"],
        "answer": "You're welcome! Ask me anything else about university processes.",
    },
    {
        "id": "bye",
        "keywords": ["bye", "goodbye", "see you", "later"],
        "answer": "Goodbye, and all the best with your studies!",
    },
    {
        "id": "about",
        "keywords": ["who are you", "what are you", "what can you do", "help",
                     "what do you do", "your name"],
        "answer": (
            "I'm **SAMS**, a rule-based assistant that guides students through "
            "university processes step by step. I match keywords in your question "
            "to a knowledge base. I don't use any AI model or external service."
        ),
    },
]

FALLBACK_MESSAGE = (
    "I'm not sure I understood that. Try rephrasing, or pick one of these topics:"
)
