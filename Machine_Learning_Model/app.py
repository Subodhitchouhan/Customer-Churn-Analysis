import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("churn_model.pkl")

model = load_model()

# EXACT features used during training
FEATURES = model.feature_names_in_

# ---------------- CHURN ANALYSIS FUNCTIONS ----------------
def analyze_churn_reasons(input_df, prob):
    """Analyze why customer is likely to churn based on most important features"""
    reasons = []
    
    # Based on feature importance graph - focusing on top features
    
    # 1. Contract Type (High Importance)
    if input_df.get('Contract_One Year', [0])[0] == 0 and input_df.get('Contract_Two Year', [0])[0] == 0:
        reasons.append({
            'reason': ' Month-to-Month Contract',
            'detail': 'Customer is on a flexible month-to-month contract, which has the highest churn risk.',
            'action': 'Offer incentives for switching to annual or two-year contracts with discounted rates.'
        })
    
    # 2. Tenure (High Importance)
    tenure = input_df.get('Tenure_in_Months', [0])[0]
    if tenure < 12:
        reasons.append({
            'reason': ' Short Tenure',
            'detail': f'Customer has only been with us for {tenure} months. New customers are at higher risk.',
            'action': 'Implement a 90-day onboarding program with regular check-ins and exclusive new customer benefits.'
        })
    
    # 3. Internet Type - Fiber Optic (High Importance)
    if input_df.get('Internet_Type_Fiber Optic', [0])[0] == 1:
        reasons.append({
            'reason': ' Fiber Optic Service Issues',
            'detail': 'Fiber Optic customers show higher churn rates, possibly due to service quality or pricing concerns.',
            'action': 'Conduct service quality audit and offer competitive pricing review for fiber customers.'
        })
    
    # 4. Monthly Charges (Very High Importance)
    monthly_charge = input_df.get('Monthly_Charge', [0])[0]
    if monthly_charge > 70:
        reasons.append({
            'reason': ' High Monthly Charges',
            'detail': f'Monthly charge of ${monthly_charge:.2f} is above average, increasing price sensitivity.',
            'action': 'Review pricing package and offer customized bundles or loyalty discounts to reduce perceived cost.'
        })
    
    # 5. No Online Security (Important Feature)
    if input_df.get('Online_Security_Yes', [0])[0] == 0:
        reasons.append({
            'reason': ' No Online Security Service',
            'detail': 'Customer lacks online security add-on, indicating lower service engagement.',
            'action': 'Offer complimentary online security trial for 3 months to increase service stickiness.'
        })
    
    # 6. Payment Method (Important Feature)
    if input_df.get('Payment_Method_Electronic Check', [0])[0] == 1:
        reasons.append({
            'reason': ' Electronic Check Payment',
            'detail': 'Electronic check users show higher churn rates compared to automatic payment methods.',
            'action': 'Incentivize switching to automatic credit card or bank transfer with billing discounts.'
        })
    
    # 7. No Premium Support (Important Feature)
    if input_df.get('Premium_Support_Yes', [0])[0] == 0:
        reasons.append({
            'reason': ' No Premium Support',
            'detail': 'Customer does not have premium support, which correlates with lower satisfaction.',
            'action': 'Offer limited-time premium support upgrade at a discounted rate.'
        })
    
    # 8. Total Revenue (Very High Importance)
    total_revenue = input_df.get('Total_Revenue', [0])[0]
    if total_revenue < 1000:
        reasons.append({
            'reason': ' Low Total Revenue',
            'detail': f'Total revenue of ${total_revenue:.2f} indicates limited service adoption.',
            'action': 'Cross-sell additional services with bundle discounts to increase customer value.'
        })
    
    # 9. No Value Deal
    if input_df.get('Value_Deal_Yes', [0])[0] == 0:
        reasons.append({
            'reason': ' No Value Deal Promotion',
            'detail': 'Customer is not enrolled in any value deal or promotional offer.',
            'action': 'Enroll customer in loyalty program with exclusive deals and rewards.'
        })
    
    # 10. Number of Referrals
    referrals = input_df.get('Number_of_Referrals', [0])[0]
    if referrals == 0:
        reasons.append({
            'reason': ' No Referrals',
            'detail': 'Customer has not referred anyone, indicating lower engagement and satisfaction.',
            'action': 'Launch referral program with attractive rewards for both referrer and referee.'
        })
    
    # Select top 5 most relevant reasons based on the input
    return reasons[:5]


