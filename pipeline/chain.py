import json
from anthropic import Anthropic
from pipeline.models import DecomposedQuestion, SubQuestionAnswer, FinalReport

client = Anthropic()

def call_llm(prompt: str, retries: int = 2) -> str:
    for attempt in range(retries + 1):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            if attempt == retries:
                raise RuntimeError(f"LLM call failed after {retries + 1} attempts: {e}")
            
def parse_json(raw: str, model):
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return model.model_validate(json.loads(raw[start:end]))
    except Exception as e:
        raise ValueError(f"Failed to parse response as {model.__name__}: {e}\nRaw: {raw}")
    
def run_pipeline(question: str) -> FinalReport:
    from pipeline.steps.decompose import decompose
    from pipeline.steps.research import reseearch
    from pipeline.steps.synthesize import synthesize

    decomposed: DecomposedQuestion = decompose(question, call_llm, parse_json)
    answers: list[SubQuestionAnswer] = research(decomposed, call_llm, parse_json)
    report: FinalReport = synthesize(question, answers, call_llm, parse_json)

    return report