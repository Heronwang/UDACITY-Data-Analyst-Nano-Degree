import numpy as np
import pandas as pd
from collections import defaultdict
import re 

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court","Place", \
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd":"Road",
            "Rd.":"Road",
            "Ave":"Avenue",
            "Ave.":"Avenue",
           "Dr":"Drive",
           "Dr.":"Drive"
            }

street_type_re=re.compile(r'\b\S+\.?$', re.IGNORECASE)
house_type_re=re=re.compile(r'\b[A-Za-z]*[0-9]+$', re.IGNORECASE)

class streets(object):
        def __init__(self,path):
                self.df=pd.read_csv(path)
                self.is_street=self.df['key']=='street'
                self.streets=self.df[self.df['key']=='street']
                self.len=len(self.df)
        def strip(self):
            '''To strip the incorrect , and . postfix of streetname'''
            for idx,each in self.streets.iterrows():
                if each['value'].endswith(',') or each['value'].endswith('.'):
                    print each['value']
                    self.streets.loc[idx,'value']=each['value'][:-1].title()

                    
        def get_street_type(self,each): 
            #from whole street name return street type 
                name=each['value']
                m=street_type_re.search(name)
                if m:
                        return m.group()


        def house_number(self,street_type):  
           #if find house number in a street type, return the house number
                m=house_type_re.search(street_type)
                if m:
                        return  m.group()

        def audit(self,showall=False,to_csv=False):
            #Find all suspected street type and print them according to frequency order
                def output(dict,showall):
                        sorted_keys=sorted(dict,key=lambda k:len(dict[k]),reverse=True)
                        sum=0
                        for key in sorted_keys:
                                print key,len(dict[key])
                                sum+=len(dict[key])
                                if showall:
                                        print dict[key]            
                               
                street_types=defaultdict(set)
                for _,each in self.streets.iterrows():
                        street_type=self.get_street_type(each)
                        street_types[street_type].add(each['value'])

                self.street_types=street_types
                output(street_types,showall=showall)
                if to_csv:
                    self.streets.to_csv('streets.csv')

        def housenumber_update(self):
             #if the street type includes also house number,
            #split the acutual street type and housenumber, 
            #and log the house number to a new dataframe housenumber 
                housenumber=pd.DataFrame(columns=['id','key','value','type'])
                def get_row(street_type):
                            hsno=self.house_number(street_type)
                            if hsno:
                                row=each
                                row['key']='housenumber'
                                row['value']=hsno
                                row['type']='addr'

                                return row
                
                count=0
                for idx,each in self.streets.iterrows():                                                
                        street_type=self.get_street_type(each)
                        row=get_row(street_type)
                        if not row is None:
                                housenumber.loc[count+self.len]=row
                                newvalue=''
                                newvalue=' '.join(self.streets.ix[idx]['value'].split(' ')[:-1])
                                self.streets.loc[idx,'value']=newvalue
                                count+=1     
                housenumber.to_csv('housenumber.csv')
                


        def mapping_update(self):
            #map abbreviations to expected form
                for idx,each in self.streets.iterrows():
                        street_type=self.get_street_type(each)
                        if not street_type in expected:
                            if street_type in mapping.keys():
                                print each['value']
                                new=mapping[street_type]                                
                                newstreetname=each['value'].split(' ')[:-1]                            
                                newstreetname.append(new)
                                newstreetname=' '.join(newstreetname)
                                            
                 

st=streets('nodes_tags.csv')
print '--------Before cleaning:'
#st.audit(showall=True)

st.strip()
st.housenumber_update()
st.mapping_update()

print '--------After cleaning:'
#st.audit(to_csv=True)


