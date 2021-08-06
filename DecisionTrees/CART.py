from DecisionTrees import Tree
import numpy as np
import operator
import math


class CART(Tree.Tree):
    """
    This class implements CART algorithm to create decision trees from a training dataset.
    """
    def __init__(self, dataset, attributeClass = 'CLASS'):
        """
        Creates an instance of CART class, creating the associated decision tree.
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        """
        super().__init__('CART')
        self._tree = self._createTree(dataset, attributeClass = attributeClass)

    def _getGini(self, dataset, attributeClass = 'CLASS', attributeName = 'CLASS', attributeValue = None,):
        """
        Computes the Gini Index for a dataset
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :param attributeName: name of the attribute to be used to filter the dataset and to compute its Gini Index
        :param attributeValue: value of the attribute to be used to filter the dataset and to compute its Gini Index
        :return: the associated Gini Index to the dataset, and, if informed, to the provided attributeName and attributeValue.
        """
        subset = dataset[attributeClass]
        if attributeValue:
            subset = dataset.where(dataset[attributeName] == attributeValue).dropna()[attributeClass]
        classes, classCounters = np.unique(subset, return_counts = True)
        total_elements = sum(classCounters)
        gini = 1.0
        for i in range(len(classes)):
            gini -= (classCounters[i] / total_elements)**2
        return gini

    def _getNextAttribute(self, dataset, attributeClass = 'CLASS'):
        """
        Returns the next attribute to split the data according to the best Gini Index
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :return: attribute and value with better Gini Index.
        """
        ginis = {}
        best_ginis = {}
        for attribute in dataset.keys():
            if attribute == attributeClass:
                continue
            values, valueCounters = np.unique(dataset[attribute], return_counts = True)
            if len (values) <= 1:
                continue
            if attribute not in ginis:
                ginis[attribute] = {}
            for value in values:
                subset_1 = dataset.where(dataset[attribute] == value).dropna()
                subset_2 = dataset.where(dataset[attribute] != value).dropna()
                gini_1 = self._getGini(subset_1)
                gini_2 = self._getGini(subset_2)
                total_elements = subset_1.count ()[0] + subset_2.count ()[0]
                gini = (subset_1.count()[0] / total_elements) * gini_1 + (subset_2.count ()[0] / total_elements) * gini_2
                ginis[attribute][value] = gini
        for attribute in ginis:
            minorValue, minorGini = sorted (ginis[attribute].items(), key = operator.itemgetter(1), reverse = True).pop()
            best_ginis[attribute] = {minorValue : minorGini}
        attributeToSplit = None
        valueToSplit = None
        minorGini = math.inf
        for attribute, value in best_ginis.items():
            attributeValue, gini = list(value.items())[0]
            if gini < minorGini:
                attributeToSplit = attribute
                valueToSplit = attributeValue
                minorGini = gini
        return attributeToSplit, valueToSplit

    def _createTree(self, dataset, attributeClass = 'CLASS', parent = None):
        """
        Creates the decision tree based on CART criteria
        :param dataset: training element dataset in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :param parent: if the decision tree is part of another dictionary
        :return: the tree for the dataset provided
        """
        if not parent:
            parent = {}
        if dataset.count ()[0] == 1:
            classes = np.unique (dataset[attributeClass])
            return classes[0]
        attributeToSplit, valueToSplit = self._getNextAttribute(dataset)
        subset_Yes = dataset.where(dataset[attributeToSplit] == valueToSplit).dropna()
        subset_No = dataset.where(dataset[attributeToSplit] != valueToSplit).dropna()
        classes_Yes = np.unique(subset_Yes[attributeClass])
        classes_No = np.unique(subset_No[attributeClass])
        if len (classes_Yes) == 1 and len (classes_No) == 1 and classes_No == classes_Yes:
            return classes_Yes[0]
        parent[(attributeToSplit, valueToSplit)] = {'YES' : self._createTree(subset_Yes),
                                                    'NO' : self._createTree(subset_No)}
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
                attribute, value = list(currentNode.keys())[0]
                if attribute in element.keys():
                    if element[attribute] == value:
                        currentNode = currentNode[(attribute, value)]['YES']
                        continue
                    else:
                        currentNode = currentNode[(attribute, value)]['NO']
                        continue
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
    cart = CART(dataset)
    nelements = 65
    elements = gen.generateData(nelements, classified = True, multiClass = False)
    hits = 0
    for element in elements:
        classification = cart.classify(element)
        if element['CLASS'] == classification:
            hits += 1
    import pprint
    pprint.pprint(cart.getTree())
    print("Total Depth: %s" % cart.getTreeDepth())
    print("Total hits: %f --> %f" % (hits, (hits / nelements) * 100))
