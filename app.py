"""
EduSimplify AI — Streamlit Application
Course Content Simplification Agent powered by IBM Granite (WatsonX AI)
"""

import streamlit as st
from agent import simplify_content, analyze_content, LEVEL_DESCRIPTIONS

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="EduSimplify AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* ── global ── */
        [data-testid="stAppViewContainer"] {
            background: #f0f4f8;
        }
        /* ── header banner ── */
        .edu-header {
            background: linear-gradient(135deg, #1a56db 0%, #7c3aed 100%);
            border-radius: 14px;
            padding: 2rem 2.5rem 1.6rem;
            color: #fff;
            margin-bottom: 1.5rem;
        }
        .edu-header h1 { margin: 0; font-size: 2.2rem; letter-spacing: -0.5px; }
        .edu-header p  { margin: 0.4rem 0 0; font-size: 1.05rem; opacity: .88; }
        /* ── level badge ── */
        .level-pill {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            margin-right: 6px;
        }
        .pill-beginner     { background:#dcfce7; color:#166534; }
        .pill-intermediate { background:#fef9c3; color:#854d0e; }
        .pill-advanced     { background:#dbeafe; color:#1e40af; }
        .pill-expert       { background:#f3e8ff; color:#6b21a8; }
        /* ── metric cards ── */
        .metric-card {
            background: #fff;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .metric-card .val { font-size: 1.6rem; font-weight: 700; color: #1a56db; }
        .metric-card .lbl { font-size: 0.78rem; color: #64748b; margin-top: 2px; }
        /* ── output box ── */
        .output-box {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #1a56db;
            border-radius: 10px;
            padding: 1.4rem 1.6rem;
            line-height: 1.75;
            font-size: 0.98rem;
        }
        /* ── complexity badge ── */
        .complexity-high   { color:#b91c1c; font-weight:700; }
        .complexity-medium { color:#d97706; font-weight:700; }
        .complexity-low    { color:#15803d; font-weight:700; }
        /* ── sidebar ── */
        [data-testid="stSidebar"] {
            background: #1e293b;
        }
        [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stTextInput label { color: #94a3b8 !important; font-size:0.82rem; }
        /* ── typed text inside sidebar inputs must be black ── */
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] input::placeholder,
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div,
        [data-testid="stSidebar"] [data-baseweb="input"] input { color: #111827 !important; }
        [data-testid="stSidebar"] input::placeholder { color: #6b7280 !important; opacity: 1; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar — configuration
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    level = st.selectbox(
        "Proficiency Level",
        options=list(LEVEL_DESCRIPTIONS.keys()),
        index=1,
        help="Select the learner's current knowledge level.",
    )

    topic = st.text_input(
        "Topic / Subject (optional)",
        placeholder="e.g. Quantum Mechanics, Neural Networks …",
        help="Providing a topic improves simplification accuracy.",
    )

    st.markdown("---")
    st.markdown("### 📖 Level Guide")

    pill_classes = {
        "Beginner": "beginner",
        "Intermediate": "intermediate",
        "Advanced": "advanced",
        "Expert": "expert",
    }
    for lvl, desc in LEVEL_DESCRIPTIONS.items():
        pill_cls = pill_classes[lvl]
        st.markdown(
            f'<span class="level-pill pill-{pill_cls}">{lvl}</span>', unsafe_allow_html=True
        )
        st.caption(desc)
        st.write("")

    st.markdown("---")
    st.markdown(
        "<small style='color:#64748b'>Powered by **IBM Granite** via WatsonX AI</small>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="edu-header">
        <h1>📚 EduSimplify AI</h1>
        <p>Course Content Simplification Agent — Personalised explanations for every learner</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Main layout: input + output
# ---------------------------------------------------------------------------
col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.markdown("#### ✍️ Paste Academic Content")
    content_input = st.text_area(
        label="Academic content",
        placeholder=(
            "Paste lecture notes, textbook paragraphs, research summaries, "
            "or any educational material here …"
        ),
        height=320,
        label_visibility="collapsed",
    )

    # Sample content buttons
    st.caption("Or load a sample:")
    s_col1, s_col2, s_col3 = st.columns(3)

    SAMPLES = {
        "⚛️ Quantum": (
            "Quantum entanglement is a physical phenomenon that occurs when a group of particles "
            "are generated, interact, or share spatial proximity in such a way that the quantum state "
            "of each particle of the group cannot be described independently of the state of the others, "
            "even when the particles are separated by a large distance. Measurements of physical properties "
            "such as position, momentum, spin, and polarization performed on entangled particles can, in some "
            "cases, be found to be perfectly correlated. The quantum state of the composite system must be "
            "described using a superposition of product states, and this superposition cannot in general be "
            "factored as a product of states of its local constituents."
        ),
        "🧬 DNA": (
            "Deoxyribonucleic acid (DNA) is a polymer composed of two polynucleotide chains that coil around "
            "each other to form a double helix. The polymer carries genetic instructions for the development, "
            "functioning, growth and reproduction of all known organisms and many viruses. DNA and ribonucleic "
            "acid (RNA) are nucleic acids. Alongside proteins, lipids and complex carbohydrates (polysaccharides), "
            "nucleic acids are one of the four major types of macromolecules that are essential for all known forms "
            "of life. The two DNA strands are known as polynucleotides as they are composed of simpler monomeric "
            "units called nucleotides. Each nucleotide is composed of one of four nitrogen-containing nucleobases "
            "(cytosine [C], guanine [G], adenine [A] or thymine [T]), a sugar called deoxyribose, and a phosphate group."
        ),
        "🤖 Neural Nets": (
            "An artificial neural network (ANN) is a computational model inspired by the structure and functions "
            "of biological neural networks. ANNs consist of layers of interconnected nodes or neurons. Each connection "
            "is associated with a weight, which is adjusted during training using a process called backpropagation "
            "combined with gradient descent optimization. The network learns a mapping from inputs to outputs by "
            "iteratively minimising a loss function. Deep neural networks, which have multiple hidden layers, "
            "are capable of learning hierarchical feature representations and have achieved state-of-the-art "
            "performance on tasks such as image recognition, natural language processing, and reinforcement learning."
        ),
    }

    with s_col1:
        if st.button("⚛️ Quantum", use_container_width=True):
            st.session_state["sample_text"] = SAMPLES["⚛️ Quantum"]
            st.session_state["sample_topic"] = "Quantum Entanglement"
    with s_col2:
        if st.button("🧬 DNA", use_container_width=True):
            st.session_state["sample_text"] = SAMPLES["🧬 DNA"]
            st.session_state["sample_topic"] = "DNA Structure"
    with s_col3:
        if st.button("🤖 Neural Nets", use_container_width=True):
            st.session_state["sample_text"] = SAMPLES["🤖 Neural Nets"]
            st.session_state["sample_topic"] = "Neural Networks"

    # Apply sample if loaded
    if "sample_text" in st.session_state and not content_input:
        content_input = st.session_state["sample_text"]
        topic = st.session_state.get("sample_topic", topic)

    simplify_btn = st.button(
        "✨ Simplify Content",
        type="primary",
        use_container_width=True,
        disabled=not content_input.strip(),
    )

with col_out:
    st.markdown("#### 📊 Content Analysis")

    if content_input.strip():
        stats = analyze_content(content_input)
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'<div class="metric-card"><div class="val">{stats["word_count"]}</div>'
                f'<div class="lbl">Words</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="metric-card"><div class="val">{stats["sentence_count"]}</div>'
                f'<div class="lbl">Sentences</div></div>',
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f'<div class="metric-card"><div class="val">{stats["avg_word_length"]}</div>'
                f'<div class="lbl">Avg Word Len</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            cplx = stats["estimated_complexity"]
            cplx_class = f"complexity-{cplx.lower()}"
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="val"><span class="{cplx_class}">{cplx}</span></div>'
                f'<div class="lbl">Complexity</div></div>',
                unsafe_allow_html=True,
            )
        st.write("")

    # ── Simplification output ──
    st.markdown("#### 🎓 Simplified Explanation")

    if "simplified_result" not in st.session_state:
        st.session_state["simplified_result"] = None
    if "result_level" not in st.session_state:
        st.session_state["result_level"] = None

    if simplify_btn and content_input.strip():
        with st.spinner(f"IBM Granite is simplifying content for a **{level}** learner …"):
            try:
                result = simplify_content(content_input, level, topic)
                st.session_state["simplified_result"] = result
                st.session_state["result_level"] = level
            except EnvironmentError as e:
                st.error(f"⚠️ Configuration Error: {e}")
                st.info("Please set your `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` in the `.env` file.")
                st.session_state["simplified_result"] = None
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
                st.session_state["simplified_result"] = None

    if st.session_state["simplified_result"]:
        pill_cls = pill_classes.get(st.session_state["result_level"], "intermediate")
        st.markdown(
            f'<span class="level-pill pill-{pill_cls}">'
            f'{st.session_state["result_level"]} Level</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="output-box">{st.session_state["simplified_result"].replace(chr(10), "<br>")}</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        # Download button
        st.download_button(
            label="⬇️ Download Explanation",
            data=st.session_state["simplified_result"],
            file_name=f"simplified_{st.session_state['result_level'].lower()}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    elif not simplify_btn:
        st.info("👈 Paste your content and click **Simplify Content** to get started.")

# ---------------------------------------------------------------------------
# History section
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 📝 Session History")

if "history" not in st.session_state:
    st.session_state["history"] = []

if simplify_btn and content_input.strip() and st.session_state.get("simplified_result"):
    st.session_state["history"].append(
        {
            "topic": topic if topic.strip() else "Untitled",
            "level": level,
            "input_preview": content_input[:120] + ("…" if len(content_input) > 120 else ""),
            "output": st.session_state["simplified_result"],
        }
    )

if st.session_state["history"]:
    for i, entry in enumerate(reversed(st.session_state["history"]), 1):
        pill_cls = pill_classes.get(entry["level"], "intermediate")
        with st.expander(
            f"#{len(st.session_state['history']) - i + 1}  |  "
            f"{entry['topic']}  —  {entry['level']} Level",
            expanded=False,
        ):
            st.markdown(f"**Input preview:** _{entry['input_preview']}_")
            st.markdown("**Simplified Output:**")
            st.markdown(
                f'<div class="output-box" style="font-size:0.92rem">'
                f'{entry["output"].replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True,
            )
else:
    st.caption("No history yet. Simplify some content to see it here.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:3rem; color:#94a3b8; font-size:0.82rem; border-top:1px solid #e2e8f0; padding-top:1rem;">
        EduSimplify AI &nbsp;|&nbsp; Powered by <strong>IBM Granite</strong> (WatsonX AI) &nbsp;|&nbsp;
        Problem Statement #19 — Course Content Simplification Agent
    </div>
    """,
    unsafe_allow_html=True,
)
