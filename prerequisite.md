# This file is a instruction to deploy this tool on Google Cloud Compute Engine or any VPS/VM (Tested on Ubuntu 18.04 LTS)

```console
sudo apt-get update
sudo dpkg-reconfigure tzdata (Change timezone to Asia\Ho Chi Minh City)
```

## python

```console
sudo apt-get install python3
sudo apt install python3-pip
```

## mysql

```console
sudo apt install mysql-server
sudo mysql_secure_installation
pip3 install mysql-connector-python
```

## Git
```console
sudo apt install git
```
For connecting MySQL remotely from your client, I strongly recommend to follow this tutorial (https://pieter-duplessis.co.za/blog/connecting-to-gcp-compute-engine-with-mysql-on-a-remote-ost/). Many thanks to Pieter du Plessis.
If you got the error code 61 when connecting MySQL remotely, trying: sudo service mysql restart

For MacOS only: Create a ssh key and connect to Google Compute Engine without accessing their console. I use Termius as SSH client.
https://www.youtube.com/watch?v=2ibBF9YqveY&t=2s



