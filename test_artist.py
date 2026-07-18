import requests

session = requests.Session()
# Login as admin
resp = session.post("http://127.0.0.1:5000/login", data={"email": "admin@inkmaster.id", "password": "admin"})
print("Login status:", resp.status_code)

# Add artist
data = {
    "name": "Test Artist via Script",
    "specialization": "Testing",
    "experience": "1",
    "instagram": "test",
    "status": "active",
    "description": "Test"
}
resp = session.post("http://127.0.0.1:5000/api/artists", json=data)
print("Add artist response:", resp.status_code, resp.text)
