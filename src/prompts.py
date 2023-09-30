from langchain.prompts import PromptTemplate

travel_template_text = """

"""

travel_prompt = PromptTemplate(
    input_variables=["output_language", "destination", "additional requirements"],
    template=travel_template_text,
)
