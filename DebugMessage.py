# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 20:42:38 2021

@author: Evan Yu
"""

class DebugMessage():
    def __init__(self):
        self.messages = {}
        self.layer = 0
        self.prefix = "";
        
    def setLayer(self, layer):
        self.layer = layer
        self.prefix = DebugMessage.generatePrefix(layer)
    
    def appendMessage(self, name, message):
        self.messages[name] = message
        
    def combineDebugMessage(self, debugMessage):
        self.messages.update(debugMessage.messages)
    
    def generatePrefix(layer):
        prefix = ""
        for i in range(layer):
            prefix += "\t"
        return prefix
    
    def __str__(self):
        output = ""
        for name in self.messages:
            message = self.messages[name]
            if isinstance(message, DebugMessage):
                message.setLayer(self.layer + 1)
                output += self.prefix + name + ": \n" + str(message)  
            else:
                output += self.prefix + name + ": " + str(message) + "\n"              
        
        return output