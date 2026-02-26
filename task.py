## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_data_tool

## Task to verify the uploaded document is a valid financial document
verification = Task(
    description=(
        "Read the financial document at the provided file path using the read_data_tool.\n"
        "Verify that it is a legitimate financial document (e.g., quarterly report, annual report, "
        "earnings release, financial statement).\n"
        "Identify and extract:\n"
        "- Document type (10-K, 10-Q, earnings release, etc.)\n"
        "- Reporting entity / company name\n"
        "- Reporting period\n"
        "- Key sections present (income statement, balance sheet, cash flow, etc.)\n"
        "If the document is not a financial report, clearly state that and explain why."
    ),
    expected_output=(
        "A verification summary including:\n"
        "- Whether the document is a valid financial report (Yes/No)\n"
        "- Document type and reporting entity\n"
        "- Reporting period covered\n"
        "- List of key financial sections identified\n"
        "- Any anomalies or missing sections noted"
    ),
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False,
)

## Task to analyze the financial document based on user query
analyze_financial_document = Task(
    description=(
        "Analyze the financial document thoroughly to address the user's query: {query}\n"
        "Use the read_data_tool to extract data from the document.\n"
        "Focus on:\n"
        "- Key financial metrics (revenue, net income, EPS, margins, cash flow)\n"
        "- Year-over-year and quarter-over-quarter trends\n"
        "- Notable items, one-time charges, or unusual entries\n"
        "- Industry context using the search tool for current market data\n"
        "Base all analysis strictly on the document data and verified external sources."
    ),
    expected_output=(
        "A detailed financial analysis report containing:\n"
        "- Executive summary of financial performance\n"
        "- Key financial metrics with actual figures from the document\n"
        "- Trend analysis (YoY / QoQ comparisons)\n"
        "- Notable findings and their implications\n"
        "- Relevant market context from verified sources with proper citations"
    ),
    agent=financial_analyst,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Task for investment analysis
investment_analysis = Task(
    description=(
        "Based on the financial analysis, provide investment recommendations for the user's query: {query}\n"
        "Consider:\n"
        "- Valuation metrics (P/E, P/B, EV/EBITDA) relative to industry peers\n"
        "- Growth trajectory and sustainability of earnings\n"
        "- Competitive position and market dynamics\n"
        "- Balance sheet strength and capital allocation strategy\n"
        "Provide balanced recommendations that include both bull and bear cases."
    ),
    expected_output=(
        "An investment analysis report including:\n"
        "- Investment thesis (bull case and bear case)\n"
        "- Key valuation metrics and peer comparison\n"
        "- Growth drivers and potential headwinds\n"
        "- Recommended investment action with rationale\n"
        "- Important caveats and disclaimers"
    ),
    agent=investment_advisor,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Task for risk assessment
risk_assessment = Task(
    description=(
        "Conduct a comprehensive risk assessment based on the financial document.\n"
        "Address the user's query: {query}\n"
        "Evaluate:\n"
        "- Financial risks (leverage, liquidity, solvency ratios)\n"
        "- Market risks (sensitivity to macro conditions, currency, interest rates)\n"
        "- Operational risks (supply chain, concentration, regulatory)\n"
        "- Company-specific risks identified in the document\n"
        "Quantify risks where possible using data from the document."
    ),
    expected_output=(
        "A structured risk assessment including:\n"
        "- Risk summary with overall risk rating (Low / Medium / High)\n"
        "- Financial risk analysis with key ratios\n"
        "- Market and operational risk factors\n"
        "- Risk mitigation strategies observed or recommended\n"
        "- Comparison to industry risk benchmarks where available"
    ),
    agent=risk_assessor,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)