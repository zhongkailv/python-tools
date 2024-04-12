# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:39:40 2024

@author: zhongkai.lv
"""

from PyPDF2 import PdfReader, PdfWriter


def page_str_handle(page_str
                    ,page_len):
    """
        Parameters
    ----------
    page_str : 字符型或整数型
        参数有以下设置形式：
        '':空字符串（默认值），表示只处理所传PDF文件第1页；
        '3'或3:表示只处理所传PDF文件第3页；
        'a' 或 'A' 或 'all' 或 'ALL':处理所传PDF文件所有页；
        '3-5':处理所传PDF文件第3页到第5页（包含第3页和第5页）；
        '3-':处理所传PDF文件第3页及之后所有页；
        '-5':处理所传PDF文件第1页到第5页（包含第5页）；
        
        特别说明：
        此处的第3页，第5页等均是按生活中计数规则计数，即以1开始
    page_len : 整数型
        没有指定结束页码时，则用该页码作为结束页码。

    Raises
    ------
    ValueError
        如果开始页码大于结束页码，则抛出错误。

    Returns
    -------
    page_start : 整数型
        开始页码（该页码针对Python索引而言，即以0开始）
    page_end : 整数型
        结束页码（该页码针对Python索引而言，即以0开始）

    """
        
    page_start,page_end = 0,1
    
    if not page_str:
        return page_start,page_end
    
    try:
        """
        处理以字符串格式传的整数型，如'3',但是需要排除'-3'这种情况
        """
        page_str = str(page_str)  
        
        ## 为了兼容数值型的3，先把它转成字符串型。若不然，运行page_str.startswith('-')
        ## 时会抛出错误 AttributeError: 'int' object has no attribute 'startswith'
        if not page_str.startswith('-'):
            page_start = page_end = int(page_str)
            return page_start - 1,page_end
    except ValueError:
        pass
        

    if page_str.lower() in ('a','all'):
        page_end = page_len + 1

    elif page_str.startswith('-'):
        page_end = min(int(page_str.strip('-')),page_len + 1)
        
    elif page_str.endswith('-'):
        page_start = int(page_str.strip('-')) - 1
        page_end = page_len + 1
        
    else:
        page_list = page_str.split('-')
        page_start = int(page_list[0]) - 1
        page_end = min(int(page_list[1]),page_len + 1)
    
    if page_start > page_end:
        raise ValueError("开始页码不能小于结束页码！！！")
    else:
        return page_start,page_end
    
    

def  split_pdf(in_file
              ,out_file
              ,page_str = ''
              ,is_out = True):
    """
    Parameters
    ----------
    in_file : 字符串
        待处理文件路径
    out_file : 字符串
        文件保存路径
    page_str：字符型或整数型
        参见page_str_handle中的page_str
    Returns
    -------
    None.
    
    """
    reader = PdfReader(in_file)
    
    page_start,page_end = page_str_handle(page_str,len(reader.pages))
    
    # print(page_start,page_end)
    
    writer = PdfWriter()
    
    for page in reader.pages[page_start:page_end]:
        writer.add_page(page)
    
    with open(out_file, "wb") as out_pdf:
        writer.write(out_pdf)




def concat_pdf(file_list,out_file):
    """
    Parameters
    ----------
    file_list : 列表
        列表的元素可以是字符串（待拼接的文档名称）和字典（key为待拼接的文档名称，value为
        拼接页面，其格式参见page_str_handle函数中的page_str）
    out_file : 字符串
        文件保存路径

    Returns
    -------
    None.
    说明：
    1.最终输出文件是按照列表中文件的先后顺序拼接而成；
    2.如果file_list的元素是字典，请严格按照指定格式输入；

    """
    if not file_list: return
    
    writer = PdfWriter()
    
    for file in file_list:
        assert isinstance(file, (str, dict)),'file_list中的元素只能是字符串和字典型！！！'
        if isinstance(file, str):
            """file是字符串的处理方式"""
            for page in PdfReader(file).pages:
                writer.add_page(page)
        else:
            """file是字典的处理方式"""
            for key,value in file.items():
                reader = PdfReader(key)
                
                page_start,page_end = page_str_handle(value,len(reader.pages))

                for page in reader.pages[page_start:page_end]:
                    writer.add_page(page)
                
    with open(out_file, "wb") as out_pdf:
        writer.write(out_pdf)



if __name__  == '__main__':
    split_pdf("test.pdf","test-a.pdf",'a')
    split_pdf("test.pdf","test_all.pdf",'all')
    split_pdf("test.pdf","test-.pdf",'')
    split_pdf("test.pdf","test-2.pdf",'2')
    split_pdf("test.pdf","test-1-2.pdf",'1-2')
    split_pdf("test.pdf","test-1-.pdf",'1-')
    split_pdf("test.pdf","test--2.pdf",'-2')
    split_pdf("test.pdf","test-1-5.pdf",'1-5')
    
    concat_pdf([{"test.pdf":1},{"test.pdf":'a'},{"test-a.pdf":'-2'},"test-2.pdf"]
                ,"test3.pdf")



