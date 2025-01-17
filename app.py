import streamlit as st
from io import BytesIO
import zipfile
import time
from converter import jpg_to_heif_buffer
import asyncio
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="Image Converter", layout="centered")

def main():
    st.title("JPG to HEIF/HEIC Converter")
    tab1, tab2 = st.tabs(["Single Image", "Batch Images"])
    with tab1:
        uploaded_file = st.file_uploader("Upload JPG file", type=["jpg", "jpeg"])
        if uploaded_file:
            filename = uploaded_file.name
            st.image(uploaded_file, caption="Original Image", use_column_width=True)

            if st.button("Convert and Download"):
                with st.spinner("Converting..."):
                    output_buffer = jpg_to_heif_buffer(uploaded_file.getbuffer())
                    st.success("Conversion complete!")
                
                st.download_button(
                    "Download HEIF/HEIC File",
                    output_buffer,
                    file_name=f"{filename.rsplit('.', 1)[0]}.heic",
                    mime="image/heif"
                )

    with tab2:
        uploaded_files = st.file_uploader("Upload Multiple Images", type=["jpg", "jpeg"], accept_multiple_files=True)

        if uploaded_files:
            file_stats = {"original_size": 0, "converted_size": 0}
            converted_files = {}

            progress_bar = st.progress(0)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            executor = ThreadPoolExecutor()

            async def process_file(uploaded_file):
                output_buffer = await loop.run_in_executor(executor, jpg_to_heif_buffer, uploaded_file.getbuffer())
                return uploaded_file.name, output_buffer, uploaded_file.size, output_buffer.getbuffer().nbytes

            async def process_files(files):
                tasks = [process_file(file) for file in files]
                for i, task in enumerate(asyncio.as_completed(tasks)):
                    fname, output_buffer, original_size, converted_size = await task
                    file_stats["original_size"] += original_size
                    file_stats["converted_size"] += converted_size
                    converted_files[fname] = output_buffer
                    progress_bar.progress((i + 1) / len(files))

            loop.run_until_complete(process_files(uploaded_files))

            # Show stats
            st.metric("Original Size", f"{file_stats['original_size'] / 1e6:.2f} MB")
            st.metric("Converted Size", f"{file_stats['converted_size'] / 1e6:.2f} MB")
            st.metric("Space Saved", f"{(file_stats['original_size'] - file_stats['converted_size']) / 1e6:.2f} MB")

            # Download All as ZIP
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for fname, fbuffer in converted_files.items():
                    zipf.writestr(fname.replace(".jpg", ".heic"), fbuffer.getvalue())
            zip_buffer.seek(0)

            st.download_button(
                "Download All as ZIP",
                data=zip_buffer,
                file_name="converted_images.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
