Price_Volume = ['open', 'close', 'high', 'low', 'vwap', 'volume', 'returns', 'adv20', 'sharesout', 'cap', 'split', 'dividend', 'market', 'country', 'exchange', 'sector', 'industry', 'subindustry']
Fundamental_USA = ['assets', 'assets_curr', 'bookvalue_ps', 'capex', 'cash', 'cashflow', 'cashflow_dividends', 'cashflow_fin', 'cashflow_invst', 'cashflow_op', 'cogs', 'current_ratio', 'debt', 'debt_lt', 'debt_st', 'depre_amort', 'EBIT', 'EBITDA', 'employee', 'enterprise_value', 'eps', 'equity', 'goodwill', 'income', 'income_beforeextra', 'income_tax', 'interest_expense', 'inventory', 'inventory_turnover', 'invested_capital', 'liabilities', 'liabilities_curr', 'operating_expense', 'operating_income', 'ppent', 'pretax_income', 'rd_expense', 'receivable', 'retained_earnings', 'return_assets', 'return_equity', 'revenue', 'sales', 'sales_growth', 'sales_ps', 'SGA_expense', 'working_capital']
Fundamental_EUR = ['accounts_payable', 'accum_depre', 'assets', 'assets_curr', 'assets_curr_oth', 'bookvalue_ps', 'capex', 'cash', 'cash_st', 'cashflow_fin', 'cashflow_invst', 'cashflow_op', 'cogs', 'cost_of_revenue', 'current_ratio', 'debt', 'debt_lt', 'debt_lt_curr', 'debt_st', 'depre', 'depre_amort', 'EBIT', 'EBITDA', 'employee', 'enterprise_value', 'eps', 'equity', 'goodwill', 'income', 'income_beforeextra', 'income_tax', 'income_tax_payable', 'interest_expense', 'inventory', 'inventory_turnover', 'liabilities', 'liabilities_cur_oth', 'liabilities_curr', 'liabilities_oth', 'operating_expense', 'operating_income', 'operating_margin', 'ppent', 'ppent_net', 'preferred_dividends', 'pretax_income', 'quick_ratio', 'receivable', 'retained_earnings', 'return_assets', 'return_equity', 'revenue', 'sales', 'SGA_expense']
Fundamental_ASI = ['accounts_payable', 'accum_depre', 'assets', 'assets_curr', 'assets_curr_oth', 'bookvalue_ps', 'capex', 'cash', 'cash_st', 'cashflow_fin', 'cashflow_invst', 'cashflow_op', 'cogs', 'cost_of_revenue', 'current_ratio', 'debt', 'debt_lt', 'debt_lt_curr', 'debt_st', 'depre', 'depre_amort', 'EBIT', 'EBITDA', 'eps', 'equity', 'goodwill', 'income', 'income_beforeextra', 'income_tax', 'income_tax_payable', 'interest_expense', 'inventory', 'inventory_turnover', 'liabilities', 'liabilities_cur_oth', 'liabilities_curr', 'liabilities_oth', 'operating_expense', 'operating_income', 'operating_margin', 'ppent', 'ppent_net', 'preferred_dividends', 'pretax_income', 'quick_ratio', 'receivable', 'retained_earnings', 'return_assets', 'return_equity', 'revenue', 'sales', 'SGA_expense']
Estimate = ['est_bookvalue_ps', 'est_capex', 'est_cashflow_fin', 'est_cashflow_invst', 'est_cashflow_op', 'est_cashflow_ps', 'est_dividend_ps', 'est_ebit', 'est_ebitda', 'est_eps', 'est_epsa', 'est_epsr', 'est_fcf', 'est_fcf_ps', 'est_ffo', 'est_ffoa', 'est_grossincome', 'est_netdebt', 'est_netprofit', 'est_netprofit_adj', 'est_ptp', 'est_ptpr', 'est_rd_expense', 'est_sales', 'est_sga', 'est_shequity', 'est_tbv_ps', 'est_tot_assets', 'est_tot_goodwill', 'etz_eps', 'etz_eps_delta', 'etz_eps_ret', 'etz_eps_tsrank', 'etz_revenue', 'etz_revenue_delta', 'etz_revenue_ret']
Relationship = ['rel_num_all', 'rel_num_comp', 'rel_num_cust', 'rel_num_part', 'rel_ret_all', 'rel_ret_comp', 'rel_ret_cust', 'rel_ret_part']
Sentiment = ['snt_bearish', 'snt_bearish_tsrank', 'snt_bullish', 'snt_bullish_tsrank', 'snt_buzz', 'snt_buzz_bfl', 'snt_buzz_ret', 'snt_ratio', 'snt_ratio_tsrank', 'snt_social_value', 'snt_social_volume', 'snt_value']
Model_Data = ['mdf_cap', 'mdf_fnl', 'mdf_inv_q', 'mdf_nqi', 'mdf_pay_q', 'mdf_pfd', 'mdf_pmo', 'mdf_sti_q', 'mdf_cex_q', 'mdf_cfa_q', 'mdf_cfi_q', 'mdf_com', 'mdf_cse', 'mdf_dep', 'mdf_dep_q', 'mdf_fii', 'mdf_ite_q', 'mdf_mfq', 'mdf_pay', 'mdf_pbk', 'mdf_peg', 'mdf_per', 'mdf_pfd_q', 'mdf_ppe_q', 'mdf_prm', 'mdf_pva', 'mdf_pvr', 'mdf_rcv', 'mdf_rcv_q', 'mdf_rev', 'mdf_rte_q', 'mdf_sal', 'mdf_shr', 'mdf_sph', 'mdf_spm', 'mdf_std', 'mdf_std_q', 'mdf_sti', 'mdf_tax', 'mdf_tca_q', 'mdf_trr', 'mdf_val', 'mdf_vmo', 'mdf_bso', 'mdf_bso_q', 'mdf_ceq', 'mdf_cex', 'mdf_cfa', 'mdf_cfi', 'mdf_cse_q', 'mdf_das', 'mdf_ebt', 'mdf_ebt_q', 'mdf_eda', 'mdf_emo', 'mdf_eup', 'mdf_gpr', 'mdf_ibt', 'mdf_ibt_q', 'mdf_iex_q', 'mdf_inv', 'mdf_ita', 'mdf_ite', 'mdf_mci', 'mdf_nco_q', 'mdf_net', 'mdf_net_q', 'mdf_oin', 'mdf_oin_q', 'mdf_pcf', 'mdf_peh', 'mdf_plc', 'mdf_rec', 'mdf_roi', 'mdf_rte', 'mdf_sci', 'mdf_sed', 'mdf_sga', 'mdf_smo', 'mdf_tcl_q', 'mdf_ato', 'mdf_bsd', 'mdf_cne', 'mdf_csh_q', 'mdf_isd', 'mdf_ldt', 'mdf_mfy', 'mdf_nco', 'mdf_rac', 'mdf_roe', 'mdf_sdr', 'mdf_vei', 'empty:', 'mdf_chi', 'empty:', 'mdf_eno', 'mdf_grm', 'mdf_gro', 'mdf_gwl_q', 'mdf_iex', 'mdf_ito', 'mdf_ldt_q', 'mdf_odl', 'mdf_pec', 'mdf_ppe', 'mdf_pvh', 'mdf_rev_q', 'mdf_cfl', 'mdf_ebm', 'mdf_edv', 'mdf_efy', 'mdf_gwl', 'mdf_ltd', 'mdf_peq', 'mdf_plb', 'mdf_tcl', 'mdf_deq', 'mdf_grp', 'mdf_pss', 'mdf_shb', 'mdf_avi', 'mdf_div', 'mdf_fnd', 'mdf_inb', 'mdf_ass', 'mdf_csh', 'mdf_gpr_q', 'mdf_ita_q', 'mdf_qty', 'mdf_tca', 'mdf_cps', 'mdf_dpr', 'mdf_tie', 'mdf_coa', 'mdf_coa_q', 'mdf_gry', 'mdf_pre', 'mdf_exi', 'mdf_oey', 'mdf_bsd_q', 'mdf_ccc_q', 'mdf_tas_q', 'mdf_atr', 'mdf_isd_q', 'mdf_nps', 'mdf_era', 'mdf_pra', 'mdf_yld', 'mdf_tli_q', 'mdf_bkv', 'mdf_h52', 'mdf_bta', 'mdf_pro', 'mdf_sg3', 'mdf_pri', 'mdf_lpe', 'mdf_opi', 'mdf_tma', 'mdf_l52', 'mdf_alp', 'mdf_hpv', 'mdf_hpe', 'mdf_fma', 'mdf_dvp', 'mdf_bet', 'mdf_sga_q', 'mdf_rds', 'mdf_eg5', 'mdf_f2i', 'mdf_eg3', 'mdf_avl', 'mdf_hdy', 'mdf_ind', 'mdf_fdi', 'mdf_ccr', 'mdf_eq1', 'mdf_eq2', 'mdf_eq3', 'mdf_eq4', 'mdf_eq5', 'mdf_rnd_q', 'mdf_rnd', 'mdf_hdq', 'mdf_hdg', 'mdf_fni', 'mdf_ape', 'mdf_tas', 'mdf_dg3', 'mdf_ref', 'mdf_qe1', 'mdf_qe2', 'mdf_qe3', 'mdf_qe4', 'mdf_qe5', 'mdf_qe6', 'mdf_qe7', 'mdf_qe8', 'mdf_pg1', 'mdf_pg3', 'mdf_ccc', 'mdf_roa', 'mdf_ecu', 'mdf_hsy', 'mdf_hsq', 'mdf_tli', 'mdf_csp', 'mdf_hsg', 'mdf_pgy', 'mdf_vol', 'mdf_pgq', 'mdf_pgw', 'mdf_pgh', 'mdf_pgm', 'mdf_pgn', 'mdf_pgd', 'mdf_pgf', 'mdf_hey', 'mdf_sq1', 'mdf_sq2', 'mdf_sq3', 'mdf_sq4', 'mdf_sq5', 'mdf_qs1', 'mdf_qs2', 'mdf_qs3', 'mdf_qs4', 'mdf_qs5', 'mdf_qs6', 'mdf_qs7', 'mdf_qs8', 'mdf_heq', 'mdf_sic', 'mdf_heg']
US_News_Data = ['news_prev_vol', 'news_curr_vol', 'news_mov_vol', 'news_ratio_vol', 'news_open_vol', 'news_close_vol', 'news_tot_ticks', 'news_atr14', 'empty:', 'empty:', 'empty:', 'empty:', 'empty:', 'news_prev_day_ret', 'news_prev_close', 'news_open', 'news_open_gap', 'news_spy_last', 'news_ton_high', 'news_ton_low', 'news_ton_last', 'news_eod_high', 'news_eod_low', 'news_eod_close', 'news_spy_close', 'news_post_vwap', 'news_pre_vwap', 'news_main_vwap', 'news_all_vwap', 'news_eod_vwap', 'news_max_up_amt', 'news_max_up_ret', 'news_max_dn_amt', 'news_max_dn_ret', 'news_session_range', 'news_session_range_pct', 'news_ls', 'empty:', 'empty:', 'empty:', 'news_indx_perf', 'news_pct_30sec', 'news_pct_1min', 'news_pct_5_min', 'news_pct_10min', 'news_pct_30min', 'news_pct_60min', 'news_pct_90min', 'news_pct_120min', 'news_mins_1_pct_up', 'news_mins_2_pct_up', 'news_mins_3_pct_up', 'news_mins_4_pct_up', 'news_mins_5_pct_up', 'news_mins_7_5_pct_up', 'news_mins_10_pct_up', 'news_mins_20_pct_up', 'news_mins_1_pct_dn', 'news_mins_2_pct_dn', 'news_mins_3_pct_dn', 'news_mins_4_pct_dn', 'news_mins_5_pct_dn', 'news_mins_7_5_pct_dn', 'news_mins_10_pct_dn', 'news_mins_20_pct_dn', 'news_mins_1_chg', 'news_mins_2_chg', 'news_mins_3_chg', 'news_mins_4_chg', 'news_mins_5_chg', 'news_mins_7_5_chg', 'news_mins_10_chg', 'news_mins_20_chg', 'news_cap', 'news_pe_ratio', 'news_dividend_yield', 'news_short_interest', 'news_high_exc_stddev', 'news_low_exc_stddev', 'news_vol_stddev', 'news_range_stddev', 'news_atr_ratio', 'news_eps_actual']
Model_Ratings_Data = ['rating']
Volatility_Data = ['historical_volatility_10', 'historical_volatility_20', 'historical_volatility_30', 'historical_volatility_60', 'historical_volatility_90', 'historical_volatility_120', 'historical_volatility_150', 'historical_volatility_180', 'implied_volatility_call_10', 'implied_volatility_call_20', 'implied_volatility_call_30', 'implied_volatility_call_60', 'implied_volatility_call_90', 'implied_volatility_call_120', 'implied_volatility_call_150', 'implied_volatility_call_180', 'implied_volatility_call_270', 'implied_volatility_call_360', 'implied_volatility_call_720', 'implied_volatility_call_1080', 'implied_volatility_mean_10', 'implied_volatility_mean_20', 'implied_volatility_mean_30', 'implied_volatility_mean_60', 'implied_volatility_mean_90', 'implied_volatility_mean_120', 'implied_volatility_mean_150', 'implied_volatility_mean_180', 'implied_volatility_mean_270', 'implied_volatility_mean_360', 'implied_volatility_mean_720', 'implied_volatility_mean_1080', 'implied_volatility_mean_skew_10', 'implied_volatility_mean_skew_20', 'implied_volatility_mean_skew_30', 'implied_volatility_mean_skew_60', 'implied_volatility_mean_skew_90', 'implied_volatility_mean_skew_120', 'implied_volatility_mean_skew_150', 'implied_volatility_mean_skew_180', 'implied_volatility_mean_skew_270', 'implied_volatility_mean_skew_360', 'implied_volatility_mean_skew_720', 'implied_volatility_mean_skew_1080', 'implied_volatility_put_10', 'implied_volatility_put_20', 'implied_volatility_put_30', 'implied_volatility_put_60', 'implied_volatility_put_90', 'implied_volatility_put_120', 'implied_volatility_put_150', 'implied_volatility_put_180', 'implied_volatility_put_270', 'implied_volatility_put_360', 'implied_volatility_put_720', 'implied_volatility_put_1080', 'parkinson_volatility_10', 'parkinson_volatility_20', 'parkinson_volatility_30', 'parkinson_volatility_60', 'parkinson_volatility_90', 'parkinson_volatility_120', 'parkinson_volatility_150', 'parkinson_volatility_180']
Stock_Reports_Plus = ['srp_average_score', 'srp_earnings_score', 'srp_fundamental_score', 'srp_insider_trading_score', 'srp_price_momentum_score', 'srp_relative_valuation_score', 'srp_risk_score']
Systematic_Risk_Metrics = ['beta_last_30_days_spy', 'beta_last_60_days_spy', 'beta_last_90_days_spy', 'beta_last_360_days_spy', 'correlation_last_30_days_spy', 'correlation_last_60_days_spy', 'correlation_last_90_days_spy', 'correlation_last_360_days_spy', 'systematic_risk_last_30_days', 'systematic_risk_last_60_days', 'systematic_risk_last_90_days', 'systematic_risk_last_360_days', 'unsystematic_risk_last_30_days', 'unsystematic_risk_last_60_days', 'unsystematic_risk_last_90_days', 'unsystematic_risk_last_360_days']
Options_Analytics = ['call_breakeven_10', 'call_breakeven_20', 'call_breakeven_30', 'call_breakeven_60', 'call_breakeven_90', 'call_breakeven_120', 'call_breakeven_150', 'call_breakeven_180', 'call_breakeven_270', 'call_breakeven_360', 'call_breakeven_720', 'call_breakeven_1080', 'forward_price_10', 'forward_price_20', 'forward_price_30', 'forward_price_60', 'forward_price_90', 'forward_price_120', 'forward_price_150', 'forward_price_180', 'forward_price_270', 'forward_price_360', 'forward_price_720', 'forward_price_1080', 'option_breakeven_10', 'option_breakeven_20', 'option_breakeven_30', 'option_breakeven_60', 'option_breakeven_90', 'option_breakeven_120', 'option_breakeven_150', 'option_breakeven_180', 'option_breakeven_270', 'option_breakeven_360', 'option_breakeven_720', 'option_breakeven_1080', 'pcr_oi_10', 'pcr_oi_20', 'pcr_oi_30', 'pcr_oi_60', 'pcr_oi_90', 'pcr_oi_120', 'pcr_oi_150', 'pcr_oi_180', 'pcr_oi_270', 'pcr_oi_360', 'pcr_oi_720', 'pcr_oi_1080', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_oi_all', 'pcr_vol_10', 'pcr_vol_20', 'pcr_vol_30', 'pcr_vol_60', 'pcr_vol_90', 'pcr_vol_120', 'pcr_vol_150', 'pcr_vol_180', 'pcr_vol_270', 'pcr_vol_360', 'pcr_vol_720', 'pcr_vol_1080', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'pcr_vol_all', 'put_breakeven_10', 'put_breakeven_20', 'put_breakeven_30', 'put_breakeven_60', 'put_breakeven_90', 'put_breakeven_120', 'put_breakeven_150', 'put_breakeven_180', 'put_breakeven_270', 'put_breakeven_360', 'put_breakeven_720', 'put_breakeven_1080']
Street_Events = ['se_event_count', 'se_neg_words', 'se_pos_words', 'se_neg_score', 'se_pos_score', 'se_score']
Analyst_Revision_Score = ['star_arm_score', 'star_arm_score_5', 'star_arm_global_rank', 'star_arm_country_rank', 'star_arm_pref_earnings_score', 'star_arm_recommendations_score', 'star_arm_revenue_score', 'star_arm_secondary_earnings_score', 'star_arm_score_change_1m', 'star_arm_region_rank_decimal']
Short_Interest_Model = ['star_si_insown_pct', 'star_si_country_rank', 'star_si_cap_rank', 'star_si_sector_rank', 'star_si_country_rank_unadj', 'star_si_shortsqueeze_rank']
EPS_Estimate_Model = ["star_eps_analyst_number_fq1", "star_eps_analyst_number_fq2", "star_eps_analyst_number_fy1", "star_eps_analyst_number_fy2", "star_eps_fq1_enddate", "star_eps_fq2_enddate", "star_eps_fy1_enddate", "star_eps_fy2_enddate", "star_eps_surprise_prediction_fq1", "star_eps_surprise_prediction_fq2", "star_eps_surprise_prediction_fy1", "star_eps_surprise_prediction_fy2", "star_eps_smart_estimate_fq1", "star_eps_smart_estimate_fq2", "star_eps_smart_estimate_fy1", "star_eps_smart_estimate_fy2", 'star_eps_surprise_prediction_12m', 'star_eps_smart_estimate_12m']
Credit_Risk_Model = ['star_ccr_country_rank', 'star_ccr_global_rank', 'star_ccr_implied_rating', 'star_ccr_industry_rank', 'star_ccr_combined_pd', 'star_ccr_region_rank', 'star_ccr_sector_rank']
Price_Momentum_Model = ['star_pm_global_rank', 'star_pm_industry', 'star_pm_longterm', 'star_pm_midterm', 'star_pm_region_rank', 'star_pm_shortterm']
Revenue_Estimate_Model = ['star_rev_analyst_number_fq1', 'star_rev_analyst_number_fq2', 'star_rev_analyst_number_fy1', 'star_rev_analyst_number_fy2', 'star_rev_fq1_enddate', 'star_rev_fq2_enddate', 'star_rev_fy1_enddate', 'star_rev_fy2_enddate', 'star_rev_surprise_prediction_12m', 'star_rev_surprise_prediction_fq1', 'star_rev_surprise_prediction_fq2', 'star_rev_surprise_prediction_fy1', 'star_rev_surprise_prediction_fy2', 'star_rev_smart_estimate_12m', 'star_rev_smart_estimate_fq1', 'star_rev_smart_estimate_fq2', 'star_rev_smart_estimate_fy1', 'star_rev_smart_estimate_fy2']
Insider_Model = ['star_in_country_rank', 'star_in_industry_rank', 'star_in_sector_rank', 'star_in_netbuyer_ratio_rank', 'star_in_purchase_depth_rank', 'star_in_selling_depth_rank']
Growth_Valuation_Model = ["star_val_dividend_projection_fy1", "star_val_dividend_projection_fy2", "star_val_dividend_projection_fy3", "star_val_dividend_projection_fy4", "star_val_dividend_projection_fy5", "star_val_dividend_projection_fy6","star_val_dividend_projection_fy7", "star_val_dividend_projection_fy8", "star_val_dividend_projection_fy9", "star_val_dividend_projection_fy10", "star_val_dividend_projection_fy11", "star_val_dividend_projection_fy12",  "star_val_dividend_projection_fy13", "star_val_dividend_projection_fy14", "star_val_dividend_projection_fy15", "star_val_earnings_measure_type", "star_val_earnings_projection_fy1", "star_val_earnings_projection_fy2", "star_val_earnings_projection_fy3", "star_val_earnings_projection_fy4",  "star_val_earnings_projection_fy5", "star_val_earnings_projection_fy6", "star_val_earnings_projection_fy7", "star_val_earnings_projection_fy8",  "star_val_earnings_projection_fy9", "star_val_earnings_projection_fy10", "star_val_earnings_projection_fy11", "star_val_earnings_projection_fy12", "star_val_earnings_projection_fy13", "star_val_earnings_projection_fy14", "star_val_earnings_projection_fy15", "star_val_fwd10_eps_cagr", "star_val_fwd5_eps_cagr", "star_val_fy_end_date", "star_val_implied10_eps_cagr", "star_val_implied5_eps_cagr", "star_val_iv_projection", "star_val_piv_ratio", "star_val_piv_industry_rank", "star_val_piv_region_rank", "star_val_piv_sector_rank", "star_val_buyback_yield", "star_val_dividend_yield", "star_val_ev_sales", "star_val_industry_rank", "star_val_pb",  "star_val_pcf", "star_val_pe", "star_val_region_rank", "star_val_sector_rank"]
Smart_Ratios = ['star_sr_global_rank', 'star_sr_liquidity', 'star_sr_region_rank', 'star_sr_sector_rank', 'star_sr_industr_rank', 'star_sr_country_rank', 'star_sr_growth', 'star_sr_profitability', 'star_sr_leverage', 'star_sr_coverage']
Smart_Holdings = ['star_hold_global_change_rank', 'star_hold_region_change_rank', 'star_hold_country_rank', 'star_hold_global_rank', 'star_hold_industry_rank', 'star_hold_global_owner_rank', 'star_hold_region_owner_rank', 'star_hold_region_rank', 'star_hold_global_screening_rank', 'star_hold_region_screening_rank', 'star_hold_sector_rank']
Analyst_Revisions = ['star_arm_score', 'star_arm_score_5', 'star_arm_global_rank', 'star_arm_country_rank', 'star_arm_pref_earnings_score', 'star_arm_recommendations_score', 'star_arm_revenue_score', 'star_arm_secondary_earnings_score', 'star_arm_score_change_1m', 'star_arm_region_rank_decimal']
Volatility_and_Risk_Factor_Data = ['qs_alpha_1d', 'qs_alpha_5d', 'qs_alpha_22d', 'qs_beta_1d', 'qs_beta_5d', 'qs_beta_22d', 'qs_fdim_1d', 'qs_fdim_5d', 'qs_fdim_22d', 'qs_hurst_1d', 'qs_hurst_5d', 'qs_hurst_22d', 'qs_kurt_1d', 'qs_kurt_5d', 'qs_kurt_22d', 'qs_mom3_1d', 'qs_mom3_5d', 'qs_mom3_22d', 'qs_mom4_1d', 'qs_mom4_5d', 'qs_mom4_22d', 'qs_ret_1d', 'qs_ret_5d', 'qs_ret_22d', 'qs_skew_1d', 'qs_skew_5d', 'qs_skew_22d', 'qs_var_1d', 'qs_var_5d', 'qs_var_22d']
EBITDA_Estimate_Model = ["star_ebitda_analyst_number_fq1", "star_ebitda_fq1_enddate", "star_ebitda_surprise_prediction_fq1", "star_ebitda_smart_estimate_fq1", "star_ebitda_analyst_number_fq2", "star_ebitda_fq2_enddate", "star_ebitda_surprise_prediction_fq2", "star_ebitda_smart_estimate_fq2", "star_ebitda_analyst_number_fy1", "star_ebitda_fy1_enddate", "star_ebitda_surprise_prediction_fy1", "star_ebitda_smart_estimate_fy1", "star_ebitda_analyst_number_fy2", "star_ebitda_fy2_enddate", "star_ebitda_surprise_prediction_fy2", "star_ebitda_smart_estimate_fy2",  "star_ebitda_surprise_prediction_12m", "star_ebitda_smart_estimate_12m"]
Price_Target_Data = []#['rtk_ptg_high', 'rtk_ptg_low', 'rtk_ptg_mean', 'rtk_ptg_median', 'rtk_ptg_stddev', 'rtk_ptg_number']
Performance_Metrics_Data = ['qs_ir_1d', 'qs_ir_5d', 'qs_ir_22d', 'qs_sharpe_1d', 'qs_sharpe_5d', 'qs_sharpe_22d', 'qs_sortino_ratio_1d', 'qs_sortino_ratio_5d', 'qs_sortino_ratio_22d', 'qs_treynor_ratio_1d', 'qs_treynor_ratio_5d', 'qs_treynor_ratio_22d', 'qs_gain_loss_var_ratio_1d', 'qs_gain_loss_var_ratio_5d', 'qs_gain_loss_var_ratio_22d', 'qs_gain_var_1d', 'qs_gain_var_5d', 'qs_gain_var_22d', 'qs_loss_var_1d', 'qs_loss_var_5d', 'qs_loss_var_22d', 'qs_exp_shortfall_95ci_1d', 'qs_exp_shortfall_95ci_5d', 'qs_exp_shortfall_95ci_22d', 'qs_exp_shortfall_99ci_1d', 'qs_exp_shortfall_99ci_5d', 'qs_exp_shortfall_99ci_22d', 'qs_mod_sharpe_95ci_1d', 'qs_mod_sharpe_95ci_5d', 'qs_mod_sharpe_95ci_22d', 'qs_mod_sharpe_99ci_1d', 'qs_mod_sharpe_99ci_5d', 'qs_mod_sharpe_99ci_22d', 'qs_rachev_ratio_95ci_1d', 'qs_rachev_ratio_95ci_5d', 'qs_rachev_ratio_95ci_22d', 'qs_rachev_ratio_99ci_1d', 'qs_rachev_ratio_99ci_5d', 'qs_rachev_ratio_99ci_22d', 'qs_starr_ratio_95ci_1d', 'qs_starr_ratio_95ci_5d', 'qs_starr_ratio_95ci_22d', 'qs_starr_ratio_99ci_1d', 'qs_starr_ratio_99ci_5d', 'qs_starr_ratio_99ci_22d', 'qs_var_95ci_1d', 'qs_var_95ci_5d', 'qs_var_95ci_22d', 'qs_var_99ci_1d', 'qs_var_99ci_5d', 'qs_var_99ci_22d']
Institutional_Ownership_Data = ['io_inst_holding', 'io_inst_prev_holding', 'io_inst_mv', 'io_inst_prev_mv', 'io_inst_pct', 'io_inst_number', 'io_fund_holding', 'io_fund_prev_holding', 'io_fund_mv', 'io_fund_prev_mv', 'io_fund_pct', 'io_fund_number']
Creditworthiness_Model = ['cr_class', 'cr_confidence_level_percent', 'cr_probability_of_default_percent']
Fundamental_Scores = ['fscore_growth', 'fscore_total', 'fscore_momentum', 'fscore_surface_accel', 'fscore_surface', 'fscore_profitability', 'fscore_quality', 'fscore_value']
Fundamental_Analysis_Model = ['fam_beta_pct', 'fam_beta_rank', 'fam_book_value_pct', 'fam_book_value_rank', 'fam_cash_flow_pct', 'fam_cash_flow_rank', 'fam_alpha_pct', 'fam_alpha_rank', 'fam_core_rank', 'fam_core_score', 'fam_earn_change_pct', 'fam_earn_change_rank', 'fam_earn_growth_pct', 'fam_earn_growth_rank', 'fam_earn_surp_pct', 'fam_earn_surp_rank', 'fam_earn_vol_rank', 'fam_est_eps_pct', 'fam_est_eps_rank', 'fam_est_rev_pct', 'fam_est_rev_rank', 'fam_mkt_liq_pct', 'fam_mkt_liq_rank', 'fam_roe_pct', 'fam_roe_rank', 'fam_rpt_eps_pct', 'fam_rpt_eps_rank']
Report_Footnotes = ['fn_accrued_liab_a', 'fn_accrued_liab_curr_a', 'fn_accrued_liab_curr_q', 'fn_accrued_liab_q', 'fn_accum_depr_depletion_and_amortization_ppne_a', 'fn_accum_depr_depletion_and_amortization_ppne_q', 'fn_accum_oth_income_loss_fx_adj_net_of_tax_a', 'fn_accum_oth_income_loss_fx_adj_net_of_tax_q', 'fn_accum_oth_income_loss_net_of_tax_a', 'fn_accum_oth_income_loss_net_of_tax_q', 'fn_allocated_share_based_compensation_expense_a', 'fn_allocated_share_based_compensation_expense_q', 'fn_allowance_for_doubtful_accounts_receivable_a', 'fn_allowance_for_doubtful_accounts_receivable_q', 'fn_amortization_of_intangible_assets_a', 'fn_amortization_of_intangible_assets_q', 'fn_antidilutive_securities_excl_from_eps_a', 'fn_antidilutive_securities_excl_from_eps_q', 'fn_assets_fair_val_a', 'fn_assets_fair_val_l1_a', 'fn_assets_fair_val_l1_q', 'fn_assets_fair_val_l2_a', 'fn_assets_fair_val_l2_q', 'fn_assets_fair_val_l3_a', 'fn_assets_fair_val_l3_q', 'fn_assets_fair_val_q', 'fn_avg_diluted_sharesout_adj_a', 'fn_avg_diluted_sharesout_adj_q', 'fn_business_acq_ppne_a', 'fn_business_acq_ppne_q', 'fn_business_combination_assets_aquired_goodwill_a', 'fn_business_combination_assets_aquired_goodwill_q', 'fn_business_combination_purchase_price_a', 'fn_business_combination_purchase_price_q', 'fn_comp_fair_value_assumptions_weighted_avg_vol_rate_a', 'fn_comp_fair_value_assumptions_weighted_avg_vol_rate_q', 'fn_comp_non_opt_forfeited_a', 'fn_comp_non_opt_forfeited_q', 'fn_comp_non_opt_grants_a', 'fn_comp_non_opt_grants_q', 'fn_comp_non_opt_nonvested_number_a', 'fn_comp_non_opt_nonvested_number_q', 'fn_comp_non_opt_vested_a', 'fn_comp_non_opt_vested_q', 'fn_comp_not_rec_a', 'fn_comp_not_rec_q', 'fn_comp_not_rec_stock_options_a', 'fn_comp_not_rec_stock_options_q', 'fn_comp_number_of_shares_authorized_a', 'fn_comp_number_of_shares_authorized_q', 'fn_comp_options_exercisable_number_a', 'fn_comp_options_exercisable_number_q', 'fn_comp_options_exercisable_weighted_avg_a', 'fn_comp_options_exercisable_weighted_avg_q', 'fn_comp_options_exercises_weighted_avg_a', 'fn_comp_options_exercises_weighted_avg_q', 'fn_comp_options_forfeitures_and_expirations_a', 'fn_comp_options_forfeitures_and_expirations_q', 'fn_comp_options_grants_a', 'fn_comp_options_grants_fair_value_a', 'fn_comp_options_grants_fair_value_q', 'fn_comp_options_grants_q', 'fn_comp_options_grants_weighted_avg_a', 'fn_comp_options_grants_weighted_avg_q', 'fn_comp_options_out_intrinsic_value_a', 'fn_comp_options_out_intrinsic_value_q', 'fn_comp_options_out_number_a', 'fn_comp_options_out_number_q', 'fn_comp_options_out_weighted_avg_a', 'fn_comp_options_out_weighted_avg_q', 'fn_comprehensive_income_net_of_tax_a', 'fn_comprehensive_income_net_of_tax_q', 'fn_debt_instrument_carrying_amount_a', 'fn_debt_instrument_carrying_amount_q', 'fn_debt_instrument_face_amount_a', 'fn_debt_instrument_face_amount_q', 'fn_debt_instrument_interest_rate_stated_percentage_a', 'fn_debt_instrument_interest_rate_stated_percentage_q', 'fn_debt_issuance_costs_a', 'fn_debt_issuance_costs_q', 'fn_def_income_tax_expense_a', 'fn_def_income_tax_expense_q', 'fn_def_tax_assets_liab_net_a', 'fn_def_tax_assets_liab_net_q', 'fn_def_tax_assets_net_a', 'fn_def_tax_assets_net_q', 'fn_def_tax_liab_a', 'fn_def_tax_liab_q', 'fn_derivative_fair_value_of_derivative_asset_a', 'fn_derivative_fair_value_of_derivative_asset_q', 'fn_derivative_fair_value_of_derivative_liability_a', 'fn_derivative_fair_value_of_derivative_liability_q', 'fn_derivative_notional_amount_a', 'fn_derivative_notional_amount_q', 'fn_eff_income_tax_rate_continuing_operations_a', 'fn_eff_income_tax_rate_continuing_operations_q', 'fn_effect_of_exchange_rate_on_cash_and_equiv_a', 'fn_effect_of_exchange_rate_on_cash_and_equiv_q', 'fn_employee_related_liab_a', 'fn_employee_related_liab_q', 'fn_entity_common_stock_shares_out_a', 'fn_entity_common_stock_shares_out_q', 'fn_excess_tax_benefit_from_share_based_comp_fin_activities_a', 'fn_excess_tax_benefit_from_share_based_comp_fin_activities_q', 'fn_finite_lived_intangible_assets_acq_a', 'fn_finite_lived_intangible_assets_acq_q', 'fn_finite_lived_intangible_assets_gross_a', 'fn_finite_lived_intangible_assets_gross_q', 'fn_finite_lived_intangible_assets_net_a', 'fn_finite_lived_intangible_assets_net_q', 'fn_goodwill_acquired_during_period_a', 'fn_goodwill_acquired_during_period_q', 'fn_income_from_equity_investments_a', 'fn_income_from_equity_investments_q', 'fn_income_tax_expense_a', 'fn_income_tax_expense_q', 'fn_income_taxes_paid_a', 'fn_income_taxes_paid_q', 'fn_incremental_shares_attributable_to_share_based_payment_a', 'fn_incremental_shares_attributable_to_share_based_payment_q', 'fn_intangible_assets_accum_amort_a', 'fn_intangible_assets_accum_amort_q', 'fn_interest_paid_net_a', 'fn_interest_paid_net_q', 'fn_interest_payable_a', 'fn_interest_payable_q', 'fn_liab_fair_val_a', 'fn_liab_fair_val_l1_a', 'fn_liab_fair_val_l1_q', 'fn_liab_fair_val_l2_a', 'fn_liab_fair_val_l2_q', 'fn_liab_fair_val_l3_a', 'fn_liab_fair_val_l3_q', 'fn_liab_fair_val_q', 'fn_line_of_credit_facility_amount_out_a', 'fn_line_of_credit_facility_amount_out_q', 'fn_line_of_credit_facility_max_borrowing_capacity_a', 'fn_line_of_credit_facility_max_borrowing_capacity_q', 'fn_mne_a', 'fn_new_shares_issued_a', 'fn_new_shares_options_a', 'fn_new_shares_options_q', 'fn_op_lease_min_pay_due_a', 'fn_op_lease_min_pay_due_after_5y_a', 'fn_op_lease_min_pay_due_in_2y_a', 'fn_op_lease_min_pay_due_in_3y_a', 'fn_op_lease_min_pay_due_in_4y_a', 'fn_op_lease_min_pay_due_in_5y_a', 'fn_op_lease_rent_exp_a', 'fn_oth_comp_fair_value_a', 'fn_oth_comp_forfeitures_fair_value_a', 'fn_oth_comp_grants_weighted_avg_grant_date_fair_value_a', 'fn_oth_comp_grants_weighted_avg_grant_date_fair_value_q', 'fn_oth_income_loss_available_for_sale_securities_adj_of_tax_a', 'fn_oth_income_loss_available_for_sale_securities_adj_of_tax_q', 'fn_oth_income_loss_derivatives_qualifying_as_hedges_of_tax_a', 'fn_oth_income_loss_derivatives_qualifying_as_hedges_of_tax_q', 'fn_oth_income_loss_fx_transaction_and_tax_translation_adj_a', 'fn_oth_income_loss_fx_transaction_and_tax_translation_adj_q', 'fn_oth_income_loss_net_of_tax_a', 'fn_oth_income_loss_net_of_tax_q', 'fn_payments_for_repurchase_of_common_stock_a', 'fn_payments_for_repurchase_of_common_stock_q', 'fn_payments_to_acquire_businesses_net_of_cash_acquired_a', 'fn_payments_to_acquire_businesses_net_of_cash_acquired_q', 'fn_ppne_gross_a', 'fn_ppne_gross_q', 'fn_prepaid_expense_a', 'fn_prepaid_expense_q', 'fn_proceeds_from_issuance_of_common_stock_a', 'fn_proceeds_from_issuance_of_common_stock_q', 'fn_proceeds_from_issuance_of_debt_a', 'fn_proceeds_from_issuance_of_debt_q', 'fn_proceeds_from_lt_debt_a', 'fn_proceeds_from_lt_debt_q', 'fn_proceeds_from_stock_options_exercised_a', 'fn_proceeds_from_stock_options_exercised_q', 'fn_profit_loss_a', 'fn_profit_loss_q', 'fn_repayments_of_debt_a', 'fn_repayments_of_debt_q', 'fn_repayments_of_lines_of_credit_a', 'fn_repayments_of_lines_of_credit_q', 'fn_repayments_of_lt_debt_a', 'fn_repayments_of_lt_debt_q', 'fn_repurchased_shares_a', 'fn_repurchased_shares_q', 'fn_repurchased_shares_value_a', 'fn_repurchased_shares_value_q', 'fn_taxes_payable_a', 'fn_taxes_payable_q', 'fn_treasury_stock_shares_a', 'fn_treasury_stock_shares_q', 'fn_unrecognized_tax_benefits_a']

data = dict()

data['USA'] = Price_Volume + Fundamental_USA + Estimate + Relationship + Sentiment + Model_Data + US_News_Data + Model_Ratings_Data +\
      Volatility_Data + Stock_Reports_Plus + Systematic_Risk_Metrics + Options_Analytics + Street_Events + Analyst_Revision_Score +\
      Short_Interest_Model + EPS_Estimate_Model + Credit_Risk_Model + Price_Momentum_Model + Revenue_Estimate_Model + Insider_Model +\
      Growth_Valuation_Model + Smart_Ratios + Smart_Holdings + Analyst_Revisions + Volatility_and_Risk_Factor_Data + EBITDA_Estimate_Model +\
      Price_Target_Data + Performance_Metrics_Data + Institutional_Ownership_Data \
      + Creditworthiness_Model + Fundamental_Scores + Fundamental_Analysis_Model + Report_Footnotes

data['EUR'] = Price_Volume + Fundamental_EUR + Stock_Reports_Plus + Analyst_Revision_Score + EPS_Estimate_Model + Credit_Risk_Model + Price_Momentum_Model +\
      Revenue_Estimate_Model + Growth_Valuation_Model + Smart_Ratios + Smart_Holdings + Analyst_Revisions + EBITDA_Estimate_Model \
      + Creditworthiness_Model + Fundamental_Scores #+ Fundamental_Analysis_Model + Report_Footnotes

data['ASI'] = Price_Volume + Fundamental_ASI + Stock_Reports_Plus + Analyst_Revision_Score + EPS_Estimate_Model + Credit_Risk_Model + Price_Momentum_Model +\
      Revenue_Estimate_Model + Growth_Valuation_Model + Smart_Ratios + Analyst_Revisions + EBITDA_Estimate_Model \
      + Creditworthiness_Model + Fundamental_Scores #+ Fundamental_Analysis_Model + Report_Footnotes
