import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
from io import BytesIO
import base64
import zipfile

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your images")
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
TARGET_SIZE = (480, 328)  # 원하는 이미지 크기, 예: 800x600

# Convert image to bytes for download
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Resize and add a white background
from PIL import Image, ImageOps

# Resize the entire image without cropping and center it on a white background
def resize_and_background(image, target_size=TARGET_SIZE, image_size=(350, 250), background_color=(255, 255, 255)):
    # 이미지 배경 제거
    image_no_bg = remove(image)
    # 이미지 전체 크기 조정 (비율 유지하지 않음)
    image_resized = image_no_bg.resize(image_size, Image.ANTIALIAS)
    # 흰색 배경 생성 (480x328)
    background = Image.new("RGB", target_size, background_color)
    # 조정된 이미지를 배경의 중앙에 배치
    background.paste(image_resized, ((target_size[0] - image_size[0]) // 2, (target_size[1] - image_size[1]) // 2), mask=image_resized.split()[3] if image_resized.mode == 'RGBA' else None)
    return background






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

                        fixed_image = resize_and_background(image)
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
