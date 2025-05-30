
from genericpath import isfile
from os import listdir
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

import itertools as it

import networkx as nx

import bs4
#from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
#%matplotlib qt

import numpy as np



# exploratory only
def scrapeModules(): #devolve lista de modulos. 

    url = "https://www.kegg.jp/entry/M00001"
    url = "file:///C:/Users/Pedro/Desktop/Programas/fileManipulator/M00001.html"
    url = "file:\\C:\\Users\\Pedro\\Desktop\\Programas\\fileManipulator\\savedScrapes\\savedHTMLs\\M00001.html"
    #url = "https://www.kegg.jp/entry/M00004"
        
    print("Pimbas")

    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser" )#.encode('UTF-8')
    body = soup.body
    tbody = soup.find_all("table")
    results = tbody

    # SAVE FILE JUST OPENED
    # with open("M00004.html", "w") as file:
    #     file.write(str(soup))

    for x in body.contents:
        print(x.name)
    print("|\||\|\|\|")

    tables = body.find_all("table")
    # for tab in tables:
    #     print(tab.name)

    print([[(i, cont.string) for cont in tables[i].contents] for i in range(len(tables))])

    print("==========") # should be 3
    print([cont for cont in tables[3].contents])
    print("==========") # should be 3
    print([cont.name for cont in tables[3].contents])
    # print("==========") # should be 3
    # print([cont.name for cont in tables[3].children])
    
    print("##########") # should be 3
    print([[(i, cont) for cont in tables[3].contents[i]] for i in range(len(tables[3].contents))])
    print("") # should be 3
    
    for lini, line in enumerate(tables[3].contents):
        if line.name != None:
            print(f"[Ln{lini}]", [column.name for column in line.children])
            for coli, column in enumerate(line.children):
                if column.name == "td":
                    print(f"  --[ln{lini}-TD1({coli})]", [child.text for child in column.children])
                    print(f"  --[ln{lini}-TD2({coli})]", [child.string for child in column.children])
                    #print(f"  --[ln{lini}-TD7({coli})]", [child3.string for child in column.children for child2 in child.children for child3 in child2.children])
                    print(f"  --[ln{lini}-TD6({coli})]", [child2.string for child in column.children for child2 in child.children])
                    #print(f"  --[ln{lini}-TD7({coli})]", [[child2.contents] for child in column.children for child2 in child.children])
                    #print(f"  --[ln{lini}-TD3({coli})]", [child.prettify( formatter="html" ) for child in column.children])
                    print(f"  --[ln{lini}-TD4({coli})]", [child.prettify() for child in column.children])
                    
    
    #  if type(child)!=BeautifulSoup.element.NavigableString
    interest = [[child2.contents for child2 in child if type(child2)!=bs4.element.NavigableString] for child in tables[3].contents[15].contents[2].contents[0]]
    #interest = [[type(child2) for child2 in child] for child in tables[3].contents[15].contents[2].contents[0]]
    print(f"EKSTRA {len(interest)}", interest)# column.children for child2 in child.children for child3 in child2.children])
    print(len(interest), [len(intt) for intt in interest])
    print("EKSTRA\n" + '\n'.join([f"{ii:2.0f}-{iii} : " + ",".join(interestii) for ii,interesti in enumerate(interest) for iii,interestii in enumerate(interesti)])) # scrape compounds
    del interest[2::3] # remove empty
    interest = interest
    print("ANOTHE", interest)
    print("\nAnother:", [[len(childi) for childi in child] for child in tables[3].contents[15].contents[2].contents[0] ])
    #print("\nAnother:", "\n".join([["\n".join([childii.string for childii in childi if type(childii)!=str]) for childi in child] for child in tables[3].contents[15].contents[2].contents[0] ]))
    print("\nAnother:", [[[childii.string if type(childii)!=str else childii for childii in childi ] for childi in child] for child in tables[3].contents[15].contents[2].contents[0]])
    objeto_marado = [[[childii.string if type(childii)!=str else childii for childii in childi ] for childi in child] for child in tables[3].contents[15].contents[2].contents[0]]
    print("\nCOMPRIMENTOS: \n", [[len(childii) for childii in childi] for childi in objeto_marado])
    print("\nCOMPRIMENTOS: \n", "\n".join([str([len(childii) for childii in childi]) for childi in objeto_marado]))
    print("\nCOMPRIMENTOS: \n", "\n".join([str([childii for childii in childi]) for childi in objeto_marado]))
    print("\nCOMPRIMENTOS: \n", "\n".join([str([[len(childiii) for childiii in childii] for childii in childi]) for childi in objeto_marado]))


