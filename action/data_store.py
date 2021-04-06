from utils.db_handler import DB

class RelyDataStore(object):
    def __init__(self):
        pass

    @classmethod
    def do(cls, store_point, api_name, case_id, req_source, res_source):
        '''实现被依赖数据存储逻辑处理'''
        #tmp字典，用来生成数据库中data_store字段的格式。
        tmp = {"request":{}, "response":{}}
        """
        需要存入数据库的格式：
                {"request": ["username", "password"]}

                {'request': {'用户注册':
                                 {1:
                                      {'username': 'zhangsan123',
                                      'password': 'zhagn123zhagn'}
                                  }
                             },
                 'response': {'用户注册':
                                  {1:
                                       {'code': '00'}
                                   }
                              }
                 }

        """
        for key, value in store_point.items():
            if key == "request":
            # 说明取的是被依赖接口请求参数中的数据
                for i in value:
                    if i in req_source:
                        val = req_source[i]
                        if api_name not in tmp["request"]:
                            tmp["request"] = {api_name: {case_id: {i: val}}}
                        elif case_id not in tmp["request"][api_name]:
                            tmp["request"][api_name] = {case_id: {i: val}}
                        else:
                            tmp["request"][api_name][case_id][i] = val
                    else:
                        print("字段[%s]在原始数据源req_source中不存在！" %i)
            elif key == "response":
            # 说明取的是被依赖接口响应body中的数据
                for i in value:
                    if i in res_source:
                        val = res_source.get(i)
                        if api_name not in tmp["response"]:
                            tmp["response"] = {api_name: {case_id: {i:val}}}
                        elif case_id not in tmp["response"][api_name]:
                            tmp["response"][api_name] = {case_id: {i:val}}
                        else:
                            tmp["response"][api_name][case_id][i] = val
                    else:
                        print("字段[%s]在原始数据源res_source中不存在！" % i)

        # 将处理好的被依赖数据存入数据库中
        if tmp["request"] or tmp["response"]:
            db = DB()
            api_id = db.get_api_id(api_name)
            db.update_store_data(api_id, case_id, tmp)


















