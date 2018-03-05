# useful functions for language models
#import networkx as nx
import matplotlib.pyplot as plt
from numpy.random import choice
#from collections import Counter
import math
import time
from matplotlib_colors_dict import color_names


lang_encoding = ['X', 'Y', 'Z', 'W', 'R', 'U', 'S', 'T']


"""
possible_colors = ["red", "green", "blue", "yellow", "pink", "purple", 
    "yellowgreen", "grey", "m", "olive", "orange", "darkgreen", 
    "coral", "fushsia", "crimson", "plum", "lime", "indigo", 
    "y", "goldenrod"]
"""
possible_colors = list(color_names.keys())

def lang2color(lang):
    # return list
    mapping = {'X': 10, 'Y':20, 'Z':30, 'W': 40, 'R':50,
        'F':60, 'G':70, 'H':80}
    p = 0.6 # the importance of first color w.r.t. 2nd
    ret = []
    for ch in lang:
        if len(ch) == 2:
            tmp = mapping[ch[0]] * p + mapping[ch[1]] * (1-p)
        else:
            tmp = mapping[ch]
        ret.append(tmp)
    return ret



def draw_graph(graph, lang_speaker, fig_name):
    # graph: a networkx graph
    # lang_speaker: list of string
    now = time.localtime()
    timestamp = "_" + str(now.tm_hour) + "_" + str(now.tm_min) + "_" + str(now.tm_sec)
    fig_name += timestamp

    
    lang_set = list(set(lang_speaker))
    colors = lang2color(lang_set)
    num_lang = len(lang_set)
    num_speakers = len(lang_speaker)

    node_dict = {lang:[] for lang in lang_set} # dict of (lang:index)
    for index in range(num_speakers):
        node_dict[lang_speaker[index]].append(index)

    # dict of (lang: legend_labels)
    label_dict = {lang: lang + " {:.2%}".format(len(node_dict[lang])/num_speakers) for lang in lang_set}  

    # color_dict = {lang_set[x]:([colors[x]] * len(node_dict[lang_set[x]])) for x in range(num_lang)}
    color_dict = {lang_set[x]:possible_colors[x] for x in range(len(lang_set))}
    minColor = min(colors)
    maxColor = max(colors)
    
    pos = nx.spring_layout(graph)

    #print(node_dict, label_dict, color_dict)
    

    for lang in lang_set:
        nx.draw_networkx_nodes(graph, 
            pos=pos,
            nodelist=node_dict[lang],
            label=label_dict[lang],
            with_labels=False,
            vmin=minColor,
            vmax=maxColor,
            node_color=color_dict[lang],
            node_size=50)
    nx.draw_networkx_edges(graph, pos=pos, edge_color='skyblue')

    plt.legend(numpoints =1)
    plt.axis('off')
    plt.show()
    plt.savefig("img/" + fig_name + ".png")
    plt.close()


def draw_trend_avg(his_list, all_lang, add):
    pass


def draw_record(add_list, win, fail):
    X = [0.5+x for x in add_list]

    ax = plt.gca()  # 获取当前图像的坐标轴信息
    ax.yaxis.get_major_formatter().set_powerlimits((0,1)) # 将坐标轴的base number设置为一位。
    plt.plot(X, win, '-o', label="win")
    plt.plot(X, fail, '-*', label="fail")
    plt.legend()
    plt.title("Language Survival over prestige")
    plt.show()

    now = time.localtime()
    timestamp = "_" + str(now.tm_hour) + "h" + str(now.tm_min) + "m" + str(now.tm_sec) + "s"
    plt.savefig("img./final" + timestamp + ".png")
    plt.close()


