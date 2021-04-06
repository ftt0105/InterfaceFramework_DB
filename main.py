from utils.db_handler import DB
from utils.HttpClient import HttpClient
from action.get_rely import GetRely
from action.data_store import RelyDataStore
from action.check_result import CheckResult
from utils.log import *

def main():
    # 第一步，连接数据库，获取接口测试相关数据
    db = DB()  # 创建连接数据库类的实例对象
    # 从数据库中获取需要执行的api集合
    api_list = db.get_api_list()
    for id, api in enumerate(api_list, 1):
        # 首先从api表中获取需要被执行的api集合数据
        api_id = api[0]
        api_name = api[1]
        req_url = api[2]
        req_method = api[3]
        parm_type = api[4]
        # 通过api_id获取它对应的测试用例数据集
        api_case_list = db.get_api_case(api_id)
        print(api_case_list)
        for idx, case in enumerate(api_case_list, 1):
            case_id = case[0]
            req_data = eval(case[2]) if case[2] else {}
            rely_data = eval(case[3]) if case[3] else {}
            protocol_code = case[4]
            data_store = eval(case[6]) if case[6] else {}
            check_point = eval(case[7]) if case[7] else {}
            flag = -1  # -1表示不需要数据依赖，0表示依赖数据替换失败，1表示依赖数据替换成功
            # 第二步，处理数据依赖
            if rely_data:
                flag, req_data = GetRely.get(req_data, rely_data)
            else:
                info("接口[%s]的第%s条用例不需要依赖数据!" % (api_name, idx))

            # 第三步，发送接口请求，执行接口测试用例，并获取响应body
            if flag == 0:
                info("依赖数据未正确替换!")
                continue
            hc = HttpClient()
            responseObj = hc.request(req_url, req_method, parm_type, req_data)
            prot_code = responseObj.status_code
            # 第四步，处理数据依赖存储
            if prot_code == protocol_code:
                res_data = responseObj.json()
                # 说明接口是正常响应的
                if data_store:
                    RelyDataStore.do(data_store, api_name, case_id, req_data, res_data)
                # 第五步，结果校验
                if check_point:
                    error_info = CheckResult.Check(res_data, check_point)
                # 第六步，日志收集、整理并展示
                if error_info:
                    info(error_info)
                    db.write_check_result(case_id, error_info, res_data)
            else:
                info("接口[%s]的用例编号为%s用例的响应协议code=%s,不符合预期code=%s" % (api_name, case_id, prot_code, protocol_code))





if __name__ == "__main__":
    main()











