from typing import Dict, Optional

from langchain.prompts import PromptTemplate

system_text_travel_agent = """You are a friendly travel planning assistant.
Speak in a polite but informal tone.
You will be provided with specific details below (indicated by the single quotation marks).
Details may include:
the destination and duration,
the way of travel (e.g. plane or ship),
the type of travel (e.g. roundtrip vs. staying in one location and exploring it's surroundings),
where to mainly explore (e.g. city vs. nature or both).
additional things to consider

You're goal is to provide an overview over the destination, including best travel times,
 list the best things to do and rough cost estimates,
Then create a rough daily itinerary given the specifications.
For the itinerary create a Markdown table with a column for the days and one for the activities.

If you are unsure about any part of the answer indicate it clearly.
Answer in German and use German currency if possible.
"""

user_text_travel_prompt = """
`The trip should go to {destination}. For the duration of {duration}.
The prefered way of travel is by {mode_of_transport} (changeable depending on safety and cost).
It should be a {mode_of_travel}.
The exploration focus is {mode_of_exploration}.
{additional_info} `

"""
# travel_user_prompt = PromptTemplate(
#    input_variables=[
#        "destination",
#        "duration",
#        "mode_of_transport",
#        "mode_of_travel",
#        "mode_of_exploration",
#        "additional_info",
#    ],
#    template=travel_user_prompt_text,
# )

sample_prompt_data = {
    "destination": "one or more african countries that allow for a safari tour",
    "duration": "at least two weeks no longer than three",
    "mode_of_transport": "plane and then using the best local sources (e.g public transport or rental car)",
    "mode_of_travel": "roundtrip",
    "mode_of_exploration": "Nature",
    "additional_info": "The travel group consist of a middle aged women and three young adults.",
}

prompt_input_modifiers = dict(
    roundtrip_modifier=" however not with too many single destinations allowing for a couple nights at each location.",
    single_location_modifier=" however still allowing for daytrips further away and variability in locations",
    nature_modifier=" however cities are still welcome",
    city_modifier=" however nature is still welcome",
)


def apply_input_modifiers(
    input_data: Dict[str, str], modifiers: Dict[str, str] = prompt_input_modifiers
) -> Dict[str, str]:
    """Modify the input dictionary based on partial matches between input
    values and modifier keys.

    Args:
        input_data (dict): The input dictionary to be modified.
        modifiers (dict): The dictionary of modifiers where keys partially match input values.

    Returns:
        dict: A new dictionary with modified values based on partial matches with modifiers.
    """
    modified_data = input_data.copy()
    for key, value in input_data.items():
        for modifier_key, modifier_value in modifiers.items():
            if value.lower() in modifier_key:
                modified_data[key] = f"{value}{modifier_value}"
    return modified_data


def create_initial_prompt_template(
    user_prompt_text: str,
    system_prompt_text: Optional[str] = None,
    input_data: Dict[str, str] = None,
) -> PromptTemplate:
    """Create an initial formatted prompt template for a chat conversation,
    with variable substitutions.

    Args:
        user_prompt_text (str): The user-specific prompt text to be included in the template.
        system_prompt_text (str, optional): The system-specific prompt text (prefix) to be included in the template.
            Defaults to None.
        input_data (dict, optional): A dictionary containing variable substitutions for the template.
            Defaults to None.

    Returns:
        PromptTemplate: A langchain prompt template with variables and template text.
    """
    initial_prompt = PromptTemplate(
        input_variables=list(input_data.keys()),
        template=f"{system_prompt_text}{user_prompt_text}",
    )
    initial_prompt = initial_prompt.format(**input_data)
    return initial_prompt
