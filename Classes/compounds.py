


class CompoundList():
    
    def __init__(self):
        self.compoundList = []

    ### SETTERS
    def clear(self):
        self.compoundList = []

    def setCompounds(self, compounds):
        self.compoundList = compounds

    def addCompound(self, code, name):
        self.compoundList.append((code, name))

    def addCompoundsFromList(self, compounds):
        for comp in compounds:
            self.compoundList.append(comp)


    ### GETTERS

    ### READ WRITE
    def readFromTXT(self, path):
        pass
    def writeToTXT(self, path):
        with open(path, "w+") as file:
            file.write("\n".join([str(comp).replace("'","").replace("[","").replace("]","") for comp in self.compoundList]))


    def readFromCSV(self, path):
        pass
    def writeToCSV(self, path):
        pass
