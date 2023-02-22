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

    query = "Bob Dylan's hit song “Yellow Rush” has baffled fans and critics alike. Its cryptic tone and lack of any obvious message or topic bothers some, but its use of vivid imagery makes it an instant classic. The lyrics are beautiful: \n\
I saw you standing on the corner, \n\
With a yellow rose in your hand, \n\
You looked like you were waiting, \n\
But I didn't understand, \n \n\
I felt an awful chill, \n\
in the early evening sun, \n\
You looked like an angel, \n\
so I had to turn and run, \n\
But everywhere I went, \n\
the yellow rush was coming on. \n \n"
    director.chain_of_intuition(query, 3, promptOverride=True)
