# coding: utf-8

import requests, json

class Off_Loader():
    @classmethod
    def ultima(cls):
        ultima_list = []
        with open("off_categories_A.json", "r") as f:
            data = json.load(f)
        cpy = data.copy()
        for key, value in cpy.items():
            if "childs" in value:
                data.pop(key)
        for key in data.keys():
            ultima_list.append(key)
        with open("categoies_lasts_childs.json", "w") as f:
            f.write(json.dumps(ultima_list, indent=4, sort_keys=True))

    @classmethod
    def arbo(cls):
        origin_list = []
        categories_arbo = {}
        with open("off_categories.json", "r") as f:
            all_categories = json.load(f)
        for el in all_categories["tags"]:
            if el["id"][0:3] == "en:" and el["id"][3].isalpha():
                origin_list.append(el["id"])
        with open("off_categories_A.json", "r") as f:
            all_categories = json.load(f)
        for el in origin_list:
            if el in all_categories:
                categories_arbo[el] = {"parents": all_categories[el]}
            else:
                categories_arbo[el] = {"parents" : "NO PARENTS FOUNDS !"}
        with open("off_categories_B.json", "w") as f:
            f.write(json.dumps(categories_arbo, indent=4, sort_keys=True))
   
    @classmethod
    def childs(cls):
        with open("off_categories_B.json", "r") as f:
            dict_B = json.load(f)
        dict_child = dict_B.copy()
        for child, value in dict_B.items():
            if value["parents"] != "NO PARENTS FOUNDS !":
                for parents in value["parents"]:
                    if parents in dict_child:
                        if "childs" in dict_child[parents]:
                            dict_child[parents]["childs"].append(child)
                        else:
                            dict_child[parents]["childs"] = [child]
        dict_B = dict_child.copy()
        for key, value in dict_B.items():
            if value["parents"] == "NO PARENTS FOUNDS !":
                dict_child.pop(key)
        with open("off_categories_A.json", "w") as f:
            f.write(json.dumps(dict_child, indent=4, sort_keys=True))

if __name__ == "__main__" :
    Off_Loader.ultima()
    #Off_Loader.arbo()
    #Off_Loader.childs()

"""f.write(json.dumps(data, indent=4, sort_keys=True))"""