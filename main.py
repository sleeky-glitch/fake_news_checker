import streamlit as st
import openai
import base64

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
                    "Analyze the following news for signs of being fake or misleading, also do sentiment analysis "
                    "Explain your reasoning and, if possible, suggest how to verify the claim:\n\n"
                    f"{user_input}"
                )
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4.1",
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
    uploaded_file = st.file_uploader("Upload an image (screenshot, post, etc.)", type=["png", "jpg", "jpeg", "webp", "gif"])
    if st.button("Check Image for Fake News", key="image"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            with st.spinner("Analyzing image..."):
                try:
                    image_bytes = uploaded_file.read()
                    mime = uploaded_file.type  # e.g., "image/png"
                    # Only allow supported MIME types
                    if mime not in ["image/png", "image/jpeg", "image/webp", "image/gif"]:
                        st.error("Unsupported image format. Please upload PNG, JPEG, WEBP, or GIF.")
                    else:
                        def image_to_data_url(image_bytes, mime):
                            b64 = base64.b64encode(image_bytes).decode()
                            return f"data:{mime};base64,{b64}"
                        image_data_url = image_to_data_url(image_bytes, mime)
                        response = openai.chat.completions.create(
                            model="gpt-4.1",
                            messages=[
                                {"role": "system", "content": "You are a fact-checking assistant. Analyze the uploaded image for signs of fake or misleading news. If text is present, extract and analyze it. Explain your reasoning and suggest how to verify the claim, also provide a sentiment analysis and author of the claim, also try to provide original source."},
                                {"role": "user", "content": [
                                    {"type": "image_url", "image_url": {"url": image_data_url}}
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

st.info("Made with <3 by BSPL")
