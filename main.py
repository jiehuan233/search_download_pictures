import os
import re
import time
import hashlib
import requests
from bs4 import BeautifulSoup
def file_search(path,repat='.*'):
    folders,files=[],[]
    st=time.time()
    repat='^'+repat+'$'
    for record in os.walk(path):
        fop=record[0]
        folders.append(fop)
        for fip in record[2]:
            fip = os.path.abspath(os.path.join(fop,fip)).replace('\\','/')
            files.append(fip)
        files_match=[]
        for file in files:
            a=re.findall(repat,file.lower())
            if a:
                files_match+=a
        return files_match

def fastmd5(file_path,split_piece=256,get_front_bytes=8):
    size = os.path.getsize(file_path)
    block=size//split_piece
    h = hashlib.md5()

    if size<split_piece*get_front_bytes:
        with open(file_path,'rb') as f:
            h.update(f.read())
    else:
        with open(file_path,'rb') as f:
            index = 0
            for i in range(split_piece):
                f.seek(index)
                h.update(f.read(get_front_bytes))
                index+=block
    return h.hexdigest()

def find_duplicate_file(fp_arr):
    d={}
    for fp in fp_arr:
        size=os.path.getsize(fp)
        d[size]=d.get(size,[])+[fp]
    l=[]
    for k in d:
        if len(d[k])>1:
            l.append(d[k])
    ll=[]
    for f_arr in l:
        d={}
        for f in f_arr:
            fmd5=fastmd5(f)
            d[fmd5]=d.get(fmd5,[])+[f]
        for k in d:
            if len(d[k])>1:
                ll.append(d[k])
    for i in ll:
        a=1
        while a<=len(i)-1:

            os.remove(i[a])
            a+=1
    return ll

keywords=input("请输入关键词（英文）：")

res=requests.get('https://unsplash.com/s/photos/'+keywords)

res.encoding="utf-8"
soup=BeautifulSoup(res.text)
w=soup.find_all("img",itemprop="thumbnailUrl")

n=1
for i in w:

    print(i.attrs['src'])
    da=i.attrs['src']
    f=requests.get(da)
    if not os.path.isdir("picture"):
        os.mkdir("picture")
    with open(("picture"+(os.sep)+str(n)+".jpg"),"wb+") as pic:
        pic.write(f.content)
    n+=1
path='picture'
m_fp_arr=file_search(path,r'.*\.jpg')
m_du_arr=find_duplicate_file(m_fp_arr)