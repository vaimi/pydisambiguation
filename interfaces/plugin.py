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
        """Algorithm name
        
        Returns:
            str: Algorithm name
        """
        pass

    @abstractproperty
    def description(self):
        """Algorithm description
        
        Returns:
            str: Algorithm description
        """
        pass

    @abstractproperty
    def parent(self):
        """Parent group of algorithm
        
        Returns:
            AbstractGroup: Parent group of algorithm
        """
        pass

    @abstractproperty
    def settings(self):
        """Algorithm settings
        
        Returns:
            dict: Algorithm settings
        """
        pass

    @settings.setter
    def settings(self, newSettings):
        """Set new setting dict
        
        Args:
            newSettings (dict): Dictionary for settings. No defined format
        
        """
        pass

    @abstractproperty
    def context(self):
        """Context for the ambiquate word
        
        Returns:
            TYPE: Description
        """
        pass

    @context.setter
    def context(self, newContext):
        """Set context
        
        Args:
            newContext (TYPE): Description

        """
        pass  

    @abstractproperty
    def word(self):
        """Word to be disambiquated
        
        Returns:
            str: Ambiquate word
        """
        pass

    @word.setter
    def word(self, newWord):
        """Set new word
        
        Args:
            newWord (str): Ambiquate word

        """
        pass

    @abstractmethod
    def run(self):
        pass

class DisambiquationPlugin(AbstractPlugin):
    """Somewhat normal template for disambiquation plugins.
    
    Attributes:
        description (str): Algorithm description
        name (str): Algorithm name
        parent (AbstractGroup): Algorithm parent (group)
    """

    name = "Plugin" # str
    description = "Plugin template" # str
    parent = None # AbstractGroup subclass
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

