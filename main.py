import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="Fake News Checker", page_icon="📰")
st.title("📰 Fake News Checker")
st.write("Paste a news headline/article or upload an image (screenshot, post, etc.). The AI will analyze it for signs of fake news.")

tab1, tab2 = st.tabs(["Text", "Image"])

with tab1:
    user_input = st.text_area("Paste news headline or article here:", height=150)
    if st.button("Check Text for Fake News", key="text"):
        if user_input.strip():
            with st.spinner("Analyzing text..."):
                prompt = (
                    "You are a fact-checking assistant. "
                    "Analyze the following news for signs of being fake or misleading. "
                    "Explain your reasoning and, if possible, suggest how to verify the claim:\n\n"
                    f"{user_input}"
                )
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4o",
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
        else:
            st.warning("Please enter some text.")

with tab2:
    uploaded_file = st.file_uploader("Upload an image (screenshot, post, etc.)", type=["png", "jpg", "jpeg"])
    if st.button("Check Image for Fake News", key="image"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            with st.spinner("Analyzing image..."):
                try:
                    # Read image bytes
                    image_bytes = uploaded_file.read()
                    # Send image to GPT-4o vision
                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a fact-checking assistant. Analyze the uploaded image for signs of fake or misleading news. If text is present, extract and analyze it. Explain your reasoning and suggest how to verify the claim."},
                            {"role": "user", "content": [
                                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_bytes.decode("latin1")}}
                            ]}
                        ],
                        max_tokens=700,
                        temperature=0.2
                    )
                    result = response.choices[0].message.content
                    st.success("Analysis complete!")
                    st.markdown("**AI Analysis:**")
                    st.write(result)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please upload an image.")

st.info("This tool uses OpenAI GPT-4o to analyze news. Always cross-check with trusted sources.")
