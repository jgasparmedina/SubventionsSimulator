import Attribute, Condition, Subvention

class SubventionsLoader(object):
    """
    This abstract class provides the available universe of attributes and subventions

    SubventionsLoader must to be override in terms to load info from different sources (file, dict, database, etc.)
    """
    def __init__(self):
        """
        Creates an instance of SubventionsLoader
        """
        self._attributes = {}
        self._subventions = {}

    def getSubventions(self):
        """
        Returns the loaded subventions
        :return: subventions loaded
        """
        return self._subventions

    def getAttributes(self):
        """
        Returns the loaded attributes
        :return: attributes loaded
        """
        return self._attributes

    def getSubvention(self, subventionId):
        """
        Returns an specific subvention
        :param subventionId: subvention identifier
        :return: subvention with identifier subventionId or None
        """
        return self._subventions.get(subventionId, None)


class SubventionsFileLoader(SubventionsLoader):
    """
    This class inherits from SubventionsLoader and implements a file loader
    """
    def __init__(self, filename):
        """
        Creates an instance from a file which name is filename
        :param filename: name of the file to be loaded
        """
        self._filename = filename
        super().__init__(self)


class SubventionsDictLoader(SubventionsLoader):
    """
    This class inherits from SubventionsLoader and implements a Python dict loader
    """
    def __init__(self):
        """
        Creates an instance from a file which name is filename
        """
        super().__init__()

    def load(self, attributes, subventions):
        """
        Loads attributes and subventions from two Python dict
        :param attributes: dictionary which contains data for attributes
        :param subventions: dictionary which contains data for subventions
        :return: updated instance
        """
        for key, conf in attributes.items():
            self._attributes[key] = Attribute.Attribute(key, conf['QUESTION'], conf['VALUES'], conf['HELPERS'], conf['TYPE'], conf['HELP'])

        for key, conf in subventions.items():
            ands = []
            for conditions in conf['CONDITIONS']:
                ors = []
                for condition in conditions:
                    attribute, operator, value = condition
                    ors.append(Condition.SimpleCondition(self._attributes[attribute], operator, value))
                ands.append(Condition.OR(*ors))
            finalCondition = Condition.AND(*ands)
            self._subventions[key] = Subvention.Subvention(conf['TITLE'], conf['DESCRIPTION'], conf['LAW'], finalCondition, conf.get('LAWURL', None), conf.get('REQUESTURL', None),
                                                           conf.get('INCOMPATIBILITIES', None))


if __name__ == '__main__':
    from SubventionsDataSample import AYUDAS, ATRIBUTOS

    data = SubventionsDictLoader()
    data.load(ATRIBUTOS, AYUDAS)
    import pprint

    pprint.pprint(data._attributes)
    pprint.pprint(data._subventions[1])
    data.getSubventions()[1].checkCompliance (**{'EDAD' : 16})