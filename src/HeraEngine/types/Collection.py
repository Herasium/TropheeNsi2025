#Collections of entities so I can delete them. Useful for menus and mini-games.

from HeraEngine.childs.Entity import Entity
from HeraEngine.childs.Text import Text
from HeraEngine.core import Core

class Collection:
    def __init__(self,core: Core):
        self._core = core
        self.entity_list = {}

    def Entity(self,name,**kwargs):
        kwargs["core"] = self._core
        new_entity = Entity(**kwargs)
        self._core.add_entity(new_entity)
        self.entity_list[name] = new_entity
        setattr(self,name,new_entity)

    
    def Text(self,name,**kwargs):
        kwargs["core"] = self._core
        new_entity = Text(**kwargs)
        self._core.add_entity(new_entity)
        self.entity_list[name] = new_entity
        setattr(self,name,new_entity)

    def remove(self,name):
        if name in self.entity_list:
            to_remove = self.entity_list[name]
            self._core.remove_entity(to_remove)
            del self.entity_list[name]

    def quit(self):
        for name in self.entity_list:
            self._core.remove_entity(self.entity_list[name])
        self.entity_list = {}