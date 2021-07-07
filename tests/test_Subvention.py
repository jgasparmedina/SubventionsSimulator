import unittest
import Attribute, Condition, Subvention, Exceptions


class SubventionTestCase(unittest.TestCase):
    def test1(self):
        with self.assertRaises(Exception) as e:
            s = Subvention.Subvention("Title", "Description", "Law")
        self.assertEqual(str(e.exception), "Conditions has not a valid type --> expected <class 'Condition.CombinedCondition'> and received <class 'NoneType'>")

    def test2(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        s = Subvention.Subvention("Title", "Description", "Law", c, lawURL = "url", requestURL = "requestURL", incompatibilities = "Incompatibilities")
        self.assertIsInstance(s, Subvention.Subvention)

    def test3(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", c, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        self.assertEqual(s.getTitle(), "Subvention 1")
        self.assertEqual(s.getDescription(), "Description for subvention 1")
        self.assertEqual(s.getLaw(), "Law 1")
        self.assertEqual(s.getConditions(), c)
        self.assertEqual(s.getLawURL(), "URL 1")
        self.assertEqual(s.getRequestURL(), "requestURL 1")
        self.assertEqual(s.getIncompatibilities(), "Incompatibilities 1")

    def test4(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a, "=", "European")
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", c, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s.setTitle("Subvention 2")
        s.setDescription("Description for subvention 2")
        s.setLaw("Law 2")
        s.setConditions(c2)
        s.setLawURL("URL 2")
        s.setRequestURL("requestURL 2")
        s.setIncompatibilities("Incompatibilities 2")
        self.assertEqual(s.getTitle(), "Subvention 2")
        self.assertEqual(s.getDescription(), "Description for subvention 2")
        self.assertEqual(s.getLaw(), "Law 2")
        self.assertEqual(s.getConditions(), c2)
        self.assertEqual(s.getLawURL(), "URL 2")
        self.assertEqual(s.getRequestURL(), "requestURL 2")
        self.assertEqual(s.getIncompatibilities(), "Incompatibilities 2")

    def test5(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a, "!=", "English")
        cOR = Condition.OR (c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cOR, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        self.assertEqual (s.getUniqueAttributes(), [a])

    def test6(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        cAND = Condition.AND(c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        self.assertTrue(s.checkCompliance (**{'Age' : 24, 'Nationality' : 'Spanish'}))

    def test7(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        cAND = Condition.AND(c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        self.assertFalse(s.checkCompliance(**{'Age': 25, 'Nationality': 'Spanish'}))

    def test8(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        cOR = Condition.OR(c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cOR, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        self.assertTrue(s.checkCompliance(**{'Age': 24, 'Nationality': 'Spanish'}))

    def test9(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        cOR = Condition.OR(c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cOR, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        self.assertFalse(s.checkCompliance(**{'Age': 25, 'Nationality': 'European'}))

    def test9(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        cOR = Condition.OR(c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cOR, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        with self.assertRaises(Exceptions.IncompleteDataException) as e:
            s.checkCompliance(**{'Age': 25})
        self.assertEqual(str(e.exception), "Data is incomplete!")