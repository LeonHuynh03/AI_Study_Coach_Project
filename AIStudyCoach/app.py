
import streamlit as st
import random

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="StudyFlow AI",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "page": "Dashboard",
    "attempt": 0,
    "quiz_questions": [],
    "quiz_answers": {},
    "quiz_submitted": False,
    "quiz_score": 0,
    "previous_question_ids": [],
    "quiz_completed": 0,
    "study_sessions": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# QUESTION BANK
# =========================================================
question_bank = [
    {
        "id": 1,
        "topic": "Sets",
        "question": "What does the symbol ∈ mean?",
        "options": ["Is a subset of", "Is an element of", "Is equal to", "Is not equal to"],
        "answer": "Is an element of",
        "explanation": "The symbol ∈ means an element belongs to a set."
    },
    {
        "id": 2,
        "topic": "Sets",
        "question": "Which notation represents the empty set?",
        "options": ["{0}", "{ }", "{1}", "{0, 1}"],
        "answer": "{ }",
        "explanation": "The empty set contains no elements. {0} contains one element: zero."
    },
    {
        "id": 3,
        "topic": "Sets",
        "question": "If A = {1, 2, 3}, which statement is true?",
        "options": ["4 ∈ A", "2 ∈ A", "5 ∈ A", "0 ∈ A"],
        "answer": "2 ∈ A",
        "explanation": "The number 2 is an element of set A."
    },
    {
        "id": 4,
        "topic": "Sets",
        "question": "What does A ⊆ B mean?",
        "options": [
            "A is a subset of B",
            "A is not in B",
            "A equals zero",
            "B is empty"
        ],
        "answer": "A is a subset of B",
        "explanation": "A ⊆ B means every element in A is also contained in B."
    },
    {
        "id": 5,
        "topic": "Sets",
        "question": "What is the cardinality of {a, b, c, d}?",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "explanation": "Cardinality is the number of elements in a set. This set has four elements."
    },
    {
        "id": 6,
        "topic": "Counting",
        "question": "A restaurant offers 3 appetizers and 4 entrees. How many appetizer-entree combinations are possible?",
        "options": ["7", "12", "16", "24"],
        "answer": "12",
        "explanation": "Use the multiplication rule: 3 × 4 = 12 combinations."
    },
    {
        "id": 7,
        "topic": "Counting",
        "question": "A student has 5 shirts and 3 pants. How many different outfits can they make?",
        "options": ["8", "10", "15", "20"],
        "answer": "15",
        "explanation": "Multiply the choices: 5 × 3 = 15 outfits."
    },
    {
        "id": 8,
        "topic": "Counting",
        "question": "How many ways can 3 different books be arranged on a shelf?",
        "options": ["3", "6", "9", "12"],
        "answer": "6",
        "explanation": "There are 3! = 3 × 2 × 1 = 6 arrangements."
    },
    {
        "id": 9,
        "topic": "Permutations",
        "question": "Which situation uses a permutation?",
        "options": [
            "Selecting 3 students for a team",
            "Choosing 2 pizza toppings",
            "Ranking 1st, 2nd, and 3rd place",
            "Choosing 5 cards"
        ],
        "answer": "Ranking 1st, 2nd, and 3rd place",
        "explanation": "Permutations are used when order matters. Different rankings create different outcomes."
    },
    {
        "id": 10,
        "topic": "Combinations",
        "question": "Which situation uses a combination?",
        "options": [
            "Assigning a president and vice president",
            "Arranging books in a row",
            "Selecting 3 people for a committee",
            "Creating a 4-digit code"
        ],
        "answer": "Selecting 3 people for a committee",
        "explanation": "A committee is a selection where order does not matter."
    },
    {
        "id": 11,
        "topic": "Combinations",
        "question": "How many ways can 2 people be chosen from 5 people?",
        "options": ["5", "10", "20", "25"],
        "answer": "10",
        "explanation": "Use C(5,2) = 5! / (2!3!) = 10."
    },
    {
        "id": 12,
        "topic": "Permutations",
        "question": "How many ways can 2 different people be selected and assigned President and Vice President from 5 people?",
        "options": ["10", "15", "20", "25"],
        "answer": "20",
        "explanation": "Order matters because the positions are different. P(5,2) = 5 × 4 = 20."
    },
    {
        "id": 13,
        "topic": "Pigeonhole Principle",
        "question": "If 13 people are in a room, what must be true about their birth months?",
        "options": [
            "Everyone has a different month",
            "At least 2 share a birth month",
            "Exactly 3 share a birth month",
            "No one shares a birth month"
        ],
        "answer": "At least 2 share a birth month",
        "explanation": "There are only 12 months. With 13 people, at least two must share a month."
    },
    {
        "id": 14,
        "topic": "Inclusion-Exclusion",
        "question": "If |A| = 10, |B| = 8, and |A ∩ B| = 3, what is |A ∪ B|?",
        "options": ["15", "18", "21", "24"],
        "answer": "15",
        "explanation": "|A ∪ B| = |A| + |B| − |A ∩ B| = 10 + 8 − 3 = 15."
    },
    {
        "id": 15,
        "topic": "Counting",
        "question": "How many different 3-digit codes can be made using digits 1–5 if repetition is allowed?",
        "options": ["15", "60", "125", "243"],
        "answer": "125",
        "explanation": "Each position has 5 choices. 5 × 5 × 5 = 125."
    },
]


