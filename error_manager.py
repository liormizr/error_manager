import exceptions


class _ErrorManagerType(type):
    def __getattr__(cls, item):
        if not item.startswith('for_'):
            return cls.__getattribute__(item)

        exception_name = item[4:]
        exception_type = getattr(exceptions, exception_name)
        return cls._instance_creator_for_exc(exception_type)

    def _instance_creator_for_exc(cls, exception_type):
        def creator(handler, on_success=None, on_default=None):
            handlers = {exception_type: handler}
            return cls(handlers=handlers, on_success=on_success, on_default=on_default)

        return creator

    def for_all(cls, on_success=None, on_default=None):
        return cls(on_success=on_success, on_default=on_default)


class ErrorManager(object):
    __metaclass__ = _ErrorManagerType

    def __init__(self, handlers=None, on_success=None, on_default=None):
        self.handlers = handlers or {}
        self.on_success = on_success
        self.on_default = on_default
        self._check_args()

    def _check_args(self):
        if not isinstance(self.handlers, dict):
            raise TypeError('handlers arg need to be a dict type')

        for error, handler in self.handlers.iteritems():
            if not (callable(error) and isinstance(error(), BaseException)):
                raise TypeError(
                    'handlers dict key need to be BaseException type, '
                    '{} is {}'.format(error, type(error))
                )
            if not callable(handler):
                raise TypeError(
                    'handlers dict values need to be callables, '
                    '{} is not'.format(handler)
                )

        if not (callable(self.on_success) or self.on_success is None):
            raise TypeError('on_success arg need to be a callable')

        if not (callable(self.on_default) or self.on_default is None):
            raise TypeError('on_default arg need to be a callable')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.on_success is not None:
            self.on_success()
            return True

        if self.handlers.get(exc_type):
            self.handlers[exc_type](exc_type, exc_val, exc_tb)
            return True

        if self.on_default is not None:
            self.on_default(exc_type, exc_val, exc_tb)
            return True

        return False
