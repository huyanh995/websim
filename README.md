# Websim tool
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

* Your config of number of signals/combo threads:

```python
num_signal_threads = 5
num_combo_threads = 8
```

* Your signal templates and combo templates:

```python
signal_template = ["template 1", "template 2", ... ]
combo_template = ["template 1", "template 2", ... ]
```

* Your criteria to choose alpha to submit:
```python
combo_criteria = "your_criteria" # e.g: fitness/prod_corr
```

* The number of submitted alphas before being a consultant. For better use in the future, you should hide all of them:
```python
num_alphathon = 12
```

## Follow the prerequisite.md to install requested package and settings.

