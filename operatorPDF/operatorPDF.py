# -*- coding: utf-8 -*-
"""
Created on Tue May 22 07:06:05 2018

@author: iceman
"""

import PyPDF2
import os


filename = 'The Zen of Python.pdf'
password = 'iceman'
watermarkpdf = os.path.splitext(filename)[0]+'_with watermark' + os.path.splitext(filename)[1]
tempdir = 'tempdir'

def getPdfFileText(pdfReader):
    #获取第一页
    pdfPage = pdfReader.getPage(0)
    #获取页面内容
    content = pdfPage.extractText()
    print('The content: %s' % content)
    
def addWatermark(pdfReader):
    #打印水印文件
    pdfWmReader = PyPDF2.PdfFileReader(open('watermark.pdf', 'rb'))
    #创建新的用于保存添加水印后的Pdf
    pdfWriter = PyPDF2.PdfFileWriter()
    tempPage = pdfWmReader.getPage(0)
    #遍历页面添加水印
    for pageNum in range(0, pdfReader.numPages): 
        #对每页调用合并
        pdfReader.getPage(pageNum).mergePage(tempPage)
        #把加了水印的页面添加到最终pdf中
        pdfWriter.addPage(pdfReader.getPage(pageNum))
        
    #保存
    savePdfFile = open(watermarkpdf, 'wb')
    #为下一个步骤做准备
    pdfWriter.encrypt(password)
    pdfWriter.write(savePdfFile)
    savePdfFile.close()
    print('==> add water mark finished')
    

def decryptPdf(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as fileObj:
            pdfReader= PyPDF2.PdfFileReader(fileObj)
            if pdfReader.isEncrypted:
                print('==> this pdf is encryped...')
                pdfReader.decrypt(password)
                print(pdfReader.documentInfo)
    else:
        print(filename + 'is not exist')
  
def createPdf(filename, pageObj):
    pdfWriter = PyPDF2.PdfFileWriter()
    pdfWriter.addPage(pageObj)
    savePdfFile = open(filename, 'wb')
    pdfWriter.write(savePdfFile)
    savePdfFile.close()
    
def splitPdfAndMergePdf(pdfReader):
    #首先将拆分的pdf放入临时目录
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)
    #遍历源文档，按每页拆分
    for pageNum in range(0, pdfReader.numPages):
        createPdf(tempdir + os.path.sep + 'temp_' + str(pageNum)+'.pdf',
                  pdfReader.getPage(pageNum))
    print('==>split file finshed, then merge file')
    
    pdfWriter = PyPDF2.PdfFileWriter()
    #遍历目录，如果是以pdf结尾的就合并
    for file in os.listdir(tempdir):
        if os.path.splitext(file)[1] == '.pdf':
            pdfTempReader = PyPDF2.PdfFileReader(open(tempdir + os.path.sep + file, 'rb'))
            pdfWriter.addPage(pdfTempReader.getPage(0))       
    savePdfFile = open('MergePdf.pdf', 'wb')
    pdfWriter.write(savePdfFile)
    savePdfFile.close()

def main(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as fileObj:
            pdfReader= PyPDF2.PdfFileReader(fileObj)
            print('the pdf info: %s\n' % pdfReader.documentInfo)
            
            #获取文档内容
            getPdfFileText(pdfReader)
            
            #添加水印
            addWatermark(pdfReader)
            
            #创建加密pdf，再解密打开
            decryptPdf(watermarkpdf)
            
            #拆分pdf和合并pdf
            splitPdfAndMergePdf(pdfReader)
    else:
        print('the %s not exist' % filename)
        
    
if __name__ == '__main__':
    main(filename)