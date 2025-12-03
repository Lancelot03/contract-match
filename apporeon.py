import streamlit as st
import openai
import json
from io import StringIO
import pypdf
import docx

# --- Hardcoded Orane Standard Contract ---
# This text is extracted from the uploaded 'converted_text.pdf' and is the basis for compliance.
ORANE_STANDARD_CONTRACT = """
SOFTWARE DEVELOPMENT SERVICES
AGREEMENT
ORANE TECHNOLOGIES PVT. LTD. - STANDARD
CONTRACT
Effective Date: January 1, 2025
Contract ID: ORANE-STD-2025-001

1. PARTIES
This Agreement is entered into between:
ORANE TECHNOLOGIES PVT. LTD.
Address: Tower A, Cyber City, Gurgaon, Haryana 122002, India
 ("Service Provider" or "Orane")
AND
[CLIENT NAME]
Address: [CLIENT ADDRESS]
("Client")

2. SCOPE OF SERVICES
2.1 Orane agrees to provide software development, implementation, and maintenance services as described
 in the Statement of Work (SOW) attached as Exhibit A.
2.2 All deliverables shall meet industry-standard quality benchmarks and shall be delivered according to
 the timeline specified in the SOW.
2.3 Any modifications to the scope require written approval from both parties through a formal Change
 Request process.

3. PAYMENT TERMS
3.1 Payment Schedule: Client shall pay Orane according to the milestone-based payment schedule
 outlined in Exhibit B.
3.2 Payment Method: All payments shall be made via bank transfer within 30 days of invoice date.
3.3 Late Payment: Any payment delayed beyond 30 days shall incur a late fee of 1.5% per month on the
 outstanding amount.
3.4 Currency: All payments shall be made in Indian Rupees (INR) unless otherwise specified.
3.5 Taxes: All fees are exclusive of applicable taxes. Client shall bear all tax liabilities including GST.

4. INTELLECTUAL PROPERTY RIGHTS
4.1 Client IP: All intellectual property created specifically for Client under this Agreement shall be transferred
 to Client upon full payment.
4.2 Orane IP: Orane retains ownership of all pre-existing tools, methodologies, and frameworks used in
 the development, granting Client a perpetual, royalty-free, non-exclusive license for use with the
 deliverables.

5. CONFIDENTIALITY
5.1 Both parties agree to maintain confidentiality of all proprietary information exchanged during the term
 of this Agreement and for five (5) years thereafter.
5.2 Each party shall use the same degree of care to protect the other party's Confidential Information as it
 uses to protect its own, but no less than reasonable care.

6. WARRANTIES
6.1 Workmanship Warranty: Orane warrants that services will be performed in a professional and
 workmanlike manner.
6.2 Functionality Warranty: Deliverables shall conform to specifications outlined in the SOW for a period
 of 90 days from acceptance.
6.3 No Infringement: Orane warrants that deliverables shall not infringe upon any third-party intellectual
 property rights.

7. LIABILITY AND INDEMNIFICATION
7.1 Limitation of Liability: Orane's total liability under this Agreement shall not exceed the total fees paid
 by Client in the 12 months preceding the claim, excluding claims for IP infringement or breach of
 confidentiality.
7.2 Exclusion: Neither party shall be liable for indirect, incidental, or consequential damages.
7.3 Indemnification: Each party shall indemnify the other against claims arising from: (a) breach of this
 Agreement, (b) negligence, or (c) intellectual property infringement.

8. TERM AND TERMINATION
8.1 Term: This Agreement commences on the Effective Date and continues until completion of all services
 under the SOW, unless terminated earlier.
8.2 Termination for Convenience: Either party may terminate this Agreement with 60 days written notice.
8.3 Termination for Cause: Either party may terminate immediately upon material breach that is not
 cured within 30 days of written notice.

9. DATA PROTECTION
9.1 Orane shall comply with all applicable data protection laws including the Information Technology Act,
 2000 and GDPR where applicable.
9.2 Orane shall implement and maintain appropriate technical and organizational security measures to
 protect Client Data.
9.3 In case of a data breach, Orane shall notify Client within 48 hours of discovery.
9.4 Client data shall be stored only in India unless explicitly authorized otherwise by Client in writing.

10. DISPUTE RESOLUTION
10.1 Escalation: Unresolved disputes shall first be escalated to senior management of both parties for a
 period of 15 days.
10.2 Mediation: If escalation fails, parties agree to attempt non-binding mediation.
10.3 Arbitration: Unresolved disputes shall be settled by arbitration under the Indian Arbitration and
 Conciliation Act, 1996.
10.4 Arbitration Venue: Arbitration shall be conducted in Gurgaon, Haryana, India.
10.5 Governing Law: This Agreement shall be governed by the laws of India.
10.6 Jurisdiction: Courts of Gurgaon, Haryana shall have exclusive jurisdiction.

11. FORCE MAJEURE
11.1 Neither party shall be liable for delays or failures due to circumstances beyond reasonable control
 including natural disasters, wars, pandemics, government actions, or labor strikes.
11.2 The affected party shall notify the other within 7 days and make reasonable efforts to mitigate impact.

12. GENERAL PROVISIONS
12.1 Amendment: This Agreement may only be amended in writing signed by both parties.
12.2 Assignment: Neither party may assign this Agreement without prior written consent.
12.3 Entire Agreement: This Agreement constitutes the entire understanding between parties and
 supersedes all prior agreements.
12.4 Severability: If any provision is found invalid, the remaining provisions shall remain in full force.
12.5 Waiver: Failure to enforce any provision shall not constitute a waiver.
12.6 Notices: All notices shall be in writing and delivered to the addresses specified above.

SIGNATURES
ORANE TECHNOLOGIES PVT. LTD.
Signature:
Name: Authorized Signatory
Title: Director
Date:

CLIENT
Signature:
Name:
Title:
Date:

EXHIBIT A: Statement of Work (SOW) To be attached
EXHIBIT B: Payment Schedule To be attached
"""

