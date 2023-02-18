
'''
models:
text-davinci-003
text-babbage-001
'''

if __name__ == '__main__':
    from pachinkio.core.director import Director
    from pachinkio.core.oa_client import OpenAIClient
    import configparser

    config = configparser.ConfigParser()
    config.read('.env')
    org_id = config['open-ai']['organization-id']
    api_key = config['open-ai']['api-key']

    client = OpenAIClient(organization=org_id, 
        api_key=api_key, engine='text-babbage-001')
    director = Director(client, client)

    #start = "I love to drink milkshakes becuase they are creamy and sugary."
    #target = "I hate eating cake because it is spongy and too sweet."
    #director.interpolate_concepts(start, target, fanout=5, iterations=10)
    director.chain_of_intuition("how to implement cold fusion", 2)

    #director.run_telephone_game(20)
    #print(director.compare_statements(start, target))

    