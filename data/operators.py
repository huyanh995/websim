import random
days = str(random.randint(1, 252))
std = str(round(random.uniform(0, 5), 2))
ignoreNanInput = random.choice(['', ',ignoreNanInput=true'])
filter = random.choice(['', ',filter=true'])
exponent = str(round(random.uniform(0, 1), 2))
reverse = random.choice(['', ',reverse = true'])
side = random.choice(['long', 'short'])
nan = random.choice(['', ',nan = true'])

simple_operater = [
    ['abs({})', 1, 0],
    ['add({}, {}' + filter + ')', 2, 0],
    ['ceil({})', 1, 0],
    ['divide({}, {})', 2, 0],
    ['exp({})', 1, 0],
    ['floor({})', 1, 0],
    ['frac({})', 1, 0],
    ['inverse({})', 1, 0],
    ['log({})', 1, 0],
    ['log_diff({})', 1, 0],
    ['max({}, {})', 2, 0], 
    ['min({}, {})', 2, 0],
    ['multiply({}, {}' + filter + ')', 2, 0],
    ['nan_mask({}, {})', 2, 0],
    ['power({}, {})', 2, 0], 
    ['purify({})', 1, 0],
    ['reverse({})', 1, 0],
    ['round({})', 1, 0],
    ['round0({}, f = ' + str(random.randint(0, 10)) + ')', 1, 0], # check again
    ['sign({})', 1, 0],
    ['signed_power({}, ' + exponent + ')', 1, 0],
    ['slog1p({})', 1, 0],
    ['sqrt(abs({}))', 1, 0],
    ['subtract({}, {}' + filter + ')', 2, 0],
    ['to_nan({}, value = 0' + reverse + ')', 1, 0]
]

logical_operator = [
    #['(({}) and ({}))', 2, 0],
    #['(({}) or ({}))', 2, 0],
    #['(({}) equal ({}))', 2, 0],
    ['negate({})', 1, 0],
    ['({} < {})', 2, 0],
    ['({} > {})', 2, 0],
    ['if_else({}, {}, {})', 3, 0],
    ['is_not_nan({})', 1, 0],
    ['is_nan({})', 1, 0],
    ['is_finite({})', 1, 0],
    ['is_not_finite({})', 1, 0]
]

lower = round(random.uniform(-2, 2), 2)
while True:
    upper = round(random.uniform(-2, 2), 2)
    if upper > lower:
        break
mask = round(0.5 * (lower + upper), 2)
complex_operator = [
    ['arc_cos({})', 1, 0],
    ['arc_sin({})', 1, 0],
    ['arc_tan({})', 1, 0],
    #bucket(rank(x), range="0, 1, 0.1" or buckets = "2,5,6,7,10")
    ['clamp({}, lower = ' + str(lower) + ', upper = ' + str(upper) + ', inverse = ' + random.choice(['false', 'true']) + ', mask = ' + str(mask) + ')', 1, 0],
    #['filter()'],
    ['keep({}, {}, period = ' + days + ')', 2, 0],
    ['left_tail({}, maximum = ' + str(random.uniform(-1, 1)) + ')', 1, 0],
    ['pasteurize({})', 1, 0],
    ['right_tail({}, minimum = ' + str(random.uniform(-1, 1)) + ')', 1, 0],
    ['sigmoid({})', 1, 0],
    ['tail({}, lower = -1, upper = 1, newval = 0)', 1, 0],
    ['tanh({})', 1, 0],
    ['trade_when({}, {}, {})', 3, 0] # 3 datas, 0 group. Vi tri 2 la data, vi tri 3 la group.
]

cross_sectional_operator = [
    ['normalize({}, useStd = true, limit = 0.0)', 1, 0],
    ['one_side({} , side = ' + side + ')', 1, 0],
    ['quantile({}, driver = gaussian, sigma = 1.0)', 1, 0],
    ['rank({}, rate=2)', 1, 0],
    ['rank_by_side({}, rate=2, scale=1)', 1, 0],
    ['regression_neut({}, {})', 2, 0],
    ['regression_proj({}, {})', 2, 0],
    ['scale({}, scale=1, longscale=1, shortscale=1)', 1, 0],
    ['scale_down({},constant=0)', 1, 0],
    ['truncate({},maxPercent=0.01)', 1, 0],
    ['vector_neut({}, {})', 2, 0],
    #['vector_proj({}, {}, filter=false)', 2, 0],
    ['winsorize({}, std = '+ std +')', 1, 0],
    ['zscore({})', 1, 0]
]

