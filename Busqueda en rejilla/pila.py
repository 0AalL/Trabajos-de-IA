class Pila:

    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        return self.elementos.pop()

    def esta_vacia(self):
        return len(self.elementos) == 0