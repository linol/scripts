# use from the github project : https://github.com/tobyqin/xmindparser
# the project is here to define functions on mind map xmind
# like search, xmind comparare (other xmind), get breadcrumb node
import re
from .xmindparser import *
import copy

class XmindTools():
    xmindContent={}
    node_separator = '-'
    root=[]
    root_breadcrumb=[]

    def __init__(self,filename,root=None):
        # todo : gestion des erreurs
        self.xmindContent=xmind_to_dict(filename)[0]['topic']
        if root is not None:
            self.root_breadcrumb = self.getBreadcrumb(root)
            self.root = list(map(lambda x: int(x),root.split(self.node_separator)))
            self.xmindContent = self.getNode(root)

        # todo faire une fonction "check path"


    # sur le même modèle que la fonction précédente
    def contains(self,pattern,node=None):
        """
        cherche dans toutes les listes et suivants tous les sujets qui contiennent la regex précisé
        """
        xmTarget = self.getNode(node)
        def find(d,pattern,datas,path=[]) :
            r = re.search(pattern, d['title'],re.IGNORECASE)
            if r :
                nodepath = self.node_separator.join(list(map(lambda x : str(x),path)))
                datas.append({'title':d['title'],'node':nodepath})

            if 'topic' in d.keys():
                find(d['topic'], pattern,datas,path)
            if 'topics' in d.keys():
                p = path
                for n in range(len(d['topics'])):
                    find(d['topics'][n], pattern,datas,p+[n])
        datas=[]
        find(xmTarget,pattern,datas,self.root)
        return datas

    def getMakers(self,node=None):
        xmTarget = self.getNode(node)
        def findMaker(d,datas,path=[]) :
            if 'makers' in d.keys():
                for maker in d['makers']:
                    if maker not in datas:
                        datas[maker]=[]
                    nodepath = self.node_separator.join(list(map(lambda x: str(x), path)))
                    nd= {'title': d['title'],'node': nodepath}
                    if  'link' in d :
                        nd['link']=d['link']

                    datas[maker].append(nd)
            if 'topic' in d.keys():
                findMaker(d['topic'],datas,path)
            if 'topics' in d.keys():
                p = path
                for n in range(len(d['topics'])):
                    findMaker(d['topics'][n],datas,p+[n])
        datas={}
        findMaker(xmTarget,datas,self.root)
        return datas

    def getMaker(self,maker,node=None):
        xmTarget = self.getNode(node)
        def findMaker(d,maker,datas,path=[]) :
            if 'makers' in d.keys():
                if maker in d['makers']:
                    nodepath = self.node_separator.join(list(map(lambda x : str(x),path)))
                    datas.append({'title':d['title'],'node':nodepath})

            if 'topic' in d.keys():
                findMaker(d['topic'], maker,datas,path)
            if 'topics' in d.keys():
                p = path
                for n in range(len(d['topics'])):
                    findMaker(d['topics'][n], maker,datas,p+[n])
        datas=[]
        findMaker(xmTarget, maker,datas,self.root)
        return datas



    def countMakers(self,node=None,path=[]):
        # todo : verification sur le format de "node"
        def findMakers(d,makers) :
            if 'makers' in d.keys():
                for maker in d['makers']:
                    if maker in makers.keys():
                        makers[maker]+=1
                    else :
                        makers[maker]= 1
            if 'topic' in d.keys():
                findMakers(d['topic'], makers)
            if 'topics' in d.keys():
                for n in range(len(d['topics'])):
                    findMakers(d['topics'][n], makers)
        makers={}
        xmTarget = self.getNode(node)
        findMakers(xmTarget, makers)
        return makers
    


    def countItems(self,type='labels',node=None,path=[]):
        # todo : verification sur le format de "node"
        def findtypes(d,type,types) :
            if type in d.keys():
                for type in d[type]:
                    if type in types.keys():
                        types[type]+=1
                    else :
                        types[type]= 1
            if 'topic' in d.keys():
                findtypes(d['topic'],type, types)
            if 'topics' in d.keys():
                for n in range(len(d['topics'])):
                    findtypes(d['topics'][n],type, types)
        types={}
        xmTarget = self.getNode(node)
        findtypes(xmTarget,type,types)
        return types


    def getItems(self,type='title',node=None):
        xmTarget = self.getNode(node)
        def findType(d,type,datas,path=[]) :
            if type in d.keys():
                print(d.keys())
                print(d[type])
            if 'topic' in d.keys():
                findType(d['topic'],type,datas,path)
            if 'topics' in d.keys():
                p = path
                for n in range(len(d['topics'])):
                    findType(d['topics'][n],type,datas,p+[n])
        datas={}
        findType(xmTarget,type,datas,self.root)
        return datas

    def getLabels(self,node=None):
        xmTarget = self.getNode(node)
        def findType(d,datas,path=[]) :
            if 'labels' in d.keys():
                print(node)
                print(d['title'])
                for label in d['labels']:
                    if label not in datas:
                        datas[label]=[]
                    nodepath = self.node_separator.join(list(map(lambda x: str(x), path)))
                    data = {'title': d['title'],'node': nodepath}
                    if 'makers' in d:
                        data['makers']=d['makers']
                    datas[label].append(data)
            if 'topic' in d.keys():
                findType(d['topic'],datas,path)
            if 'topics' in d.keys():
                p = path
                for n in range(len(d['topics'])):
                    findType(d['topics'][n],datas,p+[n])
        datas={}
        findType(xmTarget,datas,self.root)
        return datas


    # cible une partie de la carte
    def getNode(self,node=None):
        # todo : verification sur le format de "node"
        xmTarget = self.xmindContent # from root
        if node is None :
            return xmTarget
        indexes = list(map(lambda x : int(x),node.split(self.node_separator)))
        for i in indexes :
            xmTarget = xmTarget['topics'][i]
        return xmTarget

    # cible une partie de la carte
    def getBreadcrumb(self,node=None):
        if node is None:
            return self.root_breadcrumb
        xmTarget = self.xmindContent # from root
        indexes = list(map(lambda x : int(x),node.split(self.node_separator)))
        breadcrumb = copy.copy(self.root_breadcrumb)
        path = list(map(lambda x: str(x),self.root))
        for i in indexes[len(breadcrumb):]:
            xmTarget = xmTarget['topics'][i]
            path.append(str(i))
            breadcrumb.append({'title':xmTarget['title'],'node':self.node_separator.join(path)})
        return breadcrumb

    def getChild(self):
        # print(self.xmindContent.items())
        return self.xmindContent.items()

    def getTopics(self,item='title'):
        return [topic[item] for topic in self.xmindContent['topics']]  
    
if __name__ == '__main__':
    xt = XmindTools('example.xmind')
    print(xt.xmindContent)
