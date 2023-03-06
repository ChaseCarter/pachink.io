
def test_compare_statements(client):
    response = client.post("/compare-statements", json={"statement1": "statement a", "statement2": "statement b"})
    print(response)
    assert response.status_code == 200
    response_json = response.json
    assert "similarity" in response_json
    assert float(response_json["similarity"])

def test_interpolate_concepts(client):
    response = client.post("/interpolate-concepts", json= {
        "startStatement": "I love to drink milkshakes becuase they are creamy and sugary.",
        "targetStatement": "I hate eating cake because it is spongy and too sweet.",
        "iterations": 2,
        "fanout": 2
    })
    assert response.status_code == 200
    response_json = response.json
    assert "steps" in response_json
    steps = response_json["steps"]
    assert len(steps) > 0
    first_step = steps[0]
    assert len(first_step) == 2
    assert float(first_step[1]) 
    assert "terminationReason" in response_json

def test_telephone(client):
    response = client.post("/telephone", json={
        "statement": "Joe gave Alice two white roses and a puppy, how odd.",
        "iterations": 2,
        "temperature": 1.1
    })
    assert response.status_code == 200
    response_json = response.json
    assert "endStatement" in response_json
    assert "steps" in response_json
    assert len(response_json["steps"]) == 3
