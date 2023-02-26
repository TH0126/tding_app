from django.shortcuts import render
from django.http import HttpResponse
from .models import Gbpaud60
from .models import Gbpaud240
from .models import TermsTable
from .models import ResultDetail
from .application import ma_analysis
from .application import analysis_aggregate
import datetime
import pytz
import simplejson as json

# Create your views here.
# 入力条件create処理
def input(request):

    if request.method == 'POST':

        user_id = "1"
        cur = request.POST['currency']
        chart_time = request.POST['chart_time']
        start_ymd = request.POST['b_from_ymd']
        end_ymd = request.POST['b_to_ymd']
        rikaku_val = request.POST['rikaku_val']
        songiri_val = request.POST['songiri_val']
        wait_flg = request.POST['wait']

        #買うボタンを押した場合
        if "buy_button" in request.POST:
            buy_sell = "1"
        #売るボタンを押した場合
        elif "sell_button" in request.POST:
            buy_sell = "2"

        #terms_tableに分析条件データをセット
        cre_terms = TermsTable.objects.create(
            user_id = user_id,
            currency = cur,
            chart_time = chart_time,
            b_from_ymd = start_ymd,
            b_to_ymd = end_ymd,
            rikaku = rikaku_val,
            songiri = songiri_val,
            wait = wait_flg,
            # trend = models.CharField(max_length=1, blank=True, null=True)
            # trend_ma1 = models.SmallIntegerField(blank=True, null=True)
            # trend_ma2 = models.SmallIntegerField(blank=True, null=True)
            # trend_ma3 = models.SmallIntegerField(blank=True, null=True)
            # trend_mtf1 = models.CharField(max_length=6, blank=True, null=True)
            # trend_mtf2 = models.CharField(max_length=6, blank=True, null=True)
            # trend_mtf3 = models.CharField(max_length=6, blank=True, null=True)
            # nehaba = models.CharField(max_length=1, blank=True, null=True)
            # vola_from = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
            # vola_to = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
            # pips_from = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
            # pips_to = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
            # period = models.CharField(max_length=1, blank=True, null=True)
            # wave = models.SmallIntegerField(blank=True, null=True)
            # hour_from = models.SmallIntegerField(blank=True, null=True)
            # hour_to = models.SmallIntegerField(blank=True, null=True)
            # term_1 = models.CharField(max_length=3, blank=True, null=True)
            # term_2 = models.CharField(max_length=3, blank=True, null=True)
            # term_3 = models.CharField(max_length=3, blank=True, null=True)
            # term_4 = models.CharField(max_length=3, blank=True, null=True)
            buy_sell = buy_sell,
            del_f = "0",
            created_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo')),
            updated_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        )

        #今回の分析条件IDを取得
        term_table = TermsTable.objects.values('id').filter(user_id = user_id,currency = cur,chart_time = chart_time,buy_sell = buy_sell,del_f = "0").order_by('created_at').last()
        


        py_out = {
            "cur": cur,
            "chart_time": chart_time,
            "start_ymd": start_ymd,
            "end_ymd": end_ymd,
            "rikaku_val": rikaku_val,
            "songiri_val": songiri_val,
            "buy_sell": buy_sell,
            "user_id": user_id,
            "terms_id": term_table['id'],
        }

        if buy_sell == "1":
            analysis = ma_analysis.ma_buy_analysis(py_out)
            result = analysis_aggregate.analysis_aggregate_create(py_out)
        elif buy_sell == "2":
            #サブ分析データ作成(DatasetTempにセット)
            
            # analysis = ma_analysis.ma_sell_analysis(py_out)
            # analysis = ma_analysis.ma14_sell_analysis(py_out)
            analysis = ma_analysis.hige_4hour_sell_analysis(py_out)
            result = analysis_aggregate.analysis_aggregate_create(py_out)

        
    return render(request, "tding_app/input.html")

