from functools import partial
from abc import ABC


class AbstractDecorator(ABC):
    def __init__(self, *args, **kwargs):
        if args and callable(args[0]):
            self.function = args[0]
            self.args = None
            self.kwargs = None
        else:
            self.function = None
            self.args = args
            self.kwargs = kwargs
        self.before_result = None
        self.execution_result = None
        self.after_result = None

    def __call__(self, *args, **kwargs):
        if args and callable(args[0]):
            self.function = args[0]

            def wrapper(*func_args, **func_kwargs):
                self.before_result = self.__do_before__(*func_args, **func_kwargs)
                self.execution_result = self.__do__(*func_args, **func_kwargs)
                self.after_result = self.__do_after__(*func_args, **func_kwargs)

            return wrapper
        else:
            self.before_result = self.__do_before__(*args, **kwargs)
            self.execution_result = self.__do__(*args, **kwargs)
            self.after_result = self.__do_after__(*args, **kwargs)

    def __get_param__(self, param_name, default_value):
        try:
            setattr(self, param_name, self.kwargs[param_name])
        except Exception as e:
            setattr(self, param_name, default_value)

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def __do_before__(self, *args, **kwargs):
        pass

    def __do__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __do_after__(self, *args, **kwargs):
        pass
