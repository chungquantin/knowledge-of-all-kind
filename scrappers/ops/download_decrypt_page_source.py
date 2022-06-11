from utils import *

from dagster import op

@op(config_schema={"url": str})
def download_decrypt_page_source(context):
    url = context.op_config["url"]
    return HeadlessBrowser().get_ssg_page_source(url)
