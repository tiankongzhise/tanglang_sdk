from src.tl_sdk.client import TangLangClient
from src.tl_sdk.utils import get_data



def test_sm():
    client = TangLangClient()
    start_time,end_time = get_data('datetime')
    params = {
        'startTime':start_time,
        'endTime':end_time,
    }
    rsp = client.query_reser_list(params)
    temp_dict = rsp.to_dict()['data']
    statusCode = set()
    sm = 0
    bm = 0
    dj = 0
    for i in temp_dict:
        statusCode.add(i['statusCode'])
        if i['statusCode'] == '到访未报名':
            sm += 1
        elif i['statusCode'] == '报名':
            bm += 1
        elif i['statusCode'] == '定金':
            dj += 1
        else:
            pass
    print(f'statusCode: {statusCode},上门:{sm},报名:{bm},定金:{dj}')

def test_bm():
    client = TangLangClient()
    start_time, end_time = get_data('datetime')
    params = {
        'startTime':start_time,
        'endTime':end_time,
    }
    rsp = client.query_order(params)
    data = rsp.to_dict()
    print(data)


if __name__ == '__main__':
    test_bm()


