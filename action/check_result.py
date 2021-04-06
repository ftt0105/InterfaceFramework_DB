import re

class CheckResult(object):
    def __init__(self):
        pass
    @classmethod
    def Check(self,responseObj,checkPonit):
        errorKey={}
        for key,value in checkPonit.items():
            s_data = responseObj.get(key,None)
        #{"code": "00", "userid": {"type": "N"}, "id": {"value": "^\d+$"}}
            if not s_data:
                errorKey[key] = "not exists"
                continue
            if isinstance(value,(str,int)):
                #说明是等值校验
                if s_data!=value:
                    errorKey[key] = s_data

            elif isinstance(value,dict):
                #说明需要通过正则校验或数据类型校验
                if "type" in value:
                    #说明是数据类型校验
                    typeS = value["type"]
                    if typeS == "N":
                        if not isinstance(s_data,int):
                            errorKey[key] = s_data
                    elif typeS == "S":
                        if not isinstance(s_data,str):
                            errorKey[key] = s_data
                    elif typeS == "***":
                        pass
                elif "value" in value:
                    #说明是正则表达式校验
                    reStr = value ["value"]
                    rg = re.match(reStr, "%s" %s_data)
                    if not rg:
                        errorKey[key]=s_data

        return errorKey

if __name__ == "__main__":
    responseObj = {"code":"00","userid":"abd","id":"1213"}
    checkPonit = {"code":"00","userid":{"type":"S"},"id":{"value":"^\d+$"},"username":{"type":"S"}}
    result = CheckResult.Check(responseObj,checkPonit)
    print("responseObj:",responseObj)
    print("checkPonit:",checkPonit)
    print(result)