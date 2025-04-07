import re
from typing import Dict, Any, List, Literal,Tuple
from datetime import datetime,timedelta,date

def camel_to_snake(name):
    """
    将驼峰式字符串转换为下划线式
    :param name: 驼峰式字符串，如 'mtsLeadUuid'
    :return: 下划线式字符串，如 'mts_lead_uuid'
    """
    # 处理首字母大写的特殊情况
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # 处理连续大写字母的情况
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def convert_dict_keys(data_dict):
    """
    将字典的所有键从驼峰式转为下划线式
    :param data_dict: 原始字典，如 {'mtsLeadUuid': '123', 'firstName': 'John'}
    :return: 转换后的字典，如 {'mts_lead_uuid': '123', 'first_name': 'John'}
    """
    return {camel_to_snake(key): value for key, value in data_dict.items()}

def get_date_range(date_type:Literal['date','datetime'],date_range_type:Literal['day','year','month']|None=None)->Tuple[str,str]:
    if date_range_type is None:
        print('请输入日期范围类型:天,月,年')
        temp_input  = input()
        if temp_input:
            if temp_input not in ['天','月','年']:
                raise ValueError('请输入正确的日期范围类型:天,月,年')
        else:
            temp_input = '天'
        if temp_input == '天':
            date_range_type = 'day'
        elif temp_input == '月':
            date_range_type = 'month'
        elif temp_input == '年':
            date_range_type = 'year'
        
    
    
    
    define_start_date = ''
    define_end_date = ''
    if date_range_type == 'day':
        temp_start_date = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0)
        temp_end_date = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59)
    elif date_range_type == 'year':
        temp_start_date = datetime(2025,1,1,0,0,0)
        temp_end_date = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59)
    elif date_range_type == 'month':
        temp_start_date = datetime(datetime.now().year, datetime.now().month, 1,0,0,0)
        temp_end_date = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59)
    else:
        raise ValueError('date_range_type must be day, month or year')
    
    if date_type == 'date':
        define_start_date = temp_start_date.strftime('%Y-%m-%d')
        define_end_date = temp_end_date.strftime('%Y-%m-%d')
    elif date_type == 'datetime':
        define_start_date = temp_start_date.strftime('%Y-%m-%d %H:%M:%S')
        define_end_date = temp_end_date.strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise ValueError('date_type must be date or datetime')
    
    
    
    
    if date_type == 'date':
        print('请输入开始时间(格式:yyyy-mm-dd):')
        start_time = input() or define_start_date
        print('请输入结束时间(格式:yyyy-mm-dd):')
        end_time = input() or define_end_date
    elif date_type == 'datetime':
        print('请输入开始时间(格式:yyyy-mm-dd HH:mm:ss):')
        start_time = input() or define_start_date
        print('请输入结束时间(格式:yyyy-mm-dd HH:mm:ss):')
        end_time = input() or define_end_date
    else:
        raise ValueError('date_type参数错误')
    return start_time, end_time
