"""
merge synonyms
for example, A is similar to B and C, so B is smilar to C
"""
import networkx as nx
def default_get_new_key(terms,vocab):
    key = max(terms, key=lambda x: vocab[x] if x in vocab else 0)
    return key
class SynonymGroup(object):
    def __init__(self, group_synonym_type, get_new_key):
        self.group_synonym_type = group_synonym_type
        self.get_new_key = get_new_key

    def group_synonyms(self, dst):
        G = nx.Graph()
        nodes, edges = [], []
        for k, v in dst.items():
            nodes.append(k)
            for i in v[self.group_synonym_type]:
                edges.append((k, i))
                nodes.append(i)
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        groups = []
        for i in nx.connected_component_subgraphs(G):
            groups.append(list(i))
        # get new dict
        newDi = {}
        otherKeys = list(v.keys()).copy()
        otherKeys.remove(self.group_synonym_type)
        for group in groups:
            key = self.get_new_key(group)
            group.remove(key)
            newDi[key] = {self.group_synonym_type: group}
            for i in otherKeys:
                newDi[key][i] = []
                for j in newDi[key][self.group_synonym_type]:
                    if j in dst:
                        newDi[key][i].extend(dst[j][i])
        return newDi
