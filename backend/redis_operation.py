from redis_initialise import *
class redis_operation():
    def __init__(self) :
        self.operator=redis_initialise()
    def get(self,q,order):

        q=q.strip()
        final=q+" "+order
        
        
        if self.operator.redis.llen(final)!=0:
            output=self.operator.redis.lrange(final,0,-1)
            
        else:
            
            return 0
        length=self.operator.redis.llen(final)
        k=[]
        final=[]
        print(length)
        for j in range(length-1,-1,-1):
            k.append(output[j].decode())
            if j%5==0:
                final.append(k)
                k=[]
        # print(final)
        return final
    def set(self,q,order,result):
        q=q.strip()
        final=q+" "+order
        for i in result:
            for j in i:
                self.operator.redis.lpush(final,str(j))
        #print(self.operator.redis.lrange(final,0,-1))
        return {"redis":"insertion successfull"}
        
