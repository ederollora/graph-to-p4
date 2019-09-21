

class Header:

    POSITION = 1
    NAME = 2

    def __init__(self):
        self.name = ''
        self.fields = []
        self.longest_bw = 0
        self.stage = 0

    class Field:
        def __init__(self):
            self.position = 0
            self.name = ''
            self.bit_width = 0

    def extract(self, obj, all_fields):
        self.name = obj.get('name').lower().strip()

        for key, value in all_fields.items():
            key_values = key.split("_")
            f = self.Field()

            f.position = int(key_values[self.POSITION])
            f.name = key_values[self.NAME]
            f.bit_width = int(value)

            if len(value) > self.longest_bw: self.longest_bw = len(value)

            self.fields.append(f)

    def get_field_by_name(self, name):
        field = ''
        for f in self.fields:
            if f.name == name:
                field = f
                break

        return f


