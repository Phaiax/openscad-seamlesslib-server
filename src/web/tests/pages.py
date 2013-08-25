from django.http.response import HttpResponseRedirect, HttpResponse
from django.test import TestCase
from modulemodel import example_module
from web.forms import ModuleForm
from web.models import Module

    
    
class PagesTest(TestCase):

    
    def test_can_access_main_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        
    def test_main_page_returns_template(self):
        resp = self.client.get('/')
        self.assertContains(resp, "<html>", html=False)
        
    def test_main_page_displays_add_link(self):
        resp = self.client.get('/')
        self.assertContains(resp, '<a href="/add/"',)
        
    def test_add_page_exists_and_contains_form(self):
        resp = self.client.get('/add/')
        self.assertContains(resp, "<html>", html=False)
        self.assertContains(resp, "Author", status_code=200, html = False)
        self.assertContains(resp, '<form method="POST"', html=False)
        self.assertContains(resp, '<input type="submit" name="addmodule" ', html=False)
        self.assertContains(resp, 'csrfmiddlewaretoken', html=False)
        
    def test_add_page_saves_and_redirects(self):
        resp = self.client.post('/add/', example_module)
        M = Module.objects.get(modulename=example_module['modulename'])
        self.assertEquals(example_module['author'], M.author)
        self.assertIn('show', resp['Location'])
        self.assertIn(M.guid, resp['Location'])
        self.assertIsInstance(resp, HttpResponseRedirect)
        
    def test_add_page_checks_for_valid_input(self):
        bad_example = example_module.copy()
        bad_example['author'] = "";
        resp = self.client.post('/add/', bad_example)
        self.assertIsInstance(resp, HttpResponse)
        self.assertContains(resp, '<input type="submit" name="addmodule" ')
        self.assertContains(resp, 'error')
        self.assertContains(resp, 'required')
        
    def test_show_page(self):
        M = Module(**example_module)
        M.save()
        resp = self.client.get('/show/' + M.guid + '/')
        self.assertContains(resp, example_module['author'])
        self.assertContains(resp, example_module['sourcecode'])
        
    def test_show_page_raises_404_if_not_available(self):
        resp = self.client.get('/show/8b9a3b9e-277c-47b4-a7fa-cc5eb0905efu/')
        self.assertEqual(resp.status_code, 404)
        
    def test_can_make_rating(self):
        M = ModuleForm(example_module).save()
        resp = self.client.get('/rate/%s/3/' % M.guid)
        self.assertIsInstance(resp, HttpResponseRedirect)
        self.assertIn(M.guid, resp['Location'])
        M = Module.objects.get(guid = M.guid)
        self.assertEqual(3, M.average_rating)
        self.assertEqual(1, M.number_of_ratings)
        resp = self.client.get('/rate/%s/7/' % M.guid)
        M = Module.objects.get(guid = M.guid)
        self.assertEqual(5, M.average_rating)
        self.assertEqual(2, M.number_of_ratings)
        resp = self.client.get('/rate/%s/11/' % M.guid)
        M = Module.objects.get(guid = M.guid)
        self.assertEqual(5, M.average_rating)
        self.assertEqual(2, M.number_of_ratings)
        resp = self.client.get('/rate/%s/-1/' % M.guid)
        M = Module.objects.get(guid = M.guid)
        self.assertEqual(5, M.average_rating)
        self.assertEqual(2, M.number_of_ratings)
        
    def test_home_displays_list(self):
        resp = self.client.get("/")
        self.assertTrue('top_rated_modules' in resp.context)
        self.assertTrue('last_added_modules' in resp.context)
        
    def test_home_displays_last_10_modules(self):
        for i in range(0, 20):
            mod = example_module.copy()
            mod['title'] = "rated: %d " % i
            M = ModuleForm(mod).save()
            M.average_rating = i
            M.save()
        for i in range(0, 20):
            mod = example_module.copy()
            mod['title'] = "latest: %d " % i
            ModuleForm(mod).save()
        resp = self.client.get("/")
        self.assertContains(resp, "latest: 10 ")
        self.assertContains(resp, "latest: 19 ")
        self.assertNotContains(resp, "latest: 1 ")
        self.assertContains(resp, "rated: 19 ")
        self.assertNotContains(resp, "rated: 1 ")