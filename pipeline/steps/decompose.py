from pipeline.models import DecomposedQuestion

def decompose(question: str, call_llm, parse_json) -> DecomposedQuestion:
    prompt = f"""Break the following research question into 3-5 focused sub-questions.
    
    Question: {question}

    Respond with JSON only, no explanation:
    {{
        "sub_questions": ["...", "...", "..."]
    }}"""

    raw = call_llm(prompt)
    return parse_json(raw, DecomposedQuestion)