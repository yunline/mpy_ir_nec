class QueueEmptyError(Exception):pass
class Queue:
    class Node:
        def __init__(self,left=None,data=None,right=None):
            self.data=data
            self.left=left
            self.right=right
    def __init__(self,size=0):
        self.left_in=None#左进右出
        self.right_out=None
        self.size=size
        self.length=0
    def __len__(self):return self.length
    def __iter__(self):return self.iter()
    def iter(self):#从左到右迭代（我觉得要改
        if self.right_out==None:
            return
        pointer=self.right_out
        yield pointer.data
        while pointer.left!=None:
            pointer=pointer.left
            yield pointer.data
    def put(self,data):
        if self.length>=self.size and self.size!=0:#处理溢出
            self.right_out=self.right_out.left
            self.right_out.right=None

        if self.left_in==None:#如果队列为空
            self.left_in=self.Node(data=data)
            self.right_out=self.left_in
            self.length=0
        else:
            tmp=self.left_in
            self.left_in=self.Node(data=data,right=tmp)
            tmp.left=self.left_in
        self.length+=1
            
    def get(self):
        if self.right_out==None:
            raise QueueEmptyError("Queue is empty")
        elif self.right_out!=self.left_in:
            tmp=self.right_out
            self.right_out=tmp.left
            tmp.left.right=None
            self.length-=1
            return tmp.data
        else:
            tmp=self.right_out
            self.right_out=self.left_in=None
            self.length=0
            return tmp.data