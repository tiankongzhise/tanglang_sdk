import re

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