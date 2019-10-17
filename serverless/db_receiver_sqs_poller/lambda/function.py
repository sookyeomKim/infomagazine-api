import json
import os
import logging
import pymysql
from user_agents import parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _insert_db_to_rds(event):
    body = json.loads(event['Records'][0]['body'])
    landing_id = body['landing_id']
    data = json.dumps(body['data'])
    schema = json.dumps(body['schema'])
    user_agent = body['user_agent']
    ip_v4_address = body['ip_v4_address']
    inflow_path = body['referer']
    stay_time = body['stay_time']
    registered_date = body['registered_date']

    user_agent_group = {}
    try:
        convert_user_agent = parse(user_agent)
        if body['cloudfront-is-desktop-viewer'] == "true":
            user_agent_group['viewer_type'] = "desktop"
        elif body['cloudfront-is-mobile-viewer'] == "true":
            user_agent_group['viewer_type'] = "mobile"
        elif body['cloudfront-is-smarttv-viewer'] == "true":
            user_agent_group['viewer_type'] = "smarttv"
        elif body['cloudfront-is-tablet-viewer'] == "true":
            user_agent_group['viewer_type'] = "tablet"

        user_agent_group['browser_family'] = convert_user_agent.browser.family
        user_agent_group['browser_family_version_string'] = convert_user_agent.browser.version_string
        user_agent_group['os_family'] = convert_user_agent.os.family
        user_agent_group['os_family_version_string'] = convert_user_agent.os.version_string
        user_agent_group['device_brand'] = convert_user_agent.device.brand
        user_agent_group['device_model'] = convert_user_agent.device.model
    except Exception as e:
        logger.warning(str(e))

    user_agent_group = json.dumps(user_agent_group)

    rds_connection = pymysql.connect(os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASSWD'), database=os.getenv('DB_DATABASE'),
                                     connect_timeout=5,
                                     charset='utf8mb4')

    try:
        with rds_connection.cursor(pymysql.cursors.DictCursor) as cursor:

            insert_sql_command = "INSERT INTO `landing_page_db` (`landing_id`, `data`, `schema`, `user_agent`, `ip_v4_address`, `inflow_path`, `stay_time`, `registered_date`, `created_date`) " \
                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())"
            cursor.execute(insert_sql_command,
                           (landing_id, data, schema, user_agent_group, ip_v4_address, inflow_path, stay_time,
                            registered_date))
            rds_connection.commit()
    except Exception as e:
        logger.warning(str(e))
        logger.warning("Fail.")
    else:
        logger.info("Succeed.")
    finally:
        rds_connection.close()


def lambda_handler(event, context):
    _insert_db_to_rds(event)
