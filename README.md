# 📚 EduSimplify AI
### Course Content Simplification Agent — Problem Statement #19

An AI-powered educational agent that intelligently analyses academic content and reframes explanations based on the learner's proficiency level — from **Beginner** to **Expert** — using **IBM Granite** via **IBM WatsonX AI**.

Built with **Langflow** (visual flow) + **Streamlit** (web UI).

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎓 Proficiency-aware simplification | Rewrites content for Beginner / Intermediate / Advanced / Expert learners |
| 🔀 Langflow visual pipeline | Drag-and-drop flow: Input → Prompt → IBM Granite → Output |
| 📊 Content complexity analysis | Instant readability metrics (word count, sentence length, complexity rating) |
| 💾 Download output | Save any simplified explanation as a `.txt` file |
| 📝 Session history | View all simplifications made during the session |
| 📋 Sample content | Built-in samples for Quantum Physics, DNA, and Neural Networks |

---

## 🛠️ Tech Stack

- **Visual Flow** — [Langflow](https://github.com/logspace-ai/langflow)
- **Frontend / UI** — [Streamlit](https://streamlit.io/)
- **LLM** — `ibm/granite-4-h-small` via IBM WatsonX AI
- **IBM Cloud Lite** — WatsonX AI (free tier)
- **Python** — 3.9+

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure IBM WatsonX credentials
Copy `.env.example` to `.env` and fill in your values:
```
WATSONX_API_KEY=<your IBM Cloud API key>
WATSONX_PROJECT_ID=<your WatsonX project ID>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

> **Get credentials:** Sign up at [IBM Cloud Lite](https://cloud.ibm.com/registration) → create a WatsonX AI service → generate an API key → copy the Project ID from project settings.

---

## 🔀 Option A — Run with Langflow (Visual Flow)

```bash
py run_langflow.py
```

This starts Langflow at **http://localhost:7860** and auto-imports the `edusimplify_flow.json` flow.

### Flow architecture
```
[Academic Content Input]  ─┐
[Proficiency Level Input]  ─┼──► [EduSimplify Prompt] ──► [IBM Granite 4H] ──► [Output]
[Topic Input]              ─┘
```

### Configure the WatsonX node
Inside Langflow, click the **IBM Granite (WatsonX AI)** node and fill in:
- **IBM Cloud API Key** — your `WATSONX_API_KEY`
- **WatsonX Project ID** — your `WATSONX_PROJECT_ID`

Then click **▶ Run** to get the simplified explanation.

---

## 🌐 Option B — Run with Streamlit (Web App)

```bash
py -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
```

Opens at **http://localhost:8501**

---

## 📁 Project Structure

```
EduSimplify-AI/
│
├── app.py                  # Streamlit web UI
├── agent.py                # IBM Granite AI agent logic
├── run_langflow.py         # Langflow server launcher + auto-import
├── edusimplify_flow.json   # Langflow flow definition (importable)
├── requirements.txt        # Python dependencies
├── .env                    # Your credentials (never commit this)
├── .env.example            # Credential template
└── README.md               # This file
```

---

## 🎯 Proficiency Levels

| Level | Who it's for |
|---|---|
| **Beginner** | No prior knowledge; uses everyday analogies, zero jargon |
| **Intermediate** | Knows basics; introduces terms with brief explanations |
| **Advanced** | Comfortable learner; full technical language, deeper mechanisms |
| **Expert** | Researcher / practitioner; precise terminology, nuance, edge cases |

---

## 🔒 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `WATSONX_API_KEY` | ✅ | IBM Cloud API key |
| `WATSONX_PROJECT_ID` | ✅ | WatsonX AI Project ID |
| `WATSONX_URL` | Optional | Defaults to `https://us-south.ml.cloud.ibm.com` |

---

## 📄 License

MIT License — free for educational and research use.