def readSaveHTMLs(urls: list, htmls_savefolder: str):

    for url in urls:
        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser" )#.encode('UTF-8')

        # SAVE FILE JUST OPENED
        #with open(f"{'/' + savefolder + '/' + url.split('/')[-1]}.html", "w+") as file:
        with open(f"{htmls_savefolder + '/' + url.split('/')[-1]}.html", "w+") as file:
            file.write(str(soup))


# reads the html files and saves compounds and recipes lists
def scrapeSaveKEGG1(htmls_savefolder: str, compounds_dir:str, reactions_dir:str):

    #html_files = [htmls_savefolder+"/"+f for f in listdir(htmls_savefolder)] # if isfile(join(htmls_savefolder, f))]
    html_files = ["file:\\"+os.path.abspath(os.path.join(htmls_savefolder, f)) for f in listdir(htmls_savefolder)] # if isfile(join(htmls_savefolder, f))]
    print("\n[FILES TO READ]", html_files)
    for url in html_files:
        module_code = url.replace(".html","").split("\\")[-1]
        print(f"= MODULE CODE: {module_code}")

        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser" )#.encode('UTF-8')
        body = soup.body
        tables = body.find_all("table")

        # scrape reactions
        # reactions = [(  child.text.split("\xa0\xa0")[0].split(","), # reactions
        #                 child.text.split("\xa0\xa0")[1].split(" -> ")[0].split(" + "), # ingredients
        #                 child.text.split("\xa0\xa0")[1].split(" -> ")[1].split(" + ")) # products
        #                 for child in tables[3].contents[15].contents[2].contents]
        
        reactions_object = [[[childii.string if type(childii)!=str else childii for childii in childi ] for childi in child] for child in tables[3].contents[15].contents[2].contents[0]]
        #reactions_object = [[childii.string if type(childii)!=str else childii for childi in child for childii in childi ] for child in tables[3].contents[15].contents[2].contents[0]]
        del reactions_object[2::3]
        reactions_object = [[reactions_object[2*k], reactions_object[2*k+1]] for k in range(len(reactions_object)//2)]
        #print("R_OBJECT:", reactions_object)
        #print("R_OBJECT:\n", "\n".join([str(child) for child in reactions_object]))
        #print("R_OBJECT:", [len(child) for child in reactions_object])
        #print("R_OBJECT:", [[len(childi) for childi in child] for child in reactions_object])
        n_ingredients = [reaction[1].index([' ', '-', '>', ' ']) for reaction in reactions_object]
        #print(n_ingredients)
        reactions = [(  reaction[0][0::2], # reactions (every 2 entries)
                        reaction[1][0:n_ingredients[reaction_i]:2], # ingredients
                        reaction[1][n_ingredients[reaction_i]+1::2]) # products
                        for reaction_i,reaction in enumerate(reactions_object)]
        #print("[reactions]\n" + "\n".join([str(child) for child in reactions]))
        reactions = [tuple([[item[0] for item in component]  for component in reaction]) for reaction in reactions]
        #print("[reactions]", reactions)
        print("[REACTIONS]\n" + "\n".join([str(child) for child in reactions]))

        # scrape compounds
        compounds = [tuple(child.text.split("\xa0\xa0")) for child in tables[3].contents[17].contents[2].contents]
        print("[COMPOUNDS]", compounds)


        # SAVE COMPOUNDS AND REACTIONS
        #with open(f"{compounds_dir + '/' + url.split('/')[-1]}.html", "w+") as file:
        with open(os.path.join(compounds_dir, module_code+".txt"), "w+") as file:
            file.write("\n".join([str(comp).replace("'","").replace("(","").replace(")","") for comp in compounds]))

        with open(os.path.join(reactions_dir, module_code+".txt"), "w+") as file:
            file.write("\n".join([str(reac).replace("'","").replace("(","").replace(")","") for reac in reactions]))


def readCompoundsRecipes(compounds_dir:str, reactions_dir:str):
    compounds = []
    reactions = []

    compound_files = [os.path.abspath(os.path.join(compounds_dir, f)) for f in listdir(compounds_dir) if f != "Aggregated.txt"] # if isfile(join(htmls_savefolder, f))]
    reaction_files = [os.path.abspath(os.path.join(reactions_dir, f)) for f in listdir(reactions_dir) if f != "Aggregated.txt"] # if isfile(join(htmls_savefolder, f))]
    print("\n[COMPOUND FILES TO READ]", compound_files)
    print("\n[REACTION FILES TO READ]", reaction_files)

    # for url in compound_files:
    #     with open(url, 'r') as file:
    #         compounds.append([line.replace("\n","") for line in file.readlines()])
    # for url in reaction_files:
    #     with open(url, 'r') as file:
    #         reactions.append([line.replace("\n","") for line in file.readlines()])

    
    for url in compound_files:
        with open(url, 'r') as file:
            for line in [line.replace("\n","") for line in file.readlines()]:
                line = line.split(", ")
                if line not in compounds: compounds.append(line)
    for url in reaction_files:
        with open(url, 'r') as file:
            for line in [line.replace("\n","") for line in file.readlines()]:
                line = [[item for item in ele.replace("[", "").replace("]", "").split(", ")] for ele in line.split("], ")]
                if line not in reactions: reactions.append(line)

    ## remove duplicates:
    # compounds = list(set([str(comp) for comp in compounds]))
    # reactions = list(set([str(reac) for reac in reactions]))

    return compounds, reactions



def saveAggregated(compounds, reactions, compounds_dir:str, reactions_dir:str):
    print("\nTO SAVE AGGREGATE:", compounds)
    print("\nTO SAVE AGGREGATE:", reactions)
    with open(os.path.join(compounds_dir, "Aggregated.txt"), "w+") as file:
        file.write("\n".join([str(comp).replace("'","").replace("[","").replace("]","") for comp in compounds]))

    with open(os.path.join(reactions_dir, "Aggregated.txt"), "w+") as file:
        file.write("\n".join([str(reac).replace("'","")[1:-1] for reac in reactions]))



def buildConfusionMatrix(compounds, reactions, code_to_int):
    n_compounds = len(compounds)
    A = np.zeros((n_compounds, n_compounds))
    A = [[[] for _ in range(n_compounds)] for _ in range(n_compounds)]

    for react in reactions:
        #print("RIAÇÂO", react)
        for ingredient in react[1]:
            for product in react[2]:
                for react_code in react[0]:
                    if react_code not in A[code_to_int[ingredient]][code_to_int[product]]:
                        A[code_to_int[ingredient]][code_to_int[product]] += [react_code]

    A_ = np.array([[len(entry) for entry in line] for line in A])
    print("A_:\n", A_)

    return np.array(A), A_


# DRAW SOME GRAPHS
def draw_graph(A, node_labels:list):
    plt.figure(figsize=(6,6))
    #rows, cols = np.where(A == 1)
    rows, cols = np.where(A >= 1)
    edges = zip(rows.tolist(), cols.tolist(), A[rows,cols])
    #print("EDGES:", list(edges))
    gr = nx.DiGraph()
    gr = nx.MultiDiGraph()
    gr.add_weighted_edges_from(edges, weight="weight")
    #pos = nx.spring_layout(gr, seed=42)
    pos = nx.circular_layout(gr)
    pos = nx.kamada_kawai_layout(gr, weight=None) # to ignore weight
    nx.draw(gr, pos, node_size=100, width=0)
    nx.draw_networkx_nodes(gr, pos)
    #nx.draw(gr, pos, arrows=True, arrowstyle="->", arrowsize=20, width=1.5, node_size=200) ## ERA ESTE
    #nx.draw_networkx(gr, pos, arrows=True, node_size=100) #, node_size=100)
    connectionstyle = [f"arc3, rad={r}" for r in it.accumulate([0.15] * 3)]
    print(connectionstyle)

    curved_edges = [edge for edge in gr.edges(data=True) if tuple(reversed(edge[:2])) in list(gr.edges())] 
    straight_edges = [(node1,node2,weight) for node1,node2,weight in gr.edges(data=True) if (node1,node2,weight) not in curved_edges]
    #print(len(curved_edges), curved_edges)
    #print(len(straight_edges), straight_edges)

    all_weights = []
    for (node1,node2,data) in gr.edges(data=True):
        all_weights.append(data['weight'])
    unique_weights = list(set(all_weights))

    for weight in unique_weights:
        weighted_straight_edges = [(node1,node2) for (node1,node2,edge_attr) in straight_edges if edge_attr['weight']==weight]
        weighted_curved_edges   = [(node1,node2) for (node1,node2,edge_attr) in curved_edges   if edge_attr['weight']==weight]
        width = weight
        #nx.draw_networkx_edges(gr,pos, edgelist=weighted_edges, width=width, arrowstyle="->", connectionstyle=connectionstyle[0])
        nx.draw_networkx_edges(gr,pos, edge_color="grey", edgelist=weighted_curved_edges, width=width, arrowstyle="->", connectionstyle=connectionstyle[0])
        nx.draw_networkx_edges(gr,pos, edge_color="grey", edgelist=weighted_straight_edges, width=width, arrowstyle="->")

    nx.draw_networkx_labels(gr, pos, labels=node_labels, font_size=7)
    #nx.draw_networkx_edges( gr, pos, edge_color="grey", connectionstyle=connectionstyle[1]) #, ax=ax)
    plt.show()

    
# DRAW SOME GRAPHS
def draw_graph2(A, A_, int_to_code_dict=None, code_to_name_dict=None):
    plt.figure(figsize=(6,6))
    #rows, cols = np.where(A == 1)
    rows, cols = np.where(A_ >= 1)

    edges = []
    for row in range(len(A)):
        for col in range(len(A[row])):
            for rec in A[row][col]:
                edges += [(row, col, {"w":rec})]
    print(list(edges))
    
    gr = nx.MultiDiGraph()
    gr.add_edges_from(edges)
    #pos = nx.circular_layout(gr)
    pos = nx.kamada_kawai_layout(gr)
    nx.draw_networkx_nodes(gr, pos)
    connectionstyle = [f"arc3, rad={r}" for r in it.accumulate([0.15] * 3)]
    print(connectionstyle)
    nx.draw_networkx_labels(gr, pos, labels={intt:code_to_name_dict[code] for intt,code in int_to_code_dict.items()}, font_size=7)
    nx.draw_networkx_edges( gr, pos, edge_color="grey", connectionstyle=connectionstyle[1]) #, ax=ax)
    plt.tight_layout()
    plt.show()



# exploratory
# scrapeModules()

# scrape and save html pages
modules = ["M00001", "M00002", "M00003", "M00307"]
urls = [f"https://www.kegg.jp/entry/{module}" for module in modules]
#readSaveHTMLs(urls, "savedScrapes/savedHTMLs")


#scrapeSaveKEGG1("savedScrapes/savedHTMLs", "savedScrapes/savedCompounds", "savedScrapes/savedReactions")

compounds, reactions = readCompoundsRecipes("savedScrapes/savedCompounds","savedScrapes/savedReactions")
print("\n[COMPOUNDS]", len(compounds), compounds)
print("\n[REACTIONS]", len(reactions), reactions)
saveAggregated(compounds, reactions, "savedScrapes/savedCompounds", "savedScrapes/savedReactions")

# compound_code_to_name_dict = {comp.split(", ")[0]:comp.split(", ")[1] for comp in compounds}
# compound_code_to_int_dict  = {comp.split(", ")[0]:i for i,comp in enumerate(compounds)}
compound_code_to_name_dict = {comp[0]:comp[1] for comp in compounds}
compound_code_to_int_dict  = {comp[0]:i for i,comp in enumerate(compounds)}
compound_int_to_code_dict  = {i:comp for comp, i in compound_code_to_int_dict.items()}
print(compound_code_to_name_dict)
print(compound_code_to_int_dict)
print(compound_int_to_code_dict)
# compound_code_to_name()

A, A_ = buildConfusionMatrix(compounds, reactions, compound_code_to_int_dict)
eigenval, eigenvec = np.linalg.eig(A_)
print("VALUES:", np.absolute(eigenval))
print("VECTOR:\n", list(zip(compound_code_to_name_dict.values(), np.absolute(eigenvec[1, :]))))
print("VECTOR:\n", "\n".join([str([it1,it2]) for it1,it2 in zip(compound_code_to_name_dict.values(), np.absolute(eigenvec[1, :]))]))
# print("VECTORS:\n",  eigenvec)

node_labels = {intt:compound_code_to_name_dict[code]+f"\n{np.absolute(eigenvec[0, intt]):.3f}" for intt,code in compound_int_to_code_dict.items()}

draw_graph(A_, node_labels)
#draw_graph2(A, A_, compound_int_to_code_dict, compound_code_to_name_dict)
plt.show()