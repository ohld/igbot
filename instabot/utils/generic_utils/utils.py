class Utils(object):
    
    @staticmethod
    def get_dict(obj):
        if hasattr(obj, '__dict__'):
            obj_dict = Utils.__get_dict_obj__(obj)
        elif type(obj) is list:
            obj_dict = Utils.__get_dict_list__(obj)
        else:
            obj_dict = obj
        return obj_dict
        
    @staticmethod
    def __get_dict_obj__(obj):
        obj_dict = {}
        attributes = vars(obj).keys()
        for a in attributes:
            value = getattr(obj, a)
            if hasattr(value, '__dict__'):
                obj_dict[a] = Utils.__get_dict_obj__(value)
            elif type(value) is list:
                obj_dict[a] = Utils.__get_dict_list__(value)
            else:
                obj_dict[a] = value
        return obj_dict

    @staticmethod
    def __get_dict_list__(obj):
        obj_list = []
        for l in obj:
            if hasattr(l, '__dict__'):
                obj_list.append(Utils.__get_dict_obj__(l))
            elif type(l) is list:
                obj_list.append(Utils.__get_dict_list__(l))
            else:
                obj_list.append(l)
        return obj_list
