# Update procedure


## 1. Login

start up `ssh` on your terminal

```powershell
ssh username:password@hgis.uw.edu


```

## 2. Info

website location

```powershell
cd /var/www/html/virus
```

manually update

```
sudo git pull
```


renew the whole Website

```powershell
cd /var/www/html
sudo rm -rf virus
git clone [git url]
```


automatical update

```
cd /home/zhaobo
sudo sh virus.shauso



for countries
assets/name.csv   // lower case
virus.db  //add new columns for the new countries or states/provinces.
headless_virus.py virus_table  add the chhinese names for the new courtries
update wuhan-15.json


for US states or CA provices.

virus.db  //add new columns for the new countries or states/provinces.
update wuhan-15.json
