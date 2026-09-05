import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags in seconds.")

# Sidebar for API Key
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

# Input selection fields
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook"])
    content_type = st.selectbox("Content Type", ["Educational Post", "Promotional / Sales", "Storytelling", "Quick Tip"])
    tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Energetic", "Informative", "Humorous"])

with col2:
    topic = st.text_input("Topic / Subject", placeholder="e.g., Python Tips for Beginners")
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineering Students")

# Generate Button
if st.button("Generate Content", type="primary"):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill out both the Topic and Target Audience fields.")
    else:
        try:
            # Initialize Groq Client
            client = Groq(api_key=api_key)

            # Construct Prompt
            prompt = f"""
            You are an expert social media content creator. Generate a complete post based on these specifications:
            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}

            Requirements:
            1. An engaging hook/headline tailored to the platform.
            2. Main body caption formatted with clear line breaks and readability.
            3. A clear Call-to-Action (CTA).
            4. 5 to 10 relevant hashtags.
            """

            with st.spinner("Generating content..."):
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                
                generated_text = response.choices[0].message.content

            # Display Output
            st.success("Done!")
            st.subheader("Your Generated Content")
            st.markdown(generated_text)
            
            # Copy-friendly text box
            st.text_area("Raw Copyable Text", value=generated_text, height=250)

        except Exception as e:
            st.error(f"An error occurred: {e}")