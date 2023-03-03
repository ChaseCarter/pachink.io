
def test_compare_statements(client):
    response = client.post("/", data={"statement1": "statement a", "statement2": "statement b"})
    print(response)