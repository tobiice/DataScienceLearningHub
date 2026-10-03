import html
import math
import urllib.parse

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Science Learning Hub", page_icon="🧠", layout="wide")


def spring_easing(points=48, damping=5.0, cycles=1.5):
    """A CSS linear() easing that overshoots, wobbles a little, then settles (a spring)."""
    values = []
    for i in range(points + 1):
        t = i / points
        values.append(f"{1 - math.exp(-damping * t) * math.cos(2 * math.pi * cycles * t):.3f}")
    values[-1] = "1"
    return "linear(" + ", ".join(values) + ")"


def make_background_uri(width=1200, height=700):
    """Draw a data-science scene (scatter plot, histogram, network graph, formulas) as an inline SVG."""
    rng = np.random.default_rng(11)
    svg = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"]

    # faint chart grid
    for x in range(0, width + 1, 100):
        svg.append(f"<line x1='{x}' y1='0' x2='{x}' y2='{height}' stroke='#3a5aa8' stroke-opacity='0.14'/>")
    for y in range(0, height + 1, 100):
        svg.append(f"<line x1='0' y1='{y}' x2='{width}' y2='{y}' stroke='#3a5aa8' stroke-opacity='0.14'/>")

    # scatter plot with a trend line (bottom-left)
    xs = rng.uniform(60, 520, 46)
    ys = 620 - (xs - 60) * 0.62 + rng.normal(0, 30, 46)
    for x, y in zip(xs, ys):
        svg.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='4.5' fill='#ffc93c' fill-opacity='0.5'/>")
    svg.append("<line x1='50' y1='632' x2='540' y2='318' stroke='#ffc93c' stroke-opacity='0.55' "
               "stroke-width='2.5' stroke-dasharray='10 8'/>")

    # histogram with a bell curve (bottom-right)
    for i in range(11):
        h = 240 * math.exp(-((i - 5) ** 2) / (2 * 2.1 ** 2))
        svg.append(f"<rect x='{760 + i * 34}' y='{660 - h:.0f}' width='28' height='{h:.0f}' rx='3' "
                   "fill='#4f8ef7' fill-opacity='0.24'/>")
    curve = " ".join(f"{x},{660 - 250 * math.exp(-((x - 944) ** 2) / (2 * 72 ** 2)):.0f}" for x in range(750, 1141, 10))
    svg.append(f"<polyline points='{curve}' fill='none' stroke='#ffc93c' stroke-opacity='0.55' stroke-width='2.5'/>")

    # network graph (top-right)
    nodes = [(800, 90), (930, 150), (1060, 80), (1110, 210), (980, 270), (850, 230), (1010, 130)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 6), (6, 2), (6, 4), (1, 4)]
    for a, b in edges:
        svg.append(f"<line x1='{nodes[a][0]}' y1='{nodes[a][1]}' x2='{nodes[b][0]}' y2='{nodes[b][1]}' "
                   "stroke='#4f8ef7' stroke-opacity='0.4' stroke-width='2'/>")
    for x, y in nodes:
        svg.append(f"<circle cx='{x}' cy='{y}' r='9' fill='#0a1630' stroke='#ffc93c' stroke-opacity='0.7' stroke-width='2.5'/>")

    # formulas (top-left)
    for text, x, y, size in [("μ", 90, 150, 70), ("σ²", 250, 110, 56), ("Σ", 430, 160, 72),
                             ("p &lt; 0.05", 80, 250, 28), ("y = mx + b", 290, 250, 28)]:
        svg.append(f"<text x='{x}' y='{y}' font-family='Georgia, serif' font-style='italic' font-size='{size}' "
                   "fill='#ffc93c' fill-opacity='0.26'>" + text + "</text>")

    svg.append("</svg>")
    return "data:image/svg+xml;utf8," + urllib.parse.quote("".join(svg))


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --navy-900: #060f24;
    --navy-800: #0a1630;
    --navy-700: #101f42;
    --navy-600: #172b57;
    --line:     #26407a;
    --yellow:   #ffc93c;
    --yellow-d: #e6a800;
    --text:     #eaf0ff;
    --muted:    #9fb0d6;
    /* bouncy easing: one overshoot (fallback) ... */
    --pop:      cubic-bezier(.34, 1.56, .64, 1);
    --spring:   cubic-bezier(.34, 1.56, .64, 1);
}
/* ... upgraded to a real springy wobble in browsers that support linear() easing */
@supports (animation-timing-function: linear(0, 1)) {
    :root { --spring: __SPRING__; }
}

