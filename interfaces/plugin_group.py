from abc import ABCMeta, abstractproperty

class AbstractGroup(metaclass=ABCMeta):
    """Abstract definition for group of something
    """
    @abstractproperty
    def name(self):
        """Group name
        
        Returns:
            str: Group name
        """
        pass

    @abstractproperty
    def description(self):
        """Group description
        
        Returns:
            str: Group description
        """
        pass

class AlgorithmGroup(AbstractGroup):
    name = "Group template"
    description = "Template for group creation"

    def __init__(self, name=None, description=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description