import Condition, Attribute
from Exceptions import IncompleteDataException, WrongData


class Subvention(object):
    '''
    This class represents a Subvention.

    One subvention is, mainly, one set of conditions to be satisfied in terms to request it.
    '''
    def __init__(self, title, description, law, conditions = None, lawURL = None, requestURL = None, incompatibilities = None):
        """
        Creates one instance of Subvention
        :param title: title or resume of the subvention
        :param description: detailed description about the subvention
        :param law: name of the law where the subvention is defined
        :param conditions: set of conditions to be fulfilled
        :param lawURL: url of the law
        :param requestURL: url of the request form
        :param incompatibilities: text explaining the incompatibilities
        """
        self._title = title
        self._description = description
        self._law = law
        if not (isinstance(conditions, Condition.CombinedCondition)):
            raise WrongData ("Conditions has not a valid type --> expected %s and received %s" % (Condition.CombinedCondition, conditions.__class__))
        self._conditions = conditions
        self._lawURL = lawURL
        self._requestURL = requestURL
        self._incompatibilities = incompatibilities

    def getTitle(self):
        """
        Returns subvention title
        :return: title of the subvention
        """
        return self._title

    def getDescription(self):
        """
        Returns subvention description
        :return: description of the subvention
        """
        return self._description

    def getLaw(self):
        """
        Returns subvention law
        :return: law of the subvention
        """
        return self._law

    def getLawURL(self):
        """
        Returns subvention law URL
        :return: URL of the subvention law
        """
        return self._lawURL

    def getConditions(self):
        """
        Returns subvention conditions
        :return: conditions of the subvention
        """
        return self._conditions

    def getRequestURL(self):
        """
        Returns subvention request URL
        :return: URL of the subvention request
        """
        return self._requestURL

    def getIncompatibilities(self):
        """
        Returns subvention incompatibilites
        :return: incompatibilities of the subvention
        """
        return self._incompatibilities

    def setTitle(self, title):
        """
        Set new title
        :param title: title to be set
        :return: updated instance
        """
        self._title = title

    def setDescription(self, description):
        """
        Set new description
        :param description: description to be set
        :return: updated instance
        """
        self._description = description

    def setLaw(self, law):
        """
        Set new law
        :param law: law to be set
        :return: updated instance
        """
        self._law = law

    def setLawURL(self, lawURL):
        """
        Set new law URL
        :param lawURL: law URL to be set
        :return: updated instance
        """
        self._lawURL = lawURL

    def setConditions(self, conditions):
        """
        Set new conditions
        :param conditions: conditions to be set
        :return: updated instance
        """
        self._conditions = conditions

    def setRequestURL(self, requestURL):
        """
        Set new request URL
        :param requestURL: requestURL to be set
        :return: updated instance
        """
        self._requestURL = requestURL

    def setIncompatibilities(self, incompatibilities):
        """
        Set new incompatibilities
        :param incompatibilities: incompatibilities to be set
        :return: updated instance
        """
        self._incompatibilities = incompatibilities

    def checkCompliance(self, **answers):
        """
        Check if the data provided satisfies the conditions associated to the subvention
        :param answers: dict of attributes and their values
        :return: True if the condition is satisfied or False in other case
        """
        try:
            return self._conditions.check(**answers)
        except Exception as e:
            raise IncompleteDataException("Data is incomplete!")

    def getUniqueAttributes(self):
        """
        Returns the list of unique attributes that composes the subvention
        :return: list of attributes
        """
        return self._conditions.getUniqueAttributes()

    def __repr__(self):
        return "Title <%s>\n\tDescription <%s>\n\tLaw <%s>\n\tLawURL <%s>\n\tRequestURL <%s>\n\tConditions <%s>\n\tIncompatibilites <%s>" % (self.getTitle(),
                                                                                                                                             self.getDescription(),
                                                                                                                                             self.getLaw(),
                                                                                                                                             self.getLawURL(),
                                                                                                                                             self.getRequestURL(),
                                                                                                                                             self.getConditions(),
                                                                                                                                             self.getIncompatibilities())

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    a1 = Attribute.Attribute('COTIZACION', '', ['Sí', 'No'], bool, '')
    a2 = Attribute.Attribute('FALLECIMIENTO_CONYUGE', '', ['Sí', 'No'], bool, '')
    a3 = Attribute.Attribute('PERIODO_MINIMO_ALTA', '',
                             ['Otros', '15 años o más', '1800 días o más', '500 días (periodo ininterrumpido durante 5 años)', '365 días (6 años inmediantamente anteriores)'], list, '')
    a4 = Attribute.Attribute('PERIODO_MINIMO_NO_ALTA', '', ['Sí', 'No'], bool, '')
    c1 = Condition.SimpleCondition(a1, '=', 'Sí')
    c2 = Condition.SimpleCondition(a2, '=', 'Sí')
    c3 = Condition.SimpleCondition(a3, '=', '500 días (periodo ininterrumpido durante 5 años)')
    c4 = Condition.SimpleCondition(a4, '=', 'Sí')
    condition = Condition.AND(Condition.OR(c1, c2), Condition.OR(c3, c4))
    sub = Subvention('Titulo', 'Descripcion', 'Ley', condition)
    print(sub.checkCompliance(**{'COTIZACION': 'No',
                                 'FALLECIMIENTO_CONYUGE': 'Sí',
                                 'PERIODO_MINIMO_ALTA': '5000 días (periodo ininterrumpido durante 5 años)',
                                 'PERIODO_MINIMO_NO_ALTA': 'No'}))
