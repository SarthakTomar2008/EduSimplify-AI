"""
EduSimplify AI Agent
Analyzes academic content and reframes explanations based on learner proficiency.
Powered by IBM Granite via IBM WatsonX AI.
"""

import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

load_dotenv()

# ---------------------------------------------------------------------------
# Proficiency level definitions
# ---------------------------------------------------------------------------
LEVEL_DESCRIPTIONS = {
    "Beginner": (
        "a complete beginner with no prior knowledge of the topic. "
        "Use very simple language, everyday analogies, avoid all jargon, "
        "and explain every technical term if you must use one."
    ),
    "Intermediate": (
        "a student who knows the basics but is still learning. "
        "Use clear language, introduce domain terms with brief explanations, "
        "and use relatable examples."
    ),
    "Advanced": (
        "an advanced learner who is comfortable with the subject. "
        "Use accurate technical language, go deeper into mechanisms, "
        "and reference related concepts freely."
    ),
    "Expert": (
        "a subject-matter expert or researcher. "
        "Use precise technical terminology, assume full domain knowledge, "
        "and focus on nuance, edge cases, and connections to cutting-edge ideas."
    ),
}

# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------
SIMPLIFY_SYSTEM = (
    "You are EduSimplify, an expert educational AI tutor. "
    "Your job is to rewrite academic content so it is perfectly suited "
    "to the learner's proficiency level. Always:\n"
    "- Preserve factual accuracy.\n"
    "- Adjust vocabulary, depth, and examples to match the level.\n"
    "- Use numbered key points for clarity.\n"
    "- End with a 'Key Takeaway' section (1-2 sentences)."
)


def build_prompt(content: str, level: str, topic: str = "") -> str:
    level_desc = LEVEL_DESCRIPTIONS.get(level, LEVEL_DESCRIPTIONS["Intermediate"])
    topic_hint = f" on the topic of '{topic}'" if topic.strip() else ""
    return (
        f"{SIMPLIFY_SYSTEM}\n\n"
        f"### Learner Profile\n"
        f"The learner is {level_desc}\n\n"
        f"### Original Academic Content{topic_hint}\n"
        f"{content.strip()}\n\n"
        f"### Simplified Explanation (for a {level} learner)\n"
    )


# ---------------------------------------------------------------------------
# WatsonX client initialisation
# ---------------------------------------------------------------------------
def _get_model() -> ModelInference:
    api_key = os.getenv("WATSONX_API_KEY", "")
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    if not api_key or not project_id:
        raise EnvironmentError(
            "WATSONX_API_KEY and WATSONX_PROJECT_ID must be set in your .env file."
        )

    credentials = Credentials(url=url, api_key=api_key)

    params = {
        GenParams.MAX_NEW_TOKENS: 1024,
        GenParams.TEMPERATURE: 0.4,
        GenParams.TOP_P: 0.9,
        GenParams.REPETITION_PENALTY: 1.1,
        GenParams.STOP_SEQUENCES: ["###"],
    }

    model = ModelInference(
        model_id="ibm/granite-4-h-small",
        params=params,
        credentials=credentials,
        project_id=project_id,
    )
    return model


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def simplify_content(content: str, level: str, topic: str = "") -> str:
    """
    Simplify the given academic `content` for the specified proficiency `level`.

    Parameters
    ----------
    content : str
        The raw educational text to simplify.
    level : str
        One of 'Beginner', 'Intermediate', 'Advanced', 'Expert'.
    topic : str, optional
        A short label for the topic (improves prompt context).

    Returns
    -------
    str
        The AI-generated simplified explanation.
    """
    model = _get_model()
    prompt = build_prompt(content, level, topic)
    response = model.generate_text(prompt=prompt)
    return response.strip() if response else "No response received from the model."


def analyze_content(content: str) -> dict:
    """
    Run a quick structural analysis of the input content.
    Returns basic readability metadata without calling the LLM.
    """
    words = content.split()
    sentences = [s.strip() for s in content.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
    avg_sent_len = len(words) / max(len(sentences), 1)

    if avg_word_len > 6.5 or avg_sent_len > 25:
        complexity = "High"
    elif avg_word_len > 5.0 or avg_sent_len > 15:
        complexity = "Medium"
    else:
        complexity = "Low"

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_word_length": round(avg_word_len, 2),
        "avg_sentence_length": round(avg_sent_len, 2),
        "estimated_complexity": complexity,
    }
