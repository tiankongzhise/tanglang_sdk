from .utils import convert_dict_keys,get_date_range
from .database.curd import DBCURD
from .client import TangLangClient

def fetch_and_insert_all_customers(client:TangLangClient,start_time, end_time, batch_size=1000):
    """
    分页获取所有客户数据并批量插入数据库
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param batch_size: 每页大小(建议1000-5000)
    :return: 插入的总记录数
    """
    db_client = DBCURD()
    total_inserted = 0
    total_upserted = 0
    page_num = 1
    
    while True:
        params = {
            'startTime': start_time,
            'endTime': end_time,
            'pageNum': page_num,
            'pageSize': batch_size
        }
        
        try:
            # 1. 获取分页数据
            rsp = client.query_customer_page_list(params)
            response_data = rsp.to_dict()
            
            # 2. 检查数据是否有效
            if not response_data or not isinstance(response_data, dict):
                print(f"第 {page_num} 页返回数据格式异常")
                break
                
            data = response_data.get('data', [])
            if not data:
                break  # 没有更多数据了
                
            # 3. 转换键名并插入
            new_data = [convert_dict_keys(item) for item in data]
            inserted,upserted = db_client.batch_insert_leads(new_data)
            total_inserted += inserted
            total_upserted += upserted

            
            # 4. 打印进度
            current_count = page_num * batch_size
            total_count = response_data.get('count', 0)
            print(f"已处理 {current_count}/{total_count} 条记录...")
            
            # 5. 检查是否还有下一页
            if len(data) < batch_size:
                break
                
            page_num += 1
            
        except Exception as e:
            print(f"第 {page_num} 页处理失败: {str(e)}")
            break
    
    print(f"总共插入 {total_inserted} 条记录,总共更新 {total_upserted} 条记录")
    return total_inserted

def fetch_and_insert_all_reservation(client:TangLangClient,start_time, end_time, batch_size=1000):
    """
    分页获取所有预约数据并批量插入数据库
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param batch_size: 每页大小(建议1000-5000)
    :return: 插入的总记录数
    """
    db_client = DBCURD()
    total_inserted = 0
    total_upserted = 0

    

    params = {
        'startTime': start_time,
        'endTime': end_time,
    }
    
    try:
        # 1. 获取分页数据
        rsp = client.query_reser_list(params)
        response_data = rsp.to_dict()
        
        # 2. 检查数据是否有效
        if not response_data or not isinstance(response_data, dict):
            print(f"查询预约单返回数据格式异常,{response_data}")
            
        data = response_data.get('data', [])

        # 3. 转换键名并插入
        inserted,upserted = db_client.batch_insert_resv(data)
        total_inserted += inserted
        total_upserted += upserted
    except Exception as e:
        print(f"查询预约单处理失败: {str(e)}")

    
    print(f"预约单总共插入 {total_inserted} 条记录,总共更新 {total_upserted} 条记录")
    return total_inserted
    





def main():
    # 创建客户端实例
    client = TangLangClient()
    
    # 设置起始时间和结束时间
    start_time, end_time = get_date_range('datetime')
    
    # 调用函数获取并插入数据
    # fetch_and_insert_all_customers(client, start_time, end_time)
    fetch_and_insert_all_reservation(client, start_time, end_time)
