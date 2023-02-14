
if __name__ == '__main__':
    from pachinkio.core.director import Director
    from pachinkio.core.oa_completions import OpenAICompletions

    # TODO: read secrets from separate file/env variables
    completions = OpenAICompletions(organization='<org-id>', 
        api_key='<api-key>', engine='text-babbage-001')
    director = Director(completions)

    director.run_cycles(20)
