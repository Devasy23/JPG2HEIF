import cv2
import streamlit as st
from PIL import Image
import pillow_heif

def jpg_to_heif(input_image):
    cv_img = cv2.imread(input_image, cv2.IMREAD_UNCHANGED)
    heif_file = pillow_heif.from_bytes(
    mode="BGR",
    size=(cv_img.shape[1], cv_img.shape[0]),
    data=bytes(cv_img)
    )
    return heif_file

def main():
    st.title("JPG to HEIF Converter")

    uploaded_file = st.file_uploader("Choose a JPG file", type=["jpg", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        fname = uploaded_file.name.split(".")[0]
        
        if st.button("Convert and Download"):
            # save uploaded file to temp dir
            with open("temp.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # convert to heif
            heif_file = jpg_to_heif("temp.jpg")
            heif_file.save("temp.heic", format= "HEIF")
            
            # download heif file
            with open("temp.heic", "rb") as f:
                bytes = f.read()
            st.download_button(
                label="Download HEIF File",
                data=bytes,
                file_name=f"{fname}.heic",
                mime="application/octet-stream"
            )
            

if __name__ == "__main__":
    main()