# --- Helper Functions for File Reading ---
def read_file_content(uploaded_file):
    """
    Reads text from uploaded .txt, .pdf, or .docx files.
    Returns the extracted text as a string.
    """
    if uploaded_file is None:
        return ""
    
    try:
        # Handle PDF files
        if uploaded_file.type == "application/pdf":
            # Using pypdf for PDF reading
            reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        
        # Handle Word documents
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Using docx for Word reading
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        
        # Handle Plain Text files
        else: 
            # Decode bytes to string
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            return stringio.read()
            
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""

# --- Hardcoded Analysis Result for Quota Error Bypass (From previous run) ---
FALLBACK_ANALYSIS_JSON = """
{
  "summary": {
    "totalIssues": 10,
    "criticalViolations": 10,
    "moderateDeviations": 0,
    "minorConcerns": 0,
    "overallRisk": "HIGH"
  },
  "violations": [
    {
      "category": "Scope of Services",
      "severity": "CRITICAL",
      "title": "Vendor has unilateral right to modify scope and timeline",
      "oraneClause": "2.3 Any modifications to the scope require written approval from both parties through a formal Change Request process.",
      "thirdPartyClause": "1.2 TechMax reserves the right to modify the scope, deliverables, or timeline at its sole discretion with or without notice to Customer.",
      "violation": "The TechMax contract allows the vendor to unilaterally change the project scope, deliverables, or timeline at any time, which severely weakens Orane's control and contradicts the Orane standard for mutual written approval.",
      "recommendation": "Reject Article 1.2. Replace with a clause mandating mutual written agreement for any scope changes, following a formal Change Request process.",
      "riskImpact": "High risk of project drift, increased costs, and failure to meet business deadlines, as Orane has no contractual control over the project schedule or scope."
    },
    {
      "category": "Payment Terms",
      "severity": "CRITICAL",
      "title": "Unfavorable Payment Terms, Currency, and Price Increase Rights",
      "oraneClause": "3.2 Payment Method: All payments shall be made via bank transfer within 30 days of invoice date. 3.4 Currency: All payments shall be made in Indian Rupees (INR)...",
      "thirdPartyClause": "2.2 Payment Terms: All payments are due within 15 days of invoice date. 2.3 Late Fees: Late payments will incur a penalty of 3% per month (36% per annum)... 2.5 Price Increases: TechMax may increase fees at any time with 15 days notice.",
      "violation": "TechMax requires a much shorter payment term (15 vs 30 days), imposes a significantly higher late penalty (3% per month vs 1.5% per month), and unilaterally reserves the right to increase fees, all contradicting Orane's standard terms.",
      "recommendation": "Insist on 30-day payment terms, 1.5% late fee, and payment in INR. Reject Article 2.5 and require that price increases be mutually agreed upon in writing.",
      "riskImpact": "Significant financial risk due to exposure to currency fluctuations, double the late payment penalty, and uncontrolled price escalation by the vendor."
    },
    {
      "category": "IP Rights",
      "severity": "CRITICAL",
      "title": "Complete loss of Ownership of Developed IP",
      "oraneClause": "4.1 Client IP: All intellectual property created specifically for Client under this Agreement shall be transferred to Client upon full payment.",
      "thirdPartyClause": "3.1 Ownership: All intellectual property rights in any work product... created under this Agreement shall remain the exclusive property of TechMax. 3.2 Limited License: ...TechMax grants Customer a non-exclusive, non-transferable, revocable license...",
      "violation": "The TechMax contract retains all ownership for the vendor, granting Orane only a limited, non-transferable, and **revocable** license to use the deliverables. This is a complete reversal of the Orane standard, which mandates IP transfer to the client.",
      "recommendation": "Reject Article 3.1 and 3.2 entirely. Insist on a 'work-for-hire' clause transferring all IP rights to Orane upon payment, consistent with Article 4.1 of the Standard Contract.",
      "riskImpact": "Existential business risk. Orane cannot own, modify, sell, or commercialize the core product they paid for. The vendor can revoke the license at any time, rendering the software unusable."
    },
    {
      "category": "Warranties",
      "severity": "CRITICAL",
      "title": "Complete Disclaimer of all Warranties ('AS-IS' Basis)",
      "oraneClause": "6.2 Functionality Warranty: Deliverables shall conform to specifications outlined in the SOW for a period of 90 days from acceptance. 6.3 No Infringement: Orane warrants that deliverables shall not infringe upon any third-party intellectual property rights.",
      "thirdPartyClause": "5.1 AS-IS BASIS: ALL SERVICES AND DELIVERABLES ARE PROVIDED ON AN 'AS IS' AND 'AS AVAILABLE' BASIS... 5.2 DISCLAIMER: TECHMAX EXPRESSLY DISCLAIMS ALL WARRANTIES...",
      "violation": "The TechMax contract disclaims all express and implied warranties, including functionality and non-infringement. This is a severe deviation from the Orane standard, which guarantees quality and non-infringement.",
      "recommendation": "Reject Articles 5.1 and 5.2. Insist on the inclusion of 90-day functionality and non-infringement warranties as per the Standard Contract.",
      "riskImpact": "High legal and operational risk. Orane has no recourse if the software does not work, contains critical errors, or faces a lawsuit for infringing a third party’s intellectual property."
    },
    {
      "category": "Liability",
      "severity": "CRITICAL",
      "title": "Extremely Low Cap on Vendor Liability",
      "oraneClause": "7.1 Limitation of Liability: Orane's total liability under this Agreement shall not exceed the total fees paid by Client in the 12 months preceding the claim.",
      "thirdPartyClause": "6.1 Limitation of Liability: IN NO EVENT SHALL TECHMAX'S TOTAL LIABILITY EXCEED USD $1,000 (ONE THOUSAND US DOLLARS), REGARDLESS OF THE TOTAL FEES PAID.",
      "violation": "TechMax's cap of only $1,000 is grossly insufficient and effectively eliminates any meaningful liability for the vendor, contradicting Orane's standard of capping liability at 12 months of fees paid.",
      "recommendation": "Insist on the mutual liability cap standard: total fees paid in the preceding 12 months. Reject the $1,000 cap.",
      "riskImpact": "Extreme financial exposure. If the software causes a major failure or data loss, Orane's maximum recovery from the vendor is capped at an insignificant amount."
    },
    {
      "category": "Indemnification",
      "severity": "CRITICAL",
      "title": "One-Sided and Unlimited Customer Indemnification",
      "oraneClause": "7.3 Indemnification: Each party shall indemnify the other against claims arising from: (a) breach of this Agreement, (b) negligence, or (c) intellectual property infringement.",
      "thirdPartyClause": "6.3 Customer Indemnification: Customer shall indemnify, defend, and hold harmless TechMax from any and all claims... arising from: Customer's use of deliverables... 6.4 Unlimited Indemnity: Customer's indemnification obligations are unlimited...",
      "violation": "The TechMax contract makes indemnification one-sided (only Orane indemnifies TechMax) and Orane's indemnity obligation is **unlimited**, contrary to Orane's standard mutual and impliedly limited indemnification.",
      "recommendation": "Insist on a mutual indemnification clause. Reject the 'Unlimited Indemnity' clause and cap all indemnification obligations to a reasonable commercial limit.",
      "riskImpact": "High legal risk. Orane could be forced to pay all of TechMax's legal costs and damages for nearly any claim related to the project, without any cap."
    },
    {
      "category": "Termination",
      "severity": "CRITICAL",
      "title": "Unfair Termination Rights and Penalties",
      "oraneClause": "8.2 Termination for Convenience: Either party may terminate this Agreement with 60 days written notice.",
      "thirdPartyClause": "7.2 Termination by TechMax: TechMax may terminate this Agreement at any time, for any reason, with or without cause, upon 7 days notice. 7.3 Termination by Customer: Customer may terminate only after the initial 3-year term by providing 180 days written notice and paying a termination fee equal to 50% of the remaining contract value.",
      "violation": "TechMax has near-immediate termination rights (7 days notice), while Orane is locked into a 3-year term, requiring 180 days notice and a massive 50% penalty to exit, violating the mutual 60-day notice standard.",
      "recommendation": "Insist on mutual 60-day termination for convenience, as per the Standard Contract. Reject all penalties for convenience termination.",
      "riskImpact": "High business disruption risk. The vendor can abandon the project almost instantly, while Orane is financially penalized for trying to find a replacement."
    },
    {
      "category": "Confidentiality",
      "severity": "CRITICAL",
      "title": "Vendor Use of Customer Data for Competing Products",
      "oraneClause": "5.1 Both parties agree to maintain confidentiality of all proprietary information exchanged during the term of this Agreement.",
      "thirdPartyClause": "4.3 This confidentiality obligation shall survive indefinitely... 4.4 TechMax may freely use any information learned from Customer for its own business purposes, including development of competing products.",
      "violation": "The TechMax contract explicitly grants the vendor the right to use Orane's information to develop competing products, directly undermining Orane's business interests. This is a severe deviation from the principle of mutual confidentiality.",
      "recommendation": "Insist on a mutual confidentiality clause with a 5-year survival period. Reject Article 4.4, which allows the vendor to exploit Orane's confidential business information.",
      "riskImpact": "Severe competitive risk. Orane's strategic information could be legally used by the vendor to become a direct competitor."
    },
    {
      "category": "Data Protection",
      "severity": "CRITICAL",
      "title": "Violation of Data Residency and Security Compliance",
      "oraneClause": "9.1 Orane shall comply with all applicable data protection laws including... GDPR where applicable. 9.4 Client data shall be stored only in India unless explicitly authorized otherwise. 9.3 In case of a data breach, Orane shall notify Client within 48 hours...",
      "thirdPartyClause": "8.2 Customer data may be stored on servers located anywhere in the world... 8.4 In the event of a data breach, TechMax shall notify Customer within 60 days if TechMax deems notification appropriate. 8.5 Customer waives any claims related to data privacy or security.",
      "violation": "TechMax's data terms violate Orane's standard by allowing global data storage (violating Indian residency requirements), significantly increasing breach notification time (48 hours vs. 60 days), and forcing Orane to waive all data claims.",
      "recommendation": "Insist on compliance with GDPR/Indian laws, data residency in India, and 48-hour breach notification. Reject Article 8.5.",
      "riskImpact": "Major regulatory and legal risk, including potential fines under GDPR or Indian data protection laws, and total exposure in case of a security breach."
    },
    {
      "category": "Jurisdiction",
      "severity": "CRITICAL",
      "title": "Shift of Governing Law and Mandatory Arbitration to USA",
      "oraneClause": "10.5 Governing Law: This Agreement shall be governed by the laws of India. 10.6 Jurisdiction: Courts of Gurgaon, Haryana shall have exclusive jurisdiction. 10.3 Arbitration: Unresolved disputes shall be settled by arbitration under the Indian Arbitration and Conciliation Act, 1996.",
      "thirdPartyClause": "9.1 Governing Law: This Agreement shall be governed by the laws of the State of Texas, USA... 9.2 Jurisdiction: Customer irrevocably submits to the exclusive jurisdiction of courts located in Travis County, Texas, USA. 9.6 Mandatory Arbitration: Any dispute must be resolved through binding arbitration in Austin, Texas...",
      "violation": "The contract shifts the governing law and exclusive jurisdiction from India/Gurgaon to Texas, USA. It mandates arbitration in Austin, Texas, with Orane bearing all costs, which is commercially unfavorable and violates the Orane standard.",
      "recommendation": "Insist on the governing law and jurisdiction being India, Gurgaon, and any arbitration conducted under Indian law, as per the Standard Contract.",
      "riskImpact": "Significant legal cost and procedural risk. Orane will incur massive expenses to litigate disputes in the US legal system."
    }
  ]
}
"""

