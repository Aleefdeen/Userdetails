import jwt
import datetime



def users_encode_token(payload: dict):
    """
    The function `users_encode_token` encodes a payload dictionary into a JSON Web Token (JWT) using the
    "users_key" as the secret key and the HS256 algorithm, with the expiration time set to 7 days from
    the current UTC time.

    :param payload: The payload is a dictionary that contains the data to be encoded into the token. It
    can include any key-value pairs that you want to include in the token
    :type payload: dict
    :return: a token that has been encoded using the JWT (JSON Web Token) library.
    """
    payload["exp"] = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(days=7)
    token = jwt.encode(payload, "users_key", algorithm="HS256")
    return token
