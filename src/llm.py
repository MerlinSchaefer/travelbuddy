from langchain.llms import OpenAI, OpenAIChat


def load_base_LLM(openai_api_key, temperature: float = 0.7):
    """"""
    return OpenAI(temperature=temperature, openai_api_key=openai_api_key)


def load_chat_LLM(openai_api_key, temperature: float = 0.7):
    """"""
    return OpenAIChat(temperature=0.7, openai_api_key=openai_api_key)
