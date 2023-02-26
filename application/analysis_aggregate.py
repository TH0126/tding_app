# import psycopg2
from locale import currency
from ..models import TermsTable
from ..models import ResultDetail
import datetime
import pytz

#売りでの売買処理
def analysis_aggregate_create(py_out):

    #ユーザーIDセット
    user_id = py_out["user_id"]

    #最新の分析情報を取得
    term_table = TermsTable.objects.filter(user_id = user_id,del_f = "0").order_by('id').last()

    res_details = ResultDetail.objects.filter(user_id = user_id,terms_id = term_table.id,del_f = "0").order_by('id')

    #取引回数
    cnt = 0
    #勝率
    rate = 0.0
    #損益
    t_pips = 0.0

    w_cnt = 0

    attack_group = 0

    #取引回数、勝率、損益を算出
    for res_detail in res_details:
        #同じ取引グループの場合は集計対象から外す
        if attack_group != res_detail.start_no:

            #取引回数
            cnt += 1
            attack_group = res_detail.start_no

            #損益集計
            t_pips += float(res_detail.p_a_l)

            if res_detail.p_a_l > 0:
                w_cnt += 1
    
    #０を割るとエラーになるため
    if cnt != 0:
        rate = round((w_cnt / cnt) * 100,1)
    
    #term_tableに算出結果をセット
    term_update = TermsTable.objects.get(user_id = user_id,id = term_table.id,del_f = "0")
    
    term_update.tran_count = cnt
    term_update.win_rate = rate
    term_update.total_pips = t_pips

    term_update.save()

