import pytest
from mixer.backend.django import mixer
from .forms import *

pytestmark = pytest.mark.django_db


class TestMyModelForm:
    def test_mymodelform(self):
        form = WithdrawalForm()
        assert False is form.is_valid()

        data = {"price": "100"}
        form = WithdrawalForm(data=data)
        assert False is form.is_valid()
        assert form.errors
        assert "other_model" in form.errors, "other_model cant be null"

        other_model = mixer.blend("myapp.MyOtherModel")
        data = {
            "price": "100",
            "other_model": other_model.pk
        }
        form = WithdrawalForm(data=data)
        assert True is form.is_valid()
        assert not form.errors, "Should be no errors, when form is valid"

    def test_clean(self):
        other_model = mixer.blend("myapp.MyOtherModel")
        data = {
            "price": "100",
            "other_model": other_model.pk
        }
        form = WithdrawalForm(data=data)
        assert form.is_valid()

        # Test clean_name method
        data["price"] = "forty two"
        form = WithdrawalForm(data=data)
        assert False is form.is_valid()
        assert "name" in form.errors

        # Test clean method
        data["name"] = "42"
        form = WithdrawalForm(data=data)
        assert "__all__" in form.errors
        assert False is form.is_valid()

        # Test error code in clean method
        data["name"] = "21"
        form = WithdrawalForm(data=data)
        assert "__all__" in form.errors
        assert False is form.is_valid()
        assert form.errors["__all__"].as_data()[0].code == "truth_bending"


from django.test import TestCase

# Create your tests here.
