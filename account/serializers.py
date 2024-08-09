from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this because we need confirm password field in our Registration Request
    password_confirmation = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError("Error at serializer.py.Password and Confirm Password doesn't match")
        print("Password and Confirm Password passed in serializer.userRegistrationSerializervalidate")
        return attrs

    def create(self, validated_data):
        # validated_data.pop('password_confirmation')  # poping password confirmation from validation so that it do not acquire password confirmation field in database
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password_confirmation = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        fields = ['password', 'password_confirmation']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        user = self.context.get('user')
        if password != password_confirmation:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            print('Password Reset Link', link)
            # Send Email
            body = 'Click Following Link to Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password_confirmation = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        fields = ['password', 'password_confirmation']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password_confirmation = attrs.get('password_confirmation')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password_confirmation:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


# from rest_framework import serializers
# from account.models import User
# from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from account.utils import Util

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     # We are writing this because we need confirm password field in our Registration Request
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'password', 'password2']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     # Validating Password and Confirm Password while Registration
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         if password != password2:
#             raise serializers.ValidationError("Password and Confirm Password doesn't match")
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop('password2')
#         return User.objects.create_user(**validated_data)

# class UserLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255)
    
#     class Meta:
#         model = User
#         fields = ['email', 'password']

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth']

# class UserChangePasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
#     password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    
#     class Meta:
#         fields = ['password', 'password2']

#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         user = self.context.get('user')
#         if password != password2:
#             raise serializers.ValidationError("Password and Confirm Password doesn't match")
#         user.set_password(password)
#         user.save()
#         return attrs

# class SendPasswordResetEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255)
    
#     class Meta:
#         fields = ['email']

#     def validate(self, attrs):
#         email = attrs.get('email')
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             print('Encoded UID', uid)
#             token = PasswordResetTokenGenerator().make_token(user)
#             print('Password Reset Token', token)
#             link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
#             print('Password Reset Link', link)
#             # Send Email
#             body = 'Click Following Link to Reset Your Password ' + link
#             data = {
#                 'subject': 'Reset Your Password',
#                 'body': body,
#                 'to_email': user.email
#             }
#             # Util.send_email(data)
#             return attrs
#         else:
#             raise serializers.ValidationError('You are not a Registered User')

# class UserPasswordResetSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
#     password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    
#     class Meta:
#         fields = ['password', 'password2']

#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             password2 = attrs.get('password2')
#             uid = self.context.get('uid')
#             token = self.context.get('token')
#             if password != password2:
#                 raise serializers.ValidationError("Password and Confirm Password doesn't match")
#             id = smart_str(urlsafe_base64_decode(uid))
#             user = User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise serializers.ValidationError('Token is not Valid or Expired')
#             user.set_password(password)
#             user.save()
#             return attrs
#         except DjangoUnicodeDecodeError as identifier:
#             PasswordResetTokenGenerator().check_token(user, token)
#             raise serializers.ValidationError('Token is not Valid or Expired')