def get_retention_strategies(reasons):
    """Generate comprehensive retention strategy"""
    strategies = []
    
    for i, reason in enumerate(reasons, 1):
        strategies.append(f"**{i}. {reason['reason']}**")
        strategies.append(f"   - *Issue:* {reason['detail']}")
        strategies.append(f"   - *Retention Action:* {reason['action']}")
        strategies.append("")  # Empty line for spacing
    
    return "\n".join(strategies)


# ---------------- UI ----------------
st.title("Customer Churn Prediction & Retention")
st.markdown("---")

# Create tabs for better organization
tab1, tab2 = st.tabs([" Prediction", " About"])

with tab1:
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        Gender = st.selectbox("Gender", ["Male", "Female"])
        Age = st.number_input("Age", min_value=18, max_value=100, value=30)
        Married = st.selectbox("Married", ["Yes", "No"])
        State = st.selectbox(
            "State",
            ["Assam", "Bihar", "Chhattisgarh", "Delhi", "Gujarat", "Maharashtra"]
        )
    
    with col2:
        st.subheader("Customer Profile")
        Tenure_in_Months = st.number_input("Tenure (Months)", min_value=0, value=12)
        Number_of_Referrals = st.number_input("Number of Referrals", min_value=0, value=0)
        Value_Deal = st.selectbox("Value Deal", ["Yes", "No"])
        Contract = st.selectbox("Contract", ["Month-to-month", "One Year", "Two Year"])
    
    st.markdown("---")
    
    # Services Section
    with st.expander(" Service Details", expanded=True):
        col3, col4 = st.columns(2)
        
        with col3:
            Phone_Service = st.selectbox("Phone Service", ["Yes", "No"])
            Multiple_Lines = st.selectbox("Multiple Lines", ["Yes", "No"])
            Internet_Service = st.selectbox("Internet Service", ["Yes", "No"])
            Internet_Type = st.selectbox("Internet Type", ["DSL", "Fiber Optic", "None"])
            Online_Security = st.selectbox("Online Security", ["Yes", "No"])
            Online_Backup = st.selectbox("Online Backup", ["Yes", "No"])
        
        with col4:
            Device_Protection = st.selectbox("Device Protection Plan", ["Yes", "No"])
            Premium_Support = st.selectbox("Premium Support", ["Yes", "No"])
            Streaming_TV = st.selectbox("Streaming TV", ["Yes", "No"])
            Streaming_Movies = st.selectbox("Streaming Movies", ["Yes", "No"])
            Streaming_Music = st.selectbox("Streaming Music", ["Yes", "No"])
            Unlimited_Data = st.selectbox("Unlimited Data", ["Yes", "No"])
    
    # Billing Section
    with st.expander(" Billing & Payment", expanded=True):
        col5, col6 = st.columns(2)
        
        with col5:
            Paperless_Billing = st.selectbox("Paperless Billing", ["Yes", "No"])
            Payment_Method = st.selectbox(
                "Payment Method",
                ["Credit Card", "Mailed Check", "Electronic Check", "Bank Transfer"]
            )
            Monthly_Charge = st.number_input("Monthly Charge ($)", min_value=0.0, value=70.0, step=5.0)
            Total_Charges = st.number_input("Total Charges ($)", min_value=0.0, value=0.0, step=10.0)
        
        with col6:
            Total_Refunds = st.number_input("Total Refunds ($)", min_value=0.0, value=0.0, step=5.0)
            Total_Extra_Data_Charges = st.number_input("Extra Data Charges ($)", min_value=0.0, value=0.0, step=5.0)
            Total_Long_Distance_Charges = st.number_input("Long Distance Charges ($)", min_value=0.0, value=0.0, step=5.0)
            Total_Revenue = st.number_input("Total Revenue ($)", min_value=0.0, value=0.0, step=10.0)
    
    st.markdown("---")
    
    # Prediction Button
    predict_button = st.button(" Predict Churn Risk", type="primary", use_container_width=True)
    
    if predict_button:
        with st.spinner("Analyzing customer data..."):
            # ---- Internet consistency fix ----
            if Internet_Service == "No":
                Internet_Type = "None"
            
            # Create exact feature dataframe
            input_df = pd.DataFrame(0, index=[0], columns=FEATURES)
            
            # ---------- YES / NO FEATURES ----------
            yes_no_map = {
                "Gender_Male": Gender == "Male",
                "Married_Yes": Married == "Yes",
                "Value_Deal_Yes": Value_Deal == "Yes",
                "Phone_Service_Yes": Phone_Service == "Yes",
                "Multiple_Lines_Yes": Multiple_Lines == "Yes",
                "Internet_Service_Yes": Internet_Service == "Yes",
                "Online_Security_Yes": Online_Security == "Yes",
                "Online_Backup_Yes": Online_Backup == "Yes",
                "Device_Protection_Plan_Yes": Device_Protection == "Yes",
                "Premium_Support_Yes": Premium_Support == "Yes",
                "Streaming_TV_Yes": Streaming_TV == "Yes",
                "Streaming_Movies_Yes": Streaming_Movies == "Yes",
                "Streaming_Music_Yes": Streaming_Music == "Yes",
                "Unlimited_Data_Yes": Unlimited_Data == "Yes",
                "Paperless_Billing_Yes": Paperless_Billing == "Yes",
            }
            
            for col, condition in yes_no_map.items():
                if col in input_df.columns:
                    input_df[col] = int(condition)
            
            # ---------- GENDER FEMALE SAFETY ----------
            if "Gender_Female" in input_df.columns:
                input_df["Gender_Female"] = int(Gender == "Female")
            
            # ---------- CONTRACT ----------
            if Contract == "One Year" and "Contract_One Year" in input_df.columns:
                input_df["Contract_One Year"] = 1
            elif Contract == "Two Year" and "Contract_Two Year" in input_df.columns:
                input_df["Contract_Two Year"] = 1
            
            # ---------- INTERNET TYPE ----------
            it_col = f"Internet_Type_{Internet_Type}"
            if it_col in input_df.columns:
                input_df[it_col] = 1
            
            # ---------- PAYMENT METHOD ----------
            pm_col = f"Payment_Method_{Payment_Method}"
            if pm_col in input_df.columns:
                input_df[pm_col] = 1
            
            # ---------- STATE ----------
            st_col = f"State_{State}"
            if st_col in input_df.columns:
                input_df[st_col] = 1
            
            # ---------- NUMERICAL FEATURES ----------
            num_values = {
                "Age": Age,
                "Tenure_in_Months": Tenure_in_Months,
                "Monthly_Charge": Monthly_Charge,
                "Number_of_Referrals": Number_of_Referrals,
                "Total_Charges": Total_Charges,
                "Total_Refunds": Total_Refunds,
                "Total_Extra_Data_Charges": Total_Extra_Data_Charges,
                "Total_Long_Distance_Charges": Total_Long_Distance_Charges,
                "Total_Revenue": Total_Revenue,
            }
            
            for col, val in num_values.items():
                if col in input_df.columns:
                    input_df[col] = val
            
            # ---------- PREDICT ----------
            prediction = model.predict(input_df)[0]
            
            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(input_df)[0][1]
            else:
                prob = 0.5
            
            # ---------- OUTPUT ----------
            st.markdown("---")
            st.subheader(" Prediction Results")
            
            if prediction == 1:
                # High churn risk
                st.error(f"⚠️ **HIGH CHURN RISK** - Probability: {prob:.1%}")
                
                # Progress bar for visual representation
                st.progress(prob, text=f"Churn Risk Level: {prob:.1%}")
                
                st.markdown("---")
                
                # Analyze reasons
                reasons = analyze_churn_reasons(input_df, prob)
                
                st.subheader(" Top 5 Churn Risk Factors & Retention Strategies")
                st.info("Based on our analysis, here are the key factors contributing to churn risk and recommended actions:")
                
                # Display reasons with better formatting
                for i, reason in enumerate(reasons, 1):
                    with st.container():
                        st.markdown(f"### {i}. {reason['reason']}")
                        st.markdown(f" Issue: {reason['detail']}")
                        st.markdown(f" Retention Action: {reason['action']}")
                        if i < len(reasons):
                            st.markdown("---")
                
                # Additional retention summary
                st.markdown("---")
                st.subheader(" Immediate Action Plan")
                
                col_action1, col_action2 = st.columns(2)
                
                with col_action1:
                    st.markdown("""
                    **Priority Actions:**
                    -  Schedule retention call within 48 hours
                    -  Send personalized retention offer
                    -  Activate loyalty rewards
                    """)
                
                with col_action2:
                    st.markdown(f"""
                    **Customer Value:**
                    - Current Monthly Revenue: ${Monthly_Charge:.2f}
                    - Tenure: {Tenure_in_Months} months
                    - Total Revenue: ${Total_Revenue:.2f}
                    """)
                
            else:
                # Low churn risk
                st.success(f"✅ **LOW CHURN RISK** - Retention Probability: {(1 - prob):.1%}")
                
                # Progress bar for visual representation
                st.progress(1 - prob, text=f"Retention Confidence: {(1-prob):.1%}")
                
                st.markdown("---")
                
                st.subheader(" Customer Health Status")
                st.info("This customer shows strong loyalty indicators. Continue providing excellent service!")
                
                # Show positive indicators
                positive_indicators = []
                
                if Tenure_in_Months >= 12:
                    positive_indicators.append("✓ Long-term customer relationship")
                if Contract in ["One Year", "Two Year"]:
                    positive_indicators.append(f"✓ Committed contract: {Contract}")
                if Number_of_Referrals > 0:
                    positive_indicators.append(f"✓ Active promoter: {Number_of_Referrals} referrals")
                if input_df.get('Online_Security_Yes', [0])[0] == 1:
                    positive_indicators.append("✓ Enhanced service adoption")
                if Monthly_Charge <= 70:
                    positive_indicators.append("✓ Competitive pricing")
                
                for indicator in positive_indicators[:5]:
                    st.markdown(f"- {indicator}")
                
                st.markdown("---")
                st.markdown("Recommended Actions:")
                st.markdown("- Continue excellent service delivery")
                st.markdown("- Consider upselling premium features")
                st.markdown("- Encourage referrals with rewards")
                st.markdown("- Maintain regular engagement")

with tab2:
    st.subheader("About This Application")
    st.markdown("""
    This Customer Churn Prediction application uses machine learning to identify customers at risk of leaving 
    and provides actionable retention strategies.
    
    **Key Features:**
    -  AI-powered churn prediction using Random Forest algorithm
    -  Analysis based on customer behavior, service usage, and billing patterns
    -  Personalized retention strategies for at-risk customers
    -  Focus on top features that impact churn decisions
    
    **Most Important Factors:**
    1. Total Revenue & Charges
    2. Contract Type (Month-to-month vs. Annual)
    3. Tenure Duration
    4. Monthly Charges
    5. Service Add-ons (Security, Support, etc.)
    
    **How to Use:**
    1. Enter customer details in the Prediction tab
    2. Click "Predict Churn Risk"
    3. Review the risk assessment and recommendations
    4. Take immediate action based on the retention strategies
    
    ---
    *Developed with Streamlit & Scikit-learn*
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Customer Churn Prediction System | by Subodhit Chouhan </div>",
    unsafe_allow_html=True
)