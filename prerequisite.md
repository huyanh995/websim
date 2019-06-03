# This file is a intruction to deploy this tool on Google Cloud Compute Engine or any VPS/VM.

```console
sudo apt-get update
```

## python

```console
sudo apt-get install python3
sudo apt install python3-pip
```

## mysql

```console
sudo apt install mysql-server
pip3 install mysql-connector-python
```
For connecting MySQL remotely from your client, I strongly recommend to follow this tutorial (https://pieter-duplessis.co.za/blog/connecting-to-gcp-compute-engine-with-mysql-on-a-remote-ost/). Many thanks to Pieter du Plessis.


