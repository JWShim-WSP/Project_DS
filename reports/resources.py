from import_export import resources
from reports.models import Report
from import_export.fields import Field

class ReportResource(resources.ModelResource):
    author = Field()
    class Meta:
        model = Report
        # enumerate the fields to export
        fields = ('id', 'name', 'author', 'remarks', 'created', 'updated')
        export_order = fields

    # To change (dehydrate) the display from number('1 or 0') to text ('Ture or False')
    def dehydrate_author(self, obj):
        return obj.author.user.username