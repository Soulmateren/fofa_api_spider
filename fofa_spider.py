#_*_coding:utf-8_*_
# author = jsoned@163.com
import fofa
import redis
import pickle
import sys
# 输入自己的fofa 账号，key
email, key = ("", "")
client = fofa.Client(email,key)
list_result=[]

def search_result(search):
    # fofa 搜索结果
    try:
        query_str = '%s && header = "HTTP/1.1 200 OK" && country=CN'%search
        for page in range(1,2):
            data = client.get_data(query_str,page=page)['results']
            for i in data:
                if "http" in i:
                    pass
                else:
                    i = "http://" + i
                    print i
                    list_result.append(i)
        try:
            redis_edit(search,list_result)
        except:
            pass
    except:
        pass

class Redis:
    @staticmethod
    def connect():
        r = redis.StrictRedis(host='localhost', port=6379)
        return r
    # 将内存数据二进制通过序列号转为文本流，再存入redis
    @staticmethod
    def set_data(r, key, data, ex=None):
        r.set(key, pickle.dumps(data), ex)

    # 将文本流从redis中读取并反序列化，返回返回
    @staticmethod
    def get_data(r, key):
        data = r.get(key)
        if data is None:
            return None
        return pickle.loads(data)

def redis_edit(toal,list):
    # 生成key列表
    total_key_list = []
    total_value_list = list
    for number in range(1,99999):
        total_key = toal+str(number)
        total_key_list.append(total_key)
    try:
        r=Redis.connect()
        # key 去重
        key_list = r.keys()
        for key_ed in key_list:
            if key_ed in total_key_list:
                total_key_list.remove(key_ed)
            else:
                continue
        # value 去重
        for key_ed in key_list:
            value_ed = Redis.get_data(r,key_ed)
            if value_ed in total_value_list:
                total_value_list.remove(value_ed)
            else:
                continue
        # 新加数据存入redis
        for i in range(0,len(total_value_list)+1):
            key_result = total_key_list[i]
            value_result = total_value_list[i]
            Redis.set_data(r,key_result,value_result)
    except:
        pass

def redis_del():
    # 清空redis
    try:
        r = Redis.connect()
        r.flushdb()
        print "Success delete!"
    except:
        pass
def redis_read():
    # 读取redis
    try:
        r = Redis.connect()
        keys = r.keys()
        for key in keys:
            #if search in key:
            data = Redis.get_data(r,key)
            print data
    except:
        pass

def main():
    # search = "thinkphp"
    argv = sys.argv[1]
    if argv == "-h":
        print """
        use: python fofa_spider.py search_total
        -h help
        -d delete all data!
        -r read all data!
        """
    elif argv == "-d":
        redis_del()
    elif argv == "-r":
        redis_read()
    else:
        search = sys.argv[1]
        search_result(search)

if __name__ == '__main__':
    main()
