from configparser import ConfigParser
from injector import Module

from pachinkio.core.prompts import Prompts

class PromptsV1Module(Module):
    def configure(self, binder):
        config = ConfigParser()
        print("Reading Prompt Configs")
        config.read_file(open('./pachinkio/prompts/prompts_v1.ini'))
        COI_base_prompt = config['COI']['base_prompt']
        interpolate_concepts_base_prompt = config['interpolate-concepts']['base_prompt']
        telephone_base_prompt = config['telephone']['base_prompt']

        prompts = Prompts(COI_base_prompt=COI_base_prompt, interpolate_concepts_base_prompt=interpolate_concepts_base_prompt, 
            telephone_base_prompt=telephone_base_prompt)
        binder.bind(Prompts, to=prompts)