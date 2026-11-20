
import os
import json
from pathlib import Path
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from datasets import Dataset

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
)


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_FILE = (
    BASE_DIR / "datasets" / "spice_garden_ragas_test_corrected.csv"
)

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. Check your .env file."
    )


# ============================================================
# 2. ASSIGNMENT ACCEPTANCE THRESHOLDS
# ============================================================

THRESHOLDS = {
    "answer_relevancy": 0.80,
    "faithfulness": 0.85,
    "context_precision": 0.80,
}


# ============================================================
# 3. LOAD AND VALIDATE TEST DATASET
# ============================================================

if not DATASET_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_FILE}"
    )

df = pd.read_csv(DATASET_FILE)

required_columns = [
    "question",
    "contexts",
    "answer",
    "ground_truth",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

if df.empty:
    raise ValueError("The test dataset is empty.")

if df[required_columns].isnull().any().any():
    raise ValueError(
        "Dataset contains empty mandatory fields."
    )


# ============================================================
# 4. CONVERT CSV DATA INTO RAGAS FORMAT
# ============================================================

records = []

for index, row in df.iterrows():

    contexts = json.loads(row["contexts"])

    if not isinstance(contexts, list):
        raise ValueError(
            f"Contexts must be a JSON list in row {index + 1}"
        )

    if not all(isinstance(item, str) for item in contexts):
        raise ValueError(
            f"Every context must be a string in row {index + 1}"
        )

    records.append({
        "user_input": str(row["question"]),
        "retrieved_contexts": contexts,
        "response": str(row["answer"]),
        "reference": str(row["ground_truth"]),
    })

dataset = Dataset.from_list(records)

print("\nDataset loaded successfully.")
print("Number of test cases:", len(records))


# ============================================================
# 5. INITIALIZE EVALUATION MODELS
# ============================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=API_KEY,
)

evaluator_llm = LangchainLLMWrapper(llm)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=API_KEY,
)

evaluator_embeddings = LangchainEmbeddingsWrapper(
    embeddings
)


# ============================================================
# 6. EXECUTE RAGAS EVALUATION
# ============================================================

print("\nStarting RAGAS evaluation...")

results = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
    ],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
)

results_df = results.to_pandas()


# ============================================================
# 7. CALCULATE PASS / FAIL STATUS
# ============================================================

for metric, threshold in THRESHOLDS.items():

    results_df[metric] = pd.to_numeric(
        results_df[metric],
        errors="coerce"
    )

    results_df[f"{metric}_status"] = results_df[metric].apply(
        lambda score: (
            "PASS"
            if pd.notna(score) and score >= threshold
            else "FAIL"
        )
    )

results_df["overall_status"] = results_df.apply(
    lambda row: (
        "PASS"
        if all(
            row[f"{metric}_status"] == "PASS"
            for metric in THRESHOLDS
        )
        else "FAIL"
    ),
    axis=1,
)


# ============================================================
# 8. GENERATE SUMMARY
# ============================================================

total_tests = len(results_df)

passed_tests = (
    results_df["overall_status"] == "PASS"
).sum()

failed_tests = total_tests - passed_tests

pass_rate = (passed_tests / total_tests) * 100

average_scores = {
    metric: results_df[metric].mean()
    for metric in THRESHOLDS
}


# ============================================================
# 9. SAVE EXECUTION REPORT
# ============================================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

report_file = (
    REPORT_DIR / f"evaluation_results_{timestamp}.csv"
)

summary_file = (
    REPORT_DIR / f"evaluation_summary_{timestamp}.txt"
)

results_df.to_csv(report_file, index=False)

with open(summary_file, "w", encoding="utf-8") as file:

    file.write("RAGAS EVALUATION SUMMARY\n")
    file.write("========================\n\n")

    file.write(f"Total test cases: {total_tests}\n")
    file.write(f"Passed tests: {passed_tests}\n")
    file.write(f"Failed tests: {failed_tests}\n")
    file.write(f"Regression-style pass rate: {pass_rate:.2f}%\n\n")

    for metric, score in average_scores.items():

        file.write(
            f"{metric}: {score:.4f} "
            f"(threshold: {THRESHOLDS[metric]:.2f})\n"
        )


# ============================================================
# 10. DISPLAY RESULTS
# ============================================================

print("\n======================================")
print("       RAGAS EVALUATION RESULTS")
print("======================================")

print("\nTotal test cases:", total_tests)
print("Passed tests:", passed_tests)
print("Failed tests:", failed_tests)
print(f"Pass rate: {pass_rate:.2f}%")

print("\nAverage Metric Scores:")

for metric, score in average_scores.items():

    print(
        f"{metric}: {score:.4f} "
        f"(threshold: {THRESHOLDS[metric]:.2f})"
    )

print("\nRow-Level Results:")

display_columns = [
    "user_input",
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "overall_status",
]

print(results_df[display_columns].to_string(index=False))

print("\nReports saved successfully:")
print(report_file)
print(summary_file)

print("\nEvaluation completed.")
