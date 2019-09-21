
class Tools:

    @classmethod
    def str_to_bool(self, s):
        if s.lower() == 'True'.lower():
            return True
        elif s.lower() == 'False'.lower():
            return False