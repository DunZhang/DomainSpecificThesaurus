"""
merge synonyms
for example, A is similar to B and C, so B is smilar to C
"""
import networkx as nx


class SynonymGroup(object):
    """
    class to group synonyms
    """

    def __init__(self, group_synonym_type, domain_vocab):
        """
        :param group_synonym_type: group domain
        :param domain_vocab: dict,key:word, value: word count. the vocabulary of domain-corpus, used to select new key
        """
        self.group_synonym_type = group_synonym_type
        self.domain_vocab = domain_vocab

    def group_synonyms(self, dst):
        """
        group synonyms
        :param dst: dict, the dictionary to be grouped
        :return: dict, grouped dictionary
        """
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
            key = max(group, key=lambda x: self.domain_vocab[x] if x in self.domain_vocab else 0)
            group.remove(key)
            newDi[key] = {self.group_synonym_type: group}
            for i in otherKeys:
                newDi[key][i] = []
                for j in newDi[key][self.group_synonym_type]:
                    if j in dst:
                        newDi[key][i].extend(dst[j][i])
        return newDi
