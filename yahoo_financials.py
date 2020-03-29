import pandas as pd
import json
from urllib import request


def json_to_df(json_str):
    """
    parse raw bytes and return panda dataframes.
    :param json_str:
    :return:
    """
    data = []

    for row in json.loads(json_str):
        d = {}
        for k,v in row.items():
            if k=='endDate':d[k]= v['fmt']
            elif k != 'maxAge' and ('raw' in v):d[k] = v['raw']
        data.append(d)
    df = pd.DataFrame(data)
    return df.set_index('endDate').transpose()


def get_fundamentals(ticker):
    """
    This function returns dataframes for balance sheets, income statements and cashflow statements
    :param ticker: company ticker
    :return: tuple of 3 dataframes
    """
    url = 'https://finance.yahoo.com/quote/%s/cash-flow' % ticker
    with request.urlopen(url) as response:
        html = response.read()
        cf_json = html.split(b'cashflowStatementHistory":{"cashflowStatements":')[1].split(b'],"maxAge"')[0] + b']'
        bs_json = html.split(b'"balanceSheetHistory":{"balanceSheetStatements":')[1].split(b'],"maxAge"')[0] + b']'
        is_json = html.split(b'incomeStatementHistory":{"incomeStatementHistory":')[1].split(b'],"maxAge"')[0] + b']'

    bs = json_to_df(bs_json)
    is_ = json_to_df(is_json)
    cf = json_to_df(cf_json)
    return bs, is_, cf

def get_keystats(ticker):
    """
    Get key stats from Yahoo finance.
    :param ticker: ticker of the company
    :return: a panda data series
    """
    url = 'https://finance.yahoo.com/quote/%s/key-statistics'%ticker
    with request.urlopen(url) as response:
        html = response.read()
        key_stats = html.split(b'"QuoteSummaryStore":')[1].split(b',"financialsTemplate"')[0]+b'}'
    key_stats = json.loads(key_stats)['defaultKeyStatistics']
    return  pd.DataFrame(key_stats).transpose()['raw'].dropna()
