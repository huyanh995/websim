import json
import time
from . import utils

sim_url = "https://www.worldquantvrc.com/simulate"
max_exceptions = 10


def simulate(sess, alpha_codes, region, top, thread_num):
    num_exception = 0
    while num_exception < max_exceptions:
        print('Thread {}: simulating \''.format(thread_num) + alpha_codes[0] + '\', exception times = {}:'.format(
            num_exception))

        args = []
        for i in range(len(alpha_codes)):
            args.append({'nanhandling': 'off', 'delay': '1', 'unitcheck': 'off', 'pasteurize': 'on', 'univid': top,
                         'opcodetype': 'FLOWSEXPR', 'opassetclass': 'EQUITY', 'unithandling': 'verify',
                         'optrunc': '0.1',
                         'code': alpha_codes[i], 'region': region, 'opneut': 'none', 'IntradayType': None,
                         'tags': 'equity',
                         'decay': '0', 'DataViz': '0', 'backdays': '256', 'simtime': 'Y10'})
        sim_data_obj = {
            'args': args
        }
        sim_data_json = json.dumps(sim_data_obj)
        response = sess.post(sim_url, data=sim_data_json)
        sim_res_json = response.content

        try:
            sim_res_obj = json.loads(sim_res_json)
            if sim_res_obj['error'] is None:
                print("Thread {}: DONE, job id = {}".format(thread_num, sim_res_obj['result']))
                return 2
            elif "You have reached the limit of concurrent simulations" in sim_res_obj['error']['all']:
                # print("You have reached the limit of concurrent simulations, wait for 3s and retry!")
                # print(sim_res_obj['error'])
                time.sleep(3)

        except Exception as ex:
            num_exception = num_exception + 1
            print('-------EXCEPTION---------')
            print('Thread {}: {}'.format(thread_num, ex))
            print('-------------------------')
            if 'Login' in str(sim_res_json):
                if thread_num == 1:
                    utils.login(sess)
                else:
                    time.sleep(2)
            pass

    return 0

