
from django.test import TestCase
from web.forms import ModuleForm
from web.models import Module



example_module = {'title' : "A cylinder",
                  'modulename' : "cylinder", 
                       'author' : "Phaiax", 
                       'author_acronym' : "Px",
                       'sourcecode' : "module cylinder() { }", 
                       'documentation' : "call cylinder()", 
                       'description' : "This makes a cylinder",
                       'version' : 1}

class ModuleModelTest(TestCase):

   
    def test_can_create_and_safe_module(self):
        M = Module()
        M.author = "Phaiax"
        M.save()
        R = Module.objects.get(guid=M.guid)
        self.assertEqual("Phaiax", R.author)

        
    def test_module_generates_and_saves_uniquename(self):
        M = Module(**example_module)
        gn = M.generate_uniquename()
        M.save()
        self.assertEquals(gn, M.uniquename)
        
    def test_uniquename_is_always_unique(self):
        M = Module(**example_module)
        M.save()
        M2 = Module(**example_module)
        M2.save()
        self.assertNotEqual(M2.uniquename, M.uniquename)
        pass
    
    def test_form_validates_that_sourcecode_contains_modulename(self):
        invalid_module = example_module.copy()
        invalid_module['modulename'] = 'baseball'
        M = ModuleForm(invalid_module)
        self.assertFalse(M.is_valid())
        self.assertTrue('sourcecode' in M.errors)
        
    def test_module_validates_that_modulename_is_valid(self):
        invalid_module = example_module.copy()
        invalid_module['modulename'] = '1cylinder'
        M = ModuleForm(invalid_module)
        self.assertFalse(M.is_valid())
        self.assertTrue('modulename' in M.errors)
        invalid_module['modulename'] = 'cylin der'
        M = ModuleForm(invalid_module)
        self.assertFalse(M.is_valid())
        self.assertTrue('modulename' in M.errors)
        invalid_module['modulename'] = 'calinger%'
        M = ModuleForm(invalid_module)        
        self.assertFalse(M.is_valid())
        self.assertTrue('modulename' in M.errors)
        invalid_module['modulename'] = 'cylinder'
        M = ModuleForm(invalid_module)        
        self.assertTrue(M.is_valid())
        self.assertFalse('modulename' in M.errors)
        
        
    def test_model_generates_url(self):
        M = ModuleForm(example_module).save()
        resp = self.client.get(M.get_absolute_url())
        self.assertEqual(resp.context['module'].guid, M.guid)
