import datetime

from django.test import TestCase
from django.utils import timezone

from .models import *

# Create your tests here.
class PsybotModelTests(TestCase):
    
    def test_was_speech_valid(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is in the future.
            """
        
        future_question = Question(pub_date=time)
        self.assertEqual(response.code)
