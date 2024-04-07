from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ErrorDetail


class CustomResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        The function `render` customizes the response data and status code based on certain conditions
        before rendering it.
        
        :param data: The `data` parameter in the `render` method is the data that will be rendered by
        the renderer. It contains the response data that will be sent back to the client. The data can
        include various information such as access tokens, messages, status codes, and more depending on
        the API response
        :param accepted_media_type: The `accepted_media_type` parameter in the `render` method is used
        to specify the media type that the client can accept in the response. It indicates the format in
        which the response data should be rendered, such as JSON, XML, HTML, etc. This parameter allows
        the server to determine the
        :param renderer_context: The `renderer_context` parameter in the `render` method is a dictionary
        containing context data for the renderer. It typically includes information about the response
        being rendered, such as the status code and response object. In your code snippet, you are
        accessing the status code from the `renderer_context` dictionary to
        :return: The `render` method is returning a response object that includes session information,
        data, total count, details, and status information such as status code, status message, and a
        custom message. This response object is then passed to the `render` method of the superclass
        `CustomResponseRenderer` along with the accepted media type and renderer context.
        """
        status_code = renderer_context["response"].status_code
        print("inside the custom  renders")
        # print("data and code", data, status_code)
        # for check the the authentication failed error to change the value
        if isinstance(data.get("detail"), ErrorDetail) and (
            data.get("detail") == "Token authentication failed."
        or data.get("detail") == "Token Expired."):
            status_code = 401
            renderer_context["response"].status_code = 401
            data["details"] = (
                "Please send correct user or admin token to access the api end points"
            )
            data["message"] = "Token authentication Failed"
        elif isinstance(data.get("detail"), ErrorDetail):
            renderer_context["response"].status_code = status_code
            data["message"] = data["detail"]

        if str(status_code) == "401":
            status_message = "Unauthorized"
        elif not str(status_code).startswith("2"):
            status_message = "Error"
        else:
            status_message = "Success"
        try:
            response = {
                "session": {
                    "refresh": data.get("access", None),
                    "token": data.get("token", None),
                    "validity": 1,
                    "specialMessage": None,
                },
                "data": data.get("data", None),
                "total_count": data.get("total_count", None),
                "details": data.get("details", None),
                "status": {
                    "code": status_code,
                    "status": status_message,
                    "message": data.get("message", None),
                },
            }
        except AttributeError:
            response = data

        return super(CustomResponseRenderer, self).render(
            response, accepted_media_type, renderer_context
        )