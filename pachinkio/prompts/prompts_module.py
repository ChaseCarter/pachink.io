from configparser import ConfigParser
from injector import Module

from pachinkio.core.prompts import Prompts

class PromptsModule(Module):

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file

    def configure(self, binder):
        config = ConfigParser()
        print("Reading Prompt Configs from file", self.config_file)
        config.read_file(open(self.config_file))
        COI_base_prompt = config['COI']['base_prompt']
        interpolate_concepts_base_prompt = config['interpolate-concepts']['base_prompt']
        telephone_base_prompt = config['telephone']['base_prompt']

        prompts = Prompts(COI_base_prompt=COI_base_prompt, interpolate_concepts_base_prompt=interpolate_concepts_base_prompt, 
            telephone_base_prompt=telephone_base_prompt)
        binder.bind(Prompts, to=prompts)