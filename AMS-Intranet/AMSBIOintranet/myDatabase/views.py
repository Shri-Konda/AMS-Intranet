import json, os
import getpass
from datetime import datetime
from operator import itemgetter

from .forms import EditProductForm, EditTechDetailsForm
from .tables import (CurrencyTable, ProductRecordsTable)
from .models import (MasterCurrencies, ProductRecords, ProductRecordsTech,
                     NwCategoryLowestNodes, DataOwners, Currencies, PriceCalculator)

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.paginators import LazyPaginator

from .utils import *
from .smlrProdsUtils import *


def index(request):
    return redirect('/')


def addNewSupplier(request):
    """ Main function for rendering the Add new Supplier page! """
    if request.method == "POST" and len(request.POST['comp_name']) > 0:
        name = request.POST['comp_name']
        code = request.POST['acc_code'].upper()
        curr = request.POST['curr_code']
        if curr == 'USD':
            cur_id = 2
        else:
            cur_id = Currencies.objects.get(descriptive=curr).currencyid
        DataOwners.objects.create(
            currencyid=cur_id,
            owner=name,
            supplierpurchasecurrency=curr,
            dimmensionssuppliercode=code
        )
        context = {'c_name': name, 'c_code': code,
                   'cur': curr, 'msg': 'Supplier successfully added!'}
        return JsonResponse(context)
    else:
        return render(request, 'newsupplier.html')


def search(request):
    """ Function to control and render the search page!"""
    product_codes_with_forward_slash = ["7001-SS0601/100", "7001-SS0604/100", "7001-SS0724/100", "7001-SS0740/100", "7001-SS0741/100",
                                        "7001-SS0742/100", "7001-SS0743/100", "7001-SS0745/100", "7001-SS0794/100", "7001-SS0854/100",
                                        "AC-AML-007/1012", "AC-AML-010/0712", "AC-AML-012/0912", "AC-AML-014/1212", "AC-ANL-007/1012",
                                        "AML-010/0712-2E7", "AML-012/0912-1E7", "AML-012/0912-5E6", "ANL-007/1012-5E6", "IK-NSX007-12/1670"]
    # The list defined above leads to url error when searched from the 'Search page'. They can be accessed individually from Edit Single Product page.
    obj = ProductRecordsTable(ProductRecords.objects.all()[8:])
    RequestConfig(request, paginate={
                  "paginator_class": LazyPaginator, "per_page": 10}).configure(obj)
    obj_deleted_items = ProductRecordsTable(ProductRecords.objects.all()[8:])
    RequestConfig(request, paginate={
                  "paginator_class": LazyPaginator, "per_page": 10}).configure(obj)
    msg = True
    if request.method == "POST":
        code = request.POST['Prod']
        desc = request.POST['Desc']
        if len(code) == 0 and len(desc) == 0:
            msg = False
            obj = "*Please enter a search term!"
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        elif len(code) == 0 and len(desc) > 0:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                description__icontains=desc).filter(delete_flag=0).exclude(pk__in=product_codes_with_forward_slash)[:100])
            obj_deleted_items = ProductRecordsTable(ProductRecords.objects.filter(
                description__icontains=desc).filter(delete_flag=1).exclude(pk__in=product_codes_with_forward_slash)[:100])
            return render(request, 'search.html', {'obj': obj, 'obj_deleted_items': obj_deleted_items, 'msg': msg})
        elif len(desc) == 0 and len(code) > 0:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(Q(product_code__icontains=code) | Q(supplier_product_code__icontains=code)
                                                                    ).filter(delete_flag=0).exclude(pk__in=product_codes_with_forward_slash)[:100])
            obj_deleted_items = ProductRecordsTable(ProductRecords.objects.filter(Q(product_code__icontains=code) | Q(supplier_product_code__icontains=code)
                                                                    ).filter(delete_flag=1).exclude(pk__in=product_codes_with_forward_slash)[:100])
            return render(request, 'search.html', {'obj': obj, 'obj_deleted_items': obj_deleted_items, 'msg': msg})
        else:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code).filter(description__icontains=desc).filter(delete_flag=0).exclude(pk__in=product_codes_with_forward_slash)[:100])
            obj_deleted_items = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code).filter(description__icontains=desc).filter(delete_flag=1).exclude(pk__in=product_codes_with_forward_slash)[:100])
            return render(request, 'search.html', {'obj': obj, 'obj_deleted_items': obj_deleted_items, 'msg': msg})
    else:
        return render(request, 'search.html', {'obj': obj, 'obj_deleted_items': obj_deleted_items, 'msg': msg})


