import csv

import xlwt
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic.detail import DetailView
# CRUD
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import AddressForm, BookForm
from .models import Book

# from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# @csrf_exempt
def home(request): #http request
    # print(request.method)
    if request.method == "POST":
        data = request.POST
        # print(data)
        # print(data.getlist("cars")) # get for single value, getlist for multiple value
        bid = data.get("book_id")
        name = data.get("book_name")
        qty = data.get("book_qty")
        price = data.get("book_price")
        author = data.get("book_author")
        is_pub = data.get("book_is_publish") #yes no
        # print(name, qty, price, author, is_pub) # yes no
        if is_pub == "Yes":
            is_pub = True
        else:
            is_pub = False
        

        if not bid:
            Book.objects.create(name=name, qty=qty, price=price, author=author, is_published = is_pub)
        else:
            book_obj = Book.objects.get(id=bid)
            book_obj.name = name
            book_obj.qty = qty
            book_obj.price = price
            book_obj.author = author
            book_obj.is_published = is_pub
            book_obj.save()

        return redirect("home_page")
        # return HttpResponse("Success")
    elif request.method == "GET":
        # print(request.GET) #get query params
        # return render(request, "home.html", context={"all_books": Book.objects.all()})
        return render(request, "home.html", context={"person_name": "Saroja"})

def show_books(request):
    return render(request, "show_books.html", {"books": Book.objects.filter(is_active=True), "active":True})

def update_book(request, id):
    book_obj = Book.objects.get(id=id)
    # print(book_obj)
    return render(request, "home.html", context={"single_book": book_obj})

def delete_book(request, pk): # hard delete
    Book.objects.get(id=pk).delete()
    return redirect("all_active_books")


