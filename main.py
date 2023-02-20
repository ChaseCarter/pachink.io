if __name__ == '__main__':
    from pachinkio.core.director import Director
    from pachinkio.core.oa_client import OpenAIClient
    import configparser

    config = configparser.ConfigParser()
    config.read('.env')
    org_id = config['open-ai']['organization-id']
    api_key = config['open-ai']['api-key']

    client = OpenAIClient(organization=org_id, 
        api_key=api_key, engine='text-davinci-003')
    director = Director(client, client)

    query = "the perfect form of government"
    director.chain_of_intuition(query, 3, promptOverride=False)
