


import os
from urllib.request import urlopen
from bs4 import BeautifulSoup


### READS THE HTMLS, EVENTUALLY SAVES THEM, 
### READS THE CONTENTS AND KEEPS TRACK OF THE LISTS OF COMPOUNDS AND OF REACTIONS
### SAVES THOSE IN OTHER TXT FILES


def retrieveSaveHTMLs(urls: list, htmls_savefolder: str):
    for url in urls:
        filename = f"{htmls_savefolder + '/' + url.split('/')[-1]}.html"
        # if file doesnt exist yet
        if not os.path.isfile(filename):
            page = urlopen(url)
            soup = BeautifulSoup(page, "html.parser" )#.encode('UTF-8')

            # SAVE FILE JUST OPENED
            #with open(f"{'/' + savefolder + '/' + url.split('/')[-1]}.html", "w+") as file:
            with open(f"{htmls_savefolder + '/' + url.split('/')[-1]}.html", "w+") as file:
                file.write(str(soup))



# reads the html files and saves compounds and recipes lists
def scrapeSaveKEGG(htmls_savefolder: str, modules_list: list, compounds_dir:str, reactions_dir:str, pathwayName:str):

    #html_files = [htmls_savefolder+"/"+f for f in listdir(htmls_savefolder)] # if isfile(join(htmls_savefolder, f))]
    html_files = ["file:\\"+os.path.abspath(os.path.join(htmls_savefolder, f"{module}.html")) for module in modules_list] # if isfile(join(htmls_savefolder, f))]
    html_urls  = [f"https://www.kegg.jp/entry/{module}" for module in modules_list] # if isfile(join(htmls_savefolder, f))]
    print("\n[FILES TO READ]", html_files)
    print("\n[FILES TO READ]", html_urls)

    compounds_list = []
    reactions_list = []

    URLSTOSKIP = ["M00053.html", "M00096.html", "M00154.html", "M00155.html", "M00824.html", "M00873.html"]

    for url, html_url in zip(html_files, html_urls):
        if url[-11:] in URLSTOSKIP: 
            print("skipped 53")
            continue
        module_code = url.replace(".html","").split("\\")[-1]
        print(f"= READING MODULE: {module_code}")# ({url}, {html_url})")

        try:
            page = urlopen(url)
        except: 
            print("  [HTML FILE NOT FOUND]")
            page = urlopen(html_url)

        soup = BeautifulSoup(page, "html.parser" )#.encode('UTF-8')
        body = soup.body
        tables = body.find_all("table")

        reactions_object = [[[childii.string if type(childii)!=str else childii for childii in childi ] for childi in child] for child in tables[3].contents[15].contents[2].contents[0]]
        #reactions_object = [[childii.string if type(childii)!=str else childii for childi in child for childii in childi ] for child in tables[3].contents[15].contents[2].contents[0]]
        del reactions_object[2::3]
        reactions_object = [[reactions_object[2*k], reactions_object[2*k+1]] for k in range(len(reactions_object)//2)]
        
        #print(" -REACTION OBJECT:", [len(reac) for reac in reactions_object],  reactions_object)
        try:
            n_ingredients = [reaction[1].index([' ', '-', '>', ' ']) for reaction in reactions_object]
        except:
            print("[Skipping...]")
            continue
        #print(n_ingredients)
        reactions = [(  reaction[0][0::2], # reactions (every 2 entries)
                        reaction[1][0:n_ingredients[reaction_i]:2], # ingredients
                        reaction[1][n_ingredients[reaction_i]+1::2]) # products
                        for reaction_i,reaction in enumerate(reactions_object)]
        #print("[reactions]\n" + "\n".join([str(child) for child in reactions]))
        reactions = [tuple([[item[0] for item in component]  for component in reaction]) for reaction in reactions]
        #print("[reactions]", reactions)
        #print("[REACTIONS]\n" + "\n".join([str(child) for child in reactions]))

        # scrape compounds
        try:
            compounds = [tuple(child.text.split("\xa0\xa0")) for child in tables[3].contents[17].contents[2].contents]
        except:
            compounds = []
            print("[empty compounds]")
        #print("[COMPOUNDS]", compounds)


        # SAVE COMPOUNDS AND REACTIONS
        for compound in compounds:
            ## removing compounds without name
            if compound not in compounds_list and len(compound)==2: # and compound[1]!="\xa0": 
                compounds_list.append(compound)
        for reaction in reactions:
            if reaction not in reactions_list: 
                reactions_list.append(reaction)
    
    print("[FINAL COMPOUNDS]", compounds_list)
    print("[FINAL REACTIONS]", reactions_list)

    with open(os.path.join(compounds_dir, pathwayName+".txt"), "w+") as file:
        file.write("\n".join([str(comp).replace("'","").replace("(","").replace(")","") for comp in compounds_list]))
    with open(os.path.join(reactions_dir, pathwayName+".txt"), "w+") as file:
        file.write("\n".join([str(reac).replace("'","").replace("(","").replace(")","") for reac in reactions_list]))

    return compounds_list, reactions_list
    


## READ COMPOUNDS AND REACTIONS FROM TXT FILES
def readCompoundsRecipes(compounds_dir:str, reactions_dir:str):
    compound_codes = []
    compounds = []
    reactions = []

    compound_files = [os.path.abspath(os.path.join(compounds_dir, f)) for f in os.listdir(compounds_dir) if f != "Aggregated.txt"] # if isfile(join(htmls_savefolder, f))]
    reaction_files = [os.path.abspath(os.path.join(reactions_dir, f)) for f in os.listdir(reactions_dir) if f != "Aggregated.txt"] # if isfile(join(htmls_savefolder, f))]
    # print("\n[COMPOUND FILES TO READ]", compound_files)
    # print("\n[REACTION FILES TO READ]", reaction_files)

    for url in compound_files:
        with open(url, 'r') as file:
            for line in [line.replace("\n","") for line in file.readlines()]:
                line = line.split(", ")
                if line not in compounds and line[0] not in compound_codes: 
                    compounds.append(line)
                    compound_codes.append(line[0])

    for url in reaction_files:
        with open(url, 'r') as file:
            for line in [line.replace("\n","") for line in file.readlines()]:
                line = [[item for item in ele.replace("[", "").replace("]", "").split(", ")] for ele in line.split("], ")]
                if line not in reactions: reactions.append(line)

    return compounds, reactions


## RUN: python3 Scraper.py ModuleLists\Metabolic_pathways_map01100.txt --save-htmls
if __name__ == "__main__":
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('modules', type=str, help='Path and name of modulesList.txt file to be read',
                    default="")
    #parser.add_argument('--save-htmls', type=bool, default=False, help='Flag to save the read htmls for local use later (default: %(default)s)')
    parser.add_argument('--mode', type=str, default="complete", choices=['complete', 'fromCompounds'], help='Complete: from scratch scrape the HTMLS. FromCompounds: from presaved compounds.txt files (default: %(default)s)')
    parser.add_argument('--save-htmls', action="store_true", help='Flag to save the read htmls for local use later (default: %(default)s)')
    parser.add_argument('--htmls-folder', type=str, default="savedHTMLs", help='Path of saved and to be saved HTML files (default: %(default)s)')
    parser.add_argument('--compounds-folder', type=str, default="savedCompounds", help='Path of saved and to be saved compounds.txt files (default: %(default)s)')
    parser.add_argument('--reactions-folder', type=str, default="savedReactions", help='Path of saved and to be saved reactions.txt files (default: %(default)s)')
    
    args = parser.parse_args()
    print("# Options")
    for key, value in sorted(vars(args).items()):
        print(key, "=", value)
    print("")


    # RETREIVE LIST OF MODULES OF INTEREST
    pathwayName = args.modules.split("\\")[-1][:-4]
    with open(args.modules, 'r') as file:
        modules_list = [line.replace("\n","")[:6] for line in file.readlines()]
    HTML_urls = [f"https://www.kegg.jp/entry/{module}" for module in modules_list]

    # RETREIVE AND SAVE HTML URLS
    if args.save_htmls:
        retrieveSaveHTMLs(HTML_urls, args.htmls_folder)

    # scrape the htmls for compunds and 
    scrapeSaveKEGG(args.htmls_folder, modules_list, args.compounds_folder, args.reactions_folder, pathwayName)
