from django.test import Client

client = Client()
def test_home(client):
    """test home page view"""
    response = client.get('/home/')
    assert response.status_code == 200

def test_research(client, db):
    """test search food view"""
    response = client.get('/research/', {'search_food': 'nutella'})
    assert response.status_code == 200