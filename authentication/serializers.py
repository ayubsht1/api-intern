from authentication.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator


REQUIRED = " is required."
TAKEN = " already taken."


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, error_messages={"required": "Email is required."})
    password = serializers.CharField(required=True, error_messages={"required": "Password is required."})
    

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, error_messages={"required": "Confirm Password is required."})
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "password", "confirm_password"]
        
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Email" + TAKEN
                    )
                ],
                "required":True,
                "error_messages": {"required": "Email" + REQUIRED}
            },
            "phone": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Mobile number" + TAKEN
                    )
                ],
                "error_messages": {"required": "Mobile number" + REQUIRED}                
            },
            "first_name": {
                "error_messages": {"required": "First Name" + REQUIRED}
            },
            "last_name": {
                "error_messages": {"required": "Last Name" + REQUIRED}
            },
            "password": {
                "error_messages": {"required": "Password" + REQUIRED}
            }
        }
        
    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError({"password": "Password not valid."})
        return super().validate(data)