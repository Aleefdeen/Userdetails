from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
import jwt
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from userdetails.models import UserDetails


class UsersTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        The `authenticate` function takes a request object, decodes the authorization token, verifies its
        validity, and returns the corresponding user and role if authentication is successful.

        :param request: The `request` parameter is an object that represents the HTTP request being made to
        the server. It contains information about the request, such as the headers, body, and other
        metadata. In this code snippet, the `request` parameter is used to extract the authorization header,
        which contains the token used
        :return: The authenticate function returns two values: 'admin' and 'de_value["role"]'.
        """
        try:
            print("User inside the authenticate")
            token = get_authorization_header(request).decode("utf-8").split()
            if len(token) == 2:
                de_value = jwt.decode(token[1], "users_key", algorithms=["HS256"])
                users = UserDetails.objects.filter(id=de_value["id"])
                print(de_value)
                if users.exists():
                    return users, False
                else:
                    raise AuthenticationFailed("Token authentication failed.")
            else:
                raise AuthenticationFailed("Token authentication failed.")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token Expired.")
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed("Token authentication failed.")
        except Exception as e:
            print(e)
            raise e
            raise AuthenticationFailed("Token authentication failed.")


class SimpleAdminUserTokenScheme(SimpleJWTScheme):
    name = "userAuth"
    target_class = UsersTokenAuthentication