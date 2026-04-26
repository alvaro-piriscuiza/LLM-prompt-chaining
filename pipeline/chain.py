import json
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from pipeline.models import DecomposedQuestion, SubQuestionAnswer, FinalReport

# Initialised at module call so that the LLM client can be shared across all pipeline steps without needing reconnection on every call.
endpoint = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",
    task="conversational",
    huggingfacehub_api_token=os.getenv("HF_API_TOKEN"),
    max_new_tokens=1024,
    temperature=0.3,
)
llm = ChatHuggingFace(llm=endpoint)

def call_llm(prompt: str, retries: int = 2) -> str:
    """
    Invoke the LLM with automatic retry on transient failures.
    """
    for attempt in range(retries + 1):
        try:
            ai_msg = llm.invoke(prompt)
            return ai_msg.content
        except Exception as e:
            if attempt == retries:
                raise RuntimeError(f"LLM call failed after {retries + 1} attempts: {e}")
            
def parse_json(raw: str, model):
    """
    Extract and validatre a JSON object from a raw LLM response.

    LLMs often wrap JSON in markdown fences or prepend explanation text.
    Slicing from the firs '{' to the lat '}' allows to strip the noise before parsing.
    """
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return model.model_validate(json.loads(raw[start:end]))
    except Exception as e:
        raise ValueError(f"Failed to parse response as {model.__name__}: {e}\nRaw: {raw}")
    
def run_pipeline(question: str) -> FinalReport:
    """
    Run the full three-step research pipeline.
    """
    # Steps are imported locally to keep their dependencies explicit at the moment of use.
    from pipeline.steps.decompose import decompose
    from pipeline.steps.research import research
    from pipeline.steps.synthesize import synthesize

    # Each step employs the output from the last as an input.
    decomposed: DecomposedQuestion = decompose(question, call_llm, parse_json)
    answers: list[SubQuestionAnswer] = research(decomposed, call_llm, parse_json)
    report: FinalReport = synthesize(question, answers, call_llm, parse_json)

    return report