html, body, [class*="st-"], .stApp {
    font-family: 'DM Sans', sans-serif;
}
/* Keep Streamlit's icon font for icons (otherwise they show as text like "keyboard_double_arrow_left") */
[data-testid="stIconMaterial"],
[class*="material-symbols"],
[class*="material-icons"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
}
h1, h2, h3, h4 {
    font-family: 'Sora', sans-serif !important;
    letter-spacing: -0.02em;
    color: var(--text);
}

/* Background: a data-science picture (layer 1) over soft glows. It is bigger than the screen so it can glide. */
.stApp {
    background-color: var(--navy-800);
    background-image:
        url("__BG__"),
        radial-gradient(1000px 500px at 85% -10%, rgba(255, 201, 60, 0.10), transparent 60%),
        radial-gradient(800px 500px at -10% 110%, rgba(38, 64, 122, 0.55), transparent 60%);
    background-repeat: no-repeat, no-repeat, no-repeat;
    background-size: max(130vw, 223vh) auto, auto, auto;
    background-position: 50% 50%, 0 0, 0 0;
    background-attachment: fixed, fixed, fixed;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.5rem; max-width: 1100px; }

/* ---------- Animations (bouncy + smooth) ----------
   Opacity uses a gentle ease, movement uses the springy easing, so things fade in cleanly but bounce into place. */
@keyframes fadeIn   { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideNext {
    from { transform: translateX(120px) scale(0.96); }
    to   { transform: translateX(0) scale(1); }
}
@keyframes slidePrev {
    from { transform: translateX(-120px) scale(0.96); }
    to   { transform: translateX(0) scale(1); }
}
@keyframes popIn {
    from { transform: scale(0.82) translateY(34px); }
    to   { transform: scale(1) translateY(0); }
}
@keyframes loadBar {
    0%   { width: 0; opacity: 1; }
    75%  { width: 100%; opacity: 1; }
    100% { width: 100%; opacity: 0; }
}
@keyframes growBar {
    from { width: 0; }
    to   { width: 72px; }
}
@keyframes sweep {
    from { background-size: 0% 100%; }
    to   { background-size: 100% 100%; }
}

/* Yellow loading bar sweeps across the top on every page change */
[class*="st-key-page_"]::before {
    content: "";
    position: fixed; top: 0; left: 0; height: 4px;
    z-index: 999999;
    background: linear-gradient(90deg, var(--yellow), #fff1b8);
    box-shadow: 0 0 14px var(--yellow);
    animation: loadBar 0.9s ease-out both;
}

/* Going to the NEXT page: content bounces in from the right, one block after another.
   Going BACK: content bounces in from the left. */
[class*="st-key-page_"][class*="_next"] > * {
    animation: fadeIn 0.45s ease-out backwards, slideNext 1s var(--spring) backwards;
}
[class*="st-key-page_"][class*="_prev"] > * {
    animation: fadeIn 0.45s ease-out backwards, slidePrev 1s var(--spring) backwards;
}
[class*="st-key-page_"] > *:nth-child(1) { animation-delay: 0.05s; }
[class*="st-key-page_"] > *:nth-child(2) { animation-delay: 0.12s; }
[class*="st-key-page_"] > *:nth-child(3) { animation-delay: 0.19s; }
[class*="st-key-page_"] > *:nth-child(4) { animation-delay: 0.26s; }
[class*="st-key-page_"] > *:nth-child(5) { animation-delay: 0.33s; }
[class*="st-key-page_"] > *:nth-child(6) { animation-delay: 0.40s; }
[class*="st-key-page_"] > *:nth-child(7) { animation-delay: 0.47s; }
[class*="st-key-page_"] > *:nth-child(8) { animation-delay: 0.54s; }

/* Metrics (and other columns) bounce in one by one */
[class*="st-key-page_"] [data-testid="stColumn"],
[class*="st-key-page_"] [data-testid="column"] {
    animation: fadeIn 0.45s ease-out backwards, popIn 0.9s var(--spring) backwards;
}
[class*="st-key-page_"] [data-testid="stHorizontalBlock"] > div:nth-child(1) { animation-delay: 0.30s; }
[class*="st-key-page_"] [data-testid="stHorizontalBlock"] > div:nth-child(2) { animation-delay: 0.40s; }
[class*="st-key-page_"] [data-testid="stHorizontalBlock"] > div:nth-child(3) { animation-delay: 0.50s; }
[class*="st-key-page_"] [data-testid="stHorizontalBlock"] > div:nth-child(4) { animation-delay: 0.60s; }

/* Lifecycle step card bounces again each time the slider moves */
[class*="st-key-step_"] { animation: fadeIn 0.3s ease-out backwards, popIn 0.8s var(--spring) backwards; }

/* ---------- Aligned cards: one grid, so every card in a row has the same width and height ---------- */
.ds-grid {
    display: grid;
    grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr));
    gap: 1rem;
    align-items: stretch;
    margin: 0.4rem 0 1.2rem 0;
}
.ds-card {
    background: rgba(16, 31, 66, 0.86);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.3rem 1.4rem;
    text-align: left;
    animation: fadeIn 0.45s ease-out backwards, popIn 0.9s var(--spring) backwards;
    transition: transform 0.45s var(--pop), border-color 0.25s ease, box-shadow 0.25s ease;
}
.ds-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: var(--yellow);
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.4);
}
.ds-card h3 {
    margin: 0 0 0.55rem 0 !important;
    padding: 0 !important;
    font-size: 1.15rem !important;
    line-height: 1.3;
    color: var(--text);
}
.ds-card p { margin: 0; color: var(--muted); line-height: 1.6; }
.ds-card:nth-child(1) { animation-delay: 0.30s; }
.ds-card:nth-child(2) { animation-delay: 0.38s; }
.ds-card:nth-child(3) { animation-delay: 0.46s; }
.ds-card:nth-child(4) { animation-delay: 0.54s; }
.ds-card:nth-child(5) { animation-delay: 0.62s; }
.ds-card:nth-child(6) { animation-delay: 0.70s; }
@media (max-width: 800px) {
    .ds-grid { grid-template-columns: 1fr; }
}

