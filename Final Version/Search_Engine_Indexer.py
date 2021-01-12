import nltk
from collections import defaultdict
from bs4 import BeautifulSoup
from bs4 import Comment
import math
import os
import json
from nltk.corpus import words, stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from Tokenizer import tokenizer



class Indexer():
    def __init__(self, html_json):
        self.corpus_html = html_json
        self.inverted_index_tf = defaultdict(dict)  # {term1: {(docid_folder,docid_file): 3(this is tf), ...}, term2:...}
        self.inverted_index = defaultdict(dict)  # {term1: {(docid_folder,docid_file): [ 1.68(log_tf), 2.57(this is tfidf score for term1 in this doc), ...}, term2:...}
        self.document_length = defaultdict(float) # this dict records document length for each doc { (docid_folder1,docid_file1): 12.33, (docid_folder1,docid_file2): 3.39...}
        self.token_tf_dict = defaultdict(int) # this records term and its term-frequency {term1:12, term2:13, term3:1}
        self.token_dict = defaultdict(int) # {key is a term: value is a list [term-frequency after weighted, text_type]}
                                            #{ term1 : [weighted_frequency, "head"], term2 : [weighted_frequency, "title"]...}
        
        self.total_num_of_doc = 37497
        
         
    '''
    def tfidf_calculator(self, tf, df, size = 37497):
        if tf == 0:
            return 0
        return round(((1 + math.log(float(tf))) * math.log((size/float(df)))),1)
    '''



    def log_weighted_tf(self, tf):
        result = 1 + math.log10(tf)
        return result



    def create_index(self):
        corpus_data = json.load(open(self.corpus_html), encoding = 'utf-8')   # load the data
        print('Start to parse...')
        num = 1
        for (doc_id, url) in corpus_data.items():  # 0/19 : www.ics.uci.edu........ 0/19 means the url is in the folder named 0 and the file named 19 inside the folder
            id_info = doc_id.split('/')
            folder_id = id_info[0]
            file_id = id_info[1]
            
            file_name = "{}/{}/{}".format("WEBPAGES_RAW", folder_id, file_id)
            html = open(file_name,'r', encoding = 'utf-8')  
            soup = BeautifulSoup(html, 'lxml')
            text_info = soup.findAll(text = True)
            for text in text_info:
                if (text.parent.name not in ['style', 'script', '[document]', 'meta']) and (not isinstance(text, Comment)):
                    self.token_tf_dict = tokenizer(text.strip())
                    token_dict_items = self.token_tf_dict.items()
                    if text.parent.name in ["head", "title", "bold"]:   # if the term is in some more "important" tag, the term frequency 
                        for (token, frequency) in token_dict_items:
                            # self.token_dict[token] = frequency*2
                            
                            self.inverted_index_tf[token][doc_id] = frequency*2  # Notice that self.inverted_index is a dict of dict
                            # if self.token_dict[token] == []:
                            #     self.token_dict[token].append(frequency * 2)
                            #     self.token_dict[token].append(text.parent.name)
                            # else:
                            #     self.token_dict[token].append(frequency*2)
                            #     self.token_dict[token].append(text.parent.name)
                    else:
                        for (token, frequency) in token_dict_items:
                            # self.token_dict[token] = frequency
                            #print(token, frequency)
                            self.inverted_index_tf[token][doc_id] = frequency  # Notice that self.inverted_index is a dict of dict
                            # if self.token_dict[token] == []:
                            #     self.token_dict[token].append(frequency)
                            #     self.token_dict[token].append(text.parent.name)
                            # else:
                            #     self.token_dict[token].append(frequency)
                            #     self.token_dict[token].append(text.parent.name)
                    
            
            # for (term, tf) in token_dict_items:
            #     self.inverted_index_tf[term][doc_id] = tf  # Notice that self.inverted_index is a dict of dict
            print("Starting...."+str(num))
            num+=1
            
            
        for term in self.inverted_index_tf.keys():
            df = len(self.inverted_index_tf[term])
            idf = math.log10(self.total_num_of_doc/df)
            
            for docid in self.inverted_index_tf[term].keys():
                weighted_tf = float(1 + math.log10(self.inverted_index_tf[term][docid]))
                tf_idf_score = weighted_tf * idf
                self.inverted_index[term][docid] = []
                self.inverted_index[term][docid].append(weighted_tf)
                self.inverted_index[term][docid].append(tf_idf_score)
                #print(self.inverted_index[term][docid])
                self.document_length[docid] += math.pow(self.inverted_index[term][docid][0], 2) 
        
        for doc in self.document_length.keys():
            self.document_length[doc] = math.sqrt(self.document_length[doc])


        # write inverted_index dict into pandas pickle file
        index_storage  = pd.Series(self.inverted_index)
        index_storage.to_pickle("inverted_indexfinal_file.pkl")
        # write document_length dict into pandas pickle file
        document_storage = pd.Series(self.document_length)
        document_storage.to_pickle("document_lengthfinal_file.pkl")
        
        

def main():
    indexer = Indexer('WEBPAGES_RAW/bookkeeping.json')
    indexer.create_index()

if __name__ == "__main__" :
    main()

