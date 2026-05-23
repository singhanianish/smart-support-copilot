import os
import streamlit as st

from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()


API_KEY = (
    st.secrets.get(
        "AZURE_OPENAI_API_KEY",
        os.getenv("AZURE_OPENAI_API_KEY")
    )
)

ENDPOINT = (
    st.secrets.get(
        "AZURE_OPENAI_ENDPOINT",
        os.getenv("AZURE_OPENAI_ENDPOINT")
    )
)

API_VERSION = (
    st.secrets.get(
        "AZURE_OPENAI_API_VERSION",
        os.getenv("AZURE_OPENAI_API_VERSION")
    )
)

DEPLOYMENT_NAME = (
    st.secrets.get(
        "AZURE_GPT_DEPLOYMENT",
        os.getenv("AZURE_GPT_DEPLOYMENT")
    )
)


client = AzureOpenAI(
    api_key=API_KEY,
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT
)