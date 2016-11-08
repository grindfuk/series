# Lab15 Reference Implementation
# CS207 - Spring 2016

class LazyOperation:
	"""
	A custom implementation of a future

	Attributes:
	_function : the stored function for later evaluation
	_args: positional arguments
	_kwargs: named arguments

	Methods:
	__init__ : initializes a new LazyOperation around a given function
	eval : evaluates the function stored with its arguments

	"""

	def __init__(self, function, *args, **kwargs):
		"""
		initializes a new LazyOperation object

		Parameters
		----------
		function : a function for which the future shall be created
		args : arguments to pass to the function
		kwargs : arguments that are passed with names to the function

		"""
		self._function = function
		self._args = args
		self._kwargs = kwargs

	def eval(self):
		"""
		evaluates the stored function 

		Returns
		-------
		returns result of stored function evaluated with stored arguments
		"""

		# to avoid tuple assignment error, cast to list!
		c_args = list(self._args)
		# evaluation needs to be done recursively, first evaluate positional arguments
		for pos, arg in enumerate(c_args):
			if isinstance(arg, LazyOperation):
				c_args[pos] = arg.eval()
		# then named arguments
		for name, arg in self._kwargs.items():
			if isinstance(arg, LazyOperation):
				self._kwargs[name] = arg.eval()

		# update with copies
		self._args = tuple(c_args)
		# with updated dictionaries, eval fun itself
		return self._function(*self._args, **self._kwargs)


def lazy(f):
    '''
    decorator for function to turn them into a lazy version
    '''
    def inner_fun(*args, **kwargs):
        out_fun = LazyOperation(f, *args, **kwargs)
        return out_fun
    return inner_fun