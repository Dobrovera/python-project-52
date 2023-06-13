from django.test import TestCase
from task_manager.users.forms import SignUpForm


class TestUserForms(TestCase):

    def test_sign_up_form_valid_data(self):

        form = SignUpForm(data={
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "JANEDOE",
            "password1": 123456,
            "password2": 123456
        })

        self.assertTrue(form.is_valid())

    def test_sign_up_form_invalid_data(self):

        '''
        form1:
            The entered passwords do not match
        form2:
            Username is required field;
            The entered password is too short.
                It must contain at least 3 characters.
        '''

        form1 = SignUpForm(data={
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "JANEDOE",
            "password1": 123456,
            "password2": 123
        })

        form2 = SignUpForm(data={
            "first_name": "",
            "last_name": "",
            "username": "",
            "password1": 12,
            "password2": 12
        })

        self.assertFalse(form1.is_valid())
        self.assertEquals(len(form1.errors), 1)
        self.assertFalse(form2.is_valid())
        self.assertEquals(len(form2.errors), 2)
