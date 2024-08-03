########################################################################################################################
########################################################################################################################
import json
from typing import Any

import requests
import base64
import streamlit as st
import random
import copy
#from experiments.experimental_chatbots.technical_support.config import chatbot_config
from config import chatbot_config

########################################################################################################################
########################################################################################################################

api_address = chatbot_config["api_address"]

########################################################################################################################
########################################################################################################################

st.set_page_config(page_title=chatbot_config["page_title"],
                   page_icon=chatbot_config["page_icon"],
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)

#left_co, cent_co,last_co = st.columns(3)
#with cent_co:
#    st.image("https://static.wixstatic.com/media/63b1fb_4fb8962f303f4686822b59a8c284690a~mv2.png",
#             caption=None, width=None, use_column_width=True,
#             clamp=False, channels="RGB", output_format="auto")

#st.markdown("<h1 style='text-align: center; color: white;'>Assistente Fotovoltaico </h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = copy.deepcopy(chatbot_config["messages"])

if "ai_avatar_url" not in st.session_state:

    st.session_state.ai_avatar_url = chatbot_config["ai_avatar_url"]

if "user_avatar_url" not in st.session_state:

    st.session_state.user_avatar_url = chatbot_config["user_avatar_url"]

########################################################################################################################
########################################################################################################################


def parse_streamed_output(chunk: Any):

    return

def main():

    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=st.session_state.user_avatar_url):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar=st.session_state.ai_avatar_url):
                st.markdown(message["content"])

    if prompt := st.chat_input("Say something"):

        #url = f"{api_address}:8086/chat"

        st.session_state.messages.append({"role": "user", "content": prompt})

        #####################################################################
        # for secure
        if len(st.session_state.messages) > 10:
            st.session_state.messages = st.session_state.messages[-10:]
        #####################################################################

        with st.chat_message("user", avatar=st.session_state.user_avatar_url):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=st.session_state.ai_avatar_url):
            message_placeholder = st.empty()
            s = requests.Session()
            full_response = ""
            url = "http://34.78.163.86:8100/chains/stream_chain"
            #url = "http://127.0.0.1:8100/chains/stream_chain"
            payload = {
                "chain_id": "hf-embeddings__chat-openai_qa-chain",
                "query": {
                    "input": prompt,
                    "chat_history": st.session_state.messages
                },
                "inference_kwargs": {

                },
            }

            non_decoded_chunk = b''
            with s.post(url, json=payload, headers=None, stream=True) as resp:
                for chunk in resp.iter_lines():
                    if chunk:

                        if chunk.decode().startswith('''  "answer":'''):
                            chunk = "{" + chunk.decode() + "}"
                            chunk = json.loads(chunk)
                            chunk = chunk["answer"]
                            chunk = chunk.encode()
                            print(chunk)
                            non_decoded_chunk += chunk
                            try:
                                full_response += non_decoded_chunk.decode()
                                message_placeholder.markdown(full_response + "▌",
                                                             unsafe_allow_html=True)
                                non_decoded_chunk = b''
                            except UnicodeDecodeError:
                                pass
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

########################################################################################################################
########################################################################################################################


main()
#sidebar()
