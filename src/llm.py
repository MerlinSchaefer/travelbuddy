from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI


def load_base_LLM(openai_api_key, temperature: float = 0.7):
    """"""
    return OpenAI(temperature=temperature, openai_api_key=openai_api_key)


def load_chat_LLM(openai_api_key, temperature: float = 0.7):
    """"""
    return ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key)


def create_conversation_chain(llm, verbose=True):
    pass
