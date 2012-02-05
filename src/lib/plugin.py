#!/usr/bin/env python

# Media Dragon - the modular media manager
# Copyright (C) 2012 Brian Hrebec
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Plugin management and base classes

import os, logging, sys
import mediadragon
log = logging.getLogger('mediadragon')

class Plugin():
    ID = None

    def __init__(self, name):
        self.name = name

    def desc(self):
        return "Plugin"

    def setup(self):
        """ Called when the plugin is first loaded """
        pass

    def destroy(self):
        """ Called when the plugin is unloaded """
        pass

class Source(Plugin):
    def __init__(self, output):
        Plugin.__init__(self, Plugin.SOURCE)

    def desc(self):
        return "Source"

    def query(self, **parameters):
        return None



class Sink(Plugin):
    def __init__(self):
        Plugin.__init__(self, Plugin.SINK)

    def desc(self):
        return "Sink"

class Filter(Plugin):
    def __init__(self):
        Plugin.__init__(self, Plugin.FILTER)

    def desc(self):
        return "Filter"

class PluginManager:
    def import_plugins(self, path):
        plugin_dir = os.path.realpath(path)
        plugin_files = [x[:-3] for x in os.listdir(plugin_dir) 
                if x.endswith(".py")]
        old_path = sys.path
        sys.path.insert(0, plugin_dir)
        for f in plugin_files:
            print(f)
            try:
                if f != "__init__":
                    __import__(f)
            except ImportError:
                pass
        sys.path = old_path

    def register_plugins(self):
        for plugin in Plugin.__subclasses__():
            if plugin.ID:
                self._plugins[plugin.ID] = plugin

    def __init__(self, searchpaths):
        self._plugins = {}

        for p in searchpaths:
            try:
                self.import_plugins(p)
            except OSError:
                log.error("Plugin path not found: {}".format(p)) 

        try:
            builtin_path = __import__('mediadragon.plugins').plugins.__path__
            self.import_plugins(builtin_path[0])
        except ImportError:
            log.error("Builtin plugins not found!") 

        self.register_plugins()

    @property
    def plugins(self):
        return self._plugins
        """ Returns a list of all available plugins """

    def get_plugin(self, plugin_id):
        return _plugins[plugin_id]
        """ Returns a list of all available plugins """

    def load_plugin(self, plugin, plugin_name):
        pass

