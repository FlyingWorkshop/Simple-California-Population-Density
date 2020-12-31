import csv
import tkinter as tk

# Make the window large so that we can see more detail.
CANVAS_WIDTH = 300
CANVAS_HEIGHT = 500

# The viewpoint coordinates - the min and max long and lat
SCALE = 1
MIN_LONGITUDE = -124.26 - SCALE
MAX_LONGITUDE = -114.16 + SCALE
MIN_LATITUDE = 32.57 - SCALE
MAX_LATITUDE = 41.99 + SCALE


class CityCooked:
    def __init__(self, name, popu, lat, long):
        self.name = name
        self.popu = popu
        self.lat = lat
        self.long = long
        self.x = int(CANVAS_WIDTH * (long - MIN_LONGITUDE) / (MAX_LONGITUDE - MIN_LONGITUDE))
        self.y = int(CANVAS_HEIGHT * (1.0 - (lat - MIN_LATITUDE) / (MAX_LATITUDE - MIN_LATITUDE)))


class CityLoc:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

class CityPopu:
    def __init__(self, name, popu):
        self.name = name
        self.popu = popu

class Database:
    def __init__(self):
        self.popu_index = []
        self.loc_index = []
        self.__make_popu_index__()
        self.__make_loc_index__()

        self.cooked_index = []
        self.leftovers = []
        self.__make_cooked_index__()

    def __make_popu_index__(self):
        with open('population.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['City']
                popu = int(row['Population'].replace(',', ''))
                self.popu_index.append(CityPopu(name, popu))

    def __make_loc_index__(self):
        with open('location.csv', newline='') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                name = row['City'].removesuffix(' city').removesuffix(' town')
                lat = float(row['Latitude'])
                long = float(row['Longitude'])
                self.loc_index.append(CityLoc(name, lat, long))

    def __make_cooked_index__(self):
        temp_dict = {popu_obj.name: [popu_obj] for popu_obj in self.popu_index}
        for loc_obj in self.loc_index:
            if loc_obj.name not in temp_dict:
                self.leftovers.append(loc_obj)
            else:
                temp_dict[loc_obj.name].append(loc_obj)
        for name, vals in temp_dict.items():
            if len(vals) != 2:
                continue
            popu = vals[0].popu
            lat, long = vals[1].lat, vals[1].long
            self.cooked_index.append(CityCooked(name, popu, lat, long))

    def report(self):
        print(f'You attempted to cook {len(self.popu_index)}!')
        print(f'You successfully cooked {len(self.cooked_index)} cities!')
        print(f'You had {len(self.leftovers)} leftover!')


def main():
    root = tk.Tk()
    canvas = tk.Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    db = Database()
    for city in db.cooked_index:
        plot_one_city(canvas, city)
    canvas.pack()
    canvas.mainloop()


def plot_one_city(canvas, city):
    x = city.x
    y = city.y
    color = get_color(city.popu)
    canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)


def get_color(popu):
    if popu >= 50000:
        return 'purple'
    elif popu >= 10000:
        return 'red'
    elif popu >= 1000:
        return 'orange'
    return 'yellow'


if __name__ == "__main__":
    main()