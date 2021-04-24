import pytest
from django.test import Client
from swap_food.models import Aliment
from users.models import MyUser
from pytest_django.asserts import assertTemplateUsed, assertContains

client = Client()


@pytest.fixture
def test_password():
    return "user_test_pw"


@pytest.fixture
def create_user(db, test_password):
    user = MyUser.objects.create_user("user_test", "user_test@email.com",
                                      test_password)
    aliment = Aliment(name="chocolate")
    aliment.save()
    user.aliments_pref.add(aliment)
    return user


def test_register_get(client):
    """test eponym function"""
    response = client.get("/register/")
    assert response.status_code == 200
    assertTemplateUsed(response, "users/register.html")


def test_register_post(client, db):
    """test eponym function"""
    response = client.post('/register/', data={
        "username": "user_test_views",
        "email": "mail_test@exemple.fr",
        "password1": "dIJFEè9#0kfokdcx",
        "password2": "dIJFEè9#0kfokdcx"
        })
    account = MyUser.objects.get(username="user_test_views")
    assert MyUser.objects.get(email="mail_test@exemple.fr")
    assert response.status_code == 302


def test_profil(client, db, create_user, test_password):
    """test eponym function"""
    client.login(username=create_user.username, password=test_password)
    response = client.get("/profil/")
    assert response.status_code == 200
    assertTemplateUsed(response, "users/profil.html")
    assertContains(response, "user_test@email.com")


def test_aliments(client, db, create_user, test_password):
    """test eponym function"""
    client.login(username=create_user.username, password=test_password)
    response = client.get("/aliments/")
    assert response.status_code == 200
    assertContains(response, "chocolate")


def test_saving(client, db, create_user, test_password):
    """test eponym function"""
    client.login(username=create_user.username, password=test_password)
    aliment_to_add = Aliment(name="wine")
    aliment_to_add.save()
    response = client.post("/saving/", data={
        "aliment": "wine"
        })
    assert response.status_code == 200
    assert create_user.aliments_pref.get(name="wine")


def test_rating(client, db, create_user, test_password):
    """test eponym function"""
    client.login(username=create_user.username, password=test_password)
    response = client.post("/rating/", data={
        "aliment": "chocolate",
        "rate": 1
        })
    assert response.status_code == 200
    assert create_user.aliments_rate.get(name="chocolate")
    assert response.content == b'Rate done.'

def test_get_changemail(client, db, create_user, test_password):
    """test eponym function"""
    client.login(username=create_user.username, password=test_password)
    response = client.get('/change_mail/')
    assert response.status_code == 200
    assertTemplateUsed(response, "users/new_mail.html")

def test_post_changemail(client, db, create_user, test_password):
    """test eponym function"""
    client.login(username=create_user.username, password=test_password)
    response = client.post('/change_mail/', data={
        "new_email": "new_email@email.com"
        })
    assert response.status_code == 200
    assertTemplateUsed(response, "users/profil.html")
    assertContains(response, "new_email@email.com")
