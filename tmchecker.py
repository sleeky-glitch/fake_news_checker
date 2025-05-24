import streamlit as st
import openai
import base64
from PIL import Image
import io

# Set up OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="Trademark Authenticity Checker", page_icon="🔍")
st.title("🔍 Trademark Authenticity Checker")
st.write("Upload two trademark images to compare them. The AI will analyze which might be fake and highlight the differences.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Image 1")
    uploaded_file1 = st.file_uploader("Upload first trademark image", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_file1:
        st.image(uploaded_file1, caption="Image 1", use_container_width=True)

with col2:
    st.subheader("Image 2")
    uploaded_file2 = st.file_uploader("Upload second trademark image", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_file2:
        st.image(uploaded_file2, caption="Image 2", use_container_width=True)

if st.button("Compare Trademarks"):
    if uploaded_file1 is not None and uploaded_file2 is not None:
        with st.spinner("Analyzing trademarks..."):
            try:
                # Convert images to data URLs
                def image_to_data_url(file):
                    image_bytes = file.read()
                    file.seek(0)  # Reset file pointer
                    mime = file.type
                    b64 = base64.b64encode(image_bytes).decode()
                    return f"data:{mime};base64,{b64}"

                image1_url = image_to_data_url(uploaded_file1)
                image2_url = image_to_data_url(uploaded_file2)

                # Send both images to OpenAI for analysis
                response = openai.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": "You are a trademark authentication expert. Compare the two uploaded trademark images and identify which might be fake or counterfeit. Analyze design elements, colors, proportions, text, and other details. Highlight all differences between the images and explain your reasoning."},
                        {"role": "user", "content": [
                            {"type": "text", "text": "Compare these two trademark images and identify which might be fake and why:"},
                            {"type": "image_url", "image_url": {"url": image1_url}},
                            {"type": "image_url", "image_url": {"url": image2_url}}
                        ]}
                    ],
                    max_tokens=800,
                    temperature=0.2
                )

                result = response.choices[0].message.content
                st.success("Analysis complete!")
                st.markdown("### Trademark Comparison Analysis")
                st.markdown(result)

            except Exception as e:
                st.error(f"Error during analysis: {e}")
    else:
        st.warning("Please upload both trademark images for comparison.")

st.info("Note: This tool provides an AI-based analysis and should not replace professional legal advice for trademark disputes.")
