class WrongOperatorException(Exception):
    """
    This class represents one exception which is raised when one operator is not valid
    """
    def __str__(self):
        return 'Operator is not valid!'


class AttributeWithoutDataException(Exception):
    """
    This class represents one exception which is raised when one attribute has not value
    """
    def __init__(self, attribute):
        self._attribute = attribute
        super().__init__()

    def __str__(self):
        return 'Attribute %s not found in values!' % self._attribute


class IncompleteDataException(Exception):
    """
    This class represents one exception which is raised when there is no enough data to valuate one condition
    """
    def __init__(self, message):
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return self._message


class WrongData(Exception):
    """
    This class represents one exception which is raised when some provided data not matches with the expected type
    """
    def __init__(self, message):
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return self._message


class UnexpectedAttributeData(Exception):
    """
    This class represents one exception which is raised when some provided data attribute not matches with the expected attribute
    """
    def __init__(self, message):
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return self._message


class SimulationInProcess(Exception):
    """
    This class represents one exception which is raised when one Simulation is in process
    """
    def __init__(self, message):
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return self._message


class NoMoreAttributes(Exception):
    """
    This class represents one exception which is raised when one Simulation has not more attributes to ask for
    """
    def __init__(self, message):
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return self._message


class FileLoaderException(Exception):
    """
    This class represents one exception which is raised when the SimulationLoader fails loading the provided config file
    """
    def __init__(self, message):
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return self._message