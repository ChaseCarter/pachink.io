from injector import Injector

from pachinkio import create_app

if __name__ == '__main__':
    """Flask application entry point.
    """
    
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.prompts.prompts_module import PromptsModule

    injector = Injector([OpenAiApiModule('.env'), PromptsModule('./pachinkio/prompts/prompts_v1.ini')])
    app = create_app(injector)

    print("Initializing Flask application")
    app.run(debug = True)