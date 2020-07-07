from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import sys

def createSearchableData(root):   
 
    '''
    Schema definition: title(name of file), path(as ID), content(indexed
    but not stored),textdata (stored text content)
    '''
    schema = Schema(title=TEXT(stored=True),path=ID(stored=True),\
              content=TEXT,textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
 
    # Creating a index writer to add document as per schema
    ix = create_in("indexdir",schema)
    writer = ix.writer()
 
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    for path in filepaths:
        fp = open(path,'r')
        #print(path)
        text = fp.read()
        writer.add_document(title=path.split("\\")[1], path=path,\
          content=text,textdata=text)
        fp.close()
    writer.commit()

root = "corpus"
createSearchableData(root)

ix = open_dir("indexdir")
 
# query_str is query string
query_str = sys.argv[1]

results=None
with ix.searcher() as searcher:
    results=searcher.search(QueryParser("content", schema=ix.schema).parse(query_str), limit=None)

print(results)
