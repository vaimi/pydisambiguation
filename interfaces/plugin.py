from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractPlugin(metaclass=ABCMeta):
    """Abstract base class definition for disambiquation algorithm. This
    plugin interface have to be used if you want to ensure compatibility with
    user interfaces and especially automatic algorithm detection

    Things to be defined in subclasses:
    str name - get
    str description - get
    AlgorithmCollection subclass/None parent - get
    dict setting - get/set
    str context - get/set
    str word - get/set
    method run()

    """

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def description(self):
        pass

    @abstractproperty
    def parent(self):
        pass

    @abstractproperty
    def settings(self):
        pass

    @settings.setter
    def settings(self, newSettings):
        pass

    @abstractproperty
    def context(self):
        pass

    @context.setter
    def context(self, newContext):
        pass  

    @abstractproperty
    def word(self):
        pass

    @word.setter
    def context(self, newWord):
        pass

    @abstractmethod
    def run(self):
        pass

class DisambiquationPlugin(AbstractPlugin):
    """Somewhat normal template for disambiquation plugins."""

    name = "Plugin" # str
    description = "Plugin template" # str
    parent = None # AlgorithmCollection subclass
    _settings = {}

    def __init__(self, name=None, description=None, settings=None, parent=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if settings is not None:
            self._settings = settings
        if parent is not None:
            self.parent = parent
        self._context = None
        self._word = None

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, newSettings):
        self._settings = newSettings

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, newContext):
        self._context = newContext 

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, newWord):
        self._word = newWord

