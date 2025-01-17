import streamlit as st
from PIL import Image
import pillow_heif
from streamlit_option_menu import option_menu
import click
import os
import zipfile

def jpg_to_heif(input_image):
    cv_img = Image.open(input_image)
    heif = pillow_heif.from_pillow(cv_img)
    return heif

def convert_folder_to_heif(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.rsplit(".", 1)[0] + ".heic")
            heif_file = jpg_to_heif(input_path)
            heif_file.save(output_path, format="HEIF")

def convert_zip_to_heif(input_zip, output_folder):
    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    convert_folder_to_heif(output_folder, output_folder)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_image')
@click.argument('output_image')
def convert(input_image, output_image):
    heif_file = jpg_to_heif(input_image)
    heif_file.save(output_image, format="HEIF")

@cli.command()
@click.argument('input_folder')
@click.argument('output_folder')
def convert_folder(input_folder, output_folder):
    convert_folder_to_heif(input_folder, output_folder)

@cli.command()
@click.argument('input_zip')
@click.argument('output_folder')
def convert_zip(input_zip, output_folder):
    convert_zip_to_heif(input_zip, output_folder)

def main():
    st.title("JPG to HEIF Converter")
    choice = option_menu("",["Single", "Batch Conversion"], orientation="horizontal")
    
    if choice == "Single":
    
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
        
    elif choice == "Batch Conversion":
        uploaded_files = st.file_uploader("Choose Images", accept_multiple_files=True, type=["jpg", "jpeg", "png", "gif", "bmp"])

        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                st.image(uploaded_file, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)
                fname = uploaded_file.name.split(".")[0]
                
                if st.button(f"Convert and Download {uploaded_file.name}"):
                    # save uploaded file to temp dir
                    with open(f"{fname}.jpg", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # convert to heif
                    heif_file = jpg_to_heif(f"{fname}.jpg")
                    heif_file.save(f"{fname}.heic", format= "HEIF")
                    
                    # download heif file
                    with open(f"{fname}.heic", "rb") as f:
                        bytes = f.read()
                    st.download_button(
                        label=f"Download HEIF File: {fname}.heic",
                        data=bytes,
                        file_name=f"{fname}.heic",
                        mime="application/octet-stream"
                    )

if __name__ == "__main__":
    cli()
    main()
