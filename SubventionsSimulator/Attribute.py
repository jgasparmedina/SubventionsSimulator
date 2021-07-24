
class Attribute(object):
    '''
    This class represents an attribute.
    '''

    def __init__(self, name, question, values, helpers, type, help):
        """
        Creates one instance of Attribute
        :param name: name of the attribute
        :param question: question associated to the attribute which will be ask
        :param values: set of different values that the attribute can have
        :param helpers: set of description for each different possible value
        :param type: attribute type, is a Python class. Could be list, float, boolean
        :param help: description of the attribute.
        """
        self._name = name
        self._question = question
        self._values = values
        self._helpers = helpers
        self._type = type
        self._help = help

    def getName(self):
        """
        Returns the attribute name
        :return: name of the attribute
        """
        return self._name

    def getQuestion(self):
        """
        Returns the question
        :return: question associated to the attribute
        """
        return self._question

    def getValues(self):
        """
        Returns the set of values
        :return: set of values
        """
        return self._values

    def getHelpers(self):
        """
        Returns the set of values description
        :return: set of values description
        """
        return self._helpers

    def getType(self):
        """
        Returns the attribute type
        :return: attribute type
        """
        return self._type

    def getHelp(self):
        """
        Returns the attribute description
        :return: attribute description
        """
        return self._help

    def setName(self, name):
        """
        Set name to the attribute
        :param name: name to be set
        :return: updated instance
        """
        self._name = name

    def setQuestion(self, question):
        """
        Set question to the attribute
        :param question: question to be set
        :return: updated instance
        """
        self._question = question

    def setValues(self, values):
        """
        Set values to the attribute
        :param values: values to be set
        :return: updated instance
        """
        self._values = values

    def setHelpers(self, helpers):
        """
        Set helpers to the attribute
        :param helpers: question to be set
        :return: updated instance
        """
        self._helpers = helpers

    def setType(self, type):
        """
        Set type to the attribute
        :param type: type to be set
        :return: updated instance
        """
        self._type = type

    def setHelp(self, help):
        """
        Set help to the attribute
        :param help: help to be set
        :return: updated instance
        """
        self._help = help

    def __repr__(self):
        return "Attribute <%s>\n\tQuestion <%s>\n\tValues <%s>\n\tHelpers <%s>\n\tType <%s>\n\tHelp <%s>" % (self.getName(), self.getQuestion(), self.getValues(), self.getHelpers(), self.getType(), self.getHelp())

    def __str__(self):
        return "Attribute <%s>\tQuestion <%s>\tValues <%s>\tHelpers <%s>\tType <%s>\tHelp <%s>" % (self.getName(), self.getQuestion(), self.getValues(), self.getHelpers(), self.getType(), self.getHelp())

    def __getattr__(self, item):
        if item == 'NAME':
            return self.getName()
        if item == 'QUESTION':
            return self.getQuestion()
        if item == 'VALUES':
            return self.getValues()
        if item == 'HELPERS':
            return self.getHelpers()
        if item == 'TYPE':
            return self.getType()
        if item == 'HELP':
            return self.getHelp()

    def __getitem__(self, item):
        return self.__getattr__(item)


