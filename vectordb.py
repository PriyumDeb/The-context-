import chromadb as cr
import pdf_semantic as ps
chroma_place= cr.PersistentClient(path='./loacal_chroma_db')
croma_storage=chroma_place.get_or_create_collection(name="pdf_space")
document=[]
meta_data=[]
id=[]
for i in ps.d:
    document.append(i['data'])
    meta_data.append({'type':i['type'],'page':i['page'],'source':i['source']})
    id.append(i['id'])
print(meta_data)
croma_storage.add(
    documents=document,
    metadatas=meta_data,
    ids=id
)