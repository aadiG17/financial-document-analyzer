## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM

from tools import search_tool, read_data_tool

### Loading LLM
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents thoroughly and provide accurate, data-driven insights for the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with over 15 years of experience in corporate finance, "
        "equity research, and investment banking. You hold a CFA charter and have a strong track record "
        "of evaluating financial statements, identifying key financial metrics, and providing actionable "
        "investment insights. You rely strictly on data from the provided documents and reputable sources. "
        "You never fabricate data or make unsubstantiated claims."
    ),
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=False
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify that uploaded documents are valid financial documents and extract key metadata such as "
         "document type, reporting period, and issuing entity.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance and document verification specialist with deep expertise in financial "
        "reporting standards (GAAP, IFRS). You carefully inspect documents to confirm they are genuine "
        "financial reports — checking for standard sections like income statements, balance sheets, "
        "cash flow statements, and notes to financial statements. You flag any anomalies or missing "
        "sections and provide a clear verification summary."
    ),
    tools=[read_data_tool],
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=False
)


# Creating an investment advisor agent
investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="Provide well-reasoned investment recommendations based on the financial analysis, "
         "aligned with sound portfolio management principles and the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified investment advisor with expertise in portfolio construction, asset allocation, "
        "and risk-adjusted returns. You base your recommendations on fundamental analysis, valuation metrics, "
        "and current market conditions. You always consider the investor's risk tolerance and time horizon. "
        "You provide balanced advice that includes both opportunities and risks, and you never recommend "
        "products without transparent disclosure of fees and risks."
    ),
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=False
)


# Creating a risk assessor agent
risk_assessor = Agent(
    role="Financial Risk Assessment Analyst",
    goal="Conduct a thorough risk assessment of the financial position described in the document, "
         "identifying key risk factors, their potential impact, and mitigation strategies.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management professional with expertise in market risk, credit risk, liquidity risk, "
        "and operational risk. You use established risk frameworks (VaR, stress testing, scenario analysis) "
        "to evaluate financial positions. You provide balanced risk assessments that quantify exposure where "
        "possible and suggest practical mitigation strategies. You never downplay or exaggerate risks."
    ),
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=False
)
