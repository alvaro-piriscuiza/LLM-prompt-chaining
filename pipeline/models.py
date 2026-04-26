from pydantic import BaseModel

class DecomposedQuestion(BaseModel):
    sub_questions: list[str]

class SubQuestionAnswer(BaseModel):
    sub_question: str
    answer: str

class FinalReport(BaseModel):
    title: str
    summary: str
    findings: list[SubQuestionAnswer]