def anlys_data(request):
    user_id = "1"

    #最新の分析結果情報を取得
    term_table = TermsTable.objects.filter(user_id = user_id,del_f = "0").order_by('id').last()

    #通貨の名称取得
    if term_table.currency == "1":
        currency = "EUR / USD"
    elif term_table.currency == "2":
        currency = "USD / JPY"
    elif term_table.currency == "3":
        currency = "EUR / JPY"
    elif term_table.currency == "4":
        currency = "GBP / JPY"
    elif term_table.currency == "5":
        currency = "GBP / USD"
    elif term_table.currency == "6":
        currency = "AUD / JPY"
    elif term_table.currency == "7":
        currency = "AUD / USD"
    elif term_table.currency == "8":
        currency = "EUR / AUD"
    elif term_table.currency == "9":
        currency = "GBP / AUD"
    
    #時間足の名称取得
    if term_table.chart_time == "1":
        cha_time = "1分足"
    elif term_table.chart_time == "2":
        cha_time = "5分足"
    elif term_table.chart_time == "3":
        cha_time = "30分足"
    elif term_table.chart_time == "4":
        cha_time = "1時間足"
    elif term_table.chart_time == "5":
        cha_time = "4時間足"
    elif term_table.chart_time == "6":
        cha_time = "1日足"
    elif term_table.chart_time == "7":
        cha_time = "週足"
    elif term_table.chart_time == "8":
        cha_time = "月足"

    #分析期間
    if term_table.b_to_ymd:
        period = term_table.b_from_ymd[:4] + "/" + term_table.b_from_ymd[4:6] + "/" + term_table.b_from_ymd[6:8] + " 〜 " + term_table.b_to_ymd[:4] + "/" + term_table.b_to_ymd[4:6] + "/" + term_table.b_to_ymd[6:8]
    else:
        period = term_table.b_from_ymd[:4] + "/" + term_table.b_from_ymd[4:6] + "/" + term_table.b_from_ymd[6:8] + " 〜"

    #買いか売りか
    if term_table.buy_sell == "1":
        B_S = "BUY（買い）"
    elif term_table.buy_sell == "2":
        B_S = "SELL（売り）"

    #結果データを抽出
    res_details = ResultDetail.objects.filter(user_id = user_id,terms_id = term_table.id,del_f = "0").order_by('id')

    #結果データを加工したデータを作成
    data_results = []

    for res_detail in res_details:
        s_dt = datetime.datetime.fromtimestamp(res_detail.ymd_start)
        s_datetime = s_dt.strftime("%Y/%m/%d %H:%M")

        e_dt = datetime.datetime.fromtimestamp(res_detail.ymd_end)
        e_datetime = e_dt.strftime("%Y/%m/%d %H:%M")

        data_results.append(
            {
                 "no":res_detail.start_no \
                ,"s_datetime":s_datetime \
                ,"value_start":res_detail.value_start \
                ,"e_datetime":e_datetime \
                ,"value_end":res_detail.value_end \
                ,"pal":res_detail.p_a_l
            }
        )
    
    params = {
        "currency": currency,
        "cha_time": cha_time,
        "period": period,
        "rikaku": term_table.rikaku,
        "songiri": term_table.songiri,
        "B_S": B_S,
        "cnt": term_table.tran_count,
        "per": term_table.win_rate,
        "val": format(term_table.total_pips, '.2f'),
        "data_results": data_results,
    }

    return render(request, "tding_app/analysis_data.html", params)



