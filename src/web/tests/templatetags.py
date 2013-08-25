from django.test import TestCase
from web.templatetags.seamless_extras import round_float

class TemplateTagTest(TestCase):
    def test_rating_rounding(self):
        self.assertEqual("1.0", round_float(1.0))
        self.assertEqual("0.0", round_float(0.0))
        self.assertEqual("6.1", round_float(6.133))
        self.assertEqual("6.2", round_float(6.19))
