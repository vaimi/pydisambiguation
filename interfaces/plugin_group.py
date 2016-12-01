from abc import ABCMeta, abstractproperty

class AbstractGroup(metaclass=ABCMeta):
    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def description(self):
        pass

class AlgorithmGroup(AbstractGroup):
    name = "Group template"
    description = "Template for group creation"

    def __init__(self, name=None, description=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description