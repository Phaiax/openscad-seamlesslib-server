"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from web.forms import ModuleForm
from web.tests.modulemodel import example_module
from django.utils import simplejson
from dateutil import parser

class SimpleTest(TestCase):
    def test_api_serves_all_data(self):
        M = ModuleForm(example_module).save()
        resp = self.client.get('/api/get-by-uniquename/' + M.uniquename + "/")
        self.assertContains(resp, M.guid, count=1)
        json = simplejson.loads(resp.content, encoding="UTF-8")
        self.assertEqual(json['guid'], M.guid)
        self.assertEqual(json['title'], M.title)
        self.assertEqual(json['description'], M.description)
        self.assertEqual(json['author'], M.author)
        self.assertEqual(json['author_acronym'], M.author_acronym)
        self.assertEqual(parser.parse(json['created']), M.created)
        self.assertEqual(json['finished'], M.finished)
        self.assertEqual(json['sourcecode'], M.sourcecode)
        self.assertEqual(json['documentation'], M.documentation)
        self.assertEqual(json['version'], M.version)
        self.assertEqual(json['modulename'], M.modulename)
        self.assertEqual(json['average_rating'], M.average_rating)
        self.assertEqual(json['number_of_ratings'], M.number_of_ratings)
        self.assertEqual(json['uniquename'], M.uniquename)
        self.assertNotContains(resp, "auth_code")
    def test_404_if_not_existant(self):
        resp = self.client.get('/api/get-by-uniquename/abc/')
        self.assertEqual(resp.status_code, 404)
        
    def test_api_delivers_version_info(self):
        resp = self.client.get('/api/version-info/')
        json = simplejson.loads(resp.content, encoding="UTF-8")
        self.assertEqual(json['server_version'], 2)
        self.assertEqual(json['min_supported_client'], 2)
        self.assertEqual(json['most_recent_client_version'], 2)
        