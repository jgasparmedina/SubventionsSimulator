import operator

import SubventionsLoader, Subvention
from Exceptions import IncompleteDataException, WrongData, UnexpectedAttributeData, NoMoreAttributes, SimulationInProcess


class Simulator(object):
    """
    This class manage the simulation process.

    Simulator drives the process to get information from the conditions for all the configured subventions.
    """
    def __init__(self, subventions):
        """
        Create an instance of Simulator
        :param subventions: a dict including subventions
        """
        if not isinstance(subventions, dict):
            raise WrongData ("Subventions has not a valid type --> expected %s and received %s" % (dict, subventions.__class__))
        for sub in subventions.values():
            if not isinstance(sub, Subvention.Subvention):
                raise WrongData("Subvention has not a valid type --> expected %s and received %s" % (Subvention.Subvention, sub.__class__))
        self._subventions = subventions
        self._subventionsToSimulate = []
        self._attributes = {}
        self._attributesInOrder = []
        self._attributesData = {}
        self._inProcess = False
        self._subventionsOk = []
        self._subventionsKo = []
        self._attributeExpected = None

    def startSimulation(self, subventionIds = []):
        """
        Starts one simulation process for the subventions included in subventionsIds
        :param subventionIds: list of subventions ids to be included in the simulation
        :return: updated instance
        """
        self._attributes = {}
        self._attributesInOrder = []
        self._attributesData = {}
        self._subventionsOk = []
        self._subventionsKo = []
        self._subventionsToSimulate = []
        self._attributeExpected = None
        if subventionIds == []:
            subventionIds = self._subventions.keys()

        for subventionId in subventionIds:
            if subventionId in self._subventions:
                if self._subventions[subventionId].getActive ():
                    self._subventionsToSimulate.append(subventionId)
                    attributes = self._subventions[subventionId].getUniqueAttributes()
                    for attribute in attributes:
                        try:
                            self._attributes[attribute] += 1
                        except KeyError as e:
                            self._attributes[attribute] = 1
        self._attributesInOrder = sorted(self._attributes.items (), key = operator.itemgetter(1), reverse = False)
        self._inProcess = True

    def isFinished (self):
        """
        Returns if the simulations is finished
        :return: True if the simulation is finished, False otherwise
        """
        return not self._inProcess

    def getNextAttribute (self):
        """
        Returns next attribute to be asked for
        :return: attribute to be asked for
        """
        if self._attributes:
            self._attributesInOrder = sorted(self._attributes.items (), key = operator.itemgetter(1), reverse = False)
            self._attributeExpected, count = self._attributesInOrder.pop()
            self._attributes.pop(self._attributeExpected)
            return self._attributeExpected
        else:
            raise NoMoreAttributes ("No more attributes!")

    def setAttributeData (self, attribute, value):
        """
        Sets attribute data
        :param attribute: attribute name to be set
        :param value: value to be set
        :return: update instance
        """
        if attribute != self._attributeExpected.getName():
            raise UnexpectedAttributeData ("Attribute not expected!")
        self._attributesData[attribute] = value
        self._checkCompliance()

    def getPendingAttributes (self):
        """
        Returns the number of pending attributes
        :return: number of pending attributes
        """
        return len (self._attributesInOrder)

    def _checkCompliance (self):
        """
        Checks the status of the crossing the list of subventions with the value of the attributes already provided
        :return: updated instance
        """
        for subventionId in self._subventionsToSimulate:
            if subventionId in self._subventionsKo:
                continue
            try:
                subventionOk =  self._subventions[subventionId].checkCompliance(**self._attributesData)
                if subventionOk and subventionId not in self._subventionsOk:
                    self._subventionsOk.append(subventionId)
                if not subventionOk:
                    if subventionId not in self._subventionsKo:
                        self._subventionsKo.append(subventionId)
                    attributes = self._subventions[subventionId].getUniqueAttributes()
                    for attribute in attributes:
                        try:
                            self._attributes[attribute] -= 1
                            if self._attributes[attribute] == 0:
                                self._attributes.pop(attribute)
                        except KeyError:
                            pass
            except IncompleteDataException:
                continue
        if not self._attributes:
            self._inProcess = False
        else:
            self._attributesInOrder = sorted(self._attributes.items(), key = operator.itemgetter(1), reverse = False)

    def getSubventionsOk (self):
        """
        Returns the list of subventions which fulfill the requirements
        :return: list of subventions ids
        """
        if self._inProcess:
            raise SimulationInProcess ("Simulation is still running!")
        self._subventionsOk.sort()
        return self._subventionsOk


if __name__ == '__main__': #Console Simulator
    from SubventionsDataSample import AYUDAS, ATRIBUTOS
    data = SubventionsLoader.SubventionsDictLoader()
    data.load(ATRIBUTOS, AYUDAS)
    simulator = Simulator(data.getSubventions())
    simulator.startSimulation()
    while (not simulator.isFinished()):
        attribute = simulator.getNextAttribute()
        print (attribute['QUESTION'])
        if attribute['VALUES'] != None:
            answerValid = False
            answerIndex = -1
            while not answerValid:
                print ("Elige una opción válida:")
                for i in range (len (attribute['VALUES'])):
                    print ("%s) %s" % (i + 1, attribute['VALUES'][i]))
                answerIndex = input ("Opción elegida:")
                try:
                    answerIndex = int (answerIndex)
                    if 1 <= answerIndex <= len (attribute['VALUES']):
                        answerValid = True
                    else:
                        print ("Opción incorrecta!")
                except Exception as e:
                    print ("Por favor indica el número de la opción elegida!", e)
            #return attribute['VALORES'][attribute - 1]
            simulator.setAttributeData(attribute.getName(), attribute['VALUES'][answerIndex - 1])
        else:
            answerValid = False
            answer = -1
            while not answerValid:
                answer = input ("Introduce:")
                try:
                    answer = int (answer)
                    answerValid = True
                except:
                    print ("Por favor introduce un valor válido!")
            simulator.setAttributeData(attribute.getName(), answer)
    subventionsOk = simulator.getSubventionsOk()
    if (not subventionsOk):
        print("Lo siento, no cumples los requisitos para ninguna ayuda")
    else:
        for subventionId in subventionsOk:
            print ("Puedes acceder a la ayuda %s según el %s" % (data.getSubvention(subventionId).getTitle(), data.getSubvention(subventionId).getLaw()))