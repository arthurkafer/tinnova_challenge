class Voting:
    def __init__(self, total, validos=0, brancos=0, nulos=0):
        self.total_de_eleitores = total
        self.validos = validos
        self.brancos = brancos
        self.nulos = nulos
        
    def get_valid_voted_percentage(self):
        return self.validos/self.total_de_eleitores

    def get_blank_voted_percentage(self):
        return self.brancos/self.total_de_eleitores

    def get_null_voted_percentage(self):
        return self.nulos/self.total_de_eleitores

v = Voting(1000, 800, 150, 50)

print(v.get_valid_voted_percentage())
print(v.get_blank_voted_percentage())
print(v.get_null_voted_percentage())