class parser():

    @classmethod
    def is_int(cls, string: str):
        try:
            int(string)
        except ValueError:
            return False
        return True

    @classmethod
    def is_float(cls, string: str):
        try:
            float(string)
        except ValueError:
            return False
        return True

    @classmethod
    def is_str(cls, string: str):
        try:
            str(string)
        except ValueError:
            return False
        return True
    
    @classmethod
    def is_bool(cls, string: str):
        try:
            bool(string)
        except ValueError:
            return False
        return True