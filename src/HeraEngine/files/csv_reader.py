
class CSV():
    def read(self,input_file="result.txt"):
        coordinates_x = []
        coordinates_y = []
        with open(input_file, "r") as file:
            for line in file:
                x, y = map(int, line.strip().split(";"))
                coordinates_x.append(x)
                coordinates_y.append(y)
        return coordinates_x,coordinates_y