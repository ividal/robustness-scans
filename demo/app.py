import streamlit as st
from loguru import logger

from blueprint.chatbot import Chatbot
from blueprint.settings import IPCC_REPORT_URL, OUTPUT_FOLDER, PROMPT_TEMPLATE

st.title("Blueprint Demo")

use_serialized = True
serialized_db_path = OUTPUT_FOLDER / "vectorstore" if use_serialized else None

chatbot = Chatbot(
    pdf=IPCC_REPORT_URL,
    prompt_template=PROMPT_TEMPLATE,
    local=False,
    output_folder=OUTPUT_FOLDER,
    serialized_db_path=serialized_db_path,
)

st.write("Chatbot initialized")

response = chatbot.chain.invoke(
    {"query": "Is sea level rise avoidable? When will it stop?"}
)

logger.info(response)

st.write(response)
