from collections import defaultdict
class Graph:
    contagem = 0
    valuesdict = {}
    def __init__(self):
        self.graph = defaultdict(list)
    def addEdge(self,u,v):
        self.contagem += 1
        self.graph[u].append(v)
        self.valuesdict[u]=  False
        self.valuesdict[v] = False

    def topologicalSortUtil(self,key,stack):
        # Mark the current node as visited.

        self.valuesdict[key] = True
        # Recur for all the vertices adjacent to this vertex
        #print(self.graph)
        for i in self.graph[key]:
            #print(i)
            #print(self.graph[key])
            if self.valuesdict[i] == False: #esta tentando com 18000
                self.topologicalSortUtil(i,stack)
        # Push current vertex to stack which stores result
        stack.insert(0,key)

    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited

       # visited = [False]*self.contagem
        stack =[]


        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one

        for key, value in self.valuesdict.items():

            if value == False:
                self.topologicalSortUtil(key,stack)
		# Print contents of stack
        print (stack)
        return stack
