import matplotlib.pyplot as plt
import base64
from io import BytesIO
from .models import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
import pandas as pd
import random as r
import io
from PIL import Image

class NoneException(Exception):
    def _init_(self,request,message,file):
        self.message = message
        return render(request,file,{"msg":self.message})

def decodeDesignImage(data):
    # try:
    data1 = base64.b64encode(data)
    data1 = data1.decode('UTF-8')
    buf = io.BytesIO(data)
    img = Image.open(buf)
    return img
    # except:
    #     return None

def get_graph(u_name):
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()

    img = decodeDesignImage(image_png)
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    token="img1"
    e = ImageModel(image_field = InMemoryUploadedFile(img_io, field_name=None, name=token+".png", content_type='image/png', size=img_io.tell, charset=None))
    e.save()
    
    f = AllImageModel(uname=u_name, image_field = InMemoryUploadedFile(img_io, field_name=None, name=token+".png", content_type='image/png', size=img_io.tell, charset=None))

    f.save()

    graph = base64.b64encode(image_png)

    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y,a,b,c,d,u_name):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,5))
    plt.title(c)
    plt.plot(x,y,d)
    plt.xticks(rotation=45)
    plt.xlabel(a)
    plt.ylabel(b)
    plt.tight_layout()
    graph = get_graph(u_name)
    return graph

def bar_plot(x,y,z,a,b,c,u_name):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,5))
    plt.title(c)
    plt.bar(x,y,width=0.4,color=z)
    plt.xticks(rotation=45)
    plt.xlabel(a)
    plt.ylabel(b)
    plt.tight_layout()
    graph = get_graph(u_name)
    return graph

def pie_plot(x,y,z,a,b,u_name):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,5))
    plt.title(a)
    plt.pie(y, labels=x, colors=z, startangle=b)
    plt.legend()
    plt.tight_layout()
    graph = get_graph(u_name)
    return graph

#Random Chart Generator Code
def rand_line(u_name):
    plt.switch_backend('AGG')
    plt.tight_layout()
    plt.grid(True)
    plt.figure(figsize=(8,5))
    x = []
    for _ in range(1,16):
        _ = r.randint(1,100)
        x.append(_)
    plt.plot(x)
    graph = get_graph(u_name)
    return graph

def rand_bar(u_name):
    plt.grid(True)
    plt.switch_backend('AGG')
    plt.tight_layout()
    plt.figure(figsize=(8,5))
    x = list(range(1, 16))
    height = [r.randint(1, 100) for _ in range(15)]
    plt.bar(x, height)
    graph = get_graph(u_name)
    return graph

def rand_barh(u_name):
    plt.grid(True)
    plt.switch_backend('AGG')
    plt.tight_layout()
    plt.figure(figsize=(8,5))
    y = list(range(1, 16))
    width = [r.randint(1, 100) for _ in range(15)]
    plt.barh(y, width)
    graph = get_graph(u_name)
    return graph

def rand_pie(lbl,u_name):
    plt.grid(True)
    plt.switch_backend('AGG')
    plt.tight_layout()
    plt.figure(figsize=(8,5))
    x = []
    for _ in range(r.randint(5,15)): #random number of sections in pie chart from 5-15
        _ = r.randint(1,100)
        x.append(_)
    plt.pie(x,labels = lbl, autopct = "%1.1f%%")
    graph = get_graph(u_name)
    return graph

#CSV files to chart
def csvgraph(request,data,u_name):
    if (request.method == "POST"):
        cols = pd.Series((request.POST.get("cols").strip()).split())
        stuff = pd.DataFrame(data[cols[1:]],index = data[cols[0]])

        plt.grid(True)
        plt.switch_backend('AGG')
        plt.tight_layout()
        plt.figure(figsize=(8,6))
        plt.xlabel(cols[0])
        plt.ylabel(cols[1])

        if (request.POST.get("chart_type2")):
            chart_type = request.POST.get("chart_type2")
            if chart_type == "none":
                raise NoneException(request,"No option chosen to plot!","csv.html")
            elif chart_type == "line":
                plt.plot(stuff)
                plt.legend(cols[1:],loc = "upper right")
                output = get_graph(u_name)
            elif chart_type == "scatter":
                for _ in stuff.columns:
                    plt.scatter(stuff.index,stuff[_])
                plt.legend(cols[1:],loc = "upper right")
                output = get_graph(u_name)
    return output