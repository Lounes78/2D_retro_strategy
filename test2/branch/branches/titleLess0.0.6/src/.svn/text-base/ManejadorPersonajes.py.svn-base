class ManejadorPersonajes(object):

    def __init__(self, personajes):

        self.personajes = []
        for personaje in personajes:
            self.personajes.append([personaje, 0])

    def actualizarPersonajes(self):

        #print self.personajes
        for personaje in self.personajes:
            if personaje[0].groups() == [] and personaje[1] == personaje[0].RESURECCION:
                personaje[0] = type(personaje[0])(personaje[0].mapa, personaje[0].media, personaje[0].inicial[0], personaje[0].inicial[1], personaje[0].spriteActual.get_width(), personaje[0].spriteActual.get_height())
                personaje[1] = 0
            else:
                if personaje[0].groups() == [] and personaje[1] < personaje[0].RESURECCION: personaje[1] += 1