from dataclasses import dataclass

@dataclass
class Prompts:
    """DTO for base prompts.
    """

    COI_base_prompt: str
    interpolate_concepts_base_prompt: str
    telephone_base_prompt: str
