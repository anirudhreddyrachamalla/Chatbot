'''
##dict of response for each type of intent
intent_response_dict = {
    "intro": ["This is a GST FAQ bot. One stop-shop to all your GST related queries"],
    "greet":["Hey","Hello","Hi"],
    "goodbye":["Bye","It was nice talking to you","See you","ttyl"],
    "affirm":["Cool","I know you would like it"]

}

gstinfo_response_dict = {
    "GST": " Goods and Service Tax (GST) is a destination based tax on consumption of goods and services.",
    "benefits":"GST consumes more than a dozen taxes, thus making it hassle free and efficient.",
    "faq_link":'You can check all the answers here <a href="http://www.cbec.gov.in/resources//htdocs-cbec/deptt_offcr/faq-on-gst.pdf</a>'
}

gst_query_value_dict = {
    "12%":"Non-AC hotels, business class air ticket, frozen meat products, butter, cheese, ghee, dry fruits in packaged form, animal fat, sausage, fruit juices, namkeen and ketchup",
    "5%":"railways, air travel, branded paneer, frozen vegetables, coffee, tea, spices, kerosene, coal, medicines",
    "18%":"AC hotels that serve liquor, telecom services, IT services, flavored refined sugar, pasta, cornflakes, pastries and cakes",
    "28%":"5-star hotels, race club betting,wafers coated with chocolate, pan masala and aerated water",
    "exempt":"education, milk, butter milk, curd, natural honey, fresh fruits and vegetables, flour, besan"
}
'''

"""
def gst_info(entities):
    if entities == None:
        return "Could not find out specific information about this ..." +  gstinfo_response_dict["faq_link"]
    if len(entities) == 1:
        return gstinfo_response_dict[entities[0]]
    return "Sorry.." + gstinfo_response_dict["faq_link"]

def gst_query(entities):
    if entities == None:
        return "Could not query this ..." + gstinfo_response_dict["faq_link"]
    for ent in entities:
        qtype = ent["type"]
        qval = ent["entity"]
        if qtype == "gst-query-value":
            return gst_query_value_dict[qval]
"""

import requests
from bs4 import BeautifulSoup as soup 
import pandas as pd

def govt_info(entities):
    r = requests.get("http://cmdb.jharkhand.gov.in/")
    html_data = soup(r.content)

    req_data = html_data.find_all("div",{"class":"col-xs-12 col-sm-12 col-md-4 col-lg-4 card"})

    scraped = {}
    for total_data in req_data:
        department = total_data.find("div", {"class":"col-xs-12 col-sm-12 col-md-12 col-lg-12"}).text
        list_schemes = total_data.find_all("td")
        for scheme in list_schemes:
            scheme_name = scheme.find_all("b")[0].contents[0]
            scheme_name = scheme_name.upper()
            value = ""
            for i in scheme.find_all("span"):
                value += i.text
                scraped[scheme_name.strip()] = list()
                scraped[scheme_name.strip()].append(value)
                scraped[scheme_name.strip()].append(department.upper())
        
    final_data =  pd.DataFrame.from_dict(scraped, orient='index')
    final_data.columns = ['Values','Department']
    if entities[0]["type"] == "scheme":
        val = entities[0]["entity"].upper()
        for i in scraped.keys():
            if val.find(i) != -1:
                break
            elif i.find(val) != -1:
                break
        return("value : " + scraped[i][0] + "  Department : " + scraped[i][1])
    if entities[0]["type"] != "scheme":
        val = entities[0]["entity"].upper()
        useful_data = final_data.loc[final_data['Department'] == val ]
        msg = ""
        for i in range(len(useful_data)):
            msg +=  "\n  Scheme : "+final_data.index[i] +" ||      Value : "+ final_data.iloc[i,0]
            
        return(msg)
            
            
                
    
        
