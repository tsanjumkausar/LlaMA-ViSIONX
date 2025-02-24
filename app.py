import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

API_KEY = "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"
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG") 
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

st.title("🖼 Groq Lllma Vision - Image Analyzer")
st.write("Upload an image, and the Llama-3 Vision model will describe it!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    base64_image = encode_image(image)
    client = Groq(api_key=API_KEY)
    with st.spinner("Analyzing image... ⏳"):
        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                        ],
                    }
                ],
            )

            response = chat_completion.choices[0].message.content
            st.success("✅ Analysis Complete!")
            st.write("### 🔍 Description:")
            st.write(response)

        except Exception as e:
            st.error(f"⚠ Error: {e}")
st.write("Powered by *Groq Llama-3.2 Vision* 🚀")