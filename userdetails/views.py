from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from userdetails.utils import users_encode_token
from userdetails.authentication import UsersTokenAuthentication
from userdetails.filters import UserDetailsListSearchFilter
from userdetails.models import UserDetails
from userdetails.paginations import UserDetailsPagination
from userdetails.serializers import LoginUserDetailsSerializer, UserDetailsSerializer


class UserDetailsViewSet(ModelViewSet):
    authentication_classes = [UsersTokenAuthentication]
    filterset_class = UserDetailsListSearchFilter
    pagination_class = UserDetailsPagination
    serializer_class = UserDetailsSerializer
    queryset = UserDetails.objects.all()
    
    
    def create(self, request, *args, **kwargs):
        """
        This function creates a new user if the email provided does not already exist in the queryset.
        
        :param request: The `request` parameter in the `create` method is typically an object that
        contains information about the incoming HTTP request, such as the request method, headers, body,
        and query parameters. In this specific context, it seems like the `request` object is being used
        to access the data sent in
        :return: The code snippet provided is a method for creating a new user. Depending on the
        conditions met during the process, different responses are returned:
        """
        if self.queryset.filter(email=request.data['email']).exists():
            return Response(dict(message="Failed",details="Given Email id already exists"), status=status.HTTP_409_CONFLICT)
        user_serializer = self.get_serializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(dict(message="success",details="User created successfully", data=user_serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(dict(message="Failed", details=user_serializer.errors), status=status.HTTP_502_BAD_GATEWAY)
    
    def retrieve(self, request, *args, **kwargs):
        """
        This Python function retrieves user data based on the provided user ID and returns a response
        with success message or error details.
        
        :param request: The `request` parameter in the `retrieve` method represents the HTTP request
        that is made to retrieve a specific user's data. It contains information such as the user ID
        (primary key) for which the data is being retrieved, and any additional data or parameters that
        are sent along with the request
        :return: The code snippet is a method named "retrieve" that is used to retrieve user data based
        on the user ID provided in the request. If the user with the specified ID exists in the
        queryset, the method returns a success response with the user data serialized. If the user ID
        does not exist, it returns a failure response indicating that the user ID doesn't exist. If any
        other exception occurs during the
        """
        try:
            user_id = self.kwargs['pk']
            user_data = self.queryset.get(id=user_id)
            user_serializer = self.get_serializer(instance=user_data).data
            return Response(dict(message="success",details="User retrieve successfully", data=user_serializer), status=status.HTTP_201_CREATED)
        except UserDetails.DoesNotExist:
            return Response(dict(message="Failed", details="Given User id doesn't exists"), status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response(dict(message="Failed", details=str(e)), status=status.HTTP_502_BAD_GATEWAY)
    
    def list(self, request, *args, **kwargs):
        """
        This Python function lists and updates users with pagination and error handling.
        
        :param request: The `request` parameter in the `list` method represents the HTTP request that is
        sent to the API endpoint. It contains information such as the request method, headers, data, and
        query parameters. This parameter allows you to access and process the incoming request in your
        Django REST framework view
        :return: The code snippet is returning a response with a success message along with the updated
        user data if the serializer is valid and the update is successful. If the serializer is not
        valid, it returns a response with a failure message and details of the serializer errors.
        """
        
        filter_results = self.filter_queryset(self.queryset.order_by("-created_at"))
        page_results = self.paginate_queryset(filter_results)
        user_serializer = self.get_serializer(instance=page_results,many=True)
        return Response(dict(message="success",details="User list retrieve successfully", data=user_serializer.data, total_count=filter_results.count()), status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """
        This Python function updates user details based on the provided request data, handling cases
        where the user ID or email already exists and returning appropriate responses.
        
        :param request: The `request` parameter in the `update` method is typically an object that
        contains information about the incoming HTTP request, such as the request method, headers, body,
        and query parameters. It is used to access and manipulate the data sent by the client to the
        server
        :return: The code snippet provided is a method for updating user details in a Django REST
        framework view.
        """
        try:
            user_id = self.kwargs['pk']
            if self.queryset.exclude(id=user_id).filter(email=request.data['email']).exists():
                return Response(dict(message="success",details="Given Email id already exists"), status=status.HTTP_409_CONFLICT)
            
            user_data = self.queryset.get(id=user_id)
            user_serializer = self.get_serializer(instance=user_data,data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(dict(message="success",details="User Update successfully", data=user_serializer.data), status=status.HTTP_201_CREATED)
            else:
                return Response(dict(message="Failed", details=user_serializer.errors), status=status.HTTP_502_BAD_GATEWAY)
        except UserDetails.DoesNotExist:
            return Response(dict(message="Failed", details="Given User id doesn't exists"), status=status.HTTP_502_BAD_GATEWAY)
            
        except Exception as e:
            return Response(dict(message="Failed", details=str(e)), status=status.HTTP_502_BAD_GATEWAY)
    
    def destroy(self, request, *args, **kwargs):
        """
        This Python function deletes a user record based on the provided user ID, handling exceptions
        for non-existent user IDs and other errors.
        
        :param request: The `request` parameter in the `destroy` method is an object that contains
        information about the incoming HTTP request, such as headers, method, body, and query
        parameters. It is typically used to extract data from the request, authenticate users, and
        perform actions based on the request type (GET,
        :return: The `destroy` method is returning a Response object with a message and details based on
        the outcome of the try-except block. If the UserDetails.DoesNotExist exception is raised, it
        returns a response with a message indicating failure and details stating that the given User id
        doesn't exist. If any other exception is raised, it returns a response with a message indicating
        failure and details containing the string representation of the exception
        """
        try:
            user_id = self.kwargs['pk']
            user_data = self.queryset.get(id=user_id)
            user_data.delete()
        except UserDetails.DoesNotExist:
            return Response(dict(message="Failed", details="Given User id doesn't exists"), status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response(dict(message="Failed", details=str(e)), status=status.HTTP_502_BAD_GATEWAY)
    
    def partial_update(self, request, *args, **kwargs):
        return Response(dict(message="Method 'patch' Not allowed"), status=status.HTTP_405_METHOD_NOT_ALLOWED)



class UserReferralView(GenericAPIView):
    authentication_classes = [UsersTokenAuthentication]
    filterset_class = UserDetailsListSearchFilter
    pagination_class = UserDetailsPagination
    serializer_class = UserDetailsSerializer
    
    def get(self, request, referral_code):
        """
        This function retrieves user details based on a referral code and returns the serialized data in
        paginated format.
        
        :param request: The `request` parameter in the `get` method represents the HTTP request that is
        sent to the server. It contains information such as the request method (GET, POST, PUT, DELETE,
        etc.), headers, user authentication details, and any data that is sent along with the request
        (such as
        :param referral_code: The `referral_code` parameter in the `get` method is used to filter the
        `UserDetails` objects based on the provided referral code. The method retrieves user data from
        the database where the `referral_code` matches the provided value
        :return: A Response object with a message "success" and user data serialized using the
        serializer, along with a status code of 202 (ACCEPTED).
        """
        
        user_data = UserDetails.objects.filter(referral_code=referral_code)
        filter_result = self.filter_queryset(user_data)
        page_result = self.paginate_queryset(filter_result)
        user_serializer= self.get_serializer(instance=page_result, many=True).data
        return Response(dict(message="success", data=user_serializer, total_count=filter_result.count()), status=status.HTTP_202_ACCEPTED)


class UserLoginView(GenericAPIView):
    serializer_class = LoginUserDetailsSerializer
    
    def post(self, request):
        try:
            data = request.data
            user_data = UserDetails.objects.filter(
                email=data["email"]
            )
            if user_data.exists() and data["password"] == user_data[0].password:
                temp_dict = {
                    "id": str(user_data[0].id),
                    "email": user_data[0].email,
                }
                token = users_encode_token(temp_dict)
                user_serializer = UserDetailsSerializer(
                    instance=user_data[0]
                )
                return Response(
                    dict(
                        message="login successfully",
                        token=token,
                        data=user_serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    dict(message="The provided email or password is incorrect."),
                    status=status.HTTP_502_BAD_GATEWAY,
                )
        except Exception as e:
            return Response(dict(message=str(e)), status=status.HTTP_502_BAD_GATEWAY)


class DevUserCreateView(GenericAPIView):
    filterset_class = UserDetailsListSearchFilter
    pagination_class = UserDetailsPagination
    serializer_class = UserDetailsSerializer
    
    def post(self, request):
        
        if UserDetails.objects.filter(email=request.data['email']).exists():
            return Response(dict(message="Failed",details="Given Email id already exists"), status=status.HTTP_409_CONFLICT)
        user_serializer = self.get_serializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(dict(message="success",details="User created successfully", data=user_serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(dict(message="Failed", details=user_serializer.errors), status=status.HTTP_502_BAD_GATEWAY)
        