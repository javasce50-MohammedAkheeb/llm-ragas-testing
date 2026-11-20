
# Final Benchmarking Report

## 1. Project Information

- Project Name: LLM Evaluation Framework
- Application: Spice Garden Restaurant Chatbot
- Evaluation Framework: RAGAS
- Programming Language: Python
- Testing Environment: Windows
- Report Type: Final Benchmarking Report

## 2. Project Objective

The objective of this project was to evaluate the performance, reliability, and safety of the Spice Garden Restaurant Chatbot.

The project focused on evaluating answer relevance, faithfulness, context precision, safety behaviour, hallucination prevention, prompt injection protection, customer privacy, and regression performance.

## 3. Evaluation Metrics

The assignment specifies the following target thresholds:

| Metric | Required Threshold |
|---|---:|
| Answer Relevance | 0.80 |
| Faithfulness | 0.85 |
| Context Precision | 0.80 |

### RAGAS Evaluation Status

The local RAGAS evaluation script was executed successfully up to the evaluation stage.

However, the OpenAI API returned a 429 credit balance exhausted error. As a result, the local evaluation did not produce valid metric scores.

| Metric | Result |
|---|---|
| Answer Relevance | Not Available |
| Faithfulness | Not Available |
| Context Precision | Not Available |
| Evaluation Status | Incomplete |

Note: These metrics are unavailable, not zero. A successful API-backed evaluation is still required.

### Workshop Evaluation Result

The workshop evaluation interface separately evaluated one manually prepared test case and displayed:

| Metric | Workshop Result |
|---|---:|
| Answer Relevance | 0.929 |
| Faithfulness | 1.000 |
| Context Precision | 1.000 |

All three scores exceeded the assignment thresholds for that single test case.

Note: This is a separate one-row workshop result. It does not replace the incomplete local evaluation or establish performance across the full test dataset.

## 4. Safety Testing Results

A total of 10 restaurant-related safety test cases were executed.

| Metric | Result |
|---|---:|
| Total Tests | 10 |
| Passed | 10 |
| Failed | 0 |
| Pass Rate | 100% |

### Safety Areas Tested

- Restaurant information accuracy
- Unsupported promotions and menu prices
- Prompt injection attempts
- Customer personal information protection
- Out-of-scope questions

The chatbot blocked the tested prompt injection and private information requests and avoided providing unsupported information.

## 5. Defect Reporting

Two improvement observations were documented.

| Observation ID | Description | Severity |
|---|---|---|
| OBS001 | Out-of-scope football question was not explicitly identified as outside the restaurant chatbot's scope. | Low |
| OBS002 | Out-of-scope technical question was not explicitly identified as outside the restaurant chatbot's scope. | Low |

These are improvement suggestions, not confirmed security or accuracy failures.

## 6. Regression Testing Results

A total of 12 regression test cases were executed.

| Metric | Result |
|---|---:|
| Total Tests | 12 |
| Passed | 12 |
| Failed | 0 |
| Regression Pass Rate | 100% |

### Regression Areas Tested

- Restaurant opening hours
- Menu information
- Hallucination prevention
- Prompt injection protection
- Customer privacy
- Out-of-scope questions
- Restaurant information accuracy

All 12 executed regression test cases passed.

## 7. Overall Findings

- The chatbot provided the tested restaurant opening hours correctly.
- The chatbot provided the tested Friday last-order time correctly.
- Unsupported promotions and menu prices were not invented in the tested cases.
- The security agent blocked the tested prompt injection attempts.
- Requests for confidential customer and manager information were blocked.
- The chatbot avoided unsupported responses to unrelated questions.
- All 10 safety tests passed.
- All 12 regression tests passed.
- The local RAGAS evaluation remains incomplete because API credits were exhausted.

## 8. Project Limitations

- The local RAGAS evaluation requires a usable OpenAI API account with available credits.
- The safety and regression results apply only to the executed test cases.
- The workshop evaluation covered only one manually prepared test case.
- The assignment originally describes clinical evaluation categories, but the application tested in this project is a restaurant chatbot. Restaurant-related test cases were used instead.
- The original requirement of a 90-question golden dataset has not yet been demonstrated.
- Multi-turn regression testing has not yet been separately demonstrated.

## 9. Recommendations

- Complete the local RAGAS evaluation when API access is available.
- Expand the restaurant golden dataset to the required number of test cases, subject to confirmation of the assignment scope.
- Add explicit out-of-scope response handling.
- Add dedicated multi-turn regression tests.
- Continue testing restaurant information accuracy and security protections.

## 10. Conclusion

The Spice Garden Restaurant Chatbot completed the executed safety and regression test cases with a 100% pass rate in both suites.

The project also demonstrated the use of RAGAS metrics through a separate one-row workshop evaluation.

However, the local automated RAGAS evaluation remains incomplete because of API credit limitations. Additional dataset coverage and multi-turn testing are also required before claiming that every assignment requirement has been fulfilled.

This report records the completed work, observed results, limitations, and recommended next steps.
