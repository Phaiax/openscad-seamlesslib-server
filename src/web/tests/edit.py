from django.http.response import HttpResponseRedirect, HttpResponse
from django.test import TestCase
from modulemodel import example_module
from web.forms import ModuleForm
from web.models import Module
  
    
class PagesTest(TestCase):
    def test_edit_page_checks_auth_code(self):
        M = ModuleForm(example_module).save()
        resp = self.client.get('/edit/' + M.guid + "/auth/" + M.auth_code + "/")
        self.assertContains(resp, example_module['sourcecode'])
        resp = self.client.get('/edit/' + M.guid + "/auth/" + "f5a00a87-c1fe-46bd-872a-859ddbfa634d" + "/")
        self.assertEqual(resp.status_code, 404)
        
    def test_cannot_edit_finished_page(self):
        M = ModuleForm(example_module).save()
        M.finished = True;
        M.save()
        resp = self.client.get('/edit/' + M.guid + "/auth/" + M.auth_code + "/")
        self.assertEqual(resp.status_code, 404)
        
    def test_cannot_visit_authcode_page_if_finished(self):
        M = ModuleForm(example_module).save()
        resp = self.client.get('/edit/' + M.guid + "/")
        self.assertContains(resp, 'name="auth_code"', 1, 200)
        M.finished = True;
        M.save()
        resp = self.client.get('/edit/' + M.guid + "/")
        self.assertEqual(resp.status_code, 404)
        
    def test_auth_code_form_redirects_to_edit_page(self):
        M = ModuleForm(example_module).save()
        resp = self.client.post('/edit/' + M.guid + "/", { 'auth_code' : M.auth_code })
        self.assertIn('edit', resp['Location'])
        self.assertIn(M.guid, resp['Location'])
        self.assertIn('auth', resp['Location'])
        self.assertIn(M.auth_code, resp['Location'])
        self.assertIsInstance(resp, HttpResponseRedirect)
        resp = self.client.post('/edit/' + M.guid + "/", { 'auth_code' : "f5a00a87-c1fe-46bd-872a-859ddbfa634d" })
        self.assertContains(resp, 'name="auth_code"', 1, 200)
        self.assertNotContains(resp, M.auth_code, 200)

    def test_edit_page_saves(self):
        M = ModuleForm(example_module).save()
        post_data = {
                     'guid' : "f5a00a87-c1fe-46bd-872a-859ddbfa634d",
                     'title' : M.title + "123",
                     'description': M.description + "ff",
                     'author': M.author + "we",
                     'author_acronym': "nw",
                     'finished' : True,
                     'sourcecode' : M.sourcecode + "mmm",
                     'documentation': M.documentation + "wg",
                     'version' : M.version + 1,
                     'modulename' : M.modulename,
                     'auth_code' : "f5a00a87-c1fe-46bd-872a-859ddbfa634d",
                     'average_rating': 10,
                     'uniquename' : "bla",
                     'savemodule': ""
                     }
        resp = self.client.post('/edit/' + M.guid + "/auth/" + M.auth_code + "/", post_data)
        Msaved = Module.objects.get(guid=M.guid)
        self.assertIsInstance(resp, HttpResponseRedirect)
        self.assertIn('edit', resp['Location'])
        self.assertIn(M.guid, resp['Location'])
        self.assertEqual(Msaved.title, post_data['title'])
        self.assertEqual(Msaved.description, post_data['description'])
        self.assertEqual(Msaved.author, post_data['author'])
        self.assertEqual(Msaved.author_acronym, post_data['author_acronym'])
        self.assertEqual(Msaved.sourcecode, post_data['sourcecode'])
        self.assertEqual(Msaved.documentation, post_data['documentation'])
        self.assertEqual(Msaved.version, M.version)
        self.assertEqual(Msaved.modulename, post_data['modulename'])
        self.assertEqual(Msaved.auth_code, M.auth_code)
        self.assertEqual(Msaved.average_rating, M.average_rating)
        self.assertFalse(Msaved.finished)
        self.assertIn(post_data['author_acronym'], Msaved.uniquename)
        self.assertIn(post_data['modulename'], Msaved.uniquename)
        self.assertIn(M.version.__str__(), Msaved.uniquename)
        
    def test_edit_pages_does_not_save_if_data_is_invalid(self):
        M = ModuleForm(example_module).save()
        # Modulename has changed and does not matches the modulename in sourcecode
        post_data = {
                     'title' : M.title + "123",
                     'description': M.description + "ff",
                     'author': M.author + "we",
                     'author_acronym': "nw",
                     'sourcecode' : M.sourcecode + "mmm",
                     'documentation': M.documentation + "wg",
                     'modulename' : M.modulename + "m123",
                     'savemodule': ""
                     }
        
        resp = self.client.post('/edit/' + M.guid + "/auth/" + M.auth_code + "/", post_data)
        Msaved = Module.objects.get(guid=M.guid)
        self.assertIsInstance(resp, HttpResponse)
        self.assertNotEqual(Msaved.title, post_data['title'])

    def test_edit_pages_does_not_save_if_submit_button_is_missing(self):
        M = ModuleForm(example_module).save()
        post_data = {
                     'title' : M.title + "123",
                     'description': M.description + "ff",
                     'author': M.author + "we",
                     'author_acronym': "nw",
                     'sourcecode' : M.sourcecode + "mmm",
                     'documentation': M.documentation + "wg",
                     'modulename' : M.modulename,
                     }
        
        resp = self.client.post('/edit/' + M.guid + "/auth/" + M.auth_code + "/", post_data)
        Msaved = Module.objects.get(guid=M.guid)
        self.assertIsInstance(resp, HttpResponse)
        self.assertNotEqual(Msaved.title, post_data['title'])

    def test_edit_page_saves_and_finishes_if_finish_button_is_pressed(self):
        M = ModuleForm(example_module).save()
        post_data = {
                     'title' : M.title + "123",
                     'description': M.description + "ff",
                     'author': M.author + "we",
                     'author_acronym': "nw",
                     'sourcecode' : M.sourcecode + "mmm",
                     'documentation': M.documentation + "wg",
                     'modulename' : M.modulename,
                      'finishmodule': ""
                     }
        
        resp = self.client.post('/edit/' + M.guid + "/auth/" + M.auth_code + "/", post_data)
        Msaved = Module.objects.get(guid=M.guid)
        self.assertIsInstance(resp, HttpResponseRedirect)
        self.assertEqual(Msaved.title, post_data['title'])
        self.assertTrue(Msaved.finished)
        self.assertIn('show', resp['Location'])
        self.assertIn(M.guid, resp['Location'])

