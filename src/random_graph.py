import numpy as np
import logging, math
from heapq import heappush, heappop, heapify

class Vertex(object):
    def __init__(self, index):
        self.index = index
        # `key` is the minimum weight of any edge connecting v to a vertex in the tree
        # 2 for no such edge
        self.key = math.inf
        # `pi` names the parent of this vertex in the tree
        self.pi = None
    def __lt__(self, value):
        if not isinstance(value, Vertex):
            raise TypeError(f'Cannot compare Vertex with {value}')
        return self.key < value.key

    def __str__(self):
        res = f'Vertex: index = {self.index}, key = {self.key}, pi = {self.pi}'

class RandomGraph(object):
    """
    随机图
    """
    def _get_graph(self, n):
        """
        生成随机图，每条边的权值服从均匀分布
        n   顶点个数
        """
        vertices = [Vertex(i) for i in range(n)]
        
        # for i in range(n):
        #     for j in range(i+1, n):
        #         weight = np.random.rand()
        #         vertices[i].adj_list.append((vertices[j], weight))
        #         vertices[j].adj_list.append((vertices[i], weight))
        
        # 虽然生成了 nxn，但是我们只使用其中 i<j 的元素
        adj_matrix = np.random.rand(n, n)

        return [vertices, adj_matrix]
    
    def run(self, n):
        """
        算法运行一次
        1. 从 n 顶点随机图中均匀选取一个（调用 `_get_graph`）
        2. 计算最小生成数，并计算权值
        为了建立 n 与最小生成树权值数学期望之间的关系
        返回一个最小生成树的权值
        """
        # 使用 Prim 算法的话，adj_list 更方便
        [vertices, adj_matrix] = self._get_graph(n)
        
        # Use Prim Algorithm for minimum spanning tree
        # https://www.quora.com/What-is-the-difference-in-Kruskals-and-Prims-algorithm

        # 严格按照《算法导论》进行实现
        
        # logging.debug(f'Adjacent list is below:')
        # for i in range(len(adj_list)):
        #     for j in range(len(adj_list[i])):
        #         logging.debug(f'{i} {adj_list[i][j]}')
        #         # 修改数字为真正的引用，(vertex, weight) 对
        #         adj_list[i][j] = (vertices[adj_list[i][j][0]], adj_list[i][j][1])

        # for i in range(n):
        #     logging.debug(f'vertex[{i}].index = {vertices[i].index}')
        vertices[0].key = 0
        heap = []
        # Q will directly modiify the vertices array
        [heappush(heap, vertex) for vertex in vertices]
        total_weight = 0
        while len(heap) > 0:
            # 每次 heapify 一下
            # https://stackoverflow.com/questions/36876645/unusual-result-from-heappop
            # 非常重要！！！
            heapify(heap)
            u = heappop(heap)
            logging.debug(f'\nvertex {u.index} popped up, weight = {u.key}')
            total_weight += u.key
            # 注意任两个点之间都有边，直接遍历所有点即可
            for v_index in range(n):
                v = vertices[v_index]
                weight = adj_matrix[min(v_index, u.index)][max(v_index, u.index)]
                logging.debug(f'\tvertex {v_index} with weight {weight}')
                if v in heap and weight < v.key:
                    logging.debug(f'\tvertex {v_index} discovered')
                    v.pi = u
                    v.key = weight
                elif not v in heap:
                    logging.debug(f'\tvertex {v_index} ignored (has been poped up)')
                else:
                    logging.debug(f'\tvertex {v_index} ignored (weight not smaller)')

        logging.debug(f'\nTotal weight of the MST is {total_weight}')
        return total_weight