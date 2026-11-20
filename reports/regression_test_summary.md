
# Regression Testing Summary Report

## 1. Project Information

- Project Name: LLM Evaluation Framework
- Application: Spice Garden Restaurant Chatbot
- Testing Type: Regression Testing
- Test Dataset: regression_test_cases.csv
- Results File: regression_test_results.csv

## 2. Testing Overview

A total of 12 regression test cases were executed
to verify that the Spice Garden chatbot continues
to provide accurate and safe responses.

## 3. Test Execution Summary

| Metric | Result |
|---|---:|
| Total Test Cases | 12 |
| Passed | 12 |
| Failed | 0 |
| Pass Rate | 100% |

## 4. Categories Tested

- Restaurant Hours
- Menu Information
- Hallucination
- Prompt Injection
- Customer Privacy
- Out of Scope Handling
- Restaurant Information

## 5. Key Findings

- The chatbot correctly provided restaurant opening hours.
- The chatbot provided the Friday last-order time correctly.
- The chatbot avoided inventing unsupported menu prices and promotions.
- The security agent blocked prompt injection attempts.
- The chatbot blocked requests for confidential customer and manager information.
- The chatbot avoided unsupported answers to unrelated questions.
- The chatbot correctly provided the weekly restaurant opening-hours schedule.

## 6. Conclusion

All 12 executed regression test cases passed.

The chatbot demonstrated expected behaviour across
restaurant information, hallucination prevention,
prompt injection protection, customer privacy,
and out-of-scope questions.

The regression testing pass rate was 100%.

Note: Results apply only to the 12 test cases executed.
