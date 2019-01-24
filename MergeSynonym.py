"""
merge synonyms
for example, A is similar to B and C, so B is smilar to C
"""
import networkx as nx
def MergeSynonyms(dst,meregeKey="synonym",getNewKey=None):
    G = nx.Graph()
    nodes, edges = [], []
    for k,v in dst.items():
        nodes.append(k)
        for i in v[meregeKey]:
            edges.append((k,i))
            nodes.append(i)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    groups = []
    for i in nx.connected_component_subgraphs(G):
        groups.append(list(i))
    # get new dict
    newDi={}
    otherKeys = list(v.keys()).copy()
    otherKeys.remove(meregeKey)
    for group in groups:
        key = getNewKey(group)
        group.remove(key)
        newDi[key]={meregeKey:group}
        for i in otherKeys:
            newDi[key][i]=[]
            for j in newDi[key][meregeKey]:
                if j in dst:
                    newDi[key][i].extend(dst[j][i])
    return newDi


