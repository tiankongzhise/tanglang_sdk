from tkzs_bd_db_tool import get_session,init_db
from .models import TangLangLeadsTable
from typing import List, Dict
import math
from ..logging_config import logger

class DBCURD(object):
    def __init__(self):
        init_db()
    
    def batch_insert_leads(self,data_list:List[Dict], batch_size=100):
        """
        批量处理并插入不存在的记录
        :param data_list: 字典列表，每个字典包含lead信息
        :param batch_size: 每批处理的数量，默认为100
        """
        try:
            # 1. 获取数据库连接
            with get_session() as session:
                # 2. 分批处理
                total_batches = math.ceil(len(data_list) / batch_size)
                inserted_count = 0
                upserted_count = 0

                for batch_num in range(total_batches):
                    start_idx = batch_num * batch_size
                    end_idx = start_idx + batch_size
                    current_batch = data_list[start_idx:end_idx]
                    
                    # 3. 提取当前批次的uuid列表
                    uuids_in_batch = [lead['mts_lead_uuid'] for lead in current_batch if 'mts_lead_uuid' in lead]
                    
                    if not uuids_in_batch:
                        continue
                        
                    # 4. 查询数据库中已存在的uuid
                    existing_uuids = set(
                        session.query(TangLangLeadsTable.mts_lead_uuid)
                        .filter(TangLangLeadsTable.mts_lead_uuid.in_(uuids_in_batch))
                        .all()
                    )
                    existing_uuids = {uuid[0] for uuid in existing_uuids}
                    
                    # 5. 筛选出需要插入的记录
                    records_to_insert = [
                        lead for lead in current_batch 
                        if lead.get('mts_lead_uuid') and 
                        lead['mts_lead_uuid'] not in existing_uuids
                    ]
                    
                    records_to_upsert = [
                        lead for lead in current_batch 
                        if lead.get('mts_lead_uuid') and 
                        lead['mts_lead_uuid'] in existing_uuids
                    ]
                    # 6. 批量插入新记录
                    if records_to_insert:
                        session.bulk_insert_mappings(TangLangLeadsTable, records_to_insert)
                        inserted_count += len(records_to_insert)
                        logger.info(f'Batch {batch_num + 1}: Inserted {len(records_to_insert)} records')

                    if records_to_upsert:
                        session.bulk_update_mappings(TangLangLeadsTable, records_to_upsert)
                        upserted_count += len(records_to_upsert)
                        logger.info(f'Batch {batch_num + 1}: Updated {len(records_to_upsert)} records')

                # 7. 提交事务
                session.commit()
                
            logger.info(f'Total inserted: {inserted_count} records,Total updated: {upserted_count} records')
            return inserted_count,upserted_count
        except Exception as e:
            session.rollback()
            logger.error(f'DBCURD.get_session Error occurred: {e}')
            raise e



