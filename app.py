import streamlit as st
from gradio_client import Client
from PyPDF2 import PdfReader

# Initialize the Gradio clients
medical_client = Client("ruslanmv/Medical-Llama3-Chatbot")
arabic_client = Client("MohamedRashad/Arabic-Chatbot-Arena")

# Streamlit app title
st.title("Medical Llama 3 Chatbot")

# Tab layout for the two chatbots
tab1, tab2 = st.tabs(["Medical Chatbot", "general Chatbot"])

with tab1:
    st.header("Medical Llama 3 Chatbot")

    # File upload for PDF
    uploaded_file = st.file_uploader("Upload your medical history (PDF)", type="pdf")

    if uploaded_file is not None:
        # Extract text from PDF
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        st.write("Extracted Text:")
        st.write(pdf_text)

        # Input field for additional question
        question = st.text_input("Enter your question:")

        if st.button("Get Medical Advice"):
            # Call the Gradio model with extracted text and question
            result = medical_client.predict(
                symptoms=pdf_text,
                question=question,
                api_name="/predict"
            )
            # Display the result
            st.write("Response:")
            st.write(result)

with tab2:
    st.header("general  Arabic Chatbot ")

    # Text input for user
    user_input = st.text_input("You: ", "")

    # Button to send the user input
    if st.button("Send"):
        if user_input:
            # Call the Gradio client with the user input
            result = arabic_client.predict(
                system_prompt="أنت متحدث لبق باللغة العربية!",
                input_text=user_input,
                new_chatbot=[],
                max_new_tokens=120,
                temperature=0.2,
                top_p=0.9,
                repetition_penalty=1.1,
                api_name="/generate_both"
            )

            def clean_output(output):
                # Convert list of lists to string and replace unwanted characters
                text = str(output)
                text = text.replace("[[", "").replace("]]", "").replace("', '", "\n\n")
                text = text.replace("\\n", "\n")
                return text

            formatted_result = clean_output(result)

            # Display the formatted result
            st.markdown(f"**Bot:**\n\n{formatted_result}", unsafe_allow_html=True)