/* ---------- Headings ---------- */
h1 { font-weight: 800 !important; position: relative; padding-bottom: 0.9rem; }
h1::after {
    content: "";
    position: absolute; left: 0; bottom: 0;
    height: 4px; width: 72px; border-radius: 4px;
    background: var(--yellow);
    animation: growBar 1s 0.25s var(--spring) both;
}
h2 { font-weight: 700 !important; margin-top: 1.4rem; }

/* ---------- Hero (home page) ---------- */
.hero {
    padding: 3rem 2.5rem;
    border-radius: 20px;
    border: 1px solid var(--line);
    background:
        radial-gradient(600px 260px at 100% 0%, rgba(255, 201, 60, 0.16), transparent 70%),
        linear-gradient(135deg, var(--navy-700), var(--navy-900));
    margin-bottom: 1.5rem;
}
.hero h1 { font-size: 3rem; margin: 0 0 0.6rem 0; padding: 0; line-height: 1.1; }
.hero h1::after { display: none; }
.hero .hl {
    background: linear-gradient(var(--yellow), var(--yellow)) no-repeat 0 92% / 100% 0.14em;
    animation: sweep 1s 0.4s cubic-bezier(.2,.7,.2,1) both;
}
.hero p { font-size: 1.2rem; color: var(--muted); max-width: 40rem; margin: 0; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--navy-900);
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] h1 {
    font-size: 1.4rem; color: var(--yellow);
}
[data-testid="stSidebar"] h1::after { display: none; }

