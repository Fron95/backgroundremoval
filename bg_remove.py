import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
import zipfile

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your images")
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Convert image to bytes for download
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Process and display each image
def process_images(uploaded_files):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for uploaded_file in uploaded_files:
            if uploaded_file is not None:
                if uploaded_file.size > MAX_FILE_SIZE:
                    st.error("One of the uploaded files is too large. Please upload images smaller than 5MB.")
                    return
                else:
                    with st.container():
                        col1, col2 = st.columns(2)
                        image = Image.open(uploaded_file)
                        col1.write("Original Image :camera:")
                        col1.image(image)

                        fixed_image = remove(image)
                        col2.write("Fixed Image :wrench:")
                        col2.image(fixed_image)

                        # Add fixed image to ZIP
                        image_bytes = convert_image(fixed_image)
                        zip_file.writestr(f"{uploaded_file.name}_fixed.png", image_bytes)

    zip_buffer.seek(0)
    st.sidebar.download_button(
        label="Download All Fixed Images as ZIP",
        data=zip_buffer,
        file_name="fixed_images.zip",
        mime="application/zip"
    )


uploaded_files = st.sidebar.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if uploaded_files:
    process_images(uploaded_files)
