import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.docx_reader import extract_text_from_docx
from utils.text_cleaner import clean_text
from utils.gemini_helper import analyze_contract


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ClauseIQ",
    page_icon="⚖️",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("⚖️ ClauseIQ")
st.write("AI Legal Contract Analyzer")

st.divider()


# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "📄 Upload your legal contract",
    type=["pdf", "docx"]
)


# ==========================================
# PROCESS UPLOADED FILE
# ==========================================

if uploaded_file is not None:

    st.success("File uploaded successfully!")

    st.write("### 📄 Contract Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Filename**")
        st.write(uploaded_file.name)

    with col2:
        st.write("**File Type**")
        st.write(uploaded_file.type)

    with col3:
        st.write("**File Size**")
        st.write(
            f"{uploaded_file.size / 1024:.2f} KB"
        )


    # ==========================================
    # DOCUMENT PROCESSING
    # ==========================================

    if uploaded_file.type == "application/pdf":

        extracted_text = extract_text_from_pdf(
            uploaded_file
        )

    elif uploaded_file.type == (
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    ):

        extracted_text = extract_text_from_docx(
            uploaded_file
        )

    else:

        st.error("Unsupported file type.")
        st.stop()


    # ==========================================
    # CLEAN TEXT
    # ==========================================

    cleaned_text = clean_text(
        extracted_text
    )


    # ==========================================
    # EXTRACTED TEXT
    # ==========================================

    with st.expander(
        "📄 View Extracted Contract Text"
    ):

        st.text_area(
            label="Contract Content",
            value=cleaned_text,
            height=400
        )


    st.divider()


    # ==========================================
    # ANALYZE CONTRACT
    # ==========================================

    if st.button(
        "🔍 Analyze Contract",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing contract... Please wait..."
        ):

            analysis = analyze_contract(
                cleaned_text
            )


        # ==========================================
        # ERROR HANDLING
        # ==========================================

        if "error" in analysis:

            st.error(
                analysis["error"]
            )

        else:

            st.success(
                "Analysis Completed!"
            )

            st.markdown(
                "## 📋 Contract Analysis"
            )


            # ==========================================
            # RISK OVERVIEW
            # ==========================================

            st.markdown(
                "### 📊 Risk Overview"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    label="Overall Risk",
                    value=analysis[
                        "overall_risk"
                    ]
                )

            with col2:

                st.metric(
                    label="Risk Score",
                    value=f"{analysis['risk_score']}/100"
                )

            with col3:

                st.metric(
                    label="Risky Clauses",
                    value=len(
                        analysis[
                            "risky_clauses"
                        ]
                    )
                )


            st.divider()


            # ==========================================
            # EXECUTIVE SUMMARY
            # ==========================================

            st.markdown(
                "### 📝 Executive Summary"
            )

            with st.container(
                border=True
            ):

                st.write(
                    analysis[
                        "executive_summary"
                    ]
                )


            st.divider()


            # ==========================================
            # IMPORTANT CLAUSES
            # ==========================================

            st.markdown(
                "### 📌 Important Clauses"
            )

            important_clauses = analysis[
                "important_clauses"
            ]

            if not important_clauses:

                st.info(
                    "No important clauses "
                    "were identified."
                )

            else:

                for clause in important_clauses:

                    with st.expander(
                        f"📌 {clause['clause_name']}"
                    ):

                        st.markdown(
                            "**What the clause says**"
                        )

                        st.write(
                            clause[
                                "description"
                            ]
                        )

                        st.markdown(
                            "**Why it is important**"
                        )

                        st.write(
                            clause[
                                "importance"
                            ]
                        )


            st.divider()


            # ==========================================
            # RISKY CLAUSES
            # ==========================================

            st.markdown(
                "### 🚨 Risky Clauses"
            )

            risky_clauses = analysis[
                "risky_clauses"
            ]

            if not risky_clauses:

                st.success(
                    "No significant risky "
                    "clauses were identified."
                )

            else:

                for clause in risky_clauses:

                    with st.expander(
                        f"⚠️ "
                        f"{clause['clause_name']} "
                        f"— "
                        f"{clause['risk_level']}"
                    ):

                        st.markdown(
                            "**Risk Level**"
                        )

                        st.write(
                            clause[
                                "risk_level"
                            ]
                        )

                        st.markdown(
                            "**What the clause says**"
                        )

                        st.write(
                            clause[
                                "description"
                            ]
                        )

                        st.markdown(
                            "**Why this may be risky**"
                        )

                        st.write(
                            clause[
                                "risk_reason"
                            ]
                        )


            st.divider()


            # ==========================================
            # MISSING / WEAK CLAUSES
            # ==========================================

            st.markdown(
                "### 🔎 Missing / Weak Clauses"
            )

            missing_clauses = analysis[
                "missing_or_weak_clauses"
            ]

            if not missing_clauses:

                st.success(
                    "No significant missing "
                    "or weak clauses were identified."
                )

            else:

                for clause in missing_clauses:

                    with st.expander(
                        f"⚠️ "
                        f"{clause['clause_name']}"
                    ):

                        st.markdown(
                            "**Why it may be "
                            "missing or weak**"
                        )

                        st.write(
                            clause[
                                "reason"
                            ]
                        )


            st.divider()


            # ==========================================
            # PARTY OBLIGATIONS
            # ==========================================

            st.markdown(
                "### 👤 Party Obligations"
            )

            obligations = analysis[
                "obligations"
            ]

            if not obligations:

                st.info(
                    "No specific obligations "
                    "were identified."
                )

            else:

                parties = {}

                for item in obligations:

                    party = item[
                        "party"
                    ]

                    obligation = item[
                        "obligation"
                    ]

                    if party not in parties:

                        parties[
                            party
                        ] = []

                    parties[
                        party
                    ].append(
                        obligation
                    )


                for (
                    party,
                    party_obligations
                ) in parties.items():

                    with st.expander(
                        f"👤 {party}"
                    ):

                        for obligation in (
                            party_obligations
                        ):

                            st.markdown(
                                f"• {obligation}"
                            )


            st.divider()


            # ==========================================
            # IMPORTANT DATES
            # ==========================================

            st.markdown(
                "### 📅 Important Dates & Deadlines"
            )

            important_dates = analysis[
                "important_dates"
            ]

            if not important_dates:

                st.info(
                    "No important dates "
                    "or deadlines were identified."
                )

            else:

                for item in important_dates:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**📅 "
                            f"{item['date']}**"
                        )

                        st.write(
                            item["event"]
                        )


            st.divider()


            # ==========================================
            # RECOMMENDATIONS
            # ==========================================

            st.markdown(
                "### 💡 Recommendations"
            )

            recommendations = analysis[
                "recommendations"
            ]

            if not recommendations:

                st.info(
                    "No specific recommendations "
                    "were generated."
                )

            else:

                for (
                    index,
                    recommendation
                ) in enumerate(
                    recommendations,
                    start=1
                ):

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{index}.** "
                            f"{recommendation}"
                        )