#
group_operator = [
    ['group_backfill({}, rank({}),' + days + ', std = '+ std +')', 1, 1],
    ['group_count({}, rank({})' + ignoreNanInput + ')', 1, 1],
    ['group_extra({}, 0.01, rank({}))', 1, 1],
    ['group_max({}, rank({})' + ignoreNanInput + ')', 1, 1],
    ['group_mean({}, 0.01, rank({})' + ignoreNanInput + ')', 1, 1],
    ['group_median({}, rank({})' + ignoreNanInput + ')', 1, 1], 
    ['group_min({}, rank({})' + ignoreNanInput + ')', 1, 1],                       
    ['group_neutralize({}, rank({}))', 1, 1],
    ['group_normalize({}, rank({}), constantCheck=True, tolerance=0.01, scale=1)', 1, 1],
    ['group_percentage({}, rank({}), percentage=0.5' + ignoreNanInput + ')', 1, 1],
    ['group_rank({}, rank({})' + ignoreNanInput + ')', 1, 1],
    ['group_scale({}, rank({}))', 1, 1],
    ['group_stddev({}, rank({})' + ignoreNanInput + ')', 1, 1],
    ['group_sum({}, rank({})' + ignoreNanInput + ')', 1, 1],
    ['group_zscore({}, rank({}))', 1, 1]
]

ts_operator = [
    ['days_from_last_change({})', 1, 0],
    ['ts_weighted_delay({}, k=0.5)', 1, 0],
    ['hump({}, hump = ' + str(round(random.uniform(0, 1), 2)) + ')', 1, 0],
    ['hump_decay({}, p = ' + str(round(random.uniform(0.01, 1), 2)) + ', relative = ' + random.choice(['false', 'true']) + ')', 1, 0],
    ['inst_tvr({},' + days + ')', 1, 0],
    ['jump_decay({},' + days + ', sensitivity=0.5, force=0.1)', 1, 0],
    ['kth_element({},' + days + ', k = 1)', 1, 0],
    ['last_diff_value({},' + days + ')', 1, 0],
    ['ts_arg_max({},' + days + ')', 1, 0],
    ['ts_arg_min({},' + days + ')', 1, 0],
    ['ts_av_diff({},' + days + ')', 1, 0],
    ['ts_co_kurtosis({}, {},' + days + ')', 2, 0],
    ['ts_corr({}, {},' + days + ')', 2, 0],
    ['ts_co_skewness({}, {},' + days + ')', 2, 0],
    ['ts_count_nans({} ,252)', 1, 0],
    ['ts_covariance({}, {},' + days + ')', 2, 0],
    ['ts_decay_exp_window({},' + days + ', factor = 1' + nan + ')', 1, 0],
    ['ts_decay_linear({},' + days + nan + ', dense = true)', 1, 0],
    ['ts_delay({},' + days + ')', 1, 0],
    ['ts_delta({},' + days + ')', 1, 0],
    ['ts_ir({},' + days + ')', 1, 0],
    ['ts_kurtosis({},' + days + ')', 1, 0],
    ['ts_max({},' + days + ')', 1, 0],
    ['ts_max_diff({},' + days + ')', 1, 0],
    ['ts_mean({},' + days + nan + ')', 1, 0],
    ['ts_median({},' + days + ')', 1, 0],
    ['ts_min({},' + days + ')', 1, 0],
    ['ts_min_diff({},' + days + ')', 1, 0],
    ['ts_min_max_cps({},' + days + ', f = 2)', 1, 0],
    ['ts_min_max_diff({},' + days + ', f = 0.5)', 1, 0],
    ['ts_moment({},' + days + ', k=0)', 1, 0],
    ['ts_partial_corr({}, {}, {},' + days + ')', 3, 0],
    ['ts_percentage({},' + days + ', percentage=0.5)', 1, 0],
    ['ts_poly_regression({}, {},' + days + ', k = 1)', 2, 0],
    ['ts_product({},' + days + nan + ')', 1, 0],
    ['ts_rank({},' + days + ', constant = 0)', 1, 0],
    ['ts_regression({}, {},' + days + ', lag = ' + str(random.randint(0, 2)) + ', rettype = ' + str(random.randint(0, 9)) + ')', 2, 0],
    ['ts_returns ({},' + days + ', mode = 1)', 1, 0],
    ['ts_scale({},' + days + ', constant = 0)', 1, 0],
    ['ts_skewness({},' + days + ')', 1, 0],
    ['ts_stddev({},' + days + ')', 1, 0],
    ['ts_step(1)', 0, 0],
    ['ts_sum({},' + days + nan + ')', 1, 0],
    ['ts_theilsen({}, {},' + days + ')', 2, 0],
    ['ts_triple_corr({}, {}, {},' + days + ')', 3, 0],
    ['ts_zscore({},' + days + ')', 1, 0]
]

# def operators():
#     return simple_operater + logical_operator + complex_operator + cross_sectional_operator + ts_operator + group_operator
#operators = simple_operater +\
#            logical_operator +\
#            complex_operator + \
#            cross_sectional_operator + \
#            group_operator + \
#            ts_operator
def operators():
    return ts_operator + cross_sectional_operator


