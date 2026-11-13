# 📚 EduSimplify AI
### Course Content Simplification Agent — Problem Statement #19

An AI-powered educational agent that intelligently analyses academic content and reframes explanations based on the learner's proficiency level — from **Beginner** to **Expert** — using **IBM Granite** via **IBM WatsonX AI**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎓 Proficiency-aware simplification | Rewrites content for Beginner / Intermediate / Advanced / Expert learners |
| 📊 Content complexity analysis | Instant readability metrics (word count, sentence length, complexity rating) |
| 💾 Download output | Save any simplified explanation as a `.txt` file |
| 📝 Session history | View all simplifications made during the session |
| 📋 Sample content | Built-in samples for Quantum Physics, DNA, and Neural Networks |

---

## 🛠️ Tech Stack

- **Frontend / UI** — [Streamlit](https://streamlit.io/)
- **LLM** — `ibm/granite-13b-instruct-v2` via IBM WatsonX AI
- **IBM Cloud Lite** — WatsonX AI (free tier)
- **Python** — 3.9+

---

## 🚀 Quick Start

### 1. Clone / download the project
```bash
cd EduSimplify-AI
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure IBM WatsonX credentials
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```
Edit `.env`:
```
WATSONX_API_KEY=<your IBM Cloud API key>
WATSONX_PROJECT_ID=<your WatsonX project ID>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

> **How to get credentials:**
> 1. Sign up for [IBM Cloud Lite](https://cloud.ibm.com/registration) (free).
> 2. Create a **WatsonX AI** service instance.
> 3. Go to **Manage → Access → API Keys** and generate an API key.
> 4. Open WatsonX AI, create a project, and copy its **Project ID** from the project settings.

### 5. Run the app
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 📁 Project Structure

```
EduSimplify-AI/
│
├── app.py              # Streamlit UI (main entry point)
├── agent.py            # AI agent logic — IBM Granite integration
├── requirements.txt    # Python dependencies
├── .env                # Your credentials (never commit this)
├── .env.example        # Credential template
└── README.md           # This file
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