def soft_delete_book(request, pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = False
    book_obj.save()
    return redirect("all_active_books")

def show_inactive_books(request):
    return render(request, "show_books.html", {"books": Book.objects.filter(is_active=False), "inactive":True})

def restore_books(request, pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active =True
    book_obj.save()
    return redirect("home_page")

# 21/12/22

# from django.contrib.auth.forms import UserCreationForm

def book_form(request):
    form = BookForm()
    if request.method == "POST":
        print(request.POST)
        form = BookForm(data=request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse("Succesfully Registered!!!")

    return render(request, "book_form.html", {"form": BookForm()})

# simpleisbetterthancomplex

def sibtc(request):
    return render(request, "sibtc.html", {"form": AddressForm()})



def index(request):
    # print("in index function")
    book_list = Book.objects.all()
    page = request.GET.get('page', 1)
    # print(page)
    paginator = Paginator(book_list, 3)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    # print(books)
    return render(request, 'index.html', { 'books': books })


# from django.views import View  
# class NewView(View):  
#     def get(self, request):  
#         # View logic will place here  
#         return HttpResponse('get response')

#     def post(self, request):
#         return HttpResponse("post response")

#     def put(self, request): #update
#         return HttpResponse("put response")

#     def patch(self, request): #partial update
#         return HttpResponse("patch response")

#     def delete(self, request): #delete
#         return HttpResponse("delete response")


class BookCreate(CreateView):  
    model = Book  
    fields = '__all__'  
    success_url = "/cbv-create-book"


class BookRetrive(ListView):
    model = Book
    context_object_name = "all_books"
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    # queryset = Book.objects.filter(is_active=1)

    def get_queryset(self):
        print("in method")
        return Book.objects.filter(is_active=0)


class BookDetail(DetailView):
    model = Book



class BookUpdate(UpdateView):  
    model = Book  
    fields = '__all__'  
    success_url = "/cbv-create-book"


class BookDelete(DeleteView):  
    model = Book  
    fields = '__all__'  
    success_url = "/books"


# ASSIGNMENT - 09
# Assignement:- 9th -- 
# 1.book csv export
# 2.excel -- active books sheet- active books, inactive sheet-inactive books, 
# 3.raw queries - using objects.raw (select * from books;) -- csv me dalna
# 4.read text file and show its content on UI using view
# 5.download sample csv file
# 6.validations - duplicate book not allowed

# 1.book csv export
def create_csv(request):
    """
    creating simple csv file importing data from model and writing using writerow in csv format
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="create_csv.csv"'
    writer = csv.writer(response)
    writer.writerow(["name", "qty", "price", "author", "is_published", "is_active"])
    books = Book.objects.all().values_list("name", "qty", "price", "author", "is_published", "is_active")
    for book in books:
        writer.writerow(book)
    return response

# 2.excel -- active books sheet- active books, inactive sheet-inactive books, 
def create_excel_active_books(request):
    """
    here creating excel of active book using orm query is active true
    values list give the list of tuple data
    and downloading active books.
    wb.save is saving file
    wb.add_sheet giving the sheet name
    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Active_books.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Active_books')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Name", "Qty", "Price", "Author", "Is_published", "Is_active",]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Book.objects.filter(is_active=True).values_list("name", "qty", "price", "author", "is_published", "is_active")
    # return render(request, "show_books.html", {"books": Book.objects.filter(is_active=False), "inactive":True})
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response    


def create_excel_inactive_books(request):
    """
    here creating excel of inactive book using orm query is active false
    values list give the list of tuple data
    and downloading inactive books
    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Inactive_books.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Inactive_books')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Name", "Qty", "Price", "Author", "Is_published", "Is_active",]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Book.objects.filter(is_active=False).values_list("name", "qty", "price", "author", "is_published", "is_active")
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


# 3.raw queries - using objects.raw (select * from books;) -- csv me dalna
def create_csv_raw(request):
    """
    creating csv file using raw queries to insert data we have to pass single argument in
    writerow using list of column name, list is single argument
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="create_csv_raw.csv"'
    writer = csv.writer(response)
    writer.writerow(["name", "qty", "price", "author", "is_published", "is_active"])
    books = Book.objects.raw('select * from book;')
    # print(book.id)
    for book in books:
        # print(book.id)
        writer.writerow([ book.name, book.qty, book.price, book.author, book.is_published, book.is_active])
    return response


# 4.upload  file in database
def upload_csv(request):
    """
    uploading specific csv file in database 
    csv file data inserted into database using bulk create
    """
    file = request.FILES["csv_file"]
    # print(file)
    decoded_file = file.read().decode('utf-8').splitlines()
    # print(data)
    reader = csv.DictReader(decoded_file)
    # for i in reader:
    #     print(i)
    lst = []
    for element in reader:
        is_pub =element.get("is_published")
        if is_pub == "TRUE":
            is_pub = True
        else: 
            is_pub = False
        lst.append(Book(name=element.get("name"), qty=element.get("qty"), price=element.get("price"), author=element.get("author"), is_published =is_pub))
    # print(lst)
    Book.objects.bulk_create(lst)
    return HttpResponse("success")
    # ['name,qty,price,author,is_published', 'Book9,2,500,gnhn,TRUE', 'Book2,6,300,gkfkf,TRUE', 
    # 'Book4,5,544,klmn,FALSE', 'Book6,2,985,lkio,FALSE', 'Book7,9,236,gsd,FALSE', 'Book8,6,574,aikj,TRUE']


# 4.read text file and show its content on UI using view
def read_text(request):
    """
    reading text file and passing data in context for html 
    we have to create new html to pass text data
    render the html for read data
    """
    data_file = open(r'C:\Users\Shree\Desktop\B8\B8_Django\Library\media\sample2.txt', 'r')   
    data = data_file.readlines(1000)
    context = {'textdata': data}
    return render(request, 'text_read.html', context)
    
# 5.download sample csv file
def download_csv(request):
    """
    Create the HttpResponse object with the appropriate CSV header.
    here reading the csv file and writing data , then downloading the  sample file.
    writting multiple data in csv using the writerow multiple times 
    """
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="download_csv_sample.csv"'},
    )
    with open(r'C:\Users\Shree\Desktop\B8\B8_Django\Library\media\test_new.csv', mode ='r') as file:
        csvFile = csv.DictReader(file)
        writer = csv.writer(response)
        writer.writerow(["name", "qty", "price", "author", "is_published", "is_active"])
        for lines in csvFile:
            print(lines)
            writer.writerow([lines.get("name"), lines.get("qty"), lines.get("name"), lines.get("name"), lines.get("name"), lines.get("name")])
    
    # writer = csv.writer(response)
    # writer.writerow(['first_name', 'last_name', 'phone_number', 'country'])
    # writer.writerow(['Huzaif', 'Sayyed', '+919954465169', 'India'])
    # writer.writerow(['Adil', 'Shaikh', '+91545454169', 'India'])
    # writer.writerow(['Ahtesham', 'Shah', '+917554554169', 'India'])
    # return response
    return response


# 6.validations - duplicate book not allowed
def book_duplicate(request):
    """ 
    here duplicate book not allowed.
    duplicate book is detected then database me data insert karna nahi hai.
    databases and csv file compare book for duplicate book after bulk create book in databases.
    """
    # file = request.FILES["csv_file"]
    # decoded_file = file.read().decode('utf-8').splitlines()
    # reader = csv.DictReader(decoded_file)
    lst = []
    with open(r'C:\Users\Shree\Desktop\B8\B8_Django\Library\media\test.csv', mode ='r') as file:
        csvFile = csv.DictReader(file)
        for line in csvFile:
            # print(line)
            list_of_book_names = []
            books = Book.objects.all()
            # print(books)
            for book in books:
                # print(book.name)
                list_of_book_names.append(book.name)
            # print(list_of_book_names)
            name = line.get("name")
            # print(name)
            if name not in list_of_book_names:
                qty = line.get("qty")
                # print(qty)
                price = line.get("price")
                author = line.get("author")
                is_active = line.get("is_active")
                if is_active == "TRUE":
                    is_active = True
                else:
                    is_active = False
                is_pub =line.get("is_published")
                if is_pub == "TRUE":
                   is_pub = True
                else: 
                   is_pub = False
                lst.append(Book(name=name, qty=qty, price=price, author=author, is_published =is_pub, is_active=is_active))
            else:
                return HttpResponse("book is duplicate")
    Book.objects.bulk_create(lst)
    return HttpResponse("success")

import requests
GET_ALL_STUD_URL = "http://127.0.0.1:8000/api/get-all-students/"

def get_all_stud(request):
    response = requests.get(GET_ALL_STUD_URL)
    response = requests.request("GET", GET_ALL_STUD_URL)
    python_dict = response.json() # json to python dictionary
    return render(request, "student_data.html", {"data":python_dict})

