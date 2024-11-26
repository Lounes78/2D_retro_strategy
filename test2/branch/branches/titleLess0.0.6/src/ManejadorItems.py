class ManejadorItems(object):

    def __init__(self, items):

        self.items = []
        for item in items:
            self.items.append([item, 0])

    def actualizarItems(self):

        for item in self.items:
            if item[0].groups() == [] and item[1] == item[0].RESURECCION:
                claseTemporal = item[0].__class__
                item[0] = claseTemporal(item[0].mapa, item[0].media, item[0].inicial[0], item[0].inicial[1], item[0].spriteActual.get_width(), item[0].spriteActual.get_height())
                item[1] = 0
            else:
                if item[0].groups() == [] and item[1] < item[0].RESURECCION: item[1] += 1