import pytest

from ..models import UserExtra

def test_create_user_without_email():
    with pytest.raises(SystemExit):
        UserExtra.objects.create(email="", denominazione="denominazione")

def test_create_user_without_denominazione():
    with pytest.raises(SystemExit):
        UserExtra.objects.create(email="email@test.it", denominazione="")