def anlys_chr(request):

    user_id = "1"

    #最新の分析結果情報を取得
    term_table = TermsTable.objects.filter(user_id = user_id,del_f = "0").order_by('id').last()

    # チャートデータ(1h足)の読み込み
    results = Gbpaud60.objects.all().order_by('row_no')
    res_max_cnt = Gbpaud60.objects.count()

    # 取得したデータをJSONデータに変換
    output = []
    ma20_output = []
    ma75_output = []
    ma200_output = []
    mtf1d_output = []
    mtf1w_output = []

    for result in results:
        # メインチャートデータをセット
        output.append(
            {
                 "time":result.time +32400 \
                ,"open":result.open \
                ,"high":result.high \
                ,"low":result.low \
                ,"close":result.close
            }
        )
        # MA20データをセット
        ma20_output.append(
            {
                 "time":result.time + 32400 \
                ,"value":result.ma
            }
        )
        # MA75データをセット
        ma75_output.append(
            {
                 "time":result.time + 32400 \
                ,"value":result.ma_1
            }
        )
        # MA200データをセット
        ma200_output.append(
            {
                 "time":result.time + 32400 \
                ,"value":result.ma_2
            }
        )
        # MTF1dayデータをセット
        mtf1d_output.append(
            {
                 "time":result.time + 32400 \
                ,"value":result.mtf_ma1
            }
        )
        # MTF1weekデータをセット
        mtf1w_output.append(
            {
                 "time":result.time + 32400 \
                ,"value":result.mtf_ma
            }
        )

    # チャートデータ(4h足)の読み込み
    results4 = Gbpaud240.objects.all().order_by('row_no')
    res4_max_cnt = Gbpaud240.objects.count()

    # 取得したデータをJSONデータに変換
    output4 = []
    ma20_output4 = []
    ma75_output4 = []
    ma200_output4 = []
    mtf1d_output4 = []
    mtf1w_output4 = []

    for result4 in results4:
        # メインチャートデータをセット
        output4.append(
            {
                 "time":result4.time +32400 \
                ,"open":result4.open \
                ,"high":result4.high \
                ,"low":result4.low \
                ,"close":result4.close
            }
        )
        # MA20データをセット
        ma20_output4.append(
            {
                 "time":result4.time + 32400 \
                ,"value":result4.ma
            }
        )
        # MA75データをセット
        ma75_output4.append(
            {
                 "time":result4.time + 32400 \
                ,"value":result4.ma_1
            }
        )
        # MA200データをセット
        ma200_output4.append(
            {
                 "time":result4.time + 32400 \
                ,"value":result4.ma_2
            }
        )
        # MTF1dayデータをセット
        mtf1d_output4.append(
            {
                 "time":result4.time + 32400 \
                ,"value":result4.mtf_ma1
            }
        )
        # MTF1weekデータをセット
        mtf1w_output4.append(
            {
                 "time":result4.time + 32400 \
                ,"value":result4.mtf_ma
            }
        )
    
    # markerセット用のデータを作成

    #sell-startのマーク
    marker_ss = []
    marker4_ss = []
    #sell-endのマーク
    marker_se = []
    marker4_se = []
    #buy-startのマーク
    marker_bs = []
    marker4_bs = []
    #buy-endのマーク
    marker_be = []
    marker4_be = []

    #結果データを抽出
    res_details = ResultDetail.objects.filter(user_id = user_id,terms_id = term_table.id,del_f = "0").order_by('id')

    #ローソク位置を特定して出力データにセット
    #買いの場合
    if term_table.buy_sell == "1":
        for res_detail in res_details:
            #スタート位置取得＆セット
            #分析対象が１時間足
            if term_table.chart_time == "4":
                res_start = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res4_start = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res_end = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()
                res4_end = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()
            #分析対象が４時間足
            elif term_table.chart_time == "5":
                res_start = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res_start['row_no'] = res_start['row_no'] + 3
                res4_start = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res_end = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()
                res_end['row_no'] = res_end['row_no'] + 3
                res4_end = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()

            marker_bs.append({"start_no":int(res_max_cnt) - int(res_start['row_no'])})
            marker4_bs.append({"start_no":int(res4_max_cnt) - int(res4_start['row_no'])})
            marker_be.append({"end_no":int(res_max_cnt) - int(res_end['row_no'])})
            marker4_be.append({"end_no":int(res4_max_cnt) - int(res4_end['row_no'])})
    #売りの場合
    elif term_table.buy_sell == "2":
        for res_detail in res_details:
            #スタート位置取得＆セット
            #分析対象が１時間足
            if term_table.chart_time == "4":
                res_start = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res4_start = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res_end = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()
                res4_end = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()
            #分析対象が４時間足
            elif term_table.chart_time == "5":
                res_start = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res_start['row_no'] = res_start['row_no'] + 3
                res4_start = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_start).order_by('-time').first()
                res_end = Gbpaud60.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()
                res_end['row_no'] = res_end['row_no'] + 3
                res4_end = Gbpaud240.objects.values('row_no').filter(time__lte = res_detail.ymd_end).order_by('-time').first()

            marker_ss.append({"start_no":int(res_max_cnt) - int(res_start['row_no']), "group_cnt":res_detail.start_no})
            marker4_ss.append({"start_no":int(res4_max_cnt) - int(res4_start['row_no']), "group_cnt":res_detail.start_no})
            marker_se.append({"end_no":int(res_max_cnt) - int(res_end['row_no']), "group_cnt":res_detail.start_no})
            marker4_se.append({"end_no":int(res4_max_cnt) - int(res4_end['row_no']), "group_cnt":res_detail.start_no})


    # JSONデータに変換
    json_output = json.dumps(output)
    json_ma20 = json.dumps(ma20_output)
    json_ma75 = json.dumps(ma75_output)
    json_ma200 = json.dumps(ma200_output)
    json_mtf1d = json.dumps(mtf1d_output)
    json_mtf1w = json.dumps(mtf1w_output)
    json4_output = json.dumps(output4)
    json4_ma20 = json.dumps(ma20_output4)
    json4_ma75 = json.dumps(ma75_output4)
    json4_ma200 = json.dumps(ma200_output4)
    json4_mtf1d = json.dumps(mtf1d_output4)
    json4_mtf1w = json.dumps(mtf1w_output4)

    json_markbs = json.dumps(marker_bs)
    json4_markbs = json.dumps(marker4_bs)
    json_markbe = json.dumps(marker_be)
    json4_markbe = json.dumps(marker4_be)
    json_markss = json.dumps(marker_ss)
    json4_markss = json.dumps(marker4_ss)
    json_markse = json.dumps(marker_se)
    json4_markse = json.dumps(marker4_se)

    params = {
        "data": json_output,
        "ma20": json_ma20,
        "ma75": json_ma75,
        "ma200": json_ma200,
        "mtf1d": json_mtf1d,
        "mtf1w": json_mtf1w,
        "data_4": json4_output,
        "ma20_4": json4_ma20,
        "ma75_4": json4_ma75,
        "ma200_4": json4_ma200,
        "mtf1d_4": json4_mtf1d,
        "mtf1w_4": json4_mtf1w,
        "mark_bs": json_markbs,
        "mark_be": json_markbe,
        "mark_ss": json_markss,
        "mark_se": json_markse,
        "mark4_bs": json4_markbs,
        "mark4_be": json4_markbe,
        "mark4_ss": json4_markss,
        "mark4_se": json4_markse,
    }

    return render(request, "tding_app/analysis_chart.html", params)
