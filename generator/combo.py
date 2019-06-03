import random
import sqlite3
from datetime import datetime
import numpy as np

scale = ["alpha; ", "rank_by_side(alpha); "]

select_command = """SELECT alpha_code FROM "{t}" WHERE used <= "{s}";"""

count = 1
update_command = """UPDATE "{t}" SET {c} = {c} + 1, updated_at = "{d}" WHERE alpha_code = "{y}";"""


def connect_db(name):
    global connection, cursor
    connection = sqlite3.connect(name)
    cursor = connection.cursor()


def update_count_used(top, alpha):
    sql_command = update_command.format(t=top, c='count_used', d=datetime.now(), y=alpha)
    cursor.execute(sql_command)
    connection.commit()


def get_signal_list(lines, top, num_signals):
    rows = np.random.choice(len(lines), num_signals, replace=False)
    signals = []
    for row in rows:
        signal = lines[row][0]
        sql_command = update_command.format(t=top, c='used', d=datetime.now(), y=signal)
        cursor.execute(sql_command)
        connection.commit()
        signals.append(signal)
    return signals


def get_alpha(lines, top, num_signals):
    rnd_combo = random.choice(scale)

    signals = get_signal_list(lines, top, num_signals)
    pre_combine = ''
    combine = 'alpha = group_neutralize(add('
    for i in range(num_signals):
        signal = signals[i]
        element = 'vu' + str(i) + ' = ' + rnd_combo.replace("alpha", signal)
        pre_combine = pre_combine + element
        combine = combine + 'vu' + str(i) + ', '

    combine = combine + 'filter = true), market)'
    pre_combine = pre_combine + combine + '; alpha'

    return [pre_combine] + signals
