from src.translator import Translator
from src.save_2_db import save_to_db, read_from_db
import tqdm

Data = read_from_db()

THREAD_COUNT=10

tr = Translator(Data, THREAD_COUNT)
y_len=tr.y_len

THE_COUNT_TO_SPLIT=y_len

counter=y_len//THE_COUNT_TO_SPLIT
counter = 1
remain=y_len%THE_COUNT_TO_SPLIT
remain = 0
start=0
end=THE_COUNT_TO_SPLIT
final_res_to_save =[]
for i in tqdm.tqdm(range(counter)):


    splited_data=tr.split_data(start,end)
    thread_res=tr.thread(splited_data)
            
    translated_names = tr.get_translated(thread_res)
    for dic1, dic2 in zip(Data, translated_names):
        dic2.update({"linkedin_url":dic1["linkedin_url"]})

    save_to_db(translated_names)
    start=end
    
    if i==counter :
        start=end
        end=end+remain
        splited_data=tr.split_data(start,end)
        thread_res=tr.thread(splited_data)
        translated_names = tr.get_translated(thread_res)
        for dic1, dic2 in zip(Data, translated_names):
            dic2.update({"linkedin_url":dic1["linkedin_url"]})
        save_to_db(translated_names)
        break
        
    end=end+THE_COUNT_TO_SPLIT
    
        




