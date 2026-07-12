import urllib.request, ssl, json, gzip
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
B = 'https://servizi2.inps.it/servizi/osservatoristatistici/api'

def post(path, payload):
    req = urllib.request.Request(B+path, data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0','Accept':'application/json'})
    r = urllib.request.urlopen(req, context=ctx, timeout=300)
    raw = r.read()
    if raw[:2] == bytes([0x1f,0x8b]): raw = gzip.decompress(raw)
    return json.loads(raw.decode('utf-8'))

def build(oid, rows, cols, meas, filters=None):
    s = json.load(open('str_%s.json' % oid, encoding='utf-8'))
    d = s['definition']
    hier = lambda l: [h for h in d['Hierarchy'] if h['label']==l][0]
    fld  = lambda i: [f for f in d['fields'] if f['id']==i][0]
    p = {'id_osservatorio': oid, 'nome_osservatorio': s['nome_osservatorio'], 'language':'',
         'totalRow':True,'totalColumn':True,'subtotalRow':True,'subtotalColumn':True,
         'zip': True,
         'selections':{'rows':[],'cols':[],'measures':[],'filters':[]}}
    for n,l in enumerate(rows):
        h=hier(l)
        p['selections']['rows'].append({'id':h['Name'],'label':h['Name'],'order':n+1,
            'aggregate':fld(h['Component'][0]['id'])['aggregate'],'expand':'','hide':False})
    for n,l in enumerate(cols):
        h=hier(l)
        p['selections']['cols'].append({'id':h['Name'],'label':h['Name'],'order':n+1,
            'aggregate':fld(h['Component'][0]['id'])['aggregate'],'expand':'','hide':False})
    for mid,st in meas:
        f=fld(mid)
        p['selections']['measures'].append({'id':f['id'],'label':f['logicalName'],'order':f['cardinality'],'statistic':st})
    for fid,lbl,vals in (filters or []):
        p['selections']['filters'].append({'id':fid,'label':hier(lbl)['Name'],'values':vals})
    return p

def run(oid, rows, cols, meas, filters=None):
    return post('/getDatiOsservatorio/', build(oid, rows, cols, meas, filters))

def flatten(r):
    """yield (rowlabel, collabel, measure_label, value)"""
    out=[]
    for rv in r['values']:
        rlab = rv.get('description') or rv.get('value')
        for c in rv.get('columns') or []:
            for cv in c.get('values') or []:
                clab = cv.get('value')
                for m in cv.get('measures') or []:
                    out.append((rlab, clab, m['label'], m['value']))
    return out
