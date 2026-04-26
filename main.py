import sys
from dotenv import load_dotenv

# load_dotenv must run before pipeline imports as chain.py initialises LLM at module level and reads env vars on import
load_dotenv()

from pipeline.chain import run_pipeline

def main():
    # Safeguard for cases where user calls: python main.py without a question
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your research question here\"")
        sys.exit(1)

    # Get question from CLI arguments
    question = sys.argv[1]
    print(f"\nResearching: {question}\n")

    # Run research pipeline
    report = run_pipeline(question)

    # Output research report
    print(f"# {report.title}\n")
    print(f"{report.summary}\n")
    print("## Findings\n")
    for finding in report.findings:
        print(f"**{finding.sub_question}**")
        print(f"{finding.answer}\n")

if __name__ == "__main__":
    main()