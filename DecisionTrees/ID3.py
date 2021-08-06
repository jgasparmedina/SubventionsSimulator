from DecisionTrees import Tree
import numpy as np
import operator


class ID3(Tree.Tree):
    """
    This class implements ID3 algorithm to create decision trees from a training dataset.
    """
    def __init__(self, dataset, attributeClass = 'CLASS'):
        """
        Creates an instance of ID3 class, creating the associated decision tree.
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        """
        super().__init__('ID3')
        self._tree = self._createTree(dataset, attributeClass = attributeClass)

    def _getEntropy(self, dataset, attributeClass = 'CLASS', attributeName = 'CLASS', attributeValue = None):
        """
        Computes the entropy of one dataset
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :param attributeName: name of the attribute to be used to filter the dataset and to compute its entropy
        :param attributeValue: value of the attribute to be used to filter the dataset and to compute its entropy
        :return: the associated entropy to the dataset, and, if informed, to the provided attributeName and attributeValue.
        """
        subset = dataset[attributeName]
        if attributeValue:
            # Filtering the dataset to obtain only the records that satisfies the condition that value[attribute] == attributeValue
            subset = dataset.where(dataset[attributeName] == attributeValue).dropna()[attributeClass]
        classes, classCounters = np.unique(subset, return_counts = True)
        entropy = 0.0
        total_elements = sum(classCounters)
        for i in range(len(classes)):
            probability_i = classCounters[i] / total_elements
            entropy += -probability_i * np.log2(probability_i)
        return entropy

    def _getAttributeEntropy(self, dataset, attributeName):
        """
        Computes the entropy of one attribute
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeName: name of the attribute to be used to filter the dataset and to compute its entropy
        :return: the associated entropy to the attribute in the dataset
        """
        attributeValues, attributeCounters = np.unique(dataset[attributeName], return_counts = True)
        total_elements = sum(attributeCounters)
        attributeEntropy = 0.0
        for i in range(len(attributeValues)):
            probability_i = attributeCounters[i] / total_elements
            attributeEntropy += probability_i * self._getEntropy(dataset, attributeName = attributeName, attributeValue = attributeValues[i])
        return attributeEntropy

    def _getInformationGain(self, dataset, attributeName):
        """
        Computes the Information Gain associated to one attribute in a dataset
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeName: name of the attribute to be used to filter the dataset and to compute its Information Gain
        :return:
        """
        return self._getEntropy(dataset) - self._getAttributeEntropy(dataset, attributeName)

    def _getNextAttribute(self, dataset, attributeClass = 'CLASS'):
        """
        Returns the next attribute to split the data according to the greatest Information Gain
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :return: the attribute with better information gain.
        """
        entropies = {}
        for attribute in dataset.keys():
            if attribute == attributeClass:
                continue
            entropies[attribute] = self._getInformationGain(dataset, attribute)
        return (sorted(entropies.items(), key = operator.itemgetter(1), reverse = False)).pop()

    def _createTree(self, dataset, attributeClass = 'CLASS', parent = None):
        """
        Creates the decision tree based on ID3 criteria
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :param parent: if the decision tree is part of another dictionary
        :return: the tree for the dataset provided
        """
        if not parent:
            parent = {}
        attribute, infoGain = self._getNextAttribute(dataset)
        if attribute not in parent.keys():
            parent[attribute] = {}
        attributeValues = np.unique(dataset[attribute])
        for attributeValue in attributeValues:
            subset = dataset[dataset[attribute] == attributeValue]
            classes, counters = np.unique(subset[attributeClass], return_counts = True)
            if len(classes) <= 1:
                parent[attribute][attributeValue] = classes[0]
            else:
                parent[attribute][attributeValue] = self._createTree(subset)
        return parent

    def classify(self, element, default = 'None'):
        """
        Once the decision tree is created, using classify method one element can be classified.
        :param element: element to be classified in dict format where each key is one attribute name and each value is the value of that attribute.
        :param default: default class in case the element can not be classified.
        :return: the class which the element belongs to.
        """
        stop = False
        currentNode = dict (self._tree)
        classification = None
        while not stop:
            if not isinstance(currentNode, dict):
                classification = currentNode
                stop = True
            else:
                attribute = list(currentNode.keys())[0]
                if attribute in element.keys():
                    value = element[attribute]
                    if value in currentNode[attribute].keys():
                        currentNode = currentNode[attribute][value]
                        continue
                    else:
                        classification = default
                        stop = True
                else:
                    classification = default
                    stop = True
        return classification


if __name__ == '__main__':
    """
    Sample of use.
    """
    import DataGenerator
    from AttributesData import ATRIBUTOS
    from SubventionsData import AYUDAS

    gen = DataGenerator.DataGenerator(ATRIBUTOS, AYUDAS)
    dataset = gen.generateDataSet(100, classified = True, multiClass = False)
    id3 = ID3(dataset)
    nelements = 65
    elements = gen.generateData(nelements, classified = True, multiClass = False)
    hits = 0
    for element in elements:
        classification = id3.classify(element)
        if element['CLASS'] == classification:
            hits += 1
    import pprint
    pprint.pprint (id3.getTree())
    print ("Total Depth: %s" % id3.getTreeDepth())
    print ("Total hits: %f --> %f" % (hits, (hits/nelements) * 100))