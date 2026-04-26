import sys
from dotenv import load_dotenv

load_dotenv()

from pipeline.chain import run_pipeline

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your research question here\"")
        sys.exit(1)

    question = sys.argv[1]
    print(f"\nResearching: {question}\n")

    report = run_pipeline(question)

    print(f"# {report.title}\n")
    print(f"{report.summary}\n")
    print("## Findings\n")
    for finding in report.findings:
        print(f"**{finding.sub_question}**")
        print(f"{finding.answer}\n")

if __name__ == "__main__":
    main()