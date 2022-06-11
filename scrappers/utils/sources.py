
from typing import Any, Dict


cmc_data_source: Dict[str, Any] = {
    "name": "CoinMarketCap News",
    "base_url": "https://coinmarketcap.com",
    "url": "https://coinmarketcap.com/headlines/news/",
    "html": {
        "card_metadata": {
            "card_class": "div@sc-16r8icm-0 sc-5q2msl-0 fFalqR",
            "card_title_class": "a@sc-1eb5slv-0 kLhpLY cmc-link",
            "img_wrapper_class": "div@cover-image",
            "href_class": "a@sc-1eb5slv-0 kLhpLY cmc-link",
            "timestamp_class": "span@sc-1t3hyg7-0 hTMYuT",
            "author_class": "span@sc-1eb5slv-0 ehYyPC",
        },
    }
}

decrypt_data_source: Dict[str, Any] = {
    "name": "Decrypt News",
    "base_url": "https://decrypt.co",
    "url": "https://decrypt.co/news",
    "html": {
        "card_metadata": {
            "card_class": "div@sc-e83fcda8-1 gcNmAw border-b mobileUI:border-r border-decryptGridline",
            "card_title_class": "h2@mb-2 font-ak-bold text-base md:text-xl leading-4.5 md:leading-5.5 text-neutral-900 dark:text-primary-200",
            "img_wrapper_class": "div@md:col-span-3 shrink-0 w-22 md:w-auto mr-3 md:mr-0",
            "href_class": "a@block",
            "timestamp_class": "span@font-ak-regular font-normal text-xs md:text-sm text-neutral-700 dark:text-primary-100 leading-3 md:leading-4 whitespace-nowrap",
            "author_class": "span@font-ak-regular font-normal text-xs md:text-sm text-neutral-700 dark:text-primary-100 leading-3 md:leading-4",
        },
    }
}
