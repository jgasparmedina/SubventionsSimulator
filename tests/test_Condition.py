import unittest
from SubventionsSimulator import Condition, Attribute, Exceptions

class SimpleConditionTestCase (unittest.TestCase):
    def test1 (self):
        a = Attribute.Attribute ("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition (a, "=", "European")
        self.assertIsInstance(c, Condition.CombinedCondition)

    def test2 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "European")
        self.assertTrue(c.check(**{'Nationality' : 'European'}))

    def test3 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "European")
        self.assertFalse(c.check(**{'Nationality' : 'English'}))

    def test4 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "European")
        with self.assertRaises(Exception) as e:
            c.check()
        self.assertEqual(str(e.exception), "Attribute Nationality not found in values!")

    def test5 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "IN", ["European", "English"])
        self.assertFalse(c.check(**{'Nationality': 'Others'}))

    def test6 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "IN", ["European", "English"])
        self.assertTrue(c.check(**{'Nationality': 'European'}))

    def test7 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "NOT IN", ["European", "English"])
        self.assertTrue(c.check(**{'Nationality': 'Others'}))

    def test8 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "NOT IN", ["European", "English"])
        self.assertFalse(c.check(**{'Nationality': 'European'}))

    def test9 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "=", 22)
        self.assertTrue(c.check(**{'Age': 22}))

    def test10 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "=", 22)
        self.assertFalse(c.check(**{'Age': 23}))

    def test11 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "<", 22)
        self.assertTrue(c.check(**{'Age': 21}))

    def test12 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "<", 22)
        self.assertFalse(c.check(**{'Age': 22}))

    def test13 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "<=", 22)
        self.assertTrue(c.check(**{'Age': 22}))

    def test14 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, "<=", 22)
        self.assertFalse(c.check(**{'Age': 23}))

    def test15 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, ">", 22)
        self.assertTrue(c.check(**{'Age': 23}))

    def test16 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, ">", 22)
        self.assertFalse(c.check(**{'Age': 22}))

    def test17 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, ">=", 22)
        self.assertTrue(c.check(**{'Age': 22}))

    def test18 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, ">=", 22)
        self.assertFalse(c.check(**{'Age': 21}))

    def test19 (self):
        a = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        c = Condition.SimpleCondition(a, ">=", 22)
        self.assertEqual(c.getUniqueAttributes(), [a])


class ORTestCase (unittest.TestCase):
    def test1 (self):
        a = Attribute.Attribute ("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition (a, "=", "European")
        c2 = Condition.SimpleCondition (a, "!=", "Spanish")
        c = Condition.OR (c1, c2)
        self.assertIsInstance(c, Condition.OR)

    def test2 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c = Condition.OR(c1, c2)
        self.assertTrue(c.check(**{'Nationality' : 'European'}))

    def test3 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c = Condition.OR(c1, c2)
        self.assertTrue(c.check(**{'Nationality' : 'English'}))

    def test4 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c = Condition.OR(c1, c2)
        self.assertFalse(c.check(**{'Nationality' : 'Spanish'}))

    def test5 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c3 = Condition.SimpleCondition(a, "=", "Spanish")
        cAnd = Condition.AND (c1, c2)
        c = Condition.OR(cAnd, c3)
        self.assertTrue(c.check(**{'Nationality' : 'Spanish'}))


class ANDTestCase (unittest.TestCase):
    def test1 (self):
        a = Attribute.Attribute ("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition (a, "=", "European")
        c2 = Condition.SimpleCondition (a, "!=", "Spanish")
        c = Condition.AND (c1, c2)
        self.assertIsInstance(c, Condition.AND)

    def test2 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c = Condition.AND(c1, c2)
        self.assertTrue(c.check(**{'Nationality' : 'European'}))

    def test3 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c = Condition.AND(c1, c2)
        self.assertFalse(c.check(**{'Nationality' : 'English'}))

    def test4 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c = Condition.AND(c1, c2)
        self.assertFalse(c.check(**{'Nationality' : 'Spanish'}))

    def test5 (self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c1 = Condition.SimpleCondition(a, "=", "European")
        c2 = Condition.SimpleCondition(a, "!=", "Spanish")
        c3 = Condition.SimpleCondition(a, "=", "Spanish")
        cOr = Condition.OR (c1, c2)
        c = Condition.AND(cOr, c3)
        self.assertFalse(c.check(**{'Nationality' : 'Spanish'}))