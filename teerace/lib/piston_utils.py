import json
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from race.models import Server
from piston.decorator import decorator
from piston.resource import Resource as PistonResource
from piston.utils import rc, FormValidationError


class APIKeyAuthentication(object):
	"""
	API key authenticater.
	"""
	def __init__(self, realm='API'):
		self.realm = realm

	@staticmethod
	def is_authenticated(request):
		auth_string = request.META.get('HTTP_API_AUTH', None)

		if not auth_string:
			return False

		if not len(auth_string) == 32:
			return False

		try:
			server = Server.objects.get(public_key=auth_string)
			request.user = server.maintained_by
			request.server = server
			server.save() # bumps the last_connection_at
			request.throttle_extra = server.id
		except Server.DoesNotExist:
			request.user = AnonymousUser()

		return not request.user in (False, None, AnonymousUser())

	def challenge(self):
		resp = HttpResponse("{0} API - Authorization Required".format(self.realm))
		resp.status_code = 401
		return resp
		

def validate_mime(v_form, operation='POST'):
	""" This fetches the submitted data for the form 
	from request.data because we always expect JSON data
	It is otherwise a copy of piston.util.validate.
	"""
	del operation

	@decorator
	def wrap(wrapped_function, self, request, *a, **kwa):
		if not hasattr(request, 'data'):
			raise AttributeError("Validator expects serialized data.")
		form = v_form(request.data)

		if form.is_valid():
			setattr(request, 'form', form)
			return wrapped_function(self, request, *a, **kwa)
		else:
			raise FormValidationError(form)
	return wrap

class rcs_factory(object):
	CODES = dict(
		ALL_OK = ('OK', 200),
		CREATED = ('Created', 201),
		DELETED = ('', 204), # 204 says "Don't send a body!"
		BAD_REQUEST = ('Bad Request', 400),
		FORBIDDEN = ('Forbidden', 401),
		NOT_FOUND = ('Not Found', 404),
		DUPLICATE_ENTRY = ('Conflict/Duplicate', 409),
		NOT_HERE = ('Gone', 410),
		INTERNAL_ERROR = ('Internal Error', 500),
		NOT_IMPLEMENTED = ('Not Implemented', 501),
		THROTTLED = ('Throttled', 503)
	)
	
	def __getattr__(self, attr):
		try:
			return self.CODES.get(attr)
		except TypeError:
			raise AttributeError(attr)

rcs = rcs_factory()

def rc(attr, content=None, already_rich=False):
	(r, c) = attr

	if content is None:
		content = r

	if not already_rich:
		content = json.dumps({'message': content})

	class HttpResponseWrapper(HttpResponse):
		"""
		Wrap HttpResponse and make sure that the internal _is_string 
		flag is updated when the _set_content method (via the content 
		property) is called
		"""
		def _set_content(self, content):
			"""
			Set the _container and _is_string properties based on the 
			type of the value parameter. This logic is in the construtor
			for HttpResponse, but doesn't get repeated when setting 
			HttpResponse.content although this bug report (feature request)
			suggests that it should: http://code.djangoproject.com/ticket/9403 
			"""
			if not isinstance(content, basestring) and hasattr(content, '__iter__'):
				self._container = content
				self._is_string = False
			else:
				self._container = [content]
				self._is_string = True

			content = property(HttpResponse._get_content, _set_content)

	return HttpResponseWrapper(content,
		content_type='application/json', status=c)


class Resource(PistonResource):

	def form_validation_response(self, exception):
		"""
		Turns the error object into a serializable construct.
		All credit for this method goes to Jacob Kaplan-Moss
		"""

		# Serialize the error.form.errors object
		json_errors = json.dumps(
			dict(
				(k, map(unicode, v))
				for (k,v) in exception.form.errors.iteritems()
			)
		)
		return rc(rcs.BAD_REQUEST, json_errors, already_rich=True)
