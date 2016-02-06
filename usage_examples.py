from error_manager import ErrorManager


def example_1():
    def key_error_handler(*args, **kwargs):
        print 'KeyError handler'
        print args, kwargs

    with ErrorManager.for_KeyError(handler=key_error_handler):
        d = {}
        d['fake_item']


def example_2():
    def default_error_handler(*args, **kwargs):
        print 'defaul handler'
        print args, kwargs

    with ErrorManager.for_all(on_default=default_error_handler):
        d = {}
        d['fake_item']


def example_3():
    def success_handler(*args, **kwargs):
        print 'success handler'
        print args, kwargs

    with ErrorManager.for_all(on_success=success_handler):
        d = {'item': 0}
        d['item']
