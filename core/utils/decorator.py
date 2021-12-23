import jwt

from django.http        import JsonResponse

from guyshouse.settings import ALGORITHM, SECRET_KEY
from users.models       import User

def signin_decorator(func):
    def wrapper(self, request, *arg, **kwarg):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            request.user = User.objects.get(id = payload['id'])

            return func(self, request, *arg, **kwarg)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALED_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALED_USER'}, status=401)

    return wrapper

def host_decorator(func):
    def wrapper(self, request, *arg, **kwarg):
        if not request.user.is_host:
            return JsonResponse({'message' : 'NOT HOST'}, status=400)
        
        return func(self, request, *arg, **kwarg)

    return wrapper
        
            
