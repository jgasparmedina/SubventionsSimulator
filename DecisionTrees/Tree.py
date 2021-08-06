from collections import deque


class Tree(object):
    """
    This abstract class represent a generic Decision Tree, implements some common methods and defines other ones which mus to be implemented in its heir classes.
    """
    def __init__(self, algorithmName):
        """
        Creates an instance of Tree
        """
        self._tree = None
        self._name = algorithmName

    def getTreeName(self):
        """
        Returns algorithm name
        :return: name of the Tree
        """
        return self._name

    def getTree(self):
        """
        Returns the decision tree created
        :return: a dict including the decision tree
        """
        return self._tree

    def getTreeDepth(self, tree = None):
        """
        Computes recursively the max depth of the decision tree
        :param tree: the tree to be computed
        :return: max depth of the tree
        """
        if not tree:
            tree = self._tree
        queue = deque([(id(tree), tree, 1)])
        memo = set()
        while queue:
            id_, o, level = queue.popleft()
            if id_ in memo:
                continue
            memo.add(id_)
            if isinstance(o, dict):
                queue += ((id(v), v, level + 1) for v in o.values())
        return level

    def _createTree(self, dataset, attributeClass = 'CLASS', parent = None):
        """
        Creates the decision tree associated to one dataset.
        This method must to be overridden.
        :param dataset: training element set in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :param parent: for recursive purposes, parent is the dictionary which will contains the generated tree
        :return: dict with the decision tree
        """
        raise Exception("You must override this method!")

    def _getNextAttribute(self, dataset, attributeClass = 'CLASS'):
        """
        Provides the next attribute to split the tree. During the tree creation process this method will be called to identify what is the next attribute to split for.
        This method must to be overridden.
        :param dataset: pending training set in DataFrame format (pandas)
        :param attributeClass: name of the attribute which provides the class of the elements. By default the attribute will be 'CLASS'
        :return: the name of the attribute to split the tree
        """
        raise Exception("You must override this method!")

    def classify(self, element, default = 'None'):
        """
        Once the decision tree is created, using classify method one element can be classified.
        This method must to be overridden.
        :param element: element to be classified in dict format where each key is one attribute name and each value is the value of that attribute.
        :param default: default class in case the element can not be classified.
        :return: the class which the element belongs to.
        """
        raise Exception("You must override this method!")
