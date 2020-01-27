# wuhan


angel

Lin

crontab content

```sh
0 */2 * * * sh /home/zhaobo/virus.sh
```

virus.sh content
```sh
cd /var/www/html/virus
sudo git pull https://[username]:[password]@github.com/jakobzhao/virus.git

```



```sh
 >>>  sudo crontab -e
 >>>  sudo service cron restart
 >>>  sudo tail -f /var/log/syslog | grep CRON
 >>> history
```


```sh
>>> ls -l
>>>  rm -rf virus
>>> sudo nano virus
```
