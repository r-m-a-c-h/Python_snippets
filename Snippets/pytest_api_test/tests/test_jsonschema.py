import jsonschema
import requests 

schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["id", "name", "email"]
}

def test_user_schema(base_url):
    response = requests.get(f"{base_url}/users/1")
    data = response.json()
    jsonschema.validate(instance=data, schema=schema)
