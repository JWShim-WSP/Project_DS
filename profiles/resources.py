from import_export import resources
from profiles.models import Profile
from django.contrib.auth.models import User
from import_export.fields import Field

class MemberResource(resources.ModelResource):
    staff = Field()

    class Meta:
        model = User
        # enumerate the fields to export
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'staff', 'created')
        export_order = fields

    # To change (dehydrate) the display from number('1 or 0') to text ('Ture or False')
    def dehydrate_staff(self, obj):
        if (obj.is_staff == True):
            return "Yes"
        else:
            return "No"
