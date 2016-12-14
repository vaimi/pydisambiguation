import sys
import os
import inspect
import importlib
from interfaces.plugin import DisambiquationPlugin, AbstractPlugin
import nltk

class DisambiquateCore(object):
    def __init__(self):
        self.algorithms = {}

    def findAlgorithms(self, include, exclude):
        #https://chriscoughlin.com/2012/04/writing-a-python-plugin-framework/
        algorithms_folder = "./algorithms"
        algorithms = []
        if not algorithms_folder in sys.path:
            sys.path.append(algorithms_folder)
        for root, dirs, files in os.walk(algorithms_folder):
            for module_file in files:
                module_name, module_extension = os.path.splitext(module_file)
                if module_extension == os.extsep + "py":
                    plugin_module = importlib.import_module(module_name)
                    plugin_classes = inspect.getmembers(plugin_module, inspect.isclass)
                    for plugin_class in plugin_classes:
                        if issubclass(plugin_class[1], AbstractPlugin):
                            if plugin_class[1].__module__ == module_name:
                                if len(include):
                                    if plugin_class[0] in include:
                                        algorithms.append(plugin_class)
                                    elif set([parent.__name__ for parent in inspect.getmro(plugin_class[1])]) & set(include):
                                        algorithms.append(plugin_class)
                                    continue
                                if plugin_class[0] not in exclude:
                                    algorithms.append(plugin_class)
        return algorithms

    def getAlgorithmInstance(self, plugin_name, algorithms = None):
        """Given the name of a plugin, returns the plugin's class and an instance of the plugin,
        or (None, None) if the plugin isn't listed in the available plugins."""
        plugin_instance = None
        available_plugins = self.findAlgorithms() if algorithms is None else algorithms 
        plugin_names = [plugin[0] for plugin in available_plugins]
        plugin_classes = [plugin[1] for plugin in available_plugins]
        if plugin_name in plugin_names:
            plugin_class = plugin_classes[plugin_names.index(plugin_name)]
            try: 
                plugin_instance = plugin_class(None)
            except TypeError:
                pass
            #plugin_instance.data = self.data
        return plugin_instance

    def registerAlgorithm(self, algorithm, key=None):
        if algorithm is None:
            return False
        key = len(self.algorithms)+1 if key is None else key
        if key not in self.algorithms and isinstance(key, int):
            if key >= 1:
                self.algorithms[key] = algorithm
                return key
        return False

    def unregisterAlgorithm(self, algorithm):
        if self.algorithms.pop(key, None):
            return True
        return False

    def getAlgorithmInfo(self, key):
        if key in self.algorithms:
            current = self.algorithms[key]
            return {'key': key, 'name': current.name, 'description': current.description, 'parent':current.parent}
        return {}

    def getAlgorithmsInfo(self):
        return map(self.getAlgorithmInfo, self.algorithms)

    def runAlgorithm(self, key, word, sentence):
        algorithm = self.algorithms[key]
        pattern = r'''(?x)          # set flag to allow verbose regexps
            (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
          | \w+(?:-\w+)*        # words with optional internal hyphens
          | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
          | \.\.\.              # ellipsis
          | [][.,;"'?():_`-]    # these are separate tokens; includes ], [
        '''
        algorithm.context = nltk.regexp_tokenize(sentence, pattern)
        algorithm.word = word
        result = algorithm.run()
        return {'algorithm':key, 'sense':result}
 
