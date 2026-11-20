
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="LLM Evaluation Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. PROJECT PATHS AND THRESHOLDS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"

THRESHOLDS = {
    "answer_relevancy": 0.80,
    "faithfulness": 0.85,
    "context_precision": 0.80
}

# ==========================================
# 3. DASHBOARD HEADER
# ==========================================

st.title("📊 LLM Evaluation Dashboard")

st.write(
    "Clinical Review Assistant - Evaluation Results"
)

st.divider()

# ==========================================
# 4. FIND EVALUATION REPORTS
# ==========================================

report_files = sorted(
    REPORTS_DIR.glob("evaluation_results_*.csv"),
    reverse=True
)

if not report_files:
    st.warning(
        "No evaluation reports found. "
        "Run the evaluation script first."
    )
    st.stop()

selected_report = st.selectbox(
    "Select an evaluation report",
    report_files,
    format_func=lambda x: x.name
)

# ==========================================
# 5. LOAD REPORT
# ==========================================

try:
    df = pd.read_csv(selected_report)
except Exception as error:
    st.error(f"Unable to load report: {error}")
    st.stop()

if df.empty:
    st.warning("The selected evaluation report is empty.")
    st.stop()

# ==========================================
# 6. PREPARE METRIC DATA
# ==========================================

for metric in THRESHOLDS:
    if metric in df.columns:
        df[metric] = pd.to_numeric(
            df[metric], errors="coerce"
        )

available_metrics = [
    metric for metric in THRESHOLDS
    if metric in df.columns
]

valid_scores_exist = any(
    df[metric].notna().any()
    for metric in available_metrics
)

# ==========================================
# 7. OVERALL EVALUATION STATUS
# ==========================================

st.subheader("Overall Evaluation Status")

if valid_scores_exist:
    st.success(
        "Evaluation scores are available. "
        "Review the metric results below."
    )
else:
    st.warning(
        "Evaluation incomplete: No valid metric scores "
        "are available. Check API credits and rerun "
        "the evaluation."
    )

st.divider()

# ==========================================
# 8. EVALUATION OVERVIEW
# ==========================================

st.subheader("Evaluation Overview")

total_tests = len(df)

passed = 0
failed = 0
unavailable = 0

if "overall_status" in df.columns:
    statuses = df["overall_status"].astype(str).str.upper()

    passed = (statuses == "PASS").sum()
    failed = (statuses == "FAIL").sum()

    unavailable = (
        ~statuses.isin(["PASS", "FAIL"])
    ).sum()

else:
    unavailable = total_tests

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Test Cases", total_tests)
col2.metric("Passed", int(passed))
col3.metric("Failed", int(failed))
col4.metric("Unavailable", int(unavailable))

st.divider()

# ==========================================
# 9. METRIC PERFORMANCE
# ==========================================

st.subheader("Metric Performance")

metric_columns = st.columns(3)

metric_averages = {}

for col, metric in zip(
    metric_columns,
    THRESHOLDS
):
    with col:

        metric_name = metric.replace(
            "_", " "
        ).title()

        if metric not in df.columns:
            st.metric(metric_name, "N/A")
            st.caption("Metric column not found")
            continue

        scores = df[metric].dropna()

        if scores.empty:
            st.metric(metric_name, "N/A")
            st.caption("No valid scores available")

        else:
            average = scores.mean()
            threshold = THRESHOLDS[metric]

            metric_averages[metric_name] = average

            st.metric(
                metric_name,
                f"{average:.3f}",
                delta=f"{average - threshold:+.3f} vs threshold"
            )

            if average >= threshold:
                st.success(
                    f"Meets threshold ({threshold:.2f})"
                )
            else:
                st.error(
                    f"Below threshold ({threshold:.2f})"
                )

st.divider()

# ==========================================
# 10. METRIC COMPARISON CHART
# ==========================================

st.subheader("Metric Comparison")

if metric_averages:

    chart_data = pd.DataFrame({
        "Metric": list(metric_averages.keys()),
        "Average Score": list(metric_averages.values())
    })

    st.bar_chart(
        chart_data.set_index("Metric")
    )

    st.caption(
        "Metric averages are calculated using valid scores only."
    )

else:
    st.info(
        "Metric comparison chart will appear "
        "when valid evaluation scores are available."
    )

st.divider()

# ==========================================
# 11. PASS / FAIL CHART
# ==========================================

st.subheader("Test Case Pass / Fail Distribution")

if passed + failed > 0:

    status_data = pd.DataFrame({
        "Status": ["Passed", "Failed"],
        "Count": [passed, failed]
    })

    st.bar_chart(
        status_data.set_index("Status")
    )

else:
    st.info(
        "Pass/fail chart will appear when "
        "evaluation results are available."
    )

st.divider()

# ==========================================
# 12. TEST CASE RESULTS
# ==========================================

st.subheader("Test Case Results")

st.dataframe(
    df,
    use_container_width=True
)

# ==========================================
# 13. DOWNLOAD REPORT
# ==========================================

st.subheader("Download Evaluation Report")

csv_data = df.to_csv(index=False)

st.download_button(
    label="Download Evaluation Report",
    data=csv_data,
    file_name="evaluation_report.csv",
    mime="text/csv"
)

# ==========================================
# 14. ASSIGNMENT THRESHOLDS
# ==========================================

st.divider()

st.subheader("Assignment Evaluation Thresholds")

threshold_data = pd.DataFrame({
    "Metric": [
        "Answer Relevance",
        "Faithfulness",
        "Context Precision"
    ],
    "Required Threshold": [
        0.80,
        0.85,
        0.80
    ]
})

st.table(threshold_data)

st.caption(
    "Note: Missing metric scores are displayed as N/A. "
    "They are not treated as zero or valid evaluation results."
)

st.caption(
    "Clinical Review Assistant | LLM Evaluation Framework"
)
