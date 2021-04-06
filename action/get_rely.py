from utils.md5_encrypt import md5_encrypt
from utils.db_handler import DB
import copy

class GetRely(object):
    def __init__(self):
        pass

    @classmethod
    def get(cls, data_source, rely_data, header_source = {}):
        data = copy.deepcopy(data_source)
        db = DB()
        # 1表示依赖数据处理完毕，0表示未获取到被依赖的数据
        flag = 1
        for key, value in rely_data.items():
            for k, v in value.items():
                api_name, case_id = k.split("->")
                api_id = db.get_api_id(api_name)
                store_rely_data = db.get_rely_data(api_id, int(case_id))
                for i in v:
                    if key == "request":
                        if i in store_rely_data["request"][api_name][int(case_id)]:
                            if i == "password":
                                password = md5_encrypt(store_rely_data["request"][api_name][int(case_id)][i])
                                data[i] = password
                            else:
                                data[i] = store_rely_data["request"][api_name][int(case_id)][i]
                            flag =1
                        else:
                            flag = 0
                    elif key == "response":
                        if i in store_rely_data["response"][api_name][int(case_id)]:
                            data[i] = store_rely_data["response"][api_name][int(case_id)][i]
                            flag = 1
                        else:
                            flag = 0
        return flag, data

if __name__ == "__main__":
    data_source = {"username":"lilydsd23", "password":"ssd32de2", "code":"01"}
    rely_data = {"request":{"用户注册->1":["username","password"]},
                 "response":{"用户注册->1":["code"]}}
    flag, data = GetRely.get(data_source, rely_data)
    print(flag)
    print(data)



