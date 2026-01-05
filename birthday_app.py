import random
from pathlib import Path

import streamlit as st
from PIL import Image

# ------------------------------------------------------------
# Streamlit Page Setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="Happy 21st, Tanvi!",
    page_icon="🎉",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# Global CSS (pastel gradient, glassmorphism, animations)
# ------------------------------------------------------------
GLOBAL_CSS = """
/* Google Fonts for cute, modern vibe */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Pacifico&display=swap');

:root {
  --bg-start: #f9d3e6; /* pastel pink */
  --bg-end:   #cde7f0; /* pastel blue */
  --card: rgba(255, 255, 255, 0.22);
  --card-border: rgba(255, 255, 255, 0.35);
  --text: #ffffff;
  --accent-pink: #ff8fb1;
  --accent-rose: #ff6b9d;
  --accent-yellow: #ffe28a;
  --accent-blue: #4da3ff;
  --shadow: 0 10px 30px rgba(0,0,0,0.18);
}

/* Background gradient and base layout */
html, body, [data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, var(--bg-start) 0%, var(--bg-end) 100%) fixed;
}

/* Use friendly fonts with emoji support */
html, body, * {
  font-family: 'Poppins', 'Apple Color Emoji', 'Noto Color Emoji', system-ui, -apple-system, Segoe UI, Roboto, sans-serif !important;
}

/* Keep content above animated background */
.block-container {
  position: relative;
  z-index: 1;
  padding-top: 2rem;
  max-width: 900px;
}

/* Glowing white text */
.glow {
  color: var(--accent-blue);
  text-shadow: 0 2px 8px rgba(77,163,255,0.55), 0 0 18px rgba(77,163,255,0.35);
}

/* Highlight text across main content (excluding the main heading) */
.hero-sub.glow, .message-card .glow, .memories-grid .glow, .roast-card.glow, .footer.glow { background: none !important; text-shadow: none; }

/* Hero Section */
.hero {
  text-align: center;
  margin: 2rem 0 1.25rem 0;
}
.hero-title {
  font-size: clamp(2rem, 4.8vw, 3.2rem);
  line-height: 1.1;
  margin: 0.25rem 0;
  font-weight: 700;
  color: var(--accent-rose);
  text-shadow: 0 2px 8px rgba(255, 107, 157, 0.55), 0 0 18px rgba(255, 107, 157, 0.35);
}
.hero-sub {
  font-size: clamp(1rem, 2.6vw, 1.25rem);
  opacity: 0.95;
}

/* Glassmorphism Card */
.glass {
  background: var(--card);
  border: 1px solid var(--card-border);
  box-shadow: var(--shadow), 0 0 0 1px rgba(255,255,255,0.55) inset;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 18px;
}

/* Photo card styling (targets Streamlit image container) */
[data-testid="stImage"] {
  margin: 0 auto !important;
  display: flex;
  justify-content: center;
  background: var(--card);
  border: 1px solid var(--card-border);
  box-shadow: var(--shadow);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 18px;
  padding: 14px;
  margin-bottom: 12px;
}
[data-testid="stImage"] > img, [data-testid="stImage"] img {
  border-radius: 16px !important;
  box-shadow: 0 8px 24px rgba(0,0,0,0.18);
  width: clamp(180px, 40vw, 320px);
  height: auto;
}
/* Wrap the image visually in a glass card */
.photo-wrapper {
  display: grid;
  place-items: center;
  padding: 14px;
  margin-bottom: 12px;
}

/* Pink message card */
.message-card {
  background: rgba(255, 143, 177, 0.22);
  border: 1px solid rgba(255, 143, 177, 0.4);
  border-radius: 18px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 1.25rem 1.1rem;
  color: #222222;
}



/* Center roast button wrapper */
.roast-inline .stButton>button {
  border-radius: 999px;
  padding: 0.6rem 1.1rem;
  border: 1px solid rgba(255,255,255,0.65);
  background: linear-gradient(135deg, #ffffff, #f7ecff);
  color: #5b4b6e;
  box-shadow: 0 8px 18px rgba(0,0,0,0.12);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: transform 120ms ease, box-shadow 120ms ease;
}
.stButton>button:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 10px 22px rgba(0,0,0,0.16);
}
/* Roast card */
.roast-card {
  margin-top: 0.75rem;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255,255,255,0.35);
  border-radius: 14px;
  padding: 0.9rem 1rem;
  color: var(--text);
  text-align: center;
}

/* Memories Grid */
.memories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin-top: 0.5rem;
}
.memory-card {
  padding: 1rem;
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.35);
  border-radius: 16px;
  box-shadow: var(--shadow);
  color: #333333;
}
.memory-title {
  font-weight: 700;
  margin-bottom: 6px;

  color: #222222;
}
.memory-text {
  opacity: 0.95;
}

/* Footer */
.footer {
  margin: 2rem 0 1rem 0;
  text-align: center;
  color: var(--text);
  opacity: 0.95;
}

/* Animated Background Layers */
.bg-anim {
  position: fixed;
  inset: 0;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}
.bg-anim .layer {
  position: absolute;
  inset: 0;
}
.bg-anim .particle {
  position: absolute;
  bottom: -10vh; /* start off-screen */
  left: var(--left, 50%);
  font-size: var(--size, 1.2rem);
  opacity: var(--op, 0.65);
  filter: drop-shadow(0 6px 8px rgba(0,0,0,0.08));
  animation: floatUp var(--dur, 16s) linear infinite;
  animation-delay: var(--delay, 0s);
}
.bg-anim .balloon { color: #ff7f50; }
.bg-anim .heart { color: var(--accent-rose); }
.bg-anim .spark  { color: #ffffff; opacity: 0.55; text-shadow: 0 0 10px rgba(255,255,255,0.8); }

@keyframes floatUp {
  0%   { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0; }
  10%  { opacity: 1; }
  50%  { transform: translateY(-50vh) translateX(calc(var(--drift, 0px))) rotate(3deg); }
  100% { transform: translateY(-105vh) translateX(calc(var(--drift, 0px))) rotate(-6deg); opacity: 0; }
}

/* Buttons - rounded and soft */
.stButton>button {
  border-radius: 30px;
  border: 1px solid rgba(255,255,255,0.5);
  background: rgba(255,255,255,0.25);
  color: #ffffff;
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.stTextInput>div>div>input {
  color: #ffffff !important;
}

/* Login Card */
.login-card {
  max-width: 420px;
  margin: 16vh auto 0 auto;
  padding: 1.25rem;
}
.login-title { text-align: center; margin-bottom: 0.25rem; }
.login-sub { text-align: center; opacity: 0.9; margin-bottom: 0.75rem; }
"""


