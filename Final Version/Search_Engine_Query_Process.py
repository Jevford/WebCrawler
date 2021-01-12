import math
import os
import json
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
from Tokenizer import tokenizer

def query_process(inverted_index, document_length, query):
    tokenized_query = tokenizer(query)
    if len(tokenized_query) == 1:
        query_dict = dict()
        try:
            token = list(tokenized_query.keys())[0]
            #print(token)
            #print(inverted_index['irvine'])
            query_dict = inverted_index[token]
            #print('query dict : ')
            #print(inverted_index['irvine'])
            #query_dict = url_tfidf_dict
            #for info in url_tfidf_dict:
                #query_dict[info] = url_tfidf_dict[info][1]
        except:
            pass
        
        if len(query_dict.items()) > 20:
            query_result = sorted(list(query_dict.items()), key = lambda x: x[1], reverse = True)[0:20]
        else:
            query_result = sorted(list(query_dict.items()), key = lambda x: x[1], reverse = True)
        return query_result
    
    else:
        multi_query_dict = defaultdict(float)
        try:
            query_normalized_tfidf_dict = defaultdict(float)
            query_length_square = 0
            for token in tokenized_query.keys():
                tf_weight = 1 + math.log10(tokenized_query[token])
                idf = math.log10(len(document_length)/len(inverted_index[token]))
                tf_idf = tf_weight * idf
                query_normalized_tfidf_dict[token] = tf_idf
                query_length_square += math.pow(tf_idf, 2)
                #normalized_tf_in_query = tf_idf / query_length

            query_length = math.sqrt(query_length_square)
            for token in query_normalized_tfidf_dict.keys():
                query_normalized_tfidf_dict[token] = query_normalized_tfidf_dict[token]/query_length



            for token in query_normalized_tfidf_dict.keys():
                doc_dict = inverted_index[token]
                for doc in doc_dict.keys():
                    normalized_tf_in_doc = inverted_index[token][doc][0]/document_length[doc]
                    multi_query_dict[doc] += query_normalized_tfidf_dict[token] * normalized_tf_in_doc
            

        except:
            pass
        


        if len(multi_query_dict.items()) > 20:
            multi_query_result = sorted(list(multi_query_dict.items()), key = lambda x: x[1], reverse = True)[0:20]
        else:
            multi_query_result = sorted(list(multi_query_dict.items()), key = lambda x: x[1], reverse = True)
        return multi_query_result



def retrieve_doc(query_result_list):
    id_url = json.load(open('WEBPAGES_RAW/bookkeeping.json'), encoding="utf-8")
    final_output = []
    for docid_str, _ in query_result_list:
        id_info = docid_str.split('/')
        folder_id = id_info[0]
        file_id = id_info[1]

        file_name = "{}/{}/{}".format("WEBPAGES_RAW", folder_id, file_id)
        html = open(file_name,'r', encoding = 'utf-8')  
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("title")
        if title:
            final_output.append((" ".join(soup.title.string.strip().split()), id_url[docid_str]))
        else:
            final_output.append(("Sorry. No description for the title ", id_url[docid_str]))
    #print(final_output)
    return final_output



def search_query(query_content):
    inverted_index = pd.read_pickle("inverted_index__final_file.pkl")
    document_length = pd.read_pickle("document_length__final_file.pkl")
    search_result = retrieve_doc(query_process(inverted_index, document_length, query_content))
    #print(search_result)
    if len(search_result) > 20 :
        search_result = search_result[0:20]
    return search_result
    
    '''
    try:
        search_result = retrieve_doc(query_process(inverted_index, document_length, query_content))
        print(search_result)
        return search_result
    except:
        return [("Sorry, there is no result available")]
    '''
    