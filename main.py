import streamlit as st
import openai

# Use st.secrets to securely access your OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="Fake News Checker", page_icon="📰")

st.title("📰 Fake News Checker")
st.write("Enter a news headline or article below. The AI will analyze it for signs of fake news.")

user_input = st.text_area("Paste news headline or article here:", height=150)

if st.button("Check for Fake News") and user_input.strip():
    with st.spinner("Analyzing..."):
        prompt = (
            "You are a fact-checking assistant. "
            "Analyze the following news for signs of being fake or misleading. "
            "Explain your reasoning and, if possible, suggest how to verify the claim:\n\n"
            f"{user_input}"
        )
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",  # or "gpt-4-turbo"
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.2
            )
            result = response.choices[0].message.content
            st.success("Analysis complete!")
            st.markdown("**AI Analysis:**")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

st.info("This tool uses OpenAI GPT-4o to analyze news. Always cross-check with trusted sources.")
