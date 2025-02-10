class Treasure:
    def __init__(self, type_tresor, value):
        self.type = type_tresor  # 1 = or, 2 = pierres précieuses
        self.value = value
        self.opened = False

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def reduceValue(self, amount):
        """Réduit la valeur du trésor lorsqu'il est collecté par un agent"""
        self.value = max(0, self.value - amount)  # S'assure que la valeur ne descend pas en dessous de 0

    def isOpen(self):
        return self.opened

    def openChest(self):
        self.opened = True
        print("Coffre ouvert !")

    def resetValue(self):
        """Met à zéro la valeur du trésor"""
        self.value = 0