def currencyValue(request):
    """ Function to control and render the Current Currency page! """
    obj = CurrencyTable(MasterCurrencies.objects.exclude(exchange_rate=1))
    RequestConfig(request).configure(obj)
    export_format = request.GET.get("_export", None)
    now = datetime.today().strftime("%b-%d-%Y")
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, obj)
        return exporter.response("Currency_{}.{}".format(now, export_format))
    return render(request, 'currencyval.html', {'obj': obj})


def FormSubmit(request):
    """ Helper function for submitting a form! | Ajax Call """
    json_data = json.loads(request.POST['data'])
    form_data = {}
    for ele in json_data:
        temp = list(ele.values())
        form_data[temp[0]] = temp[1]
    print("✅ Received form data:", form_data)  # Debugging
    form_data.pop('csrfmiddlewaretoken')
    if 'supplier_product_code' in form_data.keys():
        getpass.getuser().upper()
        form_data['last_updated_user'] = form_data['username'].upper()       
        form_data['last_change_date'] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        Product = ProductRecords.objects.get(pk=form_data['product_code'])
        ProdForm = EditProductForm(form_data, instance=Product)
        if ProdForm.is_valid():
            ProdForm.save()
            return JsonResponse({"msg": "Form Submitted!"})
        else:
            return JsonResponse({"msg": ProdForm.errors})
    else:
        TechRecord = ProductRecordsTech.objects.get(
            pk=form_data['product_code'])
        TechForm = EditTechDetailsForm(form_data, instance=TechRecord)
        if TechForm.is_valid():
            TechForm.save()
            return JsonResponse({"msg": "Form Submitted!"})
        else:
            return JsonResponse({"msg": TechForm.errors})


def editSingleProduct(request, pk):
    """ Main function for rendering the Edit Product page! """
    flag = True
    nocategory = False
    europa_prices_gbp = None
    europa_prices_eur = None
    try:
            europa_prices = ProductRecords.get_europa_selling_prices(pk)
            europa_prices_gbp = europa_prices['sell_price_gbp']
            europa_prices_eur = europa_prices['sell_price_eur']
    except Exception as e:
            print(e)
    

    if request.method == "POST" and 'btnSubmitCode' in request.POST:
        code = request.POST["ProdCode"]       
        try:            
            # Case the product was deleted
            if ProductRecords.objects.get(pk=code).delete_flag == 1:
                flag = True
                return render(request, 'editsingleprod.html', {'msg': "This product was deleted", 'flag': flag})
            # Case where no categories are defined.
            if ProductRecords.objects.get(pk=code).category_1 == 0:
                ProdForm = editProductRecords(code, europa_prices_gbp, europa_prices_eur)
                noTechCategory = "No Categories defined!"
                nocategory = True
                context = {'ProdForm': ProdForm,
                           'NoTechCategory': noTechCategory, 'nocategory': nocategory}
                return render(request, 'editsingleprod.html', context)
            else:
                cat = loadCategory(code)  # generating level 1 category
                attributes = ['id_product_code'] + \
                    ['id_' + ele for ele in list(cat[0].values())[0]]
                ProdForm = editProductRecords(code, europa_prices_gbp, europa_prices_eur)
                TechForm = editTechDetails(code)
                 #  Split TechForm fields into two halves
                tech_fields = list(TechForm)
                mid_index = len(tech_fields) // 2
                TechForm_col1 = tech_fields[:mid_index]  # First half
                TechForm_col2 = tech_fields[mid_index:]  # Second half
                flag = False
                TwoCategories = True
                if len(cat) > 1:  # check if 2 categories exists
                    attributes2 = [
                        'id_' + ele for ele in list(cat[1].values())[0]]
                    merged_attrs = attributes + \
                        list(set(attributes2) - set(attributes))
                    context = {'ProdForm': ProdForm, 'TechForm_col1': TechForm_col1,  'TechForm_col2': TechForm_col2, 'flag': flag, 'cat1': list(cat[0].keys())[0],
                               'cat2': list(cat[1].keys())[0], 'catflag': TwoCategories, 'attrs': merged_attrs}
                else:
                    TwoCategories = False
                    context = {'ProdForm': ProdForm, 'TechForm_col1': TechForm_col1,  'TechForm_col2': TechForm_col2, 'flag': flag, 'cat1': list(cat[0].keys())[0],
                               'catflag': TwoCategories, 'attrs': attributes}
                return render(request, 'editsingleprod.html', context)
        except:
            flag = True
            return render(request, 'editsingleprod.html', {'msg': "Enter a valid product code", 'flag': flag})
    else:
        
        try:
            # Case where no categories are defined.
            if ProductRecords.objects.get(pk=pk).category_1 == 0:
                ProdForm = editProductRecords(pk, europa_prices_gbp, europa_prices_eur)
                noTechCategory = "No Categories defined!"
                nocategory = True
                context = {'ProdForm': ProdForm,
                           'NoTechCategory': noTechCategory, 'nocategory': nocategory}
                return render(request, 'editsingleprod.html', context)
            else:
                cat = None
                ProdForm = None
                TechForm = None
                flag = None
                TwoCategories = None
                try:
                    cat = loadCategory(pk)  # generating level 1 category
                    attributes = ['id_product_code'] + \
                        ['id_' + ele for ele in list(cat[0].values())[0]]
                    ProdForm = editProductRecords(pk, europa_prices_gbp, europa_prices_eur)
                    TechForm = editTechDetails(pk)
                    tech_fields = list(TechForm)
                    mid_index = len(tech_fields) // 2
                    TechForm_col1 = tech_fields[:mid_index]
                    TechForm_col2 = tech_fields[mid_index:]
                    flag = False
                    TwoCategories = True
                except Exception as e:
                    print(e)
                    #Case the product is not in the produc_records_tech table
                    cat = loadCategory(pk)  # generating level 1 category
                    attributes = ['id_product_code'] + \
                        ['id_' + ele for ele in list(cat[0].values())[0]]
                    ProdForm = editProductRecords(pk, europa_prices_gbp, europa_prices_eur)
                    flag = False
                    TwoCategories = True
                if len(cat) > 1:  # check if 2 categories exists 
                    attributes2 = [
                        'id_' + ele for ele in list(cat[1].values())[0]]
                    merged_attrs = attributes + \
                        list(set(attributes2) - set(attributes))
                    context = {'ProdForm': ProdForm, 'TechForm_col1': TechForm_col1,  'TechForm_col2': TechForm_col2, 'flag': flag, 'cat1': list(cat[0].keys())[0],
                               'cat2': list(cat[1].keys())[0], 'catflag': TwoCategories, 'attrs': merged_attrs}
                else:
                    TwoCategories = False
                    context = {'ProdForm': ProdForm, 'TechForm_col1': TechForm_col1,  'TechForm_col2': TechForm_col2, 'flag': flag, 'cat1': list(cat[0].keys())[0],
                               'catflag': TwoCategories, 'attrs': attributes}
                
                
                return render(request, 'editsingleprod.html', context)
        except Exception as e:
            flag = True
            return render(request, 'editsingleprod.html', {'msg': "Enter a valid product code", 'flag': flag})


