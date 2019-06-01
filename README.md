# websim_api
An automatic simulation and checking submission for websim.\
Developed by **Huy Anh Nguyen**, collaboration with Le Dang Cuong with help from Ho Duc Nhan and Luong Anh Vu.

## Before using, create a config.py file in common/ contains:
* Your account information:

```python
username = 'yourusername'
password = 'yourpassword'
```

* Your MySQL config:

```python
config_db = {
  'user': 'db_user',
  'password': 'user_password',
  'host': 'ip',
  'database': 'database_name'
}
```

* Your config of signals/combos filter:

```python
min_signal = (min_sharpe, min_fitness, max(selfcorr, prodcorr))
min_combo = (min_sharpe, min_fitness, max(selfcorr, prodcorr))
```

* Your config of ratio of signal simulation threads/ combo simulation threads:

```python
num_sim = (no of signal, no of combo)
```

* Your signal templates and combo templates:

```python
signal_template = ["template 1", "template 2", ... ]
combo_template = ["template 1", "template 2", ... ]
```


