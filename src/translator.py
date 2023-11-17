from concurrent.futures import thread
import json
from deep_translator import GoogleTranslator
import tqdm
import time
import csv
import concurrent.futures

import pathlib
import sys
path=str(pathlib.Path(__file__).parent.absolute())
sys.path.append(path)


s=time.time()

class Translator():
    def __init__(self, Data_for_translate, thread_count):
        self.header_count=0
        self.rate=0
        self.name_and_translated_name=[]
        self.proxies = {
    'http': 'http://82.115.16.187:18001',
    'https': 'http://82.115.16.187:18001'
    }
        

        # file=open('serp_seen_persons.json',encoding='utf8')
        # x=file.read()
        # y=json.loads(x)
        y = Data_for_translate
        self.y=y
        self.y_len=len(y)
        self.count=0
        self.eng_let='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.thread_count=thread_count


    def split_data(self,start,end):
        print('Segmenting ... ')
        y=self.y[start:end]
        def do_standard(y,count):
            data_list=[]
            if (len(y)% count)!=0:
                data_count=int(len(y)/count)+1
            else:
                data_count=int(len(y)/count)

            start=0
            end=count
            c_data=0

            for i in range(data_count):
                c_data=c_data+end-start
                datas=y[start:end]
                data_list.append(datas)
                start=end
                end=end+count

                if end+1>len(y) and i==data_count-1 and c_data<len(y):
                    print(end)
                    datas=y[start:]
                    data_list.append(datas)
            return data_list

        def do_standard2(y,count):
            data_list=[]
            
            if (len(y)% count)!=0:
                data_count=int(len(y)/count)+1
            else:
                data_count=int(len(y)/count)
            start=0
            end=data_count
            c_data=0
            for i in range(count):
                c_data=c_data+end-start

                datas=y[start:end]
                data_list.append(datas)
                start=end
                end=end+data_count

                if end+1>len(y) and i==count-1 and c_data<len(y):
                    print(end)
                    datas=y[start:]
                    data_list.append(datas)
            return data_list

        person_count = 50
        threads_count=self.thread_count
        res1=do_standard(y,person_count)
        res2=do_standard2(res1,threads_count)
        
        return res2
            

    def translate(self,datas):
 
        res=[]
        
        for data in (datas):
            fname_str = ''
            # lname_str = ''
            for d in (data):
                # print(d['first_middle_name'])
                if d['first_middle_name'] != None and d['last_name'] != None :
                    
                    fname_str = fname_str + d['first_middle_name'] + ' ahmadi' + '\n'
                    fname_str = fname_str + 'mohammad '  + d['last_name'] +  '\n'
                else :
                    fname_str = fname_str + '*' + '\n'
                    fname_str = fname_str + '*' + '\n'


                # lname_str = lname_str + d['last_name'] + '\n'

            if len(fname_str)<5000:
                try:
                    translated = GoogleTranslator(source='en', target='fa').translate(fname_str)
                    self.count += 1
                    print(' Count:',self.count*len(data),'Time: ',time.time()-s)
                except:
                    print('Couldnt translate ... Trying without proxiy ...')
                    try:
                        translated = GoogleTranslator(source='en', target='fa',proxies=self.proxies).translate(fname_str)
                    except:
                        print('Realy cant translate')
                        translated = None



            else:

                print('length is too long')

            if translated!=None:
                splited = translated.split('\n')
                for i in range(0,len(splited),2):
                    if len(splited[i].split(' احمدی'))>1 and len(splited[i+1].split('محمد '))>1:
                        res.append({'persian_firstname':splited[i].split(' احمدی')[0], 'persian_lastname':splited[i+1].split('محمد ')[1]})
                    else:
                        res.append({'persian_firstname':'Not translated', 'persian_lastname':"Not translated"})
                        print(splited[i])
                        print(splited[i+1])
            
        return res

    def thread(self,data_list):

        with concurrent.futures.ThreadPoolExecutor() as executer:
            results_run=[executer.submit(self.translate,data) for data in data_list]
        return results_run

    def get_translated(self,results_run):
        self.header_count+=1
 
        results=[]
        print('Extracting from thread results ....')
        for ir, res in enumerate(results_run):
            results.append(res.result())
            # print('result len:',len(res.result()))
        final_res=[]
        for result in results:
            for res in result:
                final_res.append(res)
        
        return(final_res)



