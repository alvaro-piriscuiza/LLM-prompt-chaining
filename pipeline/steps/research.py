from pipeline.models import DecomposedQuestion, SubQuestionAnswer

def research(decomposed: DecomposedQuestion, call_llm, parse_json) -> list[SubQuestionAnswer]:
    """
    Feeds the LLM the list of decomposed questions in order for research.
    """
    answers = []

    for sub_question in decomposed.sub_questions:
        prompt = f"""Answer the following research sub-question concisely and factually.
        
        Sub-question: {sub_question}

        Respond with JSON only, no explanation. The "answer" field must be a plain text string - not a list, not a nested object.
        {{
            "sub_question": "{sub_question}",
            "answer": "..."
        }}"""

        raw = call_llm(prompt)
        answer = parse_json(raw, SubQuestionAnswer)
        answers.append(answer)
    
    return answers