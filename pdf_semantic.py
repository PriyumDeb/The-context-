import pdfplumber as plix

def analyze_pdf(pdf1,page):                        #makes a parent chunk
    with plix.open(pdf1) as pdf:
        pg= pdf.pages[page]
        extracted_table = pg.extract_tables()
        extracted_text=pg.extract_text(layout = True)               # layout true means it will see the structure and select text accordingly
        thepage={
            'page_number' : page ,
            'id':f'The parent of {pdf1}' + str(page),
            'table':extracted_table,
            'text': extracted_text,
        }
        return thepage

def detail_analyzed_pdf(thepage):                            # make child chunks
    raw_texts= thepage['text']
    table=thepage['table']
    pagenumber=thepage['page_number']
    chunks=[]
    if raw_texts:
        para= raw_texts.split('\n\n')
        for index,i in enumerate(para):
            clean_para=i.strip()
            if len(clean_para)>40:
                chunk={
                    'type':'Text',
                    'id':f"child of text{thepage['id']}" + str(pagenumber)+"id"+ " " + str(index),
                    'data': clean_para,
                    'page': pagenumber
                }
                chunks.append(chunk)
    if table:
        for index,i in enumerate(table):
            tmarkdown=table_markdown(i)
            chunk={
                    'type':'Table',
                    'id':f"child of table {thepage['id']}"+ str(pagenumber)+"id"+ " " + str(index),
                    'data': tmarkdown,
                    'page': pagenumber
                }
            chunks.append(chunk)
    return (chunks) 
def table_markdown(thepage):                   #cleans the table and sends back clean markdowns
    
    if not thepage or not thepage[0]:
        return ("")
    markdowns=[]
    for i,j in enumerate(thepage):
        clean_row=[]
        for hi in j:
            if hi is None:
                clean_row.append("")
            else:
                clean_row.append(str(hi).replace('\n'," ").strip())
        markdown = '|'+" | ".join(clean_row)+'|'
        markdowns.append(markdown)
        if i==0:
            markdown= '|'+ " | ".join(["----"]*len(clean_row))+'|'
            markdowns.append(markdown)
    return "\n".join(markdowns)
            
def all_pdf_analyze(pdf3):
    with plix.open(pdf3) as mpdf:
        dta=[]
        for i in range (len(mpdf.pages)):
            pdfs=mpdf.pages[i]
            exteact_text=pdfs.extract_text(layout=True)
            extract_tables=pdfs.extract_tables()
            page_data={
                'id':f"parent of {i} " ,
                'source':pdf3,
                'text':exteact_text,
                'table':extract_tables,
                'pgno':i
                    }
            dta.append(page_data)
    return dta
def all_detailed_pdf_analyze(dta):
    big_chunk=[]
    for i in range (len(dta)):
        rtext=dta[i]['text']
        rtable=dta[i]['table']
        pageno=dta[i]['pgno']
        chunks=[]
        if rtext:
            para=rtext.split('\n\n')
            for index,j in enumerate(para):
                clean_para=j.strip()
                if len(clean_para)>40:
                    chunk={
                        'type':'Text',
                        'id':"child of text" + str(pageno)+"id"+ " " + str(index) ,
                        'source':dta[i]['source'],
                        'data': clean_para,
                        'page': pageno
                    }
                    chunks.append(chunk)
        if rtable:
            for k,j in enumerate(rtable):
                tmarkdown=table_markdown(j)
                chunk={
                    'type':'Table',
                    'id':"child of table" + str(pageno)+"id" + str(k) ,
                    'source':dta[i]['source'],
                    'data': tmarkdown,
                    'page': pageno
                }
                chunks.append(chunk)
        big_chunk.extend(chunks)
    return big_chunk


c=all_pdf_analyze('nexus.pdf')
d=all_detailed_pdf_analyze(c)


if __name__ == '__main__':
    print(c,d)
    




