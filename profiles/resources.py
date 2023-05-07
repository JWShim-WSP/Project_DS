from import_export import resources
from profiles.models import Profile
from import_export.fields import Field

class MemberResource(resources.ModelResource):
    username = Field()
    first_name = Field()
    last_name = Field()
    staff = Field()
    email = Field()

    class Meta:
        model = Profile
        # enumerate the fields to export
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'staff', 'created')
        export_order = fields

    # To change (dehydrate) the display from number('1 or 0') to text ('Ture or False')
    def dehydrate_staff(self, obj):
        if (obj.user.is_staff == True):
            return "Yes"
        else:
            return "No"

    def dehydrate_username(self, obj):
        return obj.user.username
    
    def dehydrate_first_name(self, obj):
        return obj.user.first_name
    
    def dehydrate_last_name(self, obj):
        return obj.user.last_name
    
    def dehydrate_email(self, obj):
        return obj.user.email