import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from environment variable
load_dotenv()
client = OpenAI(api_key=os.getenv("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"))

st.set_page_config(page_title="Credit Memo Generator", layout="wide")
st.title("📄 AI-Powered Credit Memo Generator")

st.markdown("""
This tool uses OpenAI's GPT model to generate professional credit memos based on borrower and financial data.
Please fill in the following fields:
""")

# Input fields
with st.form("credit_memo_form"):
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business Name", placeholder="ABC Manufacturing Inc.")
        industry = st.text_input("Industry", placeholder="Light Industrial Manufacturing")
        loan_purpose = st.text_area("Loan Purpose", placeholder="Working capital to support seasonal inventory build-up")
        notes = st.text_area("Additional Notes / Risk Factors", placeholder="Customer concentration risk. Minor decline in gross margin year-over-year.")
    with col2:
        revenue = st.number_input("Annual Revenue ($)", min_value=0.0, format="%.2f")
        ebitda = st.number_input("EBITDA ($)", min_value=0.0, format="%.2f")
        debt = st.number_input("Total Debt ($)", min_value=0.0, format="%.2f")
        assets = st.number_input("Total Assets ($)", min_value=0.0, format="%.2f")
        equity = st.number_input("Total Equity ($)", min_value=0.0, format="%.2f")

    submitted = st.form_submit_button("Generate Credit Memo")

if submitted:
    with st.spinner("Generating memo with GPT-4..."):
        prompt = f"""
You are a senior credit analyst. Write a detailed and professional credit memo based on the following borrower information:

Business Name: {business_name}
Industry: {industry}
Loan Purpose: {loan_purpose}
Annual Revenue: ${revenue:,.2f}
EBITDA: ${ebitda:,.2f}
Total Debt: ${debt:,.2f}
Total Assets: ${assets:,.2f}
Total Equity: ${equity:,.2f}
Additional Notes: {notes}

Include these sections:
1. Borrower Overview
2. Loan Purpose
3. Financial Analysis (include key ratios)
4. Risk Assessment
5. Recommendation with a credit risk rating from 1 (low risk) to 5 (high risk)
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )

            credit_memo = response.choices[0].message.content
            st.subheader("📋 Generated Credit Memo")
            st.text_area("Credit Memo", credit_memo, height=500)
            st.download_button("Download as Text File", credit_memo, file_name=f"{business_name}_credit_memo.txt")
        except Exception as e:
            st.error(f"An error occurred: {e}")
