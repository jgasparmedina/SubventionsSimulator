import unittest
from SubventionsSimulator import Attribute, Condition, Subvention, Exceptions, Simulator


class SubventionsSimulatorTestCase(unittest.TestCase):
    def test1(self):
        with self.assertRaises(Exception) as e:
            s = Simulator.Simulator(None)
        self.assertEqual(str(e.exception), "Subventions has not a valid type --> expected <class 'dict'> and received <class 'NoneType'>")

    def test2(self):
        with self.assertRaises(Exception) as e:
            s = Simulator.Simulator({1 : None})
        self.assertEqual(str(e.exception), "Subvention has not a valid type --> expected <class 'SubventionsSimulator.Subvention.Subvention'> and received <class 'NoneType'>")

    def test3(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        s = Subvention.Subvention("Title", "Description", "Law", c, lawURL = "url", requestURL = "requestURL", incompatibilities = "Incompatibilities")
        ss = Simulator.Simulator({1:s})
        self.assertIsInstance(ss, Simulator.Simulator)

    def test4(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        s = Subvention.Subvention("Title", "Description", "Law", c, lawURL = "url", requestURL = "requestURL", incompatibilities = "Incompatibilities")
        ss = Simulator.Simulator({1:s})
        self.assertTrue(ss.isFinished ())

    def test5(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        s = Subvention.Subvention("Title", "Description", "Law", c, lawURL = "url", requestURL = "requestURL", incompatibilities = "Incompatibilities")
        ss = Simulator.Simulator({1:s})
        ss.startSimulation()
        self.assertFalse(ss.isFinished ())

    def test6(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a, "!=", "English")
        cOR = Condition.OR (c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cOR, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        ss = Simulator.Simulator({1: s})
        ss.startSimulation()
        self.assertEqual (ss.getPendingAttributes(), 1)

    def test7(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a, "!=", "English")
        cOR = Condition.OR (c, c2)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cOR, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        ss = Simulator.Simulator({1: s})
        self.assertEqual (ss.getPendingAttributes(), 0)

    def test8(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        self.assertEqual(ss.getNextAttribute(), a2)

    def test9(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute ()
        with self.assertRaises(Exceptions.UnexpectedAttributeData) as e:
            ss.setAttributeData ('Nationality', 'Spanish')
        self.assertEqual(str(e.exception), "Attribute not expected!")

    def test10(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute ()
        with self.assertRaises(Exceptions.SimulationInProcess) as e:
            ss.getSubventionsOk ()
        self.assertEqual(str(e.exception), "Simulation is still running!")

    def test11(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute ()
        ss.setAttributeData ("Age", 25)
        self.assertEqual(ss.getPendingAttributes (), 1)

    def test12(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute ()
        ss.setAttributeData ("Age", 24)
        self.assertEqual(ss.getNextAttribute (), a3)

    def test13(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute ()
        ss.setAttributeData ("Age", 24)
        ss.getNextAttribute()
        ss.setAttributeData("Civil state", "No")
        self.assertEqual(ss.getNextAttribute (), a)

    def test14(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute()
        ss.setAttributeData ("Age", 24)
        ss.getNextAttribute()
        ss.setAttributeData("Civil state", "No")
        ss.getNextAttribute()
        ss.setAttributeData("Nationality", "Spanish")
        self.assertTrue(ss.isFinished ())

    def test15(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute()
        ss.setAttributeData ("Age", 24)
        ss.getNextAttribute()
        ss.setAttributeData("Civil state", "No")
        ss.getNextAttribute()
        ss.setAttributeData("Nationality", "Spanish")
        with self.assertRaises(Exceptions.NoMoreAttributes) as e:
            ss.getNextAttribute ()
        self.assertEqual(str (e.exception), "No more attributes!")

    def test16(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute()
        ss.setAttributeData ("Age", 24)
        ss.getNextAttribute()
        ss.setAttributeData("Civil state", "No")
        ss.getNextAttribute()
        ss.setAttributeData("Nationality", "Spanish")
        self.assertEqual(ss.getSubventionsOk(), [1, 2])

    def test17(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute()
        ss.setAttributeData ("Age", 24)
        ss.getNextAttribute()
        ss.setAttributeData("Civil state", "No")
        ss.getNextAttribute()
        ss.setAttributeData("Nationality", "European")
        self.assertEqual(ss.getSubventionsOk(), [2])

    def test18(self):
        a = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
        a2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
        a3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
        c = Condition.SimpleCondition(a, "=", "Spanish")
        c2 = Condition.SimpleCondition(a2, "<", 25)
        c3 = Condition.SimpleCondition(a3, "=", "No")
        cAND = Condition.AND(c, c2)
        cOR = Condition.OR(c2, c3)
        s = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
        s2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
        ss = Simulator.Simulator({1: s,
                                  2: s2})
        ss.startSimulation()
        ss.getNextAttribute()
        ss.setAttributeData ("Age", 26)
        ss.getNextAttribute()
        ss.setAttributeData("Civil state", "Yes")
        self.assertEqual(ss.getSubventionsOk(), [])