# --- Page Configuration ---
st.set_page_config(
    page_title="Orane Contract Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# --- CSS Styling ---
st.markdown("""
<style>
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        text-align: center;
        background-color: white;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 1.875rem;
        line-height: 2.25rem;
        font-weight: 700;
    }
    .metric-card p {
        margin: 0;
        font-size: 0.875rem;
        line-height: 1.25rem;
        font-weight: 500;
    }
    
    /* Severity Colors */
    .critical { background-color: #fef2f2; border-color: #fecaca; }
    .critical h3 { color: #dc2626; }
    .critical p { color: #b91c1c; }
    
    .moderate { background-color: #fff7ed; border-color: #fed7aa; }
    .moderate h3 { color: #ea580c; }
    .moderate p { color: #c2410c; }
    
    .minor { background-color: #fefce8; border-color: #fef08a; }
    .minor h3 { color: #ca8a04; }
    .minor p { color: #a16207; }
    
    /* Risk Badges */
    .risk-high { background-color: #fee2e2; color: #dc2626; border-color: #fecaca; }
    .risk-medium { background-color: #ffedd5; color: #ea580c; border-color: #fed7aa; }
    .risk-low { background-color: #dcfce7; color: #16a34a; border-color: #bbf7d0; }
    
    /* Header styling */
    h1 { color: #1f2937; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar (API Key Input) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        help="Enter your OpenAI API Key here. It starts with 'sk-...'"
    )
    st.info("Your API key is not stored. It is used only for this session.")
    st.markdown("[Get an API key here](https://platform.openai.com/api-keys)")

# --- Main App Interface ---

# Title Section
col1, col2 = st.columns([1, 15])
with col1:
    st.write("# ⚖️") 
with col2:
    st.title("Orane Contract Compliance Analyzer")

st.markdown("""
This tool compares a **Third-Party Contract** (uploaded below) against **Orane's Standard Contract** (hardcoded for consistency) 
to automatically identify violations, critical deviations, and business risks.
""")

st.divider()

# --- Contract Display and Upload Section ---
st.subheader("1. Orane's Standard Contract (Hardcoded)")
st.text_area(
    "Orane Standard Contract Text (Basis for Comparison)", 
    value=ORANE_STANDARD_CONTRACT, 
    height=200,
    disabled=True,
    help="This is the benchmark contract that the third-party document is compared against."
)

st.subheader("2. Upload Third-Party Contract to Analyze")
third_file = st.file_uploader("Upload Third-Party Contract (PDF, DOCX, or TXT)", type=['txt', 'pdf', 'docx'], key="third")

if "third_text" not in st.session_state:
    st.session_state.third_text = ""

if third_file:
    content = read_file_content(third_file)
    if content != st.session_state.third_text:
        st.session_state.third_text = content
        
third_text = st.text_area(
    "Third-Party Contract Text", 
    value=st.session_state.third_text, 
    height=300,
    placeholder="Paste third-party contract text here or upload a file above..."
)
if third_text:
    st.success(f"Loaded {len(third_text)} characters for analysis.")


# --- Analyze Button ---
st.divider()
analyze_btn = st.button("🔍 Analyze Contracts for Violations", type="primary", use_container_width=True)

# --- Logic: Call AI ---
if analyze_btn:
    # Validation
    if not api_key:
        st.error("❌ Please enter your OpenAI API Key in the sidebar to proceed.")
    elif not third_text:
        st.warning("⚠️ Please upload or paste the Third-Party Contract text before analyzing.")
    else:
        # Initialize OpenAI Client
        client = openai.OpenAI(api_key=api_key)
        
        # Define the texts
        orane_text_for_api = ORANE_STANDARD_CONTRACT
        third_party_text_for_api = third_text

        # Define System Prompt for Chat API
        system_prompt = "You are a legal contract analysis AI specializing in compliance review. Your task is to compare the two provided contract texts, identify violations, deviations, and risks, and output the analysis STRICTLY as a single JSON object conforming to the required schema and categories. Use the 'ORANE' text as the required standard."
        
        # Define User Message containing contract content and desired output format
        user_message = f"""
        ORANE'S STANDARD CONTRACT (The Required Standard):
        {orane_text_for_api}

        THIRD-PARTY CONTRACT TO ANALYZE:
        {third_party_text_for_api}

        Analyze the third-party contract and provide a JSON response with the following structure (respond ONLY with valid JSON):
        {{
          "summary": {{
            "totalIssues": number,
            "criticalViolations": number,
            "moderateDeviations": number,
            "minorConcerns": number,
            "overallRisk": "HIGH" | "MEDIUM" | "LOW"
          }},
          "violations": [
            {{
              "category": "Payment Terms" | "Liability" | "Termination" | "IP Rights" | "Confidentiality" | "Warranties" | "Jurisdiction" | "Other",
              "severity": "CRITICAL" | "MODERATE" | "MINOR",
              "title": "Brief title of the issue",
              "oraneClause": "Relevant clause from Orane's contract",
              "thirdPartyClause": "Relevant clause from third-party contract",
              "violation": "Detailed explanation of how it violates or deviates",
              "recommendation": "Suggested action or amendment",
              "riskImpact": "Business/legal risk this poses"
            }}
          ]
        }}"""

        try:
            with st.spinner("🤖 Analyzing contracts using the 'o3-mini' model..."):
                # Call OpenAI Chat Completions API with the user-specified model
                response = client.chat.completions.create(
                    model="o3-mini", # Using the user-specified model
                    response_format={"type": "json_object"}, 
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=4000
                )
                
                # Extract Response
                response_text = response.choices[0].message.content
                clean_json = response_text.replace("```json", "").replace("```", "").strip()
                analysis = json.loads(clean_json)
                
                # Save to session state
                st.session_state.analysis_result = analysis

        except openai.APIError as e: 
            st.error(f"OpenAI API Error: Details: {str(e)}")
            
            # --- Quota Error Fallback Logic ---
            if "insufficient_quota" in str(e):
                st.warning("⚠️ **Quota Exceeded Detected:** The API call failed due to 'insufficient_quota'. Loading pre-calculated analysis of your previously uploaded files as a demonstration.")
                # Load the fallback analysis based on the two contracts you initially provided
                st.session_state.analysis_result = json.loads(FALLBACK_ANALYSIS_JSON)
            else:
                st.error("The analysis could not be completed. Please check your API key status or usage limits.")
                
        except json.JSONDecodeError:
            st.error("Error parsing AI response. The model did not return valid JSON. Please try again with shorter contracts.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

# --- Display Results ---
if "analysis_result" in st.session_state:
    data = st.session_state.analysis_result
    summary = data.get("summary", {})
    
    st.markdown("## 📊 Analysis Report")
    
    # 1. Summary Metrics Display
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card critical">
            <h3>{summary.get("criticalViolations", 0)}</h3>
            <p>Critical Violations</p>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card moderate">
            <h3>{summary.get("moderateDeviations", 0)}</h3>
            <p>Moderate Deviations</p>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card minor">
            <h3>{summary.get("minorConcerns", 0)}</h3>
            <p>Minor Concerns</p>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        risk = summary.get("overallRisk", "UNKNOWN")
        risk_class = f"risk-{risk.lower()}" if risk.lower() in ["high", "medium", "low"] else ""
        st.markdown(f"""
        <div class="metric-card {risk_class}">
            <h3>{risk}</h3>
            <p>Overall Risk</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("") # Spacer

    # 2. Detailed Violations List
    st.subheader("Detailed Findings")
    violations = data.get("violations", [])
    
    if not violations:
        st.info("No violations found! The contracts seem to align perfectly.")
    
    for i, v in enumerate(violations):
        # Set icon based on severity
        severity = v.get('severity', 'MINOR')
        if severity == "CRITICAL":
            icon = "🔴"
        elif severity == "MODERATE":
            icon = "🟠"
        else:
            icon = "🟡"
            
        with st.expander(f"{icon} {v.get('title', 'Issue')} ({v.get('category', 'General')})"):
            st.caption(f"**Severity:** {severity}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**📋 Orane's Standard:**\n\n_{v.get('oraneClause', 'N/A')}_")
            with c2:
                st.error(f"**⚠️ Third-Party Clause:**\n\n_{v.get('thirdPartyClause', 'N/A')}_")
            
            st.markdown(f"**🔍 Violation Details:** \n{v.get('violation', 'No details provided.')}")
            st.markdown(f"**💼 Risk Impact:** \n{v.get('riskImpact', 'No risk impact provided.')}")
            st.success(f"**💡 Recommendation:** \n{v.get('recommendation', 'No recommendation provided.')}")

# --- Footer ---
st.divider()
st.caption("Contract Compliance Analyzer • Built with Streamlit & OpenAI")
