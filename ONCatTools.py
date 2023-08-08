class filterObj:

    category = 'str'
    value=None
    condition='=='
    target=None

    def __init__(self,item,condition,target,tolerance=0.0):
        self.item = item
        self.target = target
        self.condition = condition
        self.tolerance = tolerance

    # def setValue(self,value):
    #     self.value = value

    def checkMatch(self,value):
        # self.value = value
        if isinstance(self.target,str):
            if self.condition == '==':
                return self.target.lower() == value.lower() #case insensitive match
            elif self.condition == 'contains':
                return self.target.lower() in value.lower()
        elif isinstance(self.target,int):
            if self.condition == '<':
                return value<self.target
            if self.condition == '<=':
                return value<=self.target
            if self.condition == '>':
                return value>self.target
            if self.condition == '>=':
                return value>=self.target
            if self.condition == '==':
                return value==self.target
        elif isinstance(self.target,float):
            if self.condition == '~=':
                return (self.target-self.tolerance)<value<(self.target+self.tolerance)
            elif self.condition == '<':
                return value<self.target
            if self.condition == '<=':
                return value<=self.target
            if self.condition == '>':
                return value>self.target
            if self.condition == '>=':
                return value>=self.target
            if self.condition == '==':
                return value==self.target
            