import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure the Generative AI API
genai.configure(api_key="APIKEY")

# Load the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to Analyze the Scene in the Image
def analyze_scene(uploaded_image):
    try:
        # Convert the image to bytes
        image_bytes = uploaded_image.getvalue()

        # Send the image and prompt to the API
        response = model.generate_content(
            [  # Input includes both image and text
                {"mime_type": "image/jpeg", "data": image_bytes},
                "Describe the scene in this image."
            ]
        )
        return response.text
    except Exception as e:
        return f"Scene analysis error: {str(e)}"

# Streamlit App
st.title("Real-Time Scene Understanding")

# Upload Image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Analyze the scene using the Generative AI API
    with st.spinner("Analyzing the image..."):
        scene_description = analyze_scene(uploaded_file)
        st.write("Scene Description:")
        st.write(scene_description)