def inject_css():
    """Inject global CSS into the page."""
    st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)


def render_animated_background():
    """Create soft floating balloons, hearts, and sparkles using CSS."""
    def particles(symbol: str, cls: str, count: int, size_range=(0.9, 1.8)) -> str:
        html_parts = []
        for _ in range(count):
            left = f"{random.randint(0, 100)}%"
            delay = f"{random.uniform(0, 12):.2f}s"
            dur = f"{random.uniform(14, 26):.2f}s"
            size = f"{random.uniform(size_range[0], size_range[1]):.2f}rem"
            op = f"{random.uniform(0.45, 0.9):.2f}"
            drift = f"{random.randint(-40, 40)}px"
            html_parts.append(
                f'<span class="particle {cls}" style="--left:{left}; --delay:{delay}; --dur:{dur}; --size:{size}; --op:{op}; --drift:{drift};">{symbol}</span>'
            )
        return "".join(html_parts)

    balloons = particles("🎈", "balloon", 14, (1.1, 2.0))
    hearts = particles("❤️", "heart", 18, (1.0, 1.6))
    sparkles = particles("✦", "spark", 28, (0.7, 1.2))

    st.markdown(
        f"""
        <div class="bg-anim" aria-hidden="true">
            <div class="layer">{balloons}</div>
            <div class="layer">{hearts}</div>
            <div class="layer">{sparkles}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Authentication (Password Lock)
# ------------------------------------------------------------
PASSWORD = "bhadwi"

def render_password_gate():
    """Render an exclusive entry page that unlocks the app with correct password."""
    with st.container():
        st.markdown('<div class="glass login-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="glow login-title">Exclusive Entry 🔐</h2>', unsafe_allow_html=True)
        st.markdown('<div class="glow login-sub">Only VIPs allowed beyond this point ✨</div>', unsafe_allow_html=True)

        # Use a form so pressing Enter submits
        with st.form("password_form"):
            pwd = st.text_input("Enter password", type="password", placeholder="password")
            submitted = st.form_submit_button("Unlock ✨")

        if submitted:
            if pwd.strip() == PASSWORD:
                st.session_state["auth"] = True
                st.success("Welcome, VIP! 🎉")
                # Prefer st.rerun if available, else fallback for older versions
                _rerun = getattr(st, "rerun", None)
                if callable(_rerun):
                    _rerun()
                else:
                    st.experimental_rerun()
            else:
                st.error("Access denied. Only VIPs allowed 😎")

        st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# Main App Content
# ------------------------------------------------------------
def hero_section():
    st.markdown(
        """
        <div class="hero">
            <h1 class="hero-title glow">Happy 21st Birthday, Tanvi 🎉❤️</h1>
            <p class="hero-sub glow">You finally turned 21… but your brain is still in trial version 😂</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def photo_section():
    """Load ./pic/tanvi.jpg using PIL and display in a glassmorphism card, centered with a roast button under it."""
    img_path = Path(__file__).parent / "pic" / "tanvi.jpg"
    with st.container():
        st.markdown('<div class="glass photo-wrapper">', unsafe_allow_html=True)
        try:
            img = Image.open(img_path)
            st.image(img)
        except Exception as e:
            st.warning("Couldn't load image from ./pic/tanvi.jpg. Please make sure the file exists.")
        st.markdown('</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("Tap for a Birthday Roast 😆", key="roast_btn_inline"):
                st.session_state["roast"] = random.choice([
                    "Drama Queen since Day 1 👑",
                    "Battery 1% — dimag airplane mode",
                    "21 and still choosing chaos 💀",
                    "Warning: Overconfidence level 9000 🚨",
                    "Main character energy with side character logic 🎭",
                    "Sleep schedule: Broken. Priorities: Also broken 💤",
                    "Certified Pro in Bakchodi™ ��",
                ])
            if "roast" in st.session_state:
                st.markdown(
                    f'<div class="roast-card glow">{st.session_state["roast"]}</div>',
                    unsafe_allow_html=True,
                )


def message_card_section():
    st.markdown(
        """
        <div class="message-card">
            <div class="glow" style="white-space: pre-line; line-height: 1.45;">
Happy 21st Birthday, meri overconfident legend! 🎂
Age badh rahi hai par akal abhi bhi trial version me hai 😂
Par tension mat le — teri bakchodi ke bina zindagi boring ho jaati.
Stay toxic (for me only) 😘🎂
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def roast_section():
    """Show a button that reveals a random roast line when clicked."""
    roasts = [
        "Drama Queen since Day 1 👑",
        "Battery 1% — dimag airplane mode",
        "21 and still choosing chaos 💀",
        "Warning: Overconfidence level 9000 🚨",
        "Main character energy with side character logic 🎭",
        "Sleep schedule: Broken. Priorities: Also broken 💤",
        "Certified Pro in Bakchodi™ 🔥",
    ]

    if st.button("Tap for a Birthday Roast 😆"):
        st.session_state["roast"] = random.choice(roasts)

    if "roast" in st.session_state:
        st.markdown(
            f"""
            <div class="roast-card glow">{st.session_state['roast']}</div>
            """,
            unsafe_allow_html=True,
        )


def memories_section():
    st.markdown(
        """
        <div class="memories-grid">
            <div class="memory-card">
                <div class="memory-title glow">Late Night Chats 🌙</div>
                <div class="memory-text glow">Those 2AM therapy sessions where we talk nonsense but heal fr.</div>
            </div>
            <div class="memory-card">
                <div class="memory-title glow">Screenshot Sharing 📸</div>
                <div class="memory-text glow">From stalking to roasting — every screenshot has a story 😆</div>
            </div>
            <div class="memory-card">
                <div class="memory-title glow">Non-stop Reels 🎥</div>
                <div class="memory-text glow">1000 reels daily & still “last one I swear” 💀</div>
            </div>
            <div class="memory-card">
                <div class="memory-title glow">Roasting & Bhadwa Giri 🔥</div>
                <div class="memory-text glow">We insult each other for fun — that’s real love ❤️😂</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer_section():
    st.markdown(
        """
        <div class="footer glow">
            Made with ❤️ exclusively for Tanvi — by her favorite human
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# App Runner
# ------------------------------------------------------------
def main():
    # CSS and animated background are global
    inject_css()
    render_animated_background()

    # Password gate
    if "auth" not in st.session_state:
        st.session_state["auth"] = False

    if not st.session_state["auth"]:
        render_password_gate()
        st.stop()

    # Content after successful login
    hero_section()
    photo_section()
    message_card_section()
    memories_section()
    footer_section()


if __name__ == "__main__":
    main()
