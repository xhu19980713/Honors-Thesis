import xml.etree.ElementTree as ET
import csv
import os
from xml.dom import minidom

local = 'C:/Users/Diane_HU/Desktop/SURF/Data/'
path = local+'XML/'
xml_names = os.listdir(path)


#return the root of the imported file
def importFile(name):
    tree = ET.parse(path+name)
    root=tree.getroot()
    return root

#return the count of an element in a file given its name
def count(name):
    root = importFile(name)
    c=len(root.findall('us-patent-grant'))
    print(c)
    return c

def writeFileName():
    with open('filename.csv','w',newline='') as file: 
        writer = csv.writer(file)
        for xml in xml_names:
            writer.writerow([xml,0])

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='',encoding="utf-8") as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

#check if a word is None then substitute the word with "",return the word o/w  
def check(word):
    if word==None:
        return ""
    else: return word

#alert if an attribute or text is set to None
def help(name,word):
    if word==None: 
        print(name)
        

def strip(fileName):
    root = importFile(fileName)
    new_root = ET.Element("root")
    grant_counter=0
    res = []
    for grant in root.iter('us-bibliographic-data-grant'):
        app_ref = grant.find('application-reference')
        app_type = app_ref.get('appl-type')

        get_city = None
        get_state = None
        get_country = None
        if app_type =="utility":
            
            grant_counter+=1
            new_grant = ET.SubElement(new_root,"us-grant",num=str(grant_counter))
            ######### publication reference #################
            ### extract 
            pub_ref = grant.find('publication-reference')
            pub_document = pub_ref.find('document-id')
            country = pub_document.find('country').text
            doc_number = pub_document.find('doc-number').text
            year_granted = pub_document.find('date').text[:4]
            ### reconstruct 
            new_grant.set("country",country)
            new_grant.set("doc-number",doc_number)
            new_grant.set("year-granted",year_granted)
            help("country",country)
            help("doc_number",doc_number)
            help("year_granted",year_granted)
            
            #################################################

            ######### publication reference #################
            ### extract 
            app_document = app_ref.find('document-id')
            year_applied = app_document.find('date').text[:4]
            ### reconstruct 
            new_grant.set("year-applied",year_applied)
            help("year_granted",year_granted)
            #################################################

            classification = ET.SubElement(new_grant,"classifications")

            ######### classification icpr ###################
            if year_granted == '2005':
                icpr_s = grant.find('classification-ipc')
                icpr = icpr_s.find('main-classification').text
                new_icpr = ET.SubElement(classification,"classification-icpr",num='1')
                new_icpr.text = icpr
                new_icpr.set('level','M')
                new_icpr.set('value','I')
                help("icpr",icpr)
                
                classification.set('icpr','1')
            else:
                icpr_s = grant.find('classifications-ipcr')
                icpr_counter = 0
                for icpr in icpr_s.findall('classification-ipcr'):
                    icpr_counter+=1
            ### extract
                    level = icpr.find('classification-level').text
                    section = check(icpr.find('section').text)
                    class_icpr = check(icpr.find('class').text)
                    subclass = check(icpr.find('subclass').text)
                    main_group = check(icpr.find('main-group').text)
                    subgroup = check(icpr.find('subgroup').text)
                    value = icpr.find('classification-value').text
            ### reconstruct
                    new_icpr= ET.SubElement(classification,"classification-icpr",num=str(icpr_counter))
                    new_icpr.set('level',level)
                    new_icpr.set('value',value)
                    help("level",level)
                    help("value",value)
                    new_icpr.text = section+class_icpr+subclass+main_group+'/'+subgroup
                    help("new_icpr.text",new_icpr.text)
                    
                classification.set('icpr',str(icpr_counter))
            #################################################
            
            ######### classification cpc ####################
            #not sure when USPTO started to include cpc
            ### extract
            try:
                cpc_s = grant.find('classifications-cpc')
                main_cpc = (cpc_s.find('main-cpc')).find('classification-cpc')
                cpc_section = main_cpc.find('section').text
                cpc_class = main_cpc.find('class').text
                cpc_subclass = main_cpc.find('subclass').text
                cpc_main_group = main_cpc.find('main-group').text
                cpc_subgroup = main_cpc.find('subgroup').text
                cpc_value = main_cpc.find('classification-value').text
                ### reconstruct
                new_cpc= ET.SubElement(classification,"classification-cpc")
                new_cpc.text=cpc_section+cpc_class+cpc_subclass+' '+cpc_main_group+'/'+cpc_subgroup
                new_cpc.set('value',cpc_value)
                classification.set('cpc','1')
                help("cpc_value",cpc_value)
                
            except:
                
                classification.set('cpc','0')

            ######### classification national ###############
            try:
                ### extract
                national = grant.find('classification-national')
                uspc = national.find('main-classification').text
                ### reconstruct
                new_uspc = ET.SubElement(classification,"classification-uspc")
                new_uspc.text = uspc
                classification.set('uspc','1')
                help("uspc",uspc)
            except:
                classification.set('uspc','0')
            #################################################

            citations = ET.SubElement(new_grant,'citations')

            ######### citation ##############################
            ### extract
            if int(year_granted)<2013:
                reference_key = 'references-cited'
            else: 
                reference_key = 'us-references-cited'
            reference_cited = grant.find(reference_key)
            citation_counter = 0
            if reference_cited!=None:
                for citation in reference_cited.iter('patcit'):
                    citation_counter+=1
                    cit_doc = citation.find('document-id')
                    cit_country=cit_doc.find('country').text
                    cit_doc_num=cit_doc.find('doc-number').text
                    cit_date = cit_doc.find('date').text
                ### reconstruct
                    new_cit = ET.SubElement(citations,"citation",num=str(citation_counter))
                    new_cit.set('country',cit_country)
                    new_cit.set('doc-number',cit_doc_num)
                    new_cit.set('date',cit_date)
                    help("cit_country",cit_country)
                    help("cit_d_n",cit_doc_num)
                    help("cit_date",cit_date)
                    
            citations.set('numcit',str(citation_counter))
            #################################################
            new_inventors = ET.SubElement(new_grant,'inventors')
            inventor_counter=0
            ######### inventors ##############################
            ### extract
           
            try:
                parties = grant.find('us-parties')
                inventors = parties.find('inventors')
                applicants = parties.find('us-applicants')
            except:
                parties = grant.find('parties')
                inventors = parties.find('inventors')
                applicants = parties.find('applicants')

            #deal with applicants who are also inventors
            for applicant in applicants.findall("./applicant/.[@app-type='applicant-inventor']"):
                inventor_counter+=1
                if applicant.get('app-type')!='applicant-inventor':raise Exception
                app_addressbook = applicant.find('addressbook')
                last_name = app_addressbook.find('last-name').text
                # print(new_grant.get('doc-number'))
                try:
                    first_name = check(app_addressbook.find('first-name').text)
                except:pass
                address = app_addressbook.find('address')
                inventor_country = address.find('country').text
                new_inventor = ET.SubElement(new_inventors,'inventor',num=str(inventor_counter))
                new_inventor.set('firstname',first_name)
                new_inventor.set('lastname',last_name)
                new_inventor.set('country',inventor_country)
                help("app_fn",first_name)
                help("app_ln",last_name)
                help("app_country",inventor_country)
                
                if inventor_counter==1: get_country=inventor_country
                if inventor_country=='US':
                    try:
                        inventor_city = address.find('city').text
                        new_inventor.set('city',inventor_city)
                        help("app_city",inventor_city)
                        if inventor_counter==1: get_city=inventor_city
                    except:pass
                    try:
                        inventor_state = address.find('state').text
                        new_inventor.set('state',inventor_state)
                        help("app_State",inventor_state)
                        if inventor_counter==1: get_state=inventor_state
                    except:pass
                

            if inventors !=None:
                for inventor in inventors.iter("addressbook"):
                    inventor_counter+=1
                    last_name = check(inventor.find('last-name').text)
                    try:
                        first_name = check(inventor.find('first-name').text)
                    except: first_name=""

                    new_inventor = ET.SubElement(new_inventors,'inventor',num=str(inventor_counter))
                    new_inventor.set('firstname',first_name)
                    new_inventor.set('lastname',last_name)

                    address = inventor.find('address')
                    address_none = False
                    if address==None: address_none=True
                    if address_none: inventor_country=""
                    else: inventor_country = address.find('country').text
                    new_inventor.set('country',inventor_country)

                    help("invfirst_name",first_name)
                    help("invlast_name",last_name)
                    help('inventor_country',inventor_country)
                    if inventor_counter==1: get_country=inventor_country
                    if inventor_country=='US':
                        inventor_city = address.find('city').text
                        inventor_state = address.find('state').text
                        new_inventor.set('city',inventor_city)
                        new_inventor.set('state',inventor_state)
                        help('inventor_state',inventor_state)
                        help("inventor_city",inventor_city)
                        if inventor_counter==1 :
                            get_city=inventor_city
                            get_state=inventor_state
            new_inventors.set('numinv',str(inventor_counter))

            assignees = grant.find("assignees")
            new_assignees = ET.SubElement(new_grant,"assignees")
            assignee_counter=0
            if assignees!=None:
                for assignee in assignees.iter('addressbook'):
                    assignee_counter+=1
                    # print(new_grant.get('doc-number'))
                    new_assignee = ET.SubElement(new_assignees,'assignee',num=str(assignee_counter))
                    role = assignee.find('role').text
                    new_assignee.set("role",role)
                    help("role",role)
                    try:
                        ass_lastname=assignee.find('last-name').text
                        new_assignee.set('lastname',ass_lastname)
                        help("assln",ass_lastname)
                        try:
                            ass_firstname=assignee.find('first-name').text
                            new_assignee.set('firstname',ass_firstname)
                            help("assfn",ass_firstname)
                        except:pass
                    except:
                        orgname = assignee.find('orgname').text
                        new_assignee.set("orgname",orgname)
                        help("orgname",orgname)
                    
                    ass_address = assignee.find('address')
                    ass_country = ass_address.find('country').text
                    new_assignee.set("country",ass_country)
                    help("ass_country",ass_country)

                    if ass_country=='US':
                        ass_city = ass_address.find('city')
                        if ass_city!=None:
                            ass_city=ass_city.text
                            new_assignee.set("city",ass_city)
                            help("asscity",ass_city)
                        ass_state = ass_address.find('state')
                        if ass_state!=None:
                            ass_state = ass_state.text
                            new_assignee.set("state",ass_state)
                            help("ass_state",ass_state)
                
            new_assignees.set("numass",str(assignee_counter))
            res.append([new_grant.get('doc-number'),new_grant.get('year-applied'),new_grant.get('year-granted'),get_country,get_state,get_city])
        
    new_root.set('numpat',str(grant_counter))

    a = ET.tostring(new_root) 

    new = minidom.parseString(a).toprettyxml(encoding='utf-8')
    with open("C:/Users/Diane_HU/Desktop/SURF/Data/new/new"+fileName, "wb") as f:
        f.write(new)
    return res



def main(write_to,file_address,problem_file):
    fileName = list(csv.reader(open(file_address)))
    for i in range(len(fileName)):
        try:
            if int(fileName[i][1])==0:
                name = fileName[i][0]
                print(name)

                table = strip(name)
                for line in table:    
                    append_list_as_row(write_to,line)
                fileName[i][1]='1'
            w=csv.writer(open(file_address,'w',newline=''))
            w.writerows(fileName)
        except:
            append_list_as_row(problem_file,[fileName[i][0]])
        


#==================================================
#implement
#==================================================
#call writeFileName() first then call main()
writeFileName() #get all filename and set initial status to 0 
write_to = 'C:/Users/Diane_HU/Desktop/SURF/Data/inventor_address.csv'
file_address = 'C:/Users/Diane_HU/Desktop/SURF/Code/filename.csv'
problem_file = 'C:/Users/Diane_HU/Desktop/SURF/Data/problem_file.csv'
main(write_to,file_address,problem_file) #strip the file and extract needed element 