/* Turn the radio into a nav menu */
[data-testid="stSidebar"] [role="radiogroup"] { gap: 0.3rem; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 0.65rem 0.9rem;
    border-radius: 10px;
    border: 1px solid transparent;
    width: 100%;
    transition: background 0.2s ease, transform 0.45s var(--pop), border-color 0.2s ease;
    cursor: pointer;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: var(--navy-600);
    transform: translateX(4px);
    border-color: var(--line);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: var(--yellow);
    transform: translateX(4px);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * {
    color: var(--navy-900) !important;
    font-weight: 700;
}

/* ---------- Cards (bordered containers) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--navy-700);
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    transition: transform 0.45s var(--pop), border-color 0.25s ease, box-shadow 0.25s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
    border-color: var(--yellow) !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
    background: var(--navy-700);
    border: 1px solid var(--line);
    border-left: 4px solid var(--yellow);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    transition: transform 0.45s var(--pop), box-shadow 0.25s ease;
    min-height: 112px;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
}
[data-testid="stMetricValue"] { color: var(--yellow); font-family: 'Sora', sans-serif; font-weight: 700; }
[data-testid="stMetricLabel"] p { color: var(--muted); }

/* ---------- Info box, progress, code, tables ---------- */
[data-testid="stAlert"] { border-radius: 14px; border: 1px solid var(--line); }
[data-testid="stProgress"] > div > div > div > div { background: var(--yellow); transition: width 0.6s ease; }
[data-testid="stCode"], [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid var(--line); }

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 10px;
    border: 1px solid var(--line);
    background: var(--navy-700);
    color: var(--text);
    font-weight: 600;
    padding: 0.6rem 1.4rem;
    transition: transform 0.4s var(--pop), box-shadow 0.2s ease, background 0.2s ease;
}
.stButton > button:active { transform: scale(0.93); }
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    border-color: var(--yellow);
    color: var(--yellow);
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"],
.stFormSubmitButton > button {
    background: var(--yellow);
    color: var(--navy-900);
    border-color: var(--yellow);
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover,
.stFormSubmitButton > button:hover {
    background: var(--yellow-d);
    color: var(--navy-900);
    box-shadow: 0 8px 22px rgba(255, 201, 60, 0.3);
}
.stButton > button[kind="primary"] p,
.stButton > button[data-testid="stBaseButton-primary"] p,
.stFormSubmitButton > button p { color: var(--navy-900); }

/* Quiz form */
[data-testid="stForm"] {
    background: var(--navy-700);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.5rem;
}

/* Page footer nav spacing */
.nav-gap { height: 1.5rem; }

/* Respect people who turn animations off */
@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}
"""
CSS = CSS.replace("__SPRING__", spring_easing()).replace("__BG__", make_background_uri())
st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)


def home():
    st.markdown(
        '<div class="hero">'
        '<h1>Data Science <span class="hl">Learning Hub</span></h1>'
        "<p>A quick, beginner-friendly guide to turning data into decisions.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.write(
        "Use the menu on the left or the buttons at the bottom to move through the hub. "
        "Each page covers one big idea, and the last page is a short quiz to test what you learned."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pages", len(PAGES))
    c2.metric("Lifecycle steps", 6)
    c3.metric("Core tools", 6)
    c4.metric("Quiz questions", len(QUIZ))

    st.info(
        "💡 **One-line definition:** Data science is the practice of using data, "
        "programming, and statistics to find patterns and answer real questions."
    )


def what_is_ds():
    st.title("What is Data Science?")
    st.write(
        "Every day, apps, websites, and devices create huge amounts of data. "
        "Data science is how we make sense of it: collecting it, cleaning it, "
        "analyzing it, and using the results to make better decisions."
    )

    st.header("The three ingredients")
    card_grid(
        {
            "📐 Statistics & Math": "Finds patterns and tells us how confident we can be in them.",
            "💻 Programming": "Lets us handle large datasets quickly (usually with Python or SQL).",
            "🌍 Domain Knowledge": "Understanding the field (health, business, sports) so the results make sense.",
        }
    )

    st.header("Types of data")
    types = pd.DataFrame(
        {
            "Type": ["Numerical", "Categorical", "Text", "Time series", "Images"],
            "What it is": [
                "Numbers you can measure or count",
                "Labels or groups",
                "Words and sentences",
                "Values recorded over time",
                "Photos and video frames",
            ],
            "Example": [
                "Height, price, test score",
                "Favorite food, grade level",
                "Reviews, tweets, emails",
                "Daily temperature, stock prices",
                "X-rays, face photos",
            ],
        }
    )
    st.dataframe(types, hide_index=True, width="stretch")


LIFECYCLE = [
    ("1. Ask", "❓", "Define the question or problem you want to solve.",
     "A school asks: which students are at risk of failing?"),
    ("2. Collect", "📥", "Gather the data from surveys, databases, websites, or sensors.",
     "Pull grades, attendance, and homework records."),
    ("3. Clean", "🧹", "Fix errors, remove duplicates, and handle missing values. This often takes the most time.",
     "Remove repeated records and fill in missing attendance."),
    ("4. Explore", "🔍", "Look for patterns using statistics and charts.",
     "Students with low attendance tend to have lower grades."),
    ("5. Model", "🤖", "Build a model (such as a prediction) that learns from the data.",
     "Train a model that predicts who might fail next term."),
    ("6. Share", "📊", "Present findings with charts and clear recommendations.",
     "Show teachers a dashboard and suggest extra support."),
]


def lifecycle():
    st.title("The Data Science Lifecycle")
    st.write("Most projects follow these six steps. Move the slider to see what happens at each step.")

    step = st.select_slider(
        "Progress through the lifecycle",
        options=[s[0] for s in LIFECYCLE],
    )
    index = [s[0] for s in LIFECYCLE].index(step)
    st.progress((index + 1) / len(LIFECYCLE))

    name, icon, description, example = LIFECYCLE[index]
    
    with st.container(key=f"step_{index}"):
        with st.container(border=True):
            st.markdown(f"## {icon} {name}")
            st.write(description)
            st.markdown(f"**Example:** {example}")

    st.caption("In real projects you often loop back to earlier steps as you learn more.")


def tools():
    st.title("Common Tools")
    tool_table = pd.DataFrame(
        {
            "Tool": ["Python", "R", "SQL", "Excel", "Jupyter Notebook", "Tableau / Power BI"],
            "Used for": [
                "Cleaning, analysis, and machine learning",
                "Statistics and research",
                "Getting data out of databases",
                "Quick tables and simple charts",
                "Writing code and notes together",
                "Interactive dashboards",
            ],
            "Beginner friendly?": ["Yes", "Medium", "Yes", "Yes", "Yes", "Yes"],
        }
    )
    st.dataframe(tool_table, hide_index=True, width="stretch")

    st.header("Python libraries to know")
    st.markdown(
        "- **pandas** for tables of data\n"
        "- **NumPy** for fast math\n"
        "- **Matplotlib / Plotly** for charts\n"
        "- **scikit-learn** for machine learning"
    )

    st.header("Try it: a few lines of pandas")
    code = (
        "import pandas as pd\n\n"
        'scores = pd.DataFrame({"Student": ["Ana", "Ben", "Cara", "Dan"],\n'
        '                       "Score": [88, 72, 95, 80]})\n\n'
        'print(scores["Score"].mean())\n'
        'scores.set_index("Student").plot.bar()'
    )
    st.code(code, language="python")
    scores = pd.DataFrame({"Student": ["Ana", "Ben", "Cara", "Dan"], "Score": [88, 72, 95, 80]})
    st.write(f"**Output:** average score = {scores['Score'].mean():.1f}")
    st.bar_chart(scores.set_index("Student"), color="#ffc93c")


USES = {
    "🏥 Healthcare": "Predicting disease risk, reading medical scans, and speeding up drug research.",
    "🏦 Finance": "Detecting credit card fraud and deciding loan approvals.",
    "🛒 Retail": "Recommending products and forecasting how much stock to order.",
    "🚗 Transportation": "Finding faster routes, predicting traffic, and powering ride-hailing prices.",
    "🎓 Education": "Spotting students who need help and personalizing lessons.",
    "🎵 Entertainment": "Recommending songs, shows, and videos you will probably like.",
}


def real_world():
    st.title("Data Science in the Real World")
    st.write("You already use data science every day without noticing.")
    card_grid(USES)


QUIZ = [
    ("Which step of the lifecycle usually takes the most time?",
     ["Ask", "Clean", "Share"], "Clean",
     "Real data is messy, so cleaning it takes a large share of a project."),
    ("Which language is the most popular for data science?",
     ["Python", "HTML", "Photoshop"], "Python",
     "Python has many data libraries like pandas and scikit-learn."),
    ("What does SQL help you do?",
     ["Draw charts", "Get data from databases", "Edit photos"], "Get data from databases",
     "SQL is the standard language for querying databases."),
    ("'Favorite food' is which type of data?",
     ["Numerical", "Categorical", "Time series"], "Categorical",
     "It is a label that groups people, not a measurement."),
    ("What is the final step of the lifecycle?",
     ["Collect", "Model", "Share"], "Share",
     "Findings are only useful once they are communicated clearly."),
    ("Which measure is least affected by extreme values (outliers)?",
     ["Mean", "Median", "Range"], "Median",
     "The median is the middle value, so one huge number barely moves it."),
    ("In supervised learning, the training data includes...",
     ["No data at all", "Only images", "The correct answers (labels)"], "The correct answers (labels)",
     "The model learns by comparing its guesses to known answers."),
    ("What should you do with duplicate records?",
     ["Remove them", "Keep all of them", "Double them"], "Remove them",
     "Duplicates can make some results count more than they should."),
    ("A model that does great on training data but poorly on new data is...",
     ["Cleaning", "Overfitting", "Sharing"], "Overfitting",
     "It memorized the training examples instead of learning the real pattern."),
    ("Who builds the pipelines that collect, move, and store data?",
     ["Web designer", "Data analyst", "Data engineer"], "Data engineer",
     "Data engineers make sure clean data reaches the people who analyze it."),
]


def quiz():
    st.title("Test Yourself")
    with st.form("quiz_form"):
        answers = []
        for i, (question, options, _, _) in enumerate(QUIZ):
            answers.append(st.radio(f"{i + 1}. {question}", options, index=None, key=f"q{i}"))
        submitted = st.form_submit_button("Submit answers")

    if submitted:
        if None in answers:
            st.warning("Please answer every question first.")
            return
        score = sum(a == q[2] for a, q in zip(answers, QUIZ))
        st.subheader(f"Score: {score} / {len(QUIZ)}")
        if score == len(QUIZ):
            st.balloons()
        for i, (a, q) in enumerate(zip(answers, QUIZ)):
            if a == q[2]:
                st.success(f"Q{i + 1}: Correct. {q[3]}")
            else:
                st.error(f"Q{i + 1}: The answer is **{q[2]}**. {q[3]}")



def card_grid(items, per_row=3):
    """Show {title: text} as an even grid of cards. Every card in a row gets the same height."""
    cards = "".join(
        f'<div class="ds-card"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p></div>'
        for title, text in items.items()
    )
    st.markdown(f'<div class="ds-grid" style="--cols:{per_row}">{cards}</div>', unsafe_allow_html=True)


def statistics():
    st.title("Statistics Basics")
    st.write(
        "Statistics gives data scientists simple numbers that describe a whole "
        "dataset. Three of them show up everywhere."
    )
    card_grid(
        {
            "➗ Mean": "The average. Add everything up and divide by how many values there are.",
            "🎯 Median": "The middle value when the numbers are sorted. Great when some values are extreme.",
            "🔁 Mode": "The value that appears most often.",
        }
    )

    st.header("Try it: type your own numbers")
    raw_text = st.text_input(
        "Numbers separated by commas",
        "70, 75, 80, 85, 90",
        help="Try adding a very large number like 500 and watch what happens to the mean.",
    )
    try:
        nums = [float(x) for x in raw_text.replace(" ", "").split(",") if x]
    except ValueError:
        st.warning("Please type only numbers separated by commas.")
        return
    if len(nums) < 2:
        st.warning("Type at least two numbers.")
        return

    s = pd.Series(nums)
    if s.value_counts().max() == 1:
        mode_text = "None"
    else:
        mode_text = ", ".join(f"{m:g}" for m in s.mode())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean", f"{s.mean():.2f}")
    c2.metric("Median", f"{s.median():.2f}")
    c3.metric("Mode", mode_text)
    c4.metric("Range", f"{s.max() - s.min():g}")
    st.bar_chart(pd.DataFrame({"Value": nums}), color="#ffc93c")
    st.info(
        "💡 **Tip:** add one huge number (like 500). The mean jumps up, but the "
        "median barely moves. That is why the median is better when data has outliers."
    )


def cleaning():
    st.title("Cleaning Data")
    st.write(
        "Real data is messy. Tick the cleaning steps below and watch the table "
        "get better. The table starts with typos, duplicates, an impossible age, "
        "and missing values."
    )
    raw = pd.DataFrame(
        {
            "Name": ["Ana", "Ben", "Ben", "Cara", "Dan", "Eli"],
            "Age": [21, None, None, 19, 200, 22],
            "City": ["manila", " Cebu", "Cebu", "MANILA", "Davao ", "cebu"],
        }
    )

    c1, c2 = st.columns(2)
    fix_city = c1.checkbox("Fix spaces and capital letters in City", value=False)
    drop_dups = c1.checkbox("Remove duplicate rows", value=False)
    fix_age = c2.checkbox("Remove impossible ages (over 100)", value=False)
    fill_age = c2.checkbox("Fill missing ages with the median", value=False)

    df = raw.copy()
    if fix_city:
        df["City"] = df["City"].str.strip().str.title()
    if drop_dups:
        df = df.drop_duplicates()
    if fix_age:
        df.loc[df["Age"] > 100, "Age"] = None
    if fill_age:
        df["Age"] = df["Age"].fillna(df["Age"].median())

    m1, m2, m3 = st.columns(3)
    m1.metric("Rows", len(df))
    m2.metric("Missing values", int(df.isna().sum().sum()))
    m3.metric("Different city spellings", df["City"].nunique())
    st.dataframe(df, hide_index=True, width="stretch")

    st.header("The same steps in pandas")
    st.code(
        'df["City"] = df["City"].str.strip().str.title()\n'
        "df = df.drop_duplicates()\n"
        'df.loc[df["Age"] > 100, "Age"] = None\n'
        'df["Age"] = df["Age"].fillna(df["Age"].median())',
        language="python",
    )
    st.caption("Tip: tick the city fix before removing duplicates, so ' Cebu' and 'Cebu' count as the same.")


def machine_learning():
    st.title("Machine Learning")
    st.write(
        "Machine learning is a part of data science where a computer learns "
        "patterns from examples instead of being given step-by-step rules."
    )
    card_grid(
        {
            "🏷️ Supervised": "Learns from examples that already have answers. Example: predicting house prices.",
            "🧩 Unsupervised": "Finds groups on its own, with no answers given. Example: grouping similar customers.",
            "🎮 Reinforcement": "Learns by trial and error with rewards. Example: a game-playing program.",
        }
    )

    st.header("Try it: predict a test score")
    st.write(
        "We gave a model the study hours and scores of 8 students. It learned the "
        "pattern. Move the slider to ask it for a prediction."
    )
    data = pd.DataFrame(
        {"Hours studied": [1, 2, 3, 4, 5, 6, 7, 8], "Score": [52, 58, 63, 68, 74, 79, 84, 90]}
    )
    slope, intercept = np.polyfit(data["Hours studied"], data["Score"], 1)
    hours = st.slider("Hours of study", 0.0, 10.0, 4.5, step=0.5)
    prediction = float(np.clip(slope * hours + intercept, 0, 100))

    c1, c2 = st.columns([1, 2], vertical_alignment="center")
    with c1:
        st.metric("Predicted score", f"{prediction:.0f}")
        st.caption(f"The model learned that each extra hour adds about {slope:.1f} points.")
    with c2:
        st.scatter_chart(data, x="Hours studied", y="Score", color="#ffc93c")
    st.info(
        "💡 Real models use many more examples and many more features, "
        "but the idea is the same: learn a pattern, then predict something new."
    )


def ethics():
    st.title("Ethics and Bias")
    st.write(
        "Data science can affect real people, so it comes with responsibility. "
        "A model is only as fair as the data it learns from."
    )
    card_grid(
        {
            "🔒 Privacy": "Protect personal information and only collect what you really need.",
            "⚖️ Bias": "If the data leaves some groups out, the model can treat them unfairly.",
            "🔍 Transparency": "Be able to explain how a result was produced and what its limits are.",
            "✅ Consent": "People should know when their data is collected and how it is used.",
            "🛡️ Security": "Store data safely so it does not leak or get stolen.",
            "📣 Honest reporting": "Show the full picture. Do not cherry-pick charts that hide the truth.",
        }
    )
    st.info(
        "💡 **Example:** if a hiring model is trained only on past hires from one group, "
        "it may learn to prefer that group and reject equally good candidates."
    )
    st.header("Questions to ask before using data")
    st.markdown(
        "- Where did this data come from, and who is missing from it?\n"
        "- Did people agree to share it?\n"
        "- Could this result hurt someone if it is wrong?\n"
        "- Can I explain the result in simple words?"
    )


def careers():
    st.title("Careers in Data")
    st.write("Data skills open the door to many different jobs. Here are four common ones.")
    roles = pd.DataFrame(
        {
            "Role": ["Data Analyst", "Data Scientist", "Machine Learning Engineer", "Data Engineer"],
            "What they do": [
                "Answer business questions and build reports and dashboards",
                "Explore data and build models to predict or explain things",
                "Turn models into reliable apps and services",
                "Build the pipelines that collect, move, and store data",
            ],
            "Key skills": [
                "SQL, Excel, Tableau / Power BI",
                "Python, statistics, machine learning",
                "Python, software engineering, deployment",
                "SQL, Python, databases, cloud tools",
            ],
        }
    )
    st.dataframe(roles, hide_index=True, width="stretch")

    st.header("How to get started")
    card_grid(
        {
            "1. Learn the basics": "Start with Excel, then Python and SQL.",
            "2. Practice on real data": "Use free datasets from sites like Kaggle.",
            "3. Build a project": "Answer one question you care about and share the result.",
        }
    )


GLOSSARY = {
    "Dataset": "A collection of data, usually arranged as a table of rows and columns.",
    "Feature": "A column used as an input to a model, such as age or study hours.",
    "Label": "The answer a model is trying to predict, such as a test score.",
    "Model": "A program that learned patterns from data and can make predictions.",
    "Training data": "The examples a model learns from.",
    "Test data": "New examples used to check how well a model works.",
    "Overfitting": "When a model memorizes the training data and fails on new data.",
    "Outlier": "A value that is far away from most of the others.",
    "Missing value": "An empty spot in the data where information was not recorded.",
    "Correlation": "A measure of how two things move together. It does not prove one causes the other.",
    "Bias": "A systematic unfairness in the data or in a model's results.",
    "Visualization": "A chart or graph that makes patterns in data easy to see.",
    "Big data": "Data so large or fast-growing that normal tools struggle to handle it.",
    "Algorithm": "A set of steps a computer follows to solve a problem.",
}


def glossary():
    st.title("Glossary")
    st.write("Quick meanings for the words you will hear most. Type to search.")
    query = st.text_input("Search a word", placeholder="for example: outlier").strip().lower()
    matches = {t: d for t, d in sorted(GLOSSARY.items()) if query in t.lower() or query in d.lower()}
    if not matches:
        st.warning("No matching words. Try a different search.")
        return
    for term, definition in matches.items():
        with st.container(border=True):
            st.markdown(f"**{term}**")
            st.write(definition)



PAGES = {
    "🏠 Home": home,
    "📘 What is Data Science?": what_is_ds,
    "🔄 The Lifecycle": lifecycle,
    "📊 Statistics Basics": statistics,
    "🧹 Cleaning Data": cleaning,
    "🛠️ Tools": tools,
    "🤖 Machine Learning": machine_learning,
    "🌍 Real-World Uses": real_world,
    "⚖️ Ethics and Bias": ethics,
    "💼 Careers": careers,
    "📖 Glossary": glossary,
    "📝 Quiz": quiz,
}
NAMES = list(PAGES)

if "nav" not in st.session_state:
    st.session_state.nav = NAMES[0]


def go(delta):
    st.session_state.nav = NAMES[NAMES.index(st.session_state.nav) + delta]


st.sidebar.title("Learning Hub")
choice = st.sidebar.radio("Go to", NAMES, key="nav", label_visibility="collapsed")
position = NAMES.index(choice)


last = st.session_state.get("last_pos", position)
if position != last:
    st.session_state.direction = "next" if position > last else "prev"
st.session_state.last_pos = position
direction = st.session_state.get("direction", "next")


with st.container(key=f"page_{position}_{direction}"):
    PAGES[choice]()

st.markdown('<div class="nav-gap"></div>', unsafe_allow_html=True)
prev_col, mid_col, next_col = st.columns([1, 4, 1])
if position > 0:
    prev_col.button("Previous", on_click=go, args=(-1,), key="prev_btn", use_container_width=True)
if position < len(NAMES) - 1:
    next_col.button("Next page", on_click=go, args=(1,), key="next_btn", type="primary", use_container_width=True)

# The background picture glides in the direction you are moving. A new animation name per page restarts it.
_start = "90% 50%" if direction == "next" else "10% 50%"
_name = f"bgGlide_{position}_{direction}"
st.sidebar.markdown(
    f"<style>@keyframes {_name} {{ from {{ background-position: {_start}, 0 0, 0 0; }} "
    f"to {{ background-position: 50% 50%, 0 0, 0 0; }} }} "
    f".stApp {{ animation: {_name} 1.6s var(--spring) both; }}</style>",
    unsafe_allow_html=True,
)

st.sidebar.caption(f"Page {position + 1} of {len(NAMES)}")
st.sidebar.caption("Made with Python and Streamlit")