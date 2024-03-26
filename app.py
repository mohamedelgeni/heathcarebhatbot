# Step 1: Import All the Required Libraries

# We are creating a Webapp with Streamlit
import streamlit as st

# Replicate is an online cloud platform that allows us to host models and access the models through API
# Llama 2 models with 7B, 13 B and with 70B parameters are hosted on Replicated and we will access these models through API

import replicate
import os

# Step 2: Add a title to your Streamlit Application on Browser

st.set_page_config(page_title="💬  Chatbot ")

#Create a Side bar
with st.sidebar:
    st.title("💬 Chatbot")
    st.header("Settings")

    add_replicate_api = st.secrets["REPLICATE_API_TOKEN"]
    if not (add_replicate_api and add_replicate_api.startswith('r8_') and len(add_replicate_api)==40):
        st.warning('Please enter your credentials in the secrets.', icon='⚠️')
        st.stop()

    st.subheader(" ")

    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'

    temperature = 0.1
    top_p = 0.9
    max_length = 512

# Store the LLM Generated Response

if "messages" not in st.session_state.keys():
    st.session_state.messages=[{"role": "assistant", "content":"How may I assist you today?"}]

# Display the chat messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Create a Function to generate the Llama 2 Response
def generate_llama2_response(prompt_input):
    default_system_prompt="You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for data in st.session_state.messages:
        print("Data:", data)
        if data["role"]=="user":
            default_system_prompt+="User: " + data["content"] + "\n\n"
        else:
            default_system_prompt+="Assistant" + data["content"] + "\n\n"
    output=replicate.run(llm, input={"prompt": f"{default_system_prompt} {prompt_input} Assistant: ",
                                     "temperature": temperature, "top_p":top_p, "max_length": max_length, "repititon_penalty":1})

    return output


# User-Provided Prompt

if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a New Response if the last message is not from the assistant

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response=generate_llama2_response(prompt)
            placeholder=st.empty()
            full_response=''
            for item in response:
                full_response+=item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)

    message= {"role":"assistant", "content":full_response}
    st.session_state.messages.append(message)
