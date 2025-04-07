import hashlib
import json

from datetime import datetime
import requests
from typing import List, Dict, Any,Literal
import os
from dotenv import load_dotenv
from .models import KeyChoice

from .logging_config import logger

load_dotenv()



class ResponseBaseDTO:
    def __init__(self, code: int = 0, message: str = "", data: List[Any] = None, count:int = 0):
        self.code = code
        self.message = message
        self.data = data if data is not None else []
        self.count = count
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data,
            'count': self.count,
        }

class TangLangBaseClient(object):
    _post_url_mapping = {
        '/ShiXinCustomerCon/queryCustomerByIdOwner':'key2',
        '/ShiXinCustomerCon/queryCustomerByIdOrPhone':'key2',
        '/ShiXinCustomerCon/queryCustomerPageList':'key2',
        '/scrmCustomerApiCon/querySimpleCustomerPageList':'key2',
        '/scrmCustomerApiCon/queryCustomerPageList':'key2',
        '/ShiXinVisitCon/queryVisitList':'key2',
        '/ShiXinReserCon/queryReserList':'key2',
        '/syncApi/queryOrder':'key3',
    }
    
    
    
    
    def __init__(self,company_id:int = 0,key1: str ='',key2: str='',key3: str = '',host1:str='',host2:str='',host3:str=''):
        self.key1 = key1 if key1 != '' else os.getenv('KEY1')
        self.key2 = key2 if key2 != '' else os.getenv('KEY2')
        self.key3 = key3 if key3 != '' else os.getenv('KEY3')
        self.host1 = host1 if host1 != '' else os.getenv('HOST1')
        self.host2 = host2 if host2 != '' else os.getenv('HOST2')
        self.host3 = host3 if host3 != '' else os.getenv('HOST3')
        self.company_id = company_id if company_id != 0 else int(os.getenv('COMPANY_ID'))
        
    def md5(key_str: str) -> str:
        try:
            digest_obj = hashlib.md5(key_str.encode('utf-8'))
            digest = digest_obj.digest()
            sb = []
            for byte in digest:
                sb.append(format((byte & 255) + 256, 'x')[1:])
            result = ''.join(sb)
            logger.debug(f"The original key {key_str}, md5 key {result}")
            return result
        except Exception as e:
            raise Exception("MD5 is not supported!") from e
    @staticmethod
    def create_timestamp() -> int:
        return int(datetime.now().timestamp() * 1000)
    def create_token(self,timestamp:int,key: KeyChoice)->str:
        key = f"{getattr(self,key.data)}{timestamp}"
        self.token = TangLangBaseClient.md5(key)
        return self.token
    
    def create_key_choice(self,key: Literal['key1','key2'])->KeyChoice:
        return KeyChoice(data=key)
    
    def create_common_query(self,key: KeyChoice)-> Dict[str, int|str]:
        timestamp = self.create_timestamp()
        token = self.create_token(timestamp,key)
        logger.debug(f'timestamp:{timestamp}')
        logger.debug(f'token:{token}')
        return {
            'time': timestamp,
            'companyId': self.company_id,
            'token':token
        }
    def create_host_url(self,post_url:str)->str:
        if self._post_url_mapping.get(post_url) is None:
            raise ValueError(f'{post_url} is not in post_url_mapping')
        # if 'sync' in post_url:
        #     return self.sync_host
        
        key = self._post_url_mapping.get(post_url)
        if key == 'key1':
            return self.host1
        elif key == 'key2':
            return self.host2
        elif key == 'key3':
            return self.host3
        else:
            raise ValueError(f'create_host_url post_url:{post_url} 通过post_url_mapping 返回了意料之外的 {key}')

    
    def post_url_to_key_choice(self,post_url:str)->KeyChoice:
        key = self._post_url_mapping.get(post_url)
        if key is None:
            raise ValueError(f'post_url:{post_url} is not found in _post_url_mapping')
        return KeyChoice(data=key)
    
    def base_req(self,post_url:str,params:Dict)->ResponseBaseDTO:
        logger.debug(f"base_req-post_url:{post_url},params:{params}")
        try:
            headers = {
                "Content-Type": "application/json;charset=utf-8"
            }
            
            req_url = f'{self.create_host_url(post_url)}{post_url}'
            logger.debug(f"base_req-req_url:{req_url}")
            key_choice = self.post_url_to_key_choice(post_url)
            params.update(self.create_common_query(key_choice))
            
            logger.debug(f'post_url:{post_url},data:{params}')
            
            response = requests.post(
            req_url,
            headers=headers,
            json=params,
            timeout=120 # 120 seconds for both connect and read
        )
            if response.status_code == 200:
                resp_text = response.text
                logger.debug(f"base_req-RES:{resp_text}")
            
                if resp_text:
                    try:
                        resp_data = json.loads(resp_text)
                        result = ResponseBaseDTO()
                        result.code = resp_data.get('code', 0)
                        result.message = resp_data.get('message', '')
                        result.data = resp_data.get('data', [])
                        result.count = resp_data.get('count', 0)
                        return result
                    except json.JSONDecodeError:
                        return ResponseBaseDTO(-99, "Invalid JSON response")
                else:
                    return ResponseBaseDTO(-99, "接口请求失败，返回NULL,response.text:{response.text},response.content:{response.content},response.status_code:{response.status_code}")
            else:
                return ResponseBaseDTO(-99, f"接口请求失败，HttpStatus:{response.status_code}")
            
        except Exception as e:
            logger.error("base_req-ERROR:", exc_info=True)
            return ResponseBaseDTO(-99, f"接口请求失败，ERROR:{str(e)}") 

class TangLangClient(TangLangBaseClient):
    def __init__(self, company_id:int = 0,key1: str ='',key2: str='',host1:str='',host2:str=''):
        super().__init__(company_id=company_id,key1=key1,key2=key2,host1=host1,host2=host2)
    
    def query_customer_page_list(self,params:dict) ->ResponseBaseDTO:
        port_url = '/ShiXinCustomerCon/queryCustomerPageList'
        return self.base_req(port_url,params)
    
    def scrm_query_simple_customer_page_list(self,params:dict)->ResponseBaseDTO:
        post_url  = '/scrmCustomerApiCon/querySimpleCustomerPageList'
        return self.base_req(post_url,params)
        ...
    def scrm_query_customer_page_list(self,params:dict)->ResponseBaseDTO:
        post_url  = '/scrmCustomerApiCon/queryCustomerPageList'
        return self.base_req(post_url,params)
    def query_visit_list(self,params:dict)->ResponseBaseDTO:
        post_url  = '/ShiXinVisitCon/queryVisitList'
        return self.base_req(post_url,params)

    def query_reser_list(self,params:dict)->ResponseBaseDTO:
        post_url  = '/ShiXinReserCon/queryReserList'
        return self.base_req(post_url,params)
    def query_order(self,params:dict)->ResponseBaseDTO:
        post_url  = '/syncApi/queryOrder'
        return self.base_req(post_url,params)
