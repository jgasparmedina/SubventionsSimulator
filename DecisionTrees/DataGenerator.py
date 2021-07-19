from SubventionsSimulator import SubventionsLoader, Simulator
import random
import pandas as pd

class DataGenerator (object):
    """
    This class provides generating data capabilities according to the attributes provided.

    DataGenerator has two main functionalities:
    1. generateData in dict format
    2. generateDataSet in DataFrame format (pandas)

    Both methods generate pseudo-random elements according to the attributes provided and taking into account some dependencies between them in order to produce more realistic elements.
    Generated elements can include the classification of each one
    """
    def __init__(self):
        """
        Creates an instance of DataGenerator
        """
        self._attributes = []
        self._subventions = []

    def __init__(self, attributes, subventions):
        """
        Creates an instance of DataGenerator providing attributes and subventions
        :param attributes: attribute set to be applied in generating process
        :param subventions: subvention set to be considered in classification of each generated element
        """
        self._attributes = attributes
        self._subventions = subventions

    def getAttributes (self):
        """
        Returns attribute set
        :return: attribute set
        """
        return self._attributes

    def getSubventions (self):
        """
        Returns subvention set
        :return: subvention set
        """
        return self._subventions

    def setAttributes (self, attributes):
        """
        Sets a new attribute set
        :param attributes: attribute set to be set
        :return: updated instance
        """
        self._attributes = attributes

    def setSubventions (self, subventions):
        """
        Sets a new subvention set
        :param subventions: subvention set to be set
        :return: updated instance
        """
        self._subventions = subventions

    def generateData (self, numElements, classified = False, multiClass = False):
        """
        Generates pseudo-random data for numElements elements and return them in a list of dict format.
        :param numElements: number of elements to be generated
        :param classified: compute the class of each generated elements if is True, do nothing otherwise
        :param multiClass: if True allows to one element belongs to multiple classes, if False then one element just can belong to one class
        :return: a list of elements where each element is a dict where keys are attribute names and values are the value of each attribute.
        """
        elementsGenerated = []
        if self._attributes == []:
            return elementsGenerated
        for i in range (numElements):
            newElement = {}
            for attribute in self._attributes:
                if isinstance(self._attributes[attribute]['VALUES'], list):
                    newElement[attribute] = random.choice(self._attributes[attribute]['VALUES'])
                elif self._attributes[attribute]['TYPE'] == float:
                    newElement[attribute] = random.randint(0, 100)
            # Applying some dependencies in terms to have more realistic individuals
            for attribute in self._attributes:
                if len (self._attributes[attribute].get ("DEPENDENCIES", [])) != 0:
                    for dependency in self._attributes[attribute]['DEPENDENCIES']:
                        attr, operator, value = dependency
                        if operator == '=' and newElement[attr] != value:
                            newElement[attribute] = 'No'
                        if operator == '<' and newElement[attr] >= value:
                            newElement[attribute] = 'No'
                        if operator == '>' and newElement[attr] <= value:
                            newElement[attribute] = 'No'
            if classified:
                classes = self._classifyElement(newElement, multiClass = multiClass)
                for classification in classes:
                        element = dict (newElement)
                        element['CLASS'] = classification
                        elementsGenerated.append(element)
            else:
                elementsGenerated.append(newElement)
        return elementsGenerated

    def generateDataSet (self, numElements, classified = False, multiClass = False):
        """
        Generates pseudo-random data for numElements elements and return them in a DataFrame (pandas) format.
        :param numElements: number of elements to be generated
        :param classified: compute the class of each generated elements if is True, do nothing otherwise
        :param multiClass: if True allows to one element belongs to multiple classes, if False then one element just can belong to one class
        :return: a DataFrame where each row is one element and each column is an attribute
        """
        elementsGenerated = self.generateData(numElements, classified = classified, multiClass = multiClass)
        dataSet = {}
        for element in elementsGenerated:
            for key, value in element.items():
                if key not in dataSet:
                    dataSet[key] = []
                dataSet[key].append (value)
        return pd.DataFrame(dataSet)

    def _classifyElement (self, element, multiClass = False):
        """
        Classifies one element using SubventionsSimulator
        :param element: element to be classified. Is a dict where keys are the attribute names and values are value for each attribute.
        :param multiClass: if True allows to one element belongs to multiple classes, if False then one element just can belong to one class
        :return: a list with the classes that the element belongs to.
        """
        loader = SubventionsLoader.SubventionsDictLoader()
        loader.load(self._attributes, self._subventions)
        simulator = Simulator.Simulator(loader.getSubventions())
        simulator.startSimulation()
        while not simulator.isFinished():
            attribute = simulator.getNextAttribute()
            simulator.setAttributeData(attribute.getName(), element[attribute.getName()])
        if multiClass:
            if len (simulator.getSubventionsOk()) != 0:
                return [self._subventions[subventionId]['NAME'] for subventionId in simulator.getSubventionsOk()]
            return ['None']
        else:
            if len (simulator.getSubventionsOk()) != 0:
                return [self._subventions[simulator.getSubventionsOk().pop()]['NAME']]
            else:
                return ['None']


if __name__ == '__main__':
    """
    Sample of use.
    """
    from AttributesData import ATRIBUTOS
    from SubventionsData import AYUDAS
    generator = DataGenerator (ATRIBUTOS, AYUDAS)
    elements = generator.generateData(10, classified = True, multiClass = True)
    print(elements)
    dataSet = generator.generateDataSet(10, classified = True)
    print (dataSet)

