class Cola:

    def __init__(self):
        self.elementos = []

    def encolar(self, elemento):
        self.elementos.append(elemento)

    def desencolar(self):
        return self.elementos.pop(0)

    def esta_vacia(self):
        return len(self.elementos) == 0