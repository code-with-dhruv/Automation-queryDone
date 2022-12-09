from django.shortcuts import render, HttpResponse, redirect
import sqlite3
from django.db.models import Q
import django_excel as excel
from home.models import Excel
import csv
from pymed import PubMed
import json
import time
import pandas as pd
import woslite_client
from woslite_client.rest import ApiException
from pprint import pprint
def pubmed_gen(request,db_query):
  pubmed = PubMed(tool="PubMedSearcher", email="daspranab239@gmail.com")
  search_term =db_query
  results = pubmed.query(search_term, max_results=130)
  articleList = []
  articleInfo = []
  def get_data(article, name):
      return getattr(article, 'name', 'N/A')
  for article in results:
    pubmedId = article.pubmed_id.partition('\n')[0]
    a=article.authors
    q=""
    for i in a:
      q+=","+str(i["firstname"])+" " +str(i["lastname"])
    p="PUB"+str(pubmedId)
    articleInfo.append([p,article.title,q[1:]])
  conn = sqlite3.connect("Hello/sql.db")
  cur = conn.cursor()
  try:
    sql = "DROP TABLE home_excel"
    cur.execute(sql)

  except:
    pass
  sql = """
  CREATE TABLE home_excel (
    id TEXT,
    Title TEXT,
    authors TEXT,
    dbid TEXT
    )"""
  cur.execute(sql)
  print("Database has been created")
  conn.commit()
  conn.close()
  conn = sqlite3.connect("Hello/sql.db")
  cur = conn.cursor()
  ctr=0
  for i in articleInfo:
    
    cur.execute("INSERT INTO home_excel VALUES (?,?,?,?)",(ctr,i[1],i[2],i[0]))
    conn.commit()
    ctr+=1
  conn.close()
  print(ctr)
  return render(request, 'index.html')
def wos_gen(request,db_query):
  configuration = woslite_client.Configuration()
  configuration.api_key['X-ApiKey'] = 'e9bc939b6ec9edb8c7cb88f03da101f88bdb4942'
  integration_api_instance = woslite_client.IntegrationApi(
      woslite_client.ApiClient(configuration))
  search_api_instance = woslite_client.SearchApi(
      woslite_client.ApiClient(configuration))
  database_id = 'WOS'
  usr_query = 'TS=({})'.format(db_query) or 'AU=({})'.format(db_query)  #yo 
  count = 100
  first_record = 1
  lang = 'en'
  sort_field = 'PY+D'
  articleInfo=[]
  api_response = search_api_instance.root_get(database_id, usr_query, count, first_record, lang=lang,sort_field=sort_field)
  output = []
  for i in range(1, 100):
    title = api_response.data[i].title.title[0]
    for j in range(1, len(api_response.data[i].author.authors)):
        author = api_response.data[i].author.authors[j]
    ut = api_response.data[i].ut
    try:
      line = [ut,title,author]
    except:
      line =["Unavailable","Unavailable","Unavailable"]
    articleInfo.append(line) 
  conn = sqlite3.connect("Hello/sql.db")
  cur = conn.cursor()
  try:
    sql = "DROP TABLE home_excel"
    cur.execute(sql)

  except:
    pass
  sql = """
  CREATE TABLE home_excel (
    id TEXT,
    Title TEXT,
    authors TEXT,
    dbid TEXT
    )"""
  cur.execute(sql)
  print("Database has been created")
  conn.commit()
  conn.close()
  conn = sqlite3.connect("Hello/sql.db")
  cur = conn.cursor()
  ctr=0
  for i in articleInfo:
    cur.execute("INSERT INTO home_excel VALUES (?,?,?,?)",(ctr,i[1],i[2],i[0]))
    conn.commit()
    ctr+=1
  conn.close()
  print(ctr)
  return render(request, 'index.html')

def sco_gen(request,db_query):

  key = '14d2fafc299086f759ee409c6fa04800'
  import requests
  null=None
  true=True
  false=False
  headers = {'Accept': 'application/json',}
  response = requests.get(
      'https://api.elsevier.com/content/search/scopus?query={}&apiKey=14d2fafc299086f759ee409c6fa04800'.format(db_query),
      headers=headers,
  )
  articleInfo=[]
  print(response)
  pp=str(response.content).replace("\\","a").replace("\\","a").replace("@","a").replace("$","a").replace("/","a")
  p=eval(pp[2:-1])
  print(p)
  q=((p["search-results"]["entry"]))
  for i in q:
    a=(i["dc:title"])
    b=(i["dc:identifier"])
    c=(i["dc:creator"])
    articleInfo.append([b,a,c])
  conn = sqlite3.connect("Hello/sql.db")
  cur = conn.cursor()
  try:
    sql = "DROP TABLE home_excel"
    cur.execute(sql)

  except:
    pass
  sql = """
  CREATE TABLE home_excel (
    id TEXT,
    Title TEXT,
    authors TEXT,
    dbid TEXT
    )"""
  cur.execute(sql)
  print("Database has been created")
  conn.commit()
  conn.close()
  conn = sqlite3.connect("Hello/sql.db")
  cur = conn.cursor()
  ctr=0
  for i in articleInfo:
    cur.execute("INSERT INTO home_excel VALUES (?,?,?,?)",(ctr,i[1],i[2],i[0]))
    conn.commit()
    ctr+=1
  conn.close()
  print(ctr)
  return render(request, 'index.html')

