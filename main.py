
'''
models:
text-davinci-003
text-babbage-001
'''

if __name__ == '__main__':
    from pachinkio.core.director import Director
    from pachinkio.core.oa_client import OpenAIClient

    # TODO: read secrets from separate file/env variables
    client = OpenAIClient(organization='<org-id>', 
        api_key='<api-key>', engine='text-babbage-001')
    director = Director(client, client)

    start = "I love to drink milkshakes."
    target = "I hate eating cake."
    director.interpolate_concepts(start, target, fanout=5, iterations=10)

    #director.run_telephone_game(20)
    #print(director.compare_statements(start, target))

    