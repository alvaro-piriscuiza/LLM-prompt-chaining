from pipeline.models import SubQuestionAnswer, FinalReport

def synthesize(question: str, answers: list[SubQuestionAnswer], call_llm, parse_json) -> FinalReport:
    """
    Format answers as bullet list so that the LLM receives a compact, readable summary of all findings rather than a raw object representation.
    """
    findings_text = "\n".join(
        f"- {a.sub_question}: {a.answer}" for a in answers
    )

    prompt = f"""You are a research assistant. Synthesize the following findings into a structured report.
    
    Original question: {question}

    Findings:
    {findings_text}

    Respond wiht JSON only, no explanation:
    {{
        "title": "...",
        "summary": "...",
        "findings": [
            {{"sub_question": "...", "answer": "..."}}
        ]
    }}"""

    raw = call_llm(prompt)
    return parse_json(raw, FinalReport)