def draw_trend(history, all_lang, sa, summary=False):
    """
    # dict of (string : list)
    trend = {lang:list() for lang in all_lang}  
    X = []
    for t in range(len(history)):
        record = history[t]  # dict of (string : int)
        X.append(t+1)
        for lang in trend:
            if lang in record:
                trend[lang].append(record[lang])
            else:
                trend[lang].append(0)
    """
    trend = history
    X = [t+1 for t in range(len(history[all_lang[0]]))]

    if summary is True:
        trend["X_"] = trend["X"]
        trend["Y_"] = trend["Y"]
        trend["Z_"] = trend["Z"]
        if "XY" in trend:
            trend["X_"] = [x+y for x, y in zip(trend["X_"], trend["XY"])]
        if "XZ" in trend:
            trend["X_"] = [x+y for x, y in zip(trend["X_"], trend["XZ"])]
        if "YZ" in trend:
            trend["Y_"] = [x+y for x, y in zip(trend["Y_"], trend["YZ"])]
        if "YX" in trend:
            trend["Y_"] = [x+y for x, y in zip(trend["Y_"], trend["YX"])]
        if "ZX" in trend:
            trend["Z_"] = [x+y for x, y in zip(trend["Z_"], trend["ZX"])]
        if "ZY" in trend:
            trend["Z_"] = [x+y for x, y in zip(trend["Z_"], trend["ZY"])]
        legend = ["X_", "Y_", "Z_"]
    
    if summary is True:
        plt.plot(X, trend["X_"])
        plt.plot(X, trend["Y_"])
        plt.plot(X, trend["Z_"])
    else:
        for lang in trend:
            plt.plot(X, trend[lang])
        legend = list(trend.keys())
    
    plt.legend(legend)
    plt.title("Delta=" + str(sa))

    now = time.localtime()
    timestamp = "_" + str(now.tm_hour) + "h" + str(now.tm_min) + "m" + str(now.tm_sec) + "s"
    plt.savefig("img/trend" +"_D=" + str(sa) + timestamp + ".png")

    plt.show()
    plt.close()



def isBilinguist(node_index, lang_speaker):
    return len(lang_speaker[node_index]) == 2


def choose_lang(lang_probs, myLang):
    # lang_probs: dict of (string: floot)
    # myLang: string, the language speaking
    candidates = list(lang_probs.keys())  # Keys, string
    prob = [lang_probs[x] for x in candidates]  # Values
    candidates.append(myLang)   
    prob.append(1 - sum(prob))
    draw = choice(candidates, 1, p=prob)
    return draw[0]


def make_bilanguist(single_lang, prob):
    # return: dictionary of biLang : probabiliry
    bilinguist = {}
    num_lang = len(single_lang)
    for x in range(num_lang):
        for y in range(num_lang):
            if x == y:
                continue
            key = single_lang[x] + single_lang[y] # String concat
            value = prob[x] * prob[y]   # Improve? importance of 1st w.r.t 2nd
            bilinguist[key] = value
    return bilinguist


def update_prob(prob, bi_prob, bi_popularity=0.2):
    # bi_popularity: the ratio of bilinguists [0, 1]
    # return: list, Normalized probability
    s = sum(bi_prob)
    prob = [x * (1 - bi_popularity) for x in prob]
    tmp = sum(bi_prob)
    bi_prob = [y / tmp * bi_popularity for y in bi_prob]
    return prob + bi_prob


def generate_speakers(num_lang, num_speakers, prob=None, bilingual=False, bi_popular=0.2):
    candidates = [lang_encoding[x] for x in range(num_lang)]
    if prob is None:
        prob = [1/num_lang for x in range(num_lang)]
    #print(prob)
    if bilingual is True:
        bi_cand_dict = make_bilanguist(candidates, prob)
        #print(bi_cand_dict)
        bi_lang = list(bi_cand_dict)    # Keys
        candidates = candidates + bi_lang
        bi_prob = [bi_cand_dict[bi] for bi in bi_lang]  # Values
        prob = update_prob(prob, bi_prob, bi_popularity=bi_popular)
    #print(prob)f
    draw = choice(candidates, num_speakers, p=prob)
    if bilingual is False:
        candidates += list(make_bilanguist(candidates, prob))
    return list(draw), candidates


def prestige2matrix(p):
    # p: a list of int/floot, absolute prestige value for each language
    # return: list of list
    num_lang = len(p)
    matrix = []
    for i in range(num_lang):
        row = []
        for j in range(num_lang):
            tmp = p[i] - p[j]
            logistic = 1 / (1 + math.exp(-tmp))
            row.append(logistic)
        matrix.append(row)
    return matrix


def speaker2langList(lang_speaker):
    lang = set(lang_speaker)



def speaker_analysis(lang_speaker):
    return dict(Counter(lang_speaker))


def test():
    from numpy import random

    X = [x*0.002 for x in range(100)]
    Y = ([0] * (0.03//0.002))
    Y += 0.51 / (0.1 - 0.03) * 


if __name__ == "__main__":
    test()