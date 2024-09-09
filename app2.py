import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.title('Image to Pencil Sketch Converter')

st.markdown("Made by [Shailendra Singh](https://ssinghportfolio.netlify.app/)")


uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])


def dodgeV2(x, y):
    return cv2.divide(x, 255 - y, scale=256)

if uploaded_file is not None:
    
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    
    st.image(img, caption='Uploaded Image', use_column_width=True)

    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    img_invert = cv2.bitwise_not(img_gray)

    
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)

    
    sketch = dodgeV2(img_gray, img_smoothing)

    
    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=3)
    edges = cv2.bitwise_not(edges)

    
    pencil_sketch = cv2.multiply(sketch, edges, scale=1/256.0)

    
    st.image(pencil_sketch, caption='Pencil Sketch', use_column_width=True)

    
    def convert_image_to_bytes(img_array):
        """Convert the OpenCV image array to a downloadable byte format."""
        im_pil = Image.fromarray(img_array)  
        buf = io.BytesIO()
        im_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()
        return byte_im

    
    st.download_button(
        label="Download Sketch",
        data=convert_image_to_bytes(pencil_sketch),
        file_name="pencil_sketch.png",
        mime="image/png"
    )
