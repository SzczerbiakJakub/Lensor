class Calc:
    @staticmethod
    def tan(x, y):
        try:
            return x / y
        except ZeroDivisionError:
            return float("inf")

    @staticmethod
    def distance_between_objects(object_1, object_2):
        return abs(object_1.x - object_2.x)

    @staticmethod
    def dict_minimum_index(dict):
        if len(dict) == 0:
            return None
        else:
            keys = list(dict.keys())
            minimum = {keys[0]: dict[keys[0]]}
            minimum_value = dict[keys[0]]
            for key in keys[1:]:
                if dict[key] < minimum_value:
                    minimum_value = dict[key]
                    minimum = {key: dict[key]}
            return minimum


class GraphicCalc(Calc):
    ...


class NumericCalc(Calc):
    @staticmethod
    def newton_algorithm_x(focal, x_prime):
        try:
            value = -1 * focal * focal / x_prime
            value = float("%.2f" % value)
            return value
        except ZeroDivisionError:
            return -1 * focal * focal * float("inf")

    @staticmethod
    def carthesian_algorithm_s(focal, s_prime):
        try:
            value = focal * s_prime / (focal - s_prime)
            value = float("%.2f" % value)
            return value
        except ZeroDivisionError:
            return focal * s_prime * float("inf")

    @staticmethod
    def newton_algorithm_x_prime(focal, x):
        try:
            value = -1 * focal * focal / x
            value = float("%.2f" % value)
            return value
        except ZeroDivisionError:
            return -1 * focal * focal * float("inf")

    @staticmethod
    def carthesian_algorithm_s_prime(focal, s):
        try:
            value = focal * s / (focal + s)
            value = float("%.2f" % value)
            return value
        except ZeroDivisionError:
            return focal * s * float("inf")

    @staticmethod
    def newton_zoom(x_prime, focal):
        try:
            value = -1 * x_prime / focal
            value = float("%.2f" % value)
            return value
        except ZeroDivisionError:
            return focal * float("inf")

    @staticmethod
    def carthesian_zoom(s, s_prime):
        try:
            value = s_prime / s
            value = float("%.3f" % value)
            return value
        except ZeroDivisionError:
            return s_prime * float("inf")

    @staticmethod
    def get_real_plane_aperture(aperture):
        if aperture.image_of is not aperture:
            while aperture.image_of != None:
                aperture = aperture.image_of
        return aperture

    @staticmethod
    def determine_object_postfix(self):
        object = self
        postfix = ""
        while object.image_of != None:
            object = object.image_of
            postfix += "'"

        return postfix

    @staticmethod
    def define_main_aperture(point, apertures):
        tan_dict = {}
        for aperture in apertures:
            real_plane_aperture = NumericCalc.get_real_plane_aperture(aperture)
            distance = Calc.distance_between_objects(point, real_plane_aperture)
            height = real_plane_aperture.diameter / 2
            tan = Calc.tan(height, distance)
            tan_dict.update({real_plane_aperture: tan})

        keys = list(tan_dict.keys())

        minimum = Calc.dict_minimum_index(tan_dict)
        return minimum

    @staticmethod
    def define_field_aperture(main_aperture, apertures):
        tan_dict = {}
        aperture_list = apertures.copy()
        if main_aperture in aperture_list:
            aperture_list.remove(main_aperture)
        for aperture in aperture_list:
            real_plane_aperture = NumericCalc.get_real_plane_aperture(aperture)
            distance = Calc.distance_between_objects(main_aperture, real_plane_aperture)
            height = real_plane_aperture.diameter / 2
            tan = Calc.tan(height, distance)
            tan_dict.update({real_plane_aperture: tan})

        keys = list(tan_dict.keys())

        minimum = Calc.dict_minimum_index(tan_dict)

        return minimum