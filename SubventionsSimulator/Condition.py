import Attribute
from Exceptions import AttributeWithoutDataException, WrongOperatorException, IncompleteDataException


class CombinedCondition(object):
    """
    This abstract class represents a generic condition
    """
    def __init__(self):
        pass

    def getConditions(self):
        """
        Returns the list of conditions that make it up
        :return: list of conditions
        """
        return self._conditions

    def setConditions(self, conditions):
        """
        Set conditions
        :param conditions: conditions to be set
        :return: updated instance
        """
        self._conditions = conditions

    def getUniqueAttributes(self):
        """
        Returns the list of unique attributes which are part of the conditions
        :return: list of attributes
        """
        finalAttributes = []
        for condition in self._conditions:
            attributes = condition.getUniqueAttributes()
            for attribute in attributes:
                if attribute not in finalAttributes:
                    finalAttributes.append(attribute)
        return finalAttributes

    def check(self, **valuesToCheck):
        """
        Checks if the values provided satisfy the conditions.
        This method mus to be override
        :param valuesToCheck: dict with attributes values where key is the name of the attribute and value is the value.
        :return: nothing
        """
        raise Exception("You must to override this method!")

    def __repr__(self, operator = ""):
        text = "[ "
        for i in range(len(self._conditions)):
            text += self._conditions[i].__repr__()
            if i != (len(self._conditions) - 1):
                text += " %s " % operator
        text += ' ]'
        return text

    def __str__(self):
        return self.__repr__()


class SimpleCondition(CombinedCondition):
    """
    This class inherits from CombinedCondition and represents a simple condition

    One single conditions is which defines one attribute, one operator and one or some values to be evaluated.
    For instance:
        - Attribute could be AGE
        - Operator could be "="
        - Values could be 32
    In this example, the simple condition could understood like "AGE must to be equal to 32"

    The valid operators are:
        - "=": the attribute value must to be "equal" to the specified value.
        - "!=":  the attribute value must to be "not equal" the specified value.
        - "<":  the attribute value must to be "less than" the specified value.
        - "<=":  the attribute value must to be "less or equal than" the specified value.
        - ">":  the attribute value must to be "greater than" the specified value.
        - ">=":  the attribute value must to be "greater or equal than" the specified value.
        - "IN":  the attribute value must to be "included in" the specified list of values.
        - "NOT IN":  the attribute value must to be "not included in" the specified list of values.
    """
    def __init__(self, attribute, operator, value):
        """
        Creates a new simple condition
        :param attribute: attribute to be conditioned
        :param operator: operator to be applied, can be: '=', '!=', '<', '<=', '>', '>=', 'IN', 'NOT IN'
        :param value: expected value(s)
        """
        self._attribute = attribute
        if operator not in ('=', '!=', '<', '<=', '>', '>=', 'IN', 'NOT IN'):
            raise WrongOperatorException
        self._operator = operator
        self._value = value

    def getAttribute(self):
        """
        Returns the attribute
        :return: attribute
        """
        return self._attribute

    def getOperator(self):
        """
        Returns the operator
        :return: operator
        """
        return self._operator

    def getValue(self):
        """
        Returns the value
        :return: value
        """
        return self._value

    def setAttribute(self, attribute):
        """
        Set the attribute
        :param attribute: attribute to be set
        :return: updated instance
        """
        self._attribute = attribute

    def setOperator(self, operator):
        """
        Set the operator
        :param operator: operator to be set
        :return: updated instance
        """
        self._operator = operator

    def setValue(self, value):
        """
        Set the value
        :param value: value to be set
        :return: updated instance
        """
        self._value = value

    def check(self, **valuesToCheck):
        """
        Check if the condition is satisfied by the given value of the attribute
        :param valuesToCheck: dict of attributes and their values
        :return: True if the condition is satisfied or False in other case
        """
        valueToCheck = valuesToCheck.get(self._attribute.getName(), None)
        if not valueToCheck:
            raise AttributeWithoutDataException(self._attribute.getName())
        if self._operator == '=':
            return valueToCheck == self._value
        if self._operator == '!=':
            return valueToCheck != self._value
        if self._operator == 'IN':
            return valueToCheck in self._value
        if self._operator == 'NOT IN':
            return valueToCheck not in self._value
        if self._operator == '>':
            return valueToCheck > self._value
        if self._operator == '<':
            return valueToCheck < self._value
        if self._operator == '>=':
            return valueToCheck >= self._value
        if self._operator == '<=':
            return valueToCheck <= self._value
        raise WrongOperatorException

    def getUniqueAttributes(self):
        """
        Returns the list of unique attributes that composes the condition
        :return: list of attributes
        """
        return [self._attribute]

    def __repr__(self):
        return "(%s %s %s)" % (self.getAttribute().getName(), self.getOperator(), self.getValue())

    def __str__(self):
        return "Condition: %s %s %s" % (self.getAttribute().getName(), self.getOperator(), self.getValue())


class OR(CombinedCondition):
    """
    This class inherits from CombinedCondition and represents the composition of several conditions following an OR logic.

    OR condition will be True if, at least, one of the conditions is True.
    """
    def __init__(self, *conditions):
        """
        Creates a new OR condition
        :param conditions: list of conditions which compose the OR condition
        """
        self._conditions = conditions

    def check(self, **valuesToCheck):
        """
        Check if the condition is satisfied by the given value of the attributes
        :param valuesToCheck: dict of attributes and their values
        :return: True if the condition is satisfied or False in other case
        """
        check = False
        incomplete = False
        for condition in self._conditions:
            try:
                check = condition.check(**valuesToCheck)
                if check:
                    return True
            except AttributeWithoutDataException as e:
                incomplete = True
        if incomplete:
            raise IncompleteDataException("Data is incomplete!")
        return False

    def __repr__(self):
        return super().__repr__('OR')


class AND(CombinedCondition):
    """
    This class inherits from CombinedCondition and represents the composition of several conditions following an AND logic.

    AND condition will be True if all of the conditions are True.
    """
    def __init__(self, *conditions):
        """
        Creates a new AND condition
        :param conditions: list of conditions which compose the AND condition
        """
        self._conditions = conditions

    def check(self, **valuesToCheck):
        """
        Check if the condition is satisfied by the given value of the attributes
        :param valuesToCheck: dict of attributes and their values
        :return: True if the condition is satisfied or False in other case
        """
        incomplete = False
        for condition in self._conditions:
            try:
                check = condition.check(**valuesToCheck)
                if not check:
                    return False
            except Exception as e:
                incomplete = True
        if incomplete:
            raise IncompleteDataException("Data is incomplete!")
        return True

    def __repr__(self):
        return super().__repr__('AND')


if __name__ == '__main__':
    a1 = Attribute.Attribute('A1', 'A1', None, int, '', '')
    a2 = Attribute.Attribute('A2', 'A2', None, int, '', '')
    a3 = Attribute.Attribute('A3', 'A3', None, int, '', '')
    a4 = Attribute.Attribute('A4', 'A4', None, int, '', '')
    a5 = Attribute.Attribute('A5', 'A5', None, int, '', '')
    c1 = SimpleCondition(a1, '=', 1)
    c2 = SimpleCondition(a2, 'IN', [1, 2])
    c3 = SimpleCondition(a3, '=', 2)
    c4 = SimpleCondition(a4, '&', 1)
    c8 = SimpleCondition(a5, '<', 8)

    c5 = OR(c1, c2)
    c6 = AND(c1, c2)
    c7 = AND(c5, c6)
    c9 = OR(c6, c3, c8)
    c10 = AND(c1)
    assert (isinstance(c1, CombinedCondition))
    assert (isinstance(c5, AND))
    print(c2.check(**{'A2': 2}))
    print(c5.check(**{'A1': 2, 'A2': 2}))
    print(c6.check(**{'A1': 1, 'A2': 2}))
    print(c7.check(**{'A1': 2, 'A2': 2}))
    print(c9.check(**{'A1': 2, 'A2': 12, 'A3': 2}))
    print(c10.check(**{'A1': 1, 'A2': 12, 'A3': 2}))
    print(c9.getUniqueAttributes())
