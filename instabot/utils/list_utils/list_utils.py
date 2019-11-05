class ListUtils:

    @staticmethod
    def diff(*args):
        current_list = args[0]
        for arg in args[1:]:
            current_list = list(set(current_list) - set(arg))
        return current_list

    @staticmethod
    def commons(*args):
        current_list = args[0]
        for arg in args[1:]:
            current_list = list(set(current_list) & set(arg))
        return current_list


