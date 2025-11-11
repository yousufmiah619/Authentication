from rest_framework import serializers
from authentication.models import User 


class RegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta :
        model=User
        fields=["email","name","tc","password","password2"]
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self ,attrs):
        password=attrs.get("password") 
        password2=attrs.get("password2")
        if password != password2 :
            raise serializers.ValidationError("password and confourm password doesn't macth")
        return attrs
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'})
    class Meta :
        model = User
        fields=["email","password"]
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id', 'email', 'name', 'tc']  
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password=serializers.CharField(max_length=255,style={'input_type':"password"},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':"password"},write_only=True)
    def validate(self,attrs):
        old_password=attrs.get("old_password")
        password=attrs.get("password")
        password2=attrs.get("password2")
        user=self.context.get("user")
        if not user.check_password(old_password):
            raise serializers.ValidationError("old_password is not correct")
        if password != password2 :
            raise serializers.ValidationError("password and confourm password doesn't macth")
        if password != password2:
            raise serializers.ValidationError({
                "password": ["New password and confirm password don't match"]
            })
        return attrs
    def save(self):
        user=self.context.get('user')
        password=self.validated_data['password']
        user.set_password(password)
        user.save()