def similarProducts(request, pk="3011-100"):
    """ Main Function for rendering the Similar Product page.

    By default the page will render similar products to 3011-100.
    This is done in order to connect both the POST and click request on search page.

    arguments:  request - Default Object for accepting the Http request made
                pk - The product for which similar products are to be fetched, by default it is "3011-100"
    """
    if request.method == "POST":
        prod_code = request.POST['prod_code']
        try:
            category = list(loadCategory(prod_code)[0].keys())[0]
            return categoryWiseProductSorting(category, prod_code, request)
        except NwCategoryLowestNodes.DoesNotExist:
            return setGeneralContext(request=request, msg='Categories do not exists.')
        except (ProductRecords.DoesNotExist, ProductRecordsTech.DoesNotExist):
            return setGeneralContext(request=request, msg='Product does not exist, Enter valid Product Code.')

    else:
        try:
            category = list(loadCategory(pk)[0].keys())[0]
            return categoryWiseProductSorting(category, pk, request)
        except NwCategoryLowestNodes.DoesNotExist:
            return setGeneralContext(request=request, msg='Categories do not exist!')


def selling_prices(request):
    sell_prices = []
    supplier_id = None
    purchase_nett_price = 0
    error_message = None
    owners_data = DataOwners.get_owners_ids_and_currency()
    sorted_owners_data = sorted(owners_data, key=itemgetter('owner'))

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        purchase_nett_price = request.POST.get('purchase_nett_price')

        try:
            purchase_nett_price = float(purchase_nett_price)
            sell_prices, error_message = PriceCalculator.calculate_selling_prices(
                purchase_nett_price, int(supplier_id)
            )
        except ValueError:
            error_message = "Invalid purchase price or supplier ID."

    return render(request, 'selling_prices.html', {
        'supplier_id': supplier_id,
        'purchase_nett_price': purchase_nett_price,
        'sell_prices': sell_prices,
        'owners_data': sorted_owners_data,
        'error_message': error_message
    })