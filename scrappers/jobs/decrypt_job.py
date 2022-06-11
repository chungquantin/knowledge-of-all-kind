from dagster import job

from ops import download_decrypt_page_source, scrap_decrypt


decrypt_news_job_config = {
    "ops": {
        "download_decrypt_page_source": {
            "config": {
                "url": "https://decrypt.co/news"
            }
        }
    }
}


@job(description="Process to scrap Decrypt news", config=decrypt_news_job_config)
def decrypt_news_job():
    page_source = download_decrypt_page_source()
    data = scrap_decrypt(page_source)
    # save_json_file("dataset/decrypt.json", data)
