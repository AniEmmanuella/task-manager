import json,sys,os
from datetime import datetime

f="tasks.json"

def load():
    if os.path.exists(f):
        return json.load(open(f))
    else:
        return []

def save(t):
    json.dump(t,open(f,"w"))

def add(title,due):
    t=load()
    id=len(t)+1
    t.append({"id":id,"title":title,"due":due,"done":False})
    save(t)
    print("added",id)

def done(id):
    t=load()
    for x in t:
        if x["id"]==int(id):
            x["done"]=True
    save(t)

def ls(filter=None):
    t=load()
    for x in t:
        if filter=="done" and not x["done"]: continue
        if filter=="pending" and x["done"]: continue
        print(x["id"],x["title"],x["due"],"[x]" if x["done"] else "[ ]")

if __name__=="__main__":
    a=sys.argv
    if a[1]=="add": add(a[2],a[3])
    elif a[1]=="done": done(a[2])
    elif a[1]=="list":
        if len(a)>2: ls(a[2])
        else: ls()
    else: print("bad command")