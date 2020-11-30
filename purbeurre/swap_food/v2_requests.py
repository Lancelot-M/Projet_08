import requests, json, copy

class ImportData():
    @classmethod
    def get_all_categories(cls):
        url = "https://fr-en.openfoodfacts.org/categories.json"
        request_data = requests.get(url)
        request_data = request_data.json()
        data_list = []
        for el in request_data["tags"]:
            if el["id"][0:3] == "en:" and el["id"][3].isalpha():
                data_list.append(el["id"])
        with open("v2_all_categories.json", "w") as f:
            f.write(json.dumps(data_list, indent=4, sort_keys=True))

    @classmethod
    def get_parents(cls):
        url = "https://fr-en.openfoodfacts.org/data/taxonomies/categories.json"
        request_data = requests.get(url)
        request_data = request_data.json()
        dict_cpy = request_data.copy()
        for key in dict_cpy.keys():
            if key[0:3] == "en:" and key[3].isalpha():
                pass
            else:
                request_data.pop(key)
        dict_cpy = copy.deepcopy(request_data)
        for categorie, taxonomie in dict_cpy.items():
            if "parents" not in taxonomie:
                request_data.pop(categorie)
                continue
            for key in taxonomie.keys():
                if key != "name" and key != "parents":
                    request_data[categorie].pop(key)
        with open("v2_data_taxonomies_categories.json", "w") as f:
            f.write(json.dumps(request_data, indent=4, sort_keys=True))

    @classmethod
    def make_tree(cls):
        with open("v2_all_categories.json", "r") as f:
            categories = json.load(f)
        for i in range(len(categories)):
            categories[i] = categories[i][3:]
        with open("v2_data_taxonomies_categories.json", "r") as f:
            taxonomie = json.load(f)
        tree_dict = {}
        for child, parents in taxonomie.items():
            for parent in parents["parents"]:
                if parent[3:] in tree_dict:
                    tree_dict[parent[3:]].append(child[3:])
                else:
                    tree_dict[parent[3:]] = [child[3:]]
        """
        with open("v2_tree_dict.json", "w") as f:
            f.write(json.dumps(tree_dict, indent=4, sort_keys=True, ensure_ascii=False))
        """
        without_child = []
        for categorie in categories:
            if categorie not in tree_dict:
                without_child.append(categorie)
        with open("v2_without_child.json", "w") as f:
            f.write(json.dumps(without_child, indent=4, sort_keys=True))

if __name__ == "__main__":
    #ImportData.get_all_categories()
    #ImportData.get_parents()
    ImportData.make_tree()