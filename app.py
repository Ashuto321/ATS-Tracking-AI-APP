#1. we need a feild to put for jb
#2.upload the pdf
#3.PDF to Image----> processing--->google gemini pro
# we need to create prompt template{multiple}

import base64
import io
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
       model=genai.GenerativeModel('gemini-1.5-flash')
       if not pdf_content or len(pdf_content) == 0:
            st.error("Error: PDF content is empty!")
       else:
           response = model.generate_content([input, pdf_content[0], prompt])
           return response.text

def input_pdf_setup(uploaded_file):
       if uploaded_file is not None:
       ## convert the pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        #convert to bytes
        img_byte_arr= io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()


        pdf_parts = [
               {
               "mime_type": "image/jpeg",
               "data": base64.b64encode(img_byte_arr).decode()# encode to base64
               }
        ]
        return pdf_parts
       else:
             raise FileNotFoundError("No file uploaded")


#streamlit APP

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Discription: ",key="input")
uploaded_file= st.file_uploader("Upload your resume(PDF)...", type=["pdf"])


if uploaded_file is not None:
     st.write("PDF Uploaded Successfully")

submit1= st.button("Tell me about the resume")

submit2= st.button("How can i improve my skills")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
     if uploaded_file is not None:
          pdf_content=input_pdf_setup(uploaded_file)
          response=get_gemini_response(input_prompt1,pdf_content,input_text)          
          st.subheader("The Responses is")
          st.write(response)
     else:
          st.write("Please Upload the resume")

elif submit2:
     if uploaded_file is not None:
          pdf_content=input_pdf_setup(uploaded_file)
          response=get_gemini_response(input_prompt2,pdf_content,input_text)          
          st.subheader("The Responses is")
          st.write(response)
     else:
          st.write("Please Upload the resume")























#for checking model list in api keys

# import google.generativeai as genai

# # Configure API key
# genai.configure(api_key="AIzaSyBKHSu9MTGOC5kwfO2lf-r95ZIWz8NDgdI")

# # List available models
# models = genai.list_models()

# # Print model names
# for model in models:
#     print(model.name, "-", model.description)
