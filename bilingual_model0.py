from model_helper import *
import networkx as nx
from collections import Counter

# prepare encodings for each language
lang_encoding = ['X', 'Y', 'Z', 'W', 'R', 'U', 'S', 'T']



def main():
    
    num_speakers = 1000  # total number of speakers/nodes

    # total number of languages
    # Each language is encoded by one of capital letters A-O
    num_lang = 3

    # population ratio of num_lang languages. If equal, set None.
    # Notice: sum to 1
    lang_ratio = [0.333333, 0.333333, 0.333334]
    
    # language prestige, with length of num_lang
    absolute_prestige = [0.5, 0.5, 0.5]

    # volatility. Eg. ('A': 2)
    volatility = {}  # others are def_vol
    def_vol = 1  # default volatility

    # the ratio of bilingual persons
    bi_popularity = 0.35

    iterations = 60
    doPlotting = True
    iter_per_plot = 10  # plot a figure every ? iterations

    # the probability of connection between two nodes
    connectivity = 0.05

    
    # lang_speaker: list of string, encoding for languages
    # bilingual shown by "AB", where "A" is 1st language and 
    # "B" is 2nd language
    lang_speaker, all_lang = generate_speakers(num_lang, 
                                    num_speakers, 
                                    prob=lang_ratio,
                                    bilingual=False,
                                    bi_popular=bi_popularity
                                    )


    prestige = prestige2matrix(absolute_prestige)

    

    history_record = []

    # Construct a graph
    G = nx.fast_gnp_random_graph(n=num_speakers, p=connectivity, seed=1024, directed=False);
    #G = nx.powerlaw_cluster_graph(n=num_speakers, m=10, p=0.5, seed=2048)
    num_clique = 2
    #G = nx.relaxed_caveman_graph(num_clique, num_speakers//num_clique, 0.05)

    #draw_graph(G, lang_speaker, "Iter_0")

    new_lang_speaker = lang_speaker.copy()
    for t in range(1, iterations+1):

        for node in G.nodes():
            myLang = lang_speaker[node] # string

            neighbors = list(G.neighbors(node))
            # lang_speaker[x][0] means only consider 1st language of neighbors
            neighbor_lang = [lang_speaker[x][0] for x in neighbors] # list of string
            lang_cnt_dict = dict(Counter(neighbor_lang)) # dict of (string:int), the number of lang neighbors speak

            if not isBilinguist(node, lang_speaker):  
                # Only speak a single language

                sigma_dict = {key : (lang_cnt_dict[key]/len(neighbors)) for key in lang_cnt_dict}  # (string:floot)
                
                lang_probs = {  # lang[0] means only consider 1st language of neighbors
                    lang: ( prestige[lang_encoding.index(lang[0])][lang_encoding.index(myLang)]
                             * (sigma_dict[lang] ** volatility.get(lang, def_vol)) ) 
                    for lang in sigma_dict
                }  # (string:floot)

                
                chosen_lang = choose_lang(lang_probs, myLang)
                if chosen_lang != myLang:
                    # syn-update node: shift to bilingual speaker
                    new_lang_speaker[node] = lang_speaker[node] + chosen_lang

            else:
                # speak two languages
                
                first_lang = myLang[0]
                index1 = lang_encoding.index(first_lang)
                sec_lang = myLang[1]
                index2 = lang_encoding.index(sec_lang)

                sigma1 = lang_cnt_dict.get(first_lang, 0) / len(neighbors)
                sigma2 = lang_cnt_dict.get(sec_lang, 0) / len(neighbors)


                lang_probs = {
                    # the prob of shifting to 1st language, forgetting the 2nd
                    first_lang: 
                        0.6*prestige[index1][index2] * ((1 - sigma2) ** volatility.get(first_lang, def_vol)),
                    # the prob of shifting to 2nd language, forgetting the 1st
                    sec_lang:   
                        0.4*prestige[index2][index1] * ((1 - sigma1) ** volatility.get(sec_lang, def_vol))
                }

                # syn-update node: returns to single speaker
                new_lang_speaker[node] = choose_lang(lang_probs, myLang)

            # end single node updating
            
        # Synchronized Update lang_speaker
        lang_speaker = new_lang_speaker

        ret = speaker_analysis(lang_speaker)
        #print("Iter " + str(t) + ": ", ret, "\n")
        history_record.append(ret)

    # end iteration
    if doPlotting is True:
        #draw_graph(G, lang_speaker, "Iter_" + str(t))
        draw_trend(history_record, all_lang, add)



if __name__ == '__main__':
    main()
    