# =========================================================
# QUIZ FUNCTIONS
# =========================================================
def create_new_quiz():
    previous_ids = set(st.session_state.previous_question_ids)

    # Prefer questions not used in the previous attempt.
    fresh_questions = [
        q for q in question_bank
        if q["id"] not in previous_ids
    ]

    # If the fresh pool is too small, use the whole bank.
    if len(fresh_questions) < 5:
        fresh_questions = question_bank.copy()

    selected_questions = random.sample(fresh_questions, 5)

    # Shuffle choices separately for each selected question.
    quiz = []

    for q in selected_questions:
        new_q = q.copy()
        new_q["options"] = q["options"].copy()
        random.shuffle(new_q["options"])
        quiz.append(new_q)

    st.session_state.attempt += 1
    st.session_state.quiz_questions = quiz
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.quiz_score = 0
    st.session_state.quiz_index = 0
    st.session_state.previous_question_ids = [q["id"] for q in quiz]


def go_to_page(page):
    st.session_state.page = page


def submit_quiz():
    score = 0

    for i, q in enumerate(st.session_state.quiz_questions):
        if st.session_state.quiz_answers.get(i) == q["answer"]:
            score += 1

    st.session_state.quiz_score = score
    st.session_state.quiz_submitted = True
    st.session_state.quiz_completed += 1


# Create first quiz on initial app load.
if not st.session_state.quiz_questions:
    create_new_quiz()


# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

.stApp {
    background: #F5F6FA;
    color: #25263D;
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1220px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #25263D !important;
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.4px;
}

p {
    color: #70768B;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E4E6EF;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.8rem;
}

/* HERO */
.hero {
    background: linear-gradient(125deg, #EAE7FF, #F4F1FF 55%, #EAF3FF);
    border: 1px solid #DDD9FB;
    border-radius: 24px;
    padding: 34px 36px;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 32px;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    color: #252540;
    line-height: 1.25;
}

.hero-subtitle {
    font-size: 15px;
    color: #747990;
    margin-top: 10px;
}

/* SECTION */
.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #282841;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #888DA0;
    font-size: 14px;
    margin-bottom: 20px;
}

/* METRICS */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E4E6EF;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(28, 31, 70, 0.035);
}

[data-testid="stMetricLabel"] {
    color: #7F8499 !important;
}

[data-testid="stMetricValue"] {
    color: #292943 !important;
    font-weight: 800 !important;
}

/* CARDS */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #E2E5EF;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(28, 31, 70, 0.035);
}

/* BUTTONS */
.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 700;
    border: 1px solid #DDE0EC;
    transition: 0.15s ease;
}

.stButton > button[kind="primary"] {
    background: #6B5CE7;
    color: #FFFFFF;
    border: 1px solid #6B5CE7;
}

.stButton > button[kind="primary"]:hover {
    background: #5544C9;
    color: #FFFFFF;
    border-color: #5544C9;
}

/* INPUTS */
.stTextInput input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #DDE1EC !important;
    background: #FFFFFF !important;
}

/* QUIZ CHOICES */
div[role="radiogroup"] {
    gap: 8px;
}

/* FOOTER */
.footer {
    text-align: center;
    font-size: 13px;
    color: #A0A5B5;
    padding-top: 15px;
}

/* SMALL TEXT */
.eyebrow {
    color: #7E83A0;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 20px;">
        <div style="font-size:32px;">🎓</div>
        <div style="font-size:23px;font-weight:800;color:#25263D;">
            StudyFlow <span style="color:#6B5CE7;">AI</span>
        </div>
        <div style="color:#9297A8;font-size:13px;">
            Your personal learning companion
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<div class='eyebrow'>YOUR WORKSPACE</div>", unsafe_allow_html=True)

    st.radio(
        "Navigation",
        ["Dashboard", "Study Room", "Practice Quiz"],
        key="page",
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### ✨ Study smarter")

    st.info(
        "Don't just reread. Close your notes and try to recall "
        "the idea from memory."
    )

    st.divider()
    st.caption("STUDYFLOW AI · VERSION 2.0")


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">Your learning, in flow. ✨</div>
    <div class="hero-subtitle">
        Understand concepts, organize your notes, and practice
        with a smarter study workflow.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================
if st.session_state.page == "Dashboard":

    st.markdown("## Dashboard")
    st.caption("A little progress every day adds up.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Study Sessions", st.session_state.study_sessions)

    with c2:
        st.metric("Quizzes Completed", st.session_state.quiz_completed)

    with c3:
        st.metric("Questions in Bank", len(question_bank))

    st.markdown("")

    st.markdown("<div class='section-title'>Jump back in</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Choose what you want to work on.</div>", unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        with st.container(border=True):
            st.markdown("### 📚 Study Room")
            st.write("Transform your class notes into understandable learning material.")
            st.button(
                "Open Study Room",
                type="primary",
                use_container_width=True,
                on_click=go_to_page,
                args=("Study Room",),
                key="dash_study"
            )

    with b:
        with st.container(border=True):
            st.markdown("### 🧠 Practice Quiz")
            st.write("Challenge your memory with a new set of questions.")
            st.button(
                "Start Practice",
                type="primary",
                use_container_width=True,
                on_click=go_to_page,
                args=("Practice Quiz",),
                key="dash_quiz"
            )

    st.markdown("")
    st.markdown("<div class='section-title'>Your study toolkit</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Tools to make studying more effective.</div>", unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)

    with t1:
        with st.container(border=True):
            st.markdown("### 💡 Understand")
            st.write("Break down complicated topics into simpler explanations.")

    with t2:
        with st.container(border=True):
            st.markdown("### 📝 Organize")
            st.write("Convert notes into structured study guides.")

    with t3:
        with st.container(border=True):
            st.markdown("### 🎯 Remember")
            st.write("Practice active recall and strengthen your memory.")


# =========================================================
# STUDY ROOM
# =========================================================
elif st.session_state.page == "Study Room":

    st.markdown("## 📚 Study Room")
    st.caption("Create a focused study session.")

    with st.container(border=True):
        topic = st.text_input(
            "Topic",
            placeholder="e.g. Permutations, Recursion, Java Inheritance"
        )

        notes = st.text_area(
            "Paste your class notes",
            height=220,
            placeholder="Paste notes, lecture content, or textbook information here..."
        )

        mode = st.selectbox(
            "What do you want to create?",
            ["Explain Topic", "Create Study Guide"]
        )

        generate = st.button("Generate Study Material", type="primary", use_container_width=True)

    if generate:
        if not topic.strip() or not notes.strip():
            st.warning("Please enter a topic and some notes.")

        else:
            st.session_state.study_sessions += 1

            st.markdown("---")
            st.markdown(f"## {topic}")

            if mode == "Explain Topic":
                with st.container(border=True):
                    st.markdown("### Simple explanation")
                    st.write(
                        "Start by identifying the main idea. Break the topic into "
                        "smaller parts and connect each definition to an example."
                    )

                    st.markdown("### Your notes")
                    st.write(notes)

                    st.markdown("### Study steps")
                    st.markdown("""
                    1. Read and understand the main concept.
                    2. Explain it in your own words.
                    3. Create your own example.
                    4. Solve a practice problem without looking.
                    """)

            else:
                note_lines = [
                    line.strip() for line in notes.splitlines()
                    if line.strip()
                ]

                with st.container(border=True):
                    st.markdown("### Key points")
                    for line in note_lines:
                        st.markdown(f"- {line}")

                    st.markdown("### Self-check")
                    st.markdown("""
                    - Can I explain the key idea?
                    - Do I remember the definitions?
                    - Can I create an example?
                    - Can I solve a question on my own?
                    """)

            st.caption("Demo Mode · Not yet powered by a live AI model.")


# =========================================================
# PRACTICE QUIZ
# =========================================================
elif st.session_state.page == "Practice Quiz":

    st.markdown("## 🧠 Practice Quiz")
    st.caption("Each attempt generates a fresh question set.")

    current_quiz = st.session_state.quiz_questions

    # ---------------- RESULTS ----------------
    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score
        total = len(current_quiz)
        percentage = int(score / total * 100)

        with st.container(border=True):
            st.markdown("## Your Results")
            st.metric("Score", f"{score} / {total}")
            st.progress(score / total)

            st.markdown(f"### {percentage}%")

            if score == total:
                st.success("Perfect score! You got every question right.")
            elif score >= 3:
                st.success("Nice work! Review the questions you missed.")
            else:
                st.info("Keep practicing. Learning takes repetition.")

        st.markdown("## Answer Review")

        for i, q in enumerate(current_quiz):
            selected = st.session_state.quiz_answers.get(i)

            with st.container(border=True):
                st.markdown(f"**Question {i + 1} · {q['topic']}**")
                st.write(q["question"])

                if selected == q["answer"]:
                    st.success(f"Correct answer: {selected}")
                else:
                    st.error(f"Your answer: {selected or 'Not answered'}")
                    st.markdown(f"**Correct answer:** {q['answer']}")

                st.info(q["explanation"])

        st.button(
            "✨ Generate a New Quiz",
            type="primary",
            use_container_width=True,
            on_click=create_new_quiz,
            key="retake_quiz"
        )

    # ---------------- QUESTION ----------------
    else:

        index = st.session_state.quiz_index
        q = current_quiz[index]

        st.progress((index + 1) / len(current_quiz))

        st.markdown(
            f"<div class='eyebrow'>QUESTION {index + 1} OF {len(current_quiz)} · {q['topic'].upper()}</div>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(f"### {q['question']}")

            # Unique radio key for every question and every attempt.
            radio_key = f"quiz_{st.session_state.attempt}_{index}"

            saved_answer = st.session_state.quiz_answers.get(index)

            selected = st.radio(
                "Choose your answer",
                q["options"],
                index=q["options"].index(saved_answer) if saved_answer in q["options"] else None,
                key=radio_key,
                label_visibility="collapsed"
            )

            if selected is not None:
                st.session_state.quiz_answers[index] = selected

            st.markdown("")

            left, right = st.columns(2)

            with left:
                if index > 0:
                    st.button(
                        "← Previous",
                        use_container_width=True,
                        on_click=lambda: st.session_state.update(
                            quiz_index=st.session_state.quiz_index - 1
                        ),
                        key=f"back_{st.session_state.attempt}_{index}"
                    )

            with right:
                if index < len(current_quiz) - 1:
                    st.button(
                        "Next Question →",
                        type="primary",
                        use_container_width=True,
                        on_click=lambda: st.session_state.update(
                            quiz_index=st.session_state.quiz_index + 1
                        ),
                        key=f"next_{st.session_state.attempt}_{index}"
                    )
                else:
                    st.button(
                        "Submit Quiz",
                        type="primary",
                        use_container_width=True,
                        on_click=submit_quiz,
                        key=f"submit_{st.session_state.attempt}"
                    )

        answered = len(st.session_state.quiz_answers)

        st.caption(f"{answered} of {len(current_quiz)} questions answered")


# =========================================================
# FOOTER
# =========================================================
st.divider()

st.markdown("""
<div class="footer">
    StudyFlow AI · Built to help you learn better
</div>
""", unsafe_allow_html=True)
