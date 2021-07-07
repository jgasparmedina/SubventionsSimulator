import unittest
from SubventionsSimulator import Attribute

class AttributeTestCase (unittest.TestCase):
    def test1 (self):
        a = Attribute.Attribute ("Age", "How old are you?", None, None, float, "Indicate your age")
        self.assertIsInstance(a, Attribute.Attribute)

    def test2 (self):
        a = Attribute.Attribute ("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        self.assertIsInstance(a, Attribute.Attribute)

    def test3 (self):
        a = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        self.assertIsInstance(a, Attribute.Attribute)

    def test4 (self):
        a = Attribute.Attribute ("Age", "How old are you?", None, None, float, "Indicate your age")
        self.assertEqual(a.getName(), "Age")
        self.assertEqual(a.getQuestion(), "How old are you?")
        self.assertEqual(a.getValues(), None)
        self.assertEqual(a.getHelpers(), None)
        self.assertEqual(a.getType(), float)
        self.assertEqual(a.getHelp(), "Indicate your age")

    def test5 (self):
        a = Attribute.Attribute ("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        self.assertEqual(a.getName(), "Nationality")
        self.assertEqual(a.getQuestion(), "What is your nationality?")
        self.assertEqual(a.getValues(), ['Spanish', 'English', 'European', 'Others'])
        self.assertEqual(a.getHelpers(), ['', '', '', 'For other countries'])
        self.assertEqual(a.getType(), list)
        self.assertEqual(a.getHelp(), "Indicate your nationality")

    def test6 (self):
        a = Attribute.Attribute (None, None, None, None, None, None)
        a.setName("Nationality")
        a.setQuestion("What is your nationality?")
        a.setValues(['Spanish', 'English', 'European', 'Others'])
        a.setHelpers(['', '', '', 'For other countries'])
        a.setType(list)
        a.setHelp("Indicate your nationality")
        self.assertEqual(a.getName(), "Nationality")
        self.assertEqual(a.getQuestion(), "What is your nationality?")
        self.assertEqual(a.getValues(), ['Spanish', 'English', 'European', 'Others'])
        self.assertEqual(a.getHelpers(), ['', '', '', 'For other countries'])
        self.assertEqual(a.getType(), list)
        self.assertEqual(a.getHelp(), "Indicate your nationality")

    def test7 (self):
        a = Attribute.Attribute("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        self.assertEqual(a['NAME'], "Civil state")
        self.assertEqual(a['QUESTION'], "Are you married?")
        self.assertEqual(a['VALUES'], ['Yes', 'No'])
        self.assertEqual(a['HELPERS'], [])
        self.assertEqual(a['TYPE'], bool)
        self.assertEqual(a['HELP'], "Indicate your civil state")

    def test8 (self):
        a = Attribute.Attribute("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        self.assertEqual(str(a), "Attribute <Civil state>\tQuestion <Are you married?>\tValues <['Yes', 'No']>\tHelpers <[]>\tType <<class 'bool'>>\tHelp <Indicate your civil state>")
