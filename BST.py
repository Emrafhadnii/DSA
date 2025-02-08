class Node:
    def __init__(self,value:int = 0):
        self.value = value
        self.top = None
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    def insert(self, value:int):
        tempnode = Node(value)
        if self.root is None:
            self.root = tempnode
            self.root.top = None
        else:
            p = self.root
            while True:
                if value > p.value:
                    if p.right is None:
                        p.right = tempnode
                        tempnode.top = p
                        break
                    else:
                        p = p.right
                else:
                    if p.left is None:
                        p.left = tempnode
                        tempnode.top = p
                        break
                    else:
                        p = p.left
    def delete(self, value):
        p = self.root
        while p is not None:
            if p.value == value:
                if p.left and p.right:
                    temp = p.right
                    while temp.left is not None:
                        temp = temp.left
                    p.value = temp.value
                    if temp.top.left == temp:
                        temp.top.left = temp.right
                    else:
                        temp.top.right = temp.right
                    if temp.right:
                        temp.right.top = temp.top
                elif p.left or p.right:
                    temp = p.left if p.left else p.right
                    if p != self.root:
                        toptemp = p.top
                        if toptemp.left == p:
                            toptemp.left = temp
                        else:
                            toptemp.right = temp
                    else:
                        self.root = temp
                    p = None
                else:
                    if p.top is None:
                        self.root = None
                    else:
                        if p.top.left == p:
                            p.top.left = None
                        else:
                            p.top.right = None
                break
            elif p.value < value:
                if p.right is not None:
                    p = p.right
                else:
                    break
            else:
                if p.left is not None:
                    p = p.left
                else:
                    break

    def search(self,value):
        p = self.root
        while p is not None:
            if p.value == value:
                return True
            elif value < p.value:
                p = p.left
            else:
                p = p.right
        return False

    def printBST(self,node:Node):
        if node:
            self.printBST(node.left)
            print(node.value,' ')
            self.printBST(node.right)
x = BinarySearchTree()
x.insert(5)
x.insert(15)
x.insert(3)
x.insert(7)
x.insert(12)
x.insert(18)
x.delete(12)
print(x.search(12))
print(x.search(3))
x.printBST(x.root)