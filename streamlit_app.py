import torch
from PIL import Image
import requests
import os
import shutil
import subprocess
import streamlit as st
from streamlit_lottie import st_lottie

cwd = os.getcwd()

st.set_page_config(page_title='My Webpage', page_icon=':tade:', layout='wide')

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

local_css('style/style.css')

# Load uploaded image
@st.cache
def load_uploaded_image(img):
    im = Image.open(img)
    return im


# Load Assets
lottie_header_ani = load_lottieurl('https://assets2.lottiefiles.com/packages/lf20_bnh0nfjr.json')
lottie_coding  = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_9ycwmgb9.json')
img_sample = Image.open('images/sample.jpg')

# Header Section
with st.container():
    st_lottie(lottie_header_ani, height=300)
    st.subheader('Hi :wave:')
    st.title('A data science project')
    st.write('Recommend food')

# What I do
with st.container():
    st.write('---') # divider
    left_col, right_col = st.columns(2)
    with left_col:
        st.header('How it works')
        st.write('##')
        st.write(
            '''
            In the below section, you can
            - type in ingredients name
            - upload food image
            '''
        )

    # # https://lottiefiles.com/ 
    with right_col:
        st_lottie(lottie_coding, height=300, key='coding')

# Project
with st.container():
    st.write('---')
    st.header('My projects')
    st.write('##')
    image_col, text_col = st.columns((1, 2))

    with image_col:
        # insert image
        st.image(img_sample)

    with text_col:
        st.subheader('This is a smaple image')
        st.write('Please upload image like this')

# Upload Image
with st.container():
    st.write('---')
    image_file = st.file_uploader("Please upload a food image",type=['png','jpeg','jpg'])

    if image_file is not None:
        file_details = {"FileName": image_file.name,"FileType": image_file.type}

        st.write(file_details)

        img = Image.open(image_file)
        st.write('Original image')
        st.image(img, use_column_width=False)

        with open(os.path.join(f'{cwd}/user_uploads', image_file.name), "wb") as f: 
            f.write(image_file.getbuffer())         
            st.success("Saved File")
  
    folderPath = f'{cwd}/inferenced_imgs'; 
    # Check Folder is exists or Not
    if os.path.exists(folderPath):    
        # Delete Folder code
        shutil.rmtree(folderPath)
    
    #     st.write("The folder has been deleted successfully!")
    # else:
    #     st.write("Can not delete the folder as it doesn't exists")

    # Display inference
    subprocess.run(['python3', f'{cwd}/yolov5/detect.py', 
                '--source', f'{cwd}/user_uploads',
                '--weights', f'{cwd}/yolov5/runs/train/exp2/weights/best.pt',
                '--project', f'{cwd}',
                '--name', 'inferenced_imgs',
                '--save-txt'
                ])
    
    # Display image in Flask application web page
    infer_img = os.path.join(f'{cwd}/inferenced_imgs/', image_file.name)
    st.write('Inferenced image')
    st.image(infer_img, use_column_width=False)


# Contact form
with st.container():
    st.write('---')
    st.header('get in touch with the team')
    st.write('##')

    # https://formsubmit.co/
    contact_form = '''
    <form action="https://formsubmit.co/annieycchiu@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" required>
     <input type="email" name="email" required>
     <textarea name="message" placeholder="Your message here" required></textarea>
     <button type="submit">Send</button>
</form>
    '''

    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_col:
        st.empty()


