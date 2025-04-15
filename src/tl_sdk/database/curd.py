from tkzs_bd_db_tool import get_session,init_db
from .models import TangLangLeadsTable,TangLangReservationTable
from typing import List, Dict
import math
from ..logging_config import logger

class DBCURD(object):
    def __init__(self):
        init_db()
    
    def batch_insert_leads(self,data_list:List[Dict], batch_size=1000):
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
                    uuids_in_data = [lead['mts_lead_uuid'] for lead in current_batch if 'mts_lead_uuid' in lead]
                    
                    if not uuids_in_data:
                        print(f'batch_insert_leads->{batch_num}No uuids in data!')
                        continue
                        
                    # 4. 查询数据库中已存在的uuid及其对应的PK (key_id)
                    existing_records_info = session.query(
                        TangLangLeadsTable.mts_lead_uuid,
                        TangLangLeadsTable.key_id # <-- Fetch the primary key
                    ).filter(
                        TangLangLeadsTable.mts_lead_uuid.in_(uuids_in_data)
                    ).all()

                    # Create a mapping from uuid to primary key for quick lookup
                    uuid_to_pk_map = {uuid: pk for uuid, pk in existing_records_info}
                    existing_uuids = set(uuid_to_pk_map.keys()) # Get the set of UUIDs that exist

                    # 5. 准备插入和更新的记录列表
                    records_to_insert = []
                    records_to_update = [] # Renamed for clarity

                    for lead_data in current_batch:
                        lead_uuid = lead_data.get('mts_lead_uuid')
                        if not lead_uuid: # Skip if no uuid
                            continue

                        if lead_uuid not in existing_uuids:
                            # This record is new, prepare for insertion
                            # No PK needed here, DB usually generates it
                            records_to_insert.append(lead_data.copy()) # Use copy
                        else:
                            # This record exists, prepare for update
                            # IMPORTANT: Add the fetched primary key ('key_id')
                            update_mapping = lead_data.copy() # Use copy
                            primary_key = uuid_to_pk_map.get(lead_uuid)
                            if primary_key is None:
                                primary_key = session.query(TangLangLeadsTable.key_id).filter_by(mts_lead_uuid=lead_uuid).scalar()
                            if primary_key is None:
                                logger.error(f'DBCURD.batch_insert_resv->No primary key found for uuid: {lead_uuid}')
                                continue
                            update_mapping['key_id'] = primary_key # Add the PK
                            records_to_update.append(update_mapping)

                    # 6. 批量插入新记录
                    if records_to_insert:
                        session.bulk_insert_mappings(TangLangLeadsTable, records_to_insert)
                        inserted_count += len(records_to_insert)
                        logger.info(f'Batch {batch_num + 1}: Inserted {len(records_to_insert)} records')

                    if records_to_update:
                        session.bulk_update_mappings(TangLangLeadsTable, records_to_update)
                        upserted_count += len(records_to_update)
                        logger.info(f'Batch {batch_num + 1}: Updated {len(records_to_update)} records')
            logger.info(f'Total inserted: {inserted_count} records,Total updated: {upserted_count} records')
            return inserted_count,upserted_count
        except Exception as e:
            logger.error(f'DBCURD.get_session Error occurred: {e}')
            raise e



    def batch_insert_resv(self,data_list:List[Dict], batch_size=5000):
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
                    
                    # 3. 提取当前批次的resv_id列表
                    resv_id_in_batch = [resv['mstResvId'] for resv in current_batch if 'mstResvId' in resv]
                    
                    if not resv_id_in_batch:
                        continue
                        
                     # 4. 查询数据库中已存在的resv_id及其对应的PK (key_id)
                    existing_records_info = session.query(
                        TangLangReservationTable.mstResvId,
                        TangLangReservationTable.key_id # <-- Fetch the primary key
                    ).filter(
                        TangLangReservationTable.mstResvId.in_(resv_id_in_batch)
                    ).all()

                    # Create a mapping from resv_id to primary key for quick lookup
                    resv_id_to_pk_map = {resv_id: pk for resv_id, pk in existing_records_info}
                    existing_uuids = set(resv_id_to_pk_map.keys()) # Get the set of resv_ids that exist

                    

                    # 5. 准备插入和更新的记录列表
                    records_to_insert = []
                    records_to_update = [] # Renamed for clarity

                    for resv_data in current_batch:
                        resv_id = resv_data.get('mstResvId')
                        if not resv_id: # Skip if no resv_id
                            continue

                        if resv_id not in existing_uuids:
                            # This record is new, prepare for insertion
                            # No PK needed here, DB usually generates it
                            records_to_insert.append(resv_data.copy()) # Use copy
                        else:
                            # This record exists, prepare for update
                            # IMPORTANT: Add the fetched primary key ('key_id')
                            update_mapping = resv_data.copy() # Use copy
                            update_mapping['key_id'] = resv_id_to_pk_map[resv_id] # Add the PK
                            records_to_update.append(update_mapping)

                    # 6. 批量插入新记录
                    if records_to_insert:
                        session.bulk_insert_mappings(TangLangReservationTable, records_to_insert)
                        inserted_count += len(records_to_insert)
                        logger.info(f'Batch {batch_num + 1}: Inserted {len(records_to_insert)} records')

                    if records_to_update:
                        print(f"records_to_update: {records_to_update}")
                        session.bulk_update_mappings(TangLangReservationTable, records_to_update)
                        upserted_count += len(records_to_update)
                        logger.info(f'Batch {batch_num + 1}: Updated {len(records_to_update)} records')
            logger.info(f'Total inserted: {inserted_count} records,Total updated: {upserted_count} records')
            return inserted_count,upserted_count
        except Exception as e:
            logger.error(f'DBCURD.get_session Error occurred: {e}')
            raise e
