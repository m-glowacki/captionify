import streamlit as st
import requests
import os
import shutil
import zipfile
import uuid

API_TOKEN = st.secrets["api_key"]
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to process images and generate captions using the API
def process_images(image_folder):
    progress_bar = st.progress(0)
    total_files = len([filename for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.jpeg', '.png'))])
    processed_files = 0
    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(image_folder, filename)
            with open(image_path, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            if response.status_code == 200:
                caption = response.json()[0]['generated_text']
                new_filename = f"{caption.replace(' ', '_')}_{filename}"
                os.rename(image_path, os.path.join(image_folder, new_filename))
            else:
                st.error(f"Error processing {filename}: {response.text}")
            processed_files += 1
            progress_bar.progress(processed_files / total_files)

# Streamlit app
def main():
    # Set page title and configure layout
    st.set_page_config(page_title="Captionify.ai", page_icon=":camera:", layout="wide")

    st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
                 .css-1iyw2u1 {
                    display: none;
                }
        </style>
        """, unsafe_allow_html=True)


    st.markdown("""
    <style>
    .big-font {
        font-size:70px !important;
        font-weight: 600;
        line-height:100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<p class="big-font"> <br> </p><p class="big-font-orange"> <br>Captionify.ai</p>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    .big-font-orange {
        font-size:140px !important;
        color: orange;
        font-weight: 600;
        line-height:100%;
        
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .css-1dj0hjr {
        color: orange;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        display: table-cell;
    }
        <style>"""
    ,unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Reimagine your gallery with magic captions!")

    # Upload folder of images
    uploaded_folder = st.file_uploader("Upload a folder of images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

    if uploaded_folder is not None and len(uploaded_folder) > 0:
        st.info("Processing gallery...")

        # Create a temporary directory to store processed images
        session_id = str(uuid.uuid4())
        tmp_dir = os.path.join("tmp", session_id)
        os.makedirs(tmp_dir, exist_ok=True)

        # Save uploaded images to the temporary directory
        for uploaded_file in uploaded_folder:
            with open(os.path.join(tmp_dir, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getvalue())

        # Process images in the temporary directory
        process_images(tmp_dir)

        # Create a zip file with the renamed images
        zip_file_path = os.path.join("tmp", f"renamed_gallery_{session_id}.zip")
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tmp_dir))

        st.success("Finished!")
        with open(zip_file_path, "rb") as f:
            zip_file_bytes = f.read()
        st.download_button(label="Return my gallery!", data=zip_file_bytes, file_name="renamed_gallery.zip", mime="application/zip")
    
    elif uploaded_folder is not None and len(uploaded_folder) == 0:  # No files uploaded
        st.info("Upload single photo or folder to proceed")
    
    st.markdown("---")
    #st.video("https://www.youtube.com/watch?v=bC5XoMVYCGQ", format="video/mp4", start_time=0, subtitles=None)
    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        center_button = st.link_button("Powered by HuggingFace 🤗", "https://streamlit.io/gallery")

# Run the app
if __name__ == "__main__":
    main()
