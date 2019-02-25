import estorage as stor

#attrs = dir(cmp)
#for attr in :
#    
#    
## Get List of Variables
#toSave = ['fluid','m_dot']
#    
#if isinstance(obj,stor.Compressor):
#    attrs=[]
#    for attr in attrs:
#        getattr(obj,attr)
#        


def getAttrs(obj):
    attrs = dir(obj)
    return attrs

def getVals(obj):
    attrs = dir(obj)
    vals= {}
    for attr in attrs: 
        if not attr[0]=='_':
            vals[attr] = getattr(obj,attr)
    return vals

cmp = stor.Compressor()
attrs = getAttrs(cmp)
vals = getVals(cmp)