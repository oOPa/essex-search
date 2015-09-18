Python Code
''''' 
Requires python requests: https://github.com/kennethreitz/requests 
Requires BeautifulSoup4: http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/ 
Requires PyPDF2: https://github.com/mstamy2/PyPDF2 
 
'''  
  
import requests  
import getpass  
  
from requests.auth import HTTPBasicAuth  
from html.parser import HTMLParser  
from bs4 import BeautifulSoup  
from PyPDF2.pdf import PdfFileReader  
  
def cook(url):  
    x = requests.head(url,auth=HTTPBasicAuth(username,password))  
    if x.status_code == 401 :  
        print("Invalid password")  
        return  
    if(x.headers['content-type'].startswith("text/html")):  
        x = requests.get(url,auth=HTTPBasicAuth(username,password))  
        soup = BeautifulSoup(x.text)  
        for link in soup.find_all('a', href=True):  
            z = link['href']  
            if not (z.startswith("http") or z.startswith("ftp") or z.startswith("#")):  
                current_link = ""  
                if(z.startswith("../")):  
                    current_link = "/".join(x.url.split("/")[:-2]) + z[2:]                      
                elif (z.startswith("./")):                      
                    current_link = "/".join(x.url.split("/")[:-1]) + z[1:];  
                else :  
                    current_link = "/".join(x.url.split("/")[:-1]) + "/"+ z;  
  
                links[x.url] = True;  
                if not (current_link in links):  
                    cook(current_link);  
                links [current_link] = True  
  
              
    else :  
        resources_list.append(x.url);  
        content_type.append(x.headers['content-type']);  
        pass  
      
def searchPDF(filename,search_term):  
    search_term = search_term.lower()  
    pages = []  
    pdf = PdfFileReader(open(filename, "rb"))  
  
    for i in range(0, pdf.getNumPages()):  
        content = pdf.getPage(i).extractText().lower()  
        if(search_term in content):  
            pages.append(i + 1)  
    return pages;  
  
def searchTXT(filename,search_term):  
    search_term = search_term.lower()  
    lines = []  
    line = 1  
    file = open(filename, "r")  
    for f in file:  
        if search_term in f.lower():  
            lines.append(line);  
        line +=1          
    return lines;  
  
def search():  
    print("Searching...");  
    for i in range(0, len(content_type)):  
        if(content_type[i] ==  "application/pdf"):  
            url = resources_list[i]  
            local_filename = "/".join(url.split("/")[-1:])  
            file = open(local_filename, 'wb');  
            x = requests.get(url,auth=HTTPBasicAuth(username,password),stream=True)  
            file.write(x.content)  
            l = searchPDF(local_filename,search_term);  
            if(len(l) > 0):  
                print("Found keyword \"",search_term,"\" on ",url," on pages ",l,sep="")  
            pass  
        elif(content_type[i] == "text/plain"):  
            pass  
  
modules = input("Enter the name of the module(s) you want to be included in your search separated by spaces: ").split()  
search_term = input("Please enter your search terms: ");  
  
username = input("Please enter your essex username: ")  
username = username + "@essex.ac.uk"  
links = {}  
resources_list = []  
content_type = []  
password = getpass.getpass();  
  
for module in modules:  
    dept = module[:2]  
    url = "http://orb.essex.ac.uk/" + dept + '/' + module  
    print("Scraping", module,"from orb")  
    cook(url)  
    search()  
    links = {}  
    resources_list = []  
    content_type = [] 
