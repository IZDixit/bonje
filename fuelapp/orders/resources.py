from import_export import resources
from .models import SalesRecord

class SalesRecordResource(resources.ModelResource):
    class Meta:
        model = SalesRecord
        fields = ('id', 'Type', 'Date', 'Num', 'Name', 'Memo', 'Item', 'Qty', 'Sales_Price', 'Amount', 'Balance')