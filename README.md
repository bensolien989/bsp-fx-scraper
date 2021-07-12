# bsp-fx-scraper
BSP Exchange Rate calculator Scraper.

Modules you'll need to pip install:
1. requests
2. bs4
3. lxml

```bash
sudo pip install requests bs4 lxml
```

## Fair use:
The information provided by this script is freely available on the BSP Website (link provided below).

[BSP Exchange Rate calculator](http://www.bsp.com.pg/International/Exchange-Rates/Exchange-Rates.aspx)

Exchange rates change daily, and so this script scrapes updated fx rates from the BSP website to do calculations.
Props to BSP for the fx rates.

## Usage:
``` pyhton
python3 bsp_fx_scraper.py usd 2999
```
To get the country codes:
``` python
python3 bsp_fx_scraper.py codes
```

## Notice:
Please read the following terms and conditions carefully before using this script.
1. If you use this script, I (Bernard Solien) am not to be held liable for any damage caused from the use or misuse of this script.
2. I did not get permission from BSP to scrape its website with this script so if you use it and get into trouble, I (Bernard Solien) should not be held liable.
