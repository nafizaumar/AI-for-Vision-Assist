import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from gtts import gTTS
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("Text-to-Speech Conversion for Visual Content")

# Upload image
uploaded_file = st.file_uploader("Upload an image with text", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Preprocess the image
    image = image.convert("L")  # Convert to grayscale
    image = ImageOps.invert(image)  # Invert colors for better contrast
    image = image.point(lambda x: 0 if x < 128 else 255)  # Apply binary thresholding
    image = ImageEnhance.Contrast(image).enhance(2.5)  # Increase contrast

    # Extract text
    st.write("Extracting text from the image...")
    extracted_text = pytesseract.image_to_string(image)

    if extracted_text.strip():
        st.write("Extracted Text:")
        st.text(extracted_text)

        # Convert to speech
        tts = gTTS(text=extracted_text, lang="en")
        tts.save("output.mp3")
        st.audio("output.mp3", format="audio/mp3")

        st.success("Text has been successfully converted to speech!")
    else:
        st.error("No text found in the image. Please try another image.")
