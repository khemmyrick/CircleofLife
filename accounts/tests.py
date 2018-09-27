from django.core.urlresolvers import reverse
from django.test import TestCase

from . import models


class ModelTests(TestCase):
    def setUp(self):
        self.pink = models.Account.objects.create(
            username="RoseQuartz",
            email="fthediamonds@crystalgems.com",
            first_name="Pink",
            last_name="Diamond",
            birth_date="07/21/83",
            country="United States",
            website="http://steven-universe.wikia.com/wiki/Steven_Universe_Wiki",
            bio="Just smile and nod theyll fall into line.",
            password="Blue#DleavethisW0rld",
        )
        
    def test_account_creation(self):
        self.assertEqual(self.pink.username, 'RoseQuartz')