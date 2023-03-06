"""
For manual testing & utilizing Director from the command line without wrapping it in a Flask application.
"""

if __name__ == '__main__':
    from injector import Injector
    
    from pachinkio.core.director import Director
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.prompts.prompts_module import PromptsModule

    injector = Injector([OpenAiApiModule('.env'), PromptsModule('./pachinkio/prompts/prompts_v1.ini')])
    director = injector.get(Director)

    #start = "I love to drink milkshakes becuase they are creamy and sugary."
    #target = "I hate eating cake because it is spongy and too sweet."
    #director.interpolate_concepts(start, target, fanout=5, iterations=10)
    director.chain_of_intuition("how to implement cold fusion", 2)
    #director.compare_statements("statement a", "statement b")
