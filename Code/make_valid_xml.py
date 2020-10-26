import os

# def match(name):
#     if name in {"2014cat_xml.txt","2013_4_4cat_xml.txt"}:
#         delete = '<!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v44-2013-05-16.dtd" [ ]>'
#     elif name == "2005cat_xml.txt":
#         delete = '<!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v40-2004-12-02.dtd" [ ]>'
#     elif name == "2006cat_xml.txt":
#         delete = '<!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v41-2005-08-25.dtd" [ ]>'
#     elif name in {"2007_4_2cat_xml.txt","2008cat_xml.txt","2009cat_xml.txt","2010cat_xml.txt","2011cat_xml.txt","2012cat_xml.txt","2013_4_2cat_xml.txt"} :
#         delete = '<!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v42-2006-08-23.dtd" [ ]>'
#     elif name == "2013_4_3cat_xml.txt":
#         delete = '<!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v43-2012-12-04.dtd" [ ]>'
#     else: delete =  '<!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v45-2014-04-03.dtd" [ ]>'
#     return delete

# change all file into txt
local = 'C:/Users/Diane_HU/Desktop/SURF/Data/'
path = local+'XML/'
# xml_names = os.listdir(path)
# for xml in xml_names:
#     if not (xml[-3:]=="dtd"):
#         new_xml = xml[:-3]+"txt"
#         os.rename(os.path.join(path, xml), os.path.join(path,new_xml))


txt_names = ['ipgb20180206.txt', 'ipgb20180213.txt', 'ipgb20180220.txt', 'ipgb20180227.txt', 
'ipgb20180306.txt', 'ipgb20180313.txt', 'ipgb20180320.txt', 'ipgb20180327.txt', 
'ipgb20180403.txt', 'ipgb20180410.txt', 'ipgb20180417.txt', 'ipgb20180424.txt', 
'ipgb20180501.txt', 'ipgb20180508.txt', 'ipgb20180515.txt', 'ipgb20180522.txt', 
'ipgb20180529.txt', 'ipgb20180605.txt', 'ipgb20180612.txt', 'ipgb20180619.txt', 
'ipgb20180626.txt', 'ipgb20180703.txt', 'ipgb20180710.txt', 'ipgb20180717.txt', 
'ipgb20180724.txt', 'ipgb20180731.txt', 'ipgb20180807.txt', 'ipgb20180814.txt', 
'ipgb20180821.txt', 'ipgb20180828.txt', 'ipgb20180904.txt', 'ipgb20180911.txt', 
'ipgb20180918.txt', 'ipgb20180925.txt', 'ipgb20181002.txt', 'ipgb20181009.txt', 
'ipgb20181016.txt', 'ipgb20181023.txt', 'ipgb20181030.txt', 'ipgb20181106.txt', 
'ipgb20181113.txt', 'ipgb20181120.txt', 'ipgb20181127.txt', 'ipgb20181204.txt', 
'ipgb20181211.txt', 'ipgb20181218.txt', 'ipgb20181225.txt', 'ipgb20190101.txt', 
'ipgb20190108.txt', 'ipgb20190115.txt', 'ipgb20190122.txt', 'ipgb20190129.txt', 
'ipgb20190205.txt', 'ipgb20190212.txt', 'ipgb20190219.txt', 'ipgb20190226.txt', 
'ipgb20190305.txt', 'ipgb20190312.txt', 'ipgb20190319.txt', 'ipgb20190326.txt', 
'ipgb20190402.txt', 'ipgb20190409.txt', 'ipgb20190416.txt', 'ipgb20190423.txt', 
'ipgb20190430.txt', 'ipgb20190507.txt', 'ipgb20190514.txt', 'ipgb20190521.txt', 
'ipgb20190528.txt', 'ipgb20190604.txt', 'ipgb20190611.txt', 'ipgb20190618.txt', 
'ipgb20190625.txt', 'ipgb20190702.txt', 'ipgb20190709.txt', 'ipgb20190716.txt', 
'ipgb20190723.txt', 'ipgb20190730.txt', 'ipgb20190806.txt', 'ipgb20190813.txt', 
'ipgb20190820.txt', 'ipgb20190827.txt', 'ipgb20190903.txt', 'ipgb20190910.txt', 
'ipgb20190917.txt', 'ipgb20190924.txt', 'ipgb20191001.txt', 'ipgb20191008.txt', 
'ipgb20191015.txt', 'ipgb20191022.txt', 'ipgb20191029.txt', 'ipgb20191105.txt', 
'ipgb20191112.txt', 'ipgb20191119.txt', 'ipgb20191126.txt', 'ipgb20191203.txt', 
'ipgb20191210.txt', 'ipgb20191217.txt', 'ipgb20191224.txt', 'ipgb20191231.txt', 
'ipgb20200107.txt', 'ipgb20200114.txt', 'ipgb20200121.txt', 'ipgb20200128.txt', 
'ipgb20200204.txt', 'ipgb20200211.txt', 'ipgb20200218.txt', 'ipgb20200225.txt', 
'ipgb20200303.txt', 'ipgb20200310.txt', 'ipgb20200317.txt', 'ipgb20200324.txt', 
'ipgb20200331.txt', 'ipgb20200407.txt', 'ipgb20200414.txt', 'ipgb20200421.txt', 
'ipgb20200428.txt', 'ipgb20200505.txt', 'ipgb20200512.txt', 'ipgb20200519.txt', 
'ipgb20200526.txt', 'ipgb20200602.txt', 'ipgb20200609.txt']



left=[  ]

# for txt in txt_names:
#     print(txt)
#     with open(path+txt,encoding="utf-8") as f:
#         content = f.readlines()

#     cleanedContent = []

#     for line in content:
#         foundDOC = line.find('<!DOCTYPE us-patent-grant SYSTEM')
#         foundXML = line.find('<?xml version="1.0" encoding="UTF-8"?>')
    
#         if not (foundDOC != -1 or foundXML!=-1):
#             cleanedContent.append(line)

#     print(" ########### cleaned content ########### ")
#     file = open(path+"new_"+txt[:-3]+"txt", 'w',encoding="utf-8")
#     file.writelines(['<?xml version="1.0" encoding="UTF-8"?>\n']+['<root>\n']+cleanedContent+['</root>\n'])
#     file.close()

#change all file into xml

#txt_names = os.listdir(path)
# for txt in txt_names:
#     if not (txt[-3:]=="dtd"):
#         new_xml = txt[4:-3]+"xml"
#         os.rename(os.path.join(path, txt), os.path.join(path,new_xml))

