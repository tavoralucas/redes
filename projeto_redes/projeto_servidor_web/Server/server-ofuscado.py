import s,os,m
H,P='127.0.0.1',8081
V='HTTP/1.1'
def a(p):
    x=os.path.abspath('private')
    y=os.path.abspath(p)
    return os.path.commonpath([x,y])==x
def b(p):
    f=os.listdir(p)
    f.sort()
    c="<html><head><title>Index of {0}</title></head><body><h1>Index of {0}</h1><hr><pre>".format(p)
    for i in f:
        l=os.path.join(p,i)
        if os.path.isdir(l):i+="/"
        c+='<a href="{0}">{1}</a>\n'.format(l,i)
    c+="</pre><hr></body></html>"
    return c
def e(c,s,m):
    x='<html><head><title>{}</title></head><body><h1>{}</h1><p>{}</p></body></html>'.format(s,s,m)
    h=['{} {}'.format(V,s),'Content-Type: text/html','Content-Length: {}'.format(len(x))]
    c.send('{}\r\n\r\n'.format('\r\n'.join(h) +'\r\n'+ x).encode())
def h(c):
    r=c.recv(1024).decode()
    l=r.split('\r\n')[0]
    d=l.split()
    if len(d)!=3:
        e(c,'400 Bad Request','Bad Request')
        return
    m,p,v=d
    print("Request Data: ",d)
    if v!='1.1':
        e(c,'505 Version Not Supported','A versão do HTTP utilizada não é suportada neste servidor')
    if m!='GET':
        e(c,'405 Method Not Allowed','Method Not Allowed')
        return
    if not os.path.exists(p):
        e(c,'404 Not Found','File not found')
        return
    i=None
    if a(p):
        e(c,'403 Forbidden','Forbidden')
        return
    if os.path.isdir(p):
        if os.path.isfile(os.path.join(p, "index.html")):
            p=f'{p}/index.html'
        elif os.path.isfile(os.path.join(p, "index.hml")):
            p=f'{p}/index.hml'
        else:
            i=b(p)
            t='text/html'
            r=f'HTTP/1.1 200 OK\r\nContent-Type: {t}\r\nContent-Length: {len(i)}\r\n{i}'.encode()
            c.send(r)
            return
    try:
        t,n=m.guess_type(p)
        x=t is not None and t.startswith('text/')
        f=open(p,'r' if x else 'rb')
        i=f.read()
        f.close()
        if t is None:
            t='application/octet-stream'
        r=f'HTTP/1.1 200 OK\r\nContent-Type: {t}\r\nContent-Length: {len(i)}\r\n{i}'.encode()
    except FileNotFoundError:
        e(c,'404 Not Found','Not Found')
        return
    c.send(r)
s=socket.socket(s.AF_INET,s.SOCK_STREAM)
s.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
s.bind((H,P))
s.listen(1)
print(f'Servidor WEB aguardando conexões em http://{H}:{P}...')
while True:
    c,a=s.accept()
    print('Client connected: {}'.format(a))
    h(c)
    c.close()
