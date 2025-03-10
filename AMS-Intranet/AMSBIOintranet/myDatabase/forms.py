from .models import ProductRecords, ProductRecordsTech
from django import forms


# Django class for generating model form for 'ProductRecords' table
class EditProductForm(forms.ModelForm):
    sell_price_rest_of_world_usd = forms.CharField(max_length=64, disabled=True, required=False)
    # owner = forms.CharField(max_length=64, disabled=True, required=False)
    purchase_nett_price = forms.CharField(max_length=64, disabled=True, required=False)
    business_unit_manager = forms.CharField(max_length=64, disabled=True, required=False)
    supplier = forms.CharField(max_length=64, disabled=True, required=False)
    bundle = forms.CharField(max_length=64, disabled=True, required=False)
    username = forms.CharField(max_length=64, disabled=False, required=True)
    europa_sell_price_gbp = forms.CharField(max_length=64, disabled=True, required=False)
    europa_sell_price_eur = forms.CharField(max_length=64, disabled=True, required=False)
    last_change_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), disabled=True, required=False)
    last_updated_user = forms.CharField(max_length=64, disabled=True, required=False)
    product_code = forms.CharField(max_length=64, disabled=True, required=False)
    supplier_product_code = forms.CharField(max_length=64, disabled=True, required=False)
    commodity_code = forms.CharField(max_length=64, required=False)
    price_calculation_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {'class': 'form-control', 'rows': '0', 'cols': '10'})
    class Meta:
        model = ProductRecords
        fields = ["username",
                  "product_code",
                  "supplier_product_code",
                  "delete_flag",
                  "website_flag",
                  "description",
                  "long_description",
                  "price_update_only",
                  "packsize",
                  "bundle",
                  "storage_conditions",
                  "shipping_temperature",
                  "category_1",
                  "category_2",                  
                  "research_area_1",
                #   "price_calculation_type",
                  "purchase_nett_price",
                  "supplier_list_price",
                  "sell_price_gbp",
                  "sell_price_eur",
                  "sell_price_chf",
                  "sell_price_usd",
                  "sell_price_rest_of_world_usd",
                  "europa_sell_price_gbp",
                  "europa_sell_price_eur",
                  "commodity_code",
                  "supplier",
                  "business_unit_manager",
                  "last_updated_user",
                  "last_change_date",
                  "special_shipping"]
                #   "research_area_2",
                #   "research_area_3",
                #   "research_area_4",
                #   "supplier_category_1",
                #   "supplier_category_2",
                #   "supplier_category_3",
                #   "supplier_lead_time",
                #   "owner",
                #   "ct_supplier_id",
                #   "listing_precedence",
                #   "new_product_flag",
                #   "previous_purchase_price",
                #   "price_change_flag",
                #   "price_change_percent",
                #   "is_in_odoo",]


# Django class for generating model form for 'ProductRecordsTech' table
class EditTechDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditTechDetailsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {'class': 'form-control', 'rows': '0', 'cols': '5'})

    class Meta:
        model = ProductRecordsTech
        fields = '__all__'