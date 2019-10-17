import os
import logging
import json
import pymysql
from user_agents import parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _response_format(status_code: int = None, state: bool = None, message: str = None,
                     headers: dict = None) -> dict:
    dict_to_return = {
        "statusCode": status_code
    }

    if headers:
        dict_to_return.update({"headers": headers})

    if message:
        body = {
            "state": state,
            "message": message
        }
        dict_to_return.update({"body": json.dumps(body)})
    return dict_to_return


def _send_to_sqs(event, response_headers):
    headers = event['headers']
    referer = headers['referer']
    user_agent = headers['user-agent']
    ip_v4_address = headers['x-forwarded-for'].split(",")[0]
    event_body = event['body']
    body = json.loads(event_body)
    inflow_path = referer.split("/")[4]

    db_key_list = body.keys()
    if 'data' not in db_key_list or 'schema' not in db_key_list:
        return _response_format(status_code=500, headers=response_headers, state=False, message='유효한 db가 아닙니다')

    rds_connection = pymysql.connect(os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASSWD'), database=os.getenv('DB_DATABASE'),
                                     connect_timeout=5,
                                     charset='utf8mb4')

    exist_check = False

    with rds_connection.cursor(pymysql.cursors.DictCursor) as cursor:
        try:
            for key, item in body['schema'].items():
                if item in ['전화번호', '핸드폰번호', '연락처']:
                    key_to_search = key
                    value_to_search = body['data'][key_to_search]
                    json_exist_sql_command = f"""
                                    SELECT COUNT(*) AS '__count'
                                    FROM `landing_page_db` db
                                    WHERE landing_id = '{body['landing_id']}' 
                                    AND JSON_EXTRACT(db.data, "$.{key_to_search}") = '{value_to_search}'
                                """
                    cursor.execute(json_exist_sql_command)
                    get_count = cursor.fetchone()
                    if get_count['__count'] > 0:
                        exist_check = True
                    break

            if exist_check:
                return _response_format(status_code=200, headers=response_headers, state=False, message='이미 등록됐습니다')

            user_agent_group = {}

            try:
                convert_user_agent = parse(user_agent)
                if headers['cloudfront-is-desktop-viewer'] == "true":
                    user_agent_group['viewer_type'] = "desktop"
                elif headers['cloudfront-is-mobile-viewer'] == "true":
                    user_agent_group['viewer_type'] = "mobile"
                elif headers['cloudfront-is-smarttv-viewer'] == "true":
                    user_agent_group['viewer_type'] = "smarttv"
                elif headers['cloudfront-is-tablet-viewer'] == "true":
                    user_agent_group['viewer_type'] = "tablet"

                user_agent_group['browser_family'] = convert_user_agent.browser.family
                user_agent_group['browser_family_version_string'] = convert_user_agent.browser.version_string
                user_agent_group['os_family'] = convert_user_agent.os.family
                user_agent_group['os_family_version_string'] = convert_user_agent.os.version_string
                user_agent_group['device_brand'] = convert_user_agent.device.brand
                user_agent_group['device_model'] = convert_user_agent.device.model
            except Exception as e:
                logger.warning(str(e))

            insert_sql_command = "INSERT INTO `landing_page_db` (`landing_id`, `data`, `schema`, `user_agent`, `ip_v4_address`, `inflow_path`, `stay_time`, `registered_date`, `created_date`) " \
                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())"

            cursor.execute(insert_sql_command,
                           (body['landing_id'], json.dumps(body['data']), json.dumps(body['schema']), json.dumps(user_agent_group), ip_v4_address,
                            inflow_path, body['stay_time'],
                            body['registered_date']))
            rds_connection.commit()
        except Exception as e:
            logger.warning(str(e))
            logger.warning("DB insertion failed.")
            return _response_format(status_code=500, headers=response_headers, message='신청 실패')
        else:
            logger.info("DB insertion was successful.")
            return _response_format(status_code=200, headers=response_headers, state=True, message='신청이 완료됐습니다')


def lambda_handler(event, context):
    response_headers = {
        "Access-Control-Allow-Origin": os.getenv('WHITE_LIST'),
        "Content-Type": "application/json"
    }
    try:
        if event['httpMethod'] == 'OPTIONS':
            response_headers.update({
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "text/plain; charset=utf-8",
                "Content-Length": "0"
            })
            return _response_format(status_code=204, headers=response_headers)
        elif event['httpMethod'] == 'POST':
            if not event['body']:
                return _response_format(status_code=500, headers=response_headers, message='빈 데이터')
            return _send_to_sqs(event, response_headers)
    except Exception as e:
        logger.warning(str(e))
        return _response_format(status_code=500, headers=response_headers, message='서버 오류')
