from django.shortcuts import render, HttpResponse, redirect

from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
from django.db.models import Q
import django_excel as excel
from home.models import Excel
from home.gen_db import pubmed_gen,wos_gen,sco_gen
import csv

csv_f="a"
# Create your views here.
def index(request):
    data = Excel.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        Excel.objects.filter(
            Q(Title_icontains=q) | Q(authors_icontains=q)
            | Q(dbid_icontains=q))

    return render(request, 'index.html', {'data': data})


def search(request):
    global csv_f
    query = str(request.GET['query']).strip()
    cat = str(request.GET['cat']).strip()
   
    db_query=query
    if cat=="pubmed":
      print("Doing!!")
      pubmed_gen(request,db_query)
    if cat=="wos":
      print("Wos -- doing!!")
      wos_gen(request,db_query)
    if cat=="scopus":
      print("scopus--- doing")
      sco_gen(request,db_query)
    print(query)
    print("\n\n\n")

    allPosts = Excel.objects.filter()
    str_1=query.replace("and"," & ").replace("or"," | ").replace("{","").replace("}","")
    str_3=str_1.split()
    str_2=[]
    for i in str_3:
      a=i.replace(" ","")
      str_2.append(a)
    s=""
    for i in str_2:
        if i!="|":
          if i!="&":
            s+=str(i+" ").replace(i,f"Q(Title__icontains='{i}')")
        if i.strip()=="|":
          s+="|"
        if i.strip()=="&":
          s+="&"
    f_s=s.replace(") Q(",") | Q(")
    print(f_s)
    new_allposts = allPosts.filter(eval(str(f_s)))
    allPosts=new_allposts
    csv_f=allPosts
    params = {'allPosts': allPosts}
    return render(request, 'search.html', params)

def venue_csv(request):
    global csv_f
    print(request)
    lst = eval(str(request.GET)[12:-1])
    l=lst["ids"]

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment;filename="output2.csv"'
    writer = csv.writer(response)
    venues = Excel.objects.all()
    writer.writerow(['Title', 'Author', 'API_Id'])
    for i in csv_f:
        if i.dbid in l:
          writer.writerow([i.Title, i.authors, i.dbid])
    return response

def venue_all_csv(request):
    global csv_f
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment;filename="output2.csv"'
    writer = csv.writer(response)
    venues = Excel.objects.all()
    writer.writerow(['Title', 'Author', 'API_Id'])
    for i in csv_f:
      writer.writerow([i.Title, i.authors, i.dbid])
    return response