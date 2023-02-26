# import psycopg2
from locale import currency
from ..models import Gbpaud60
from ..models import Gbpaud240
from ..models import CurrencyLen
from ..models import ResultDetail
from ..models import DatasetTemp
from decimal import Decimal
from fractions import Fraction
from . import analysis_parts
import datetime
import pytz

#売りでの売買処理
#１時間足で上昇中の20MAが前回ローソク足よりポイントがマイナスになったら売った場合
def ma_sell_analysis(py_out):

    #connect postgreSQL
    # conn = psycopg2.connect(
    # port = 5433,
    # user = 'tding',
    # database = 'tding_db'
    # )

    # cur = conn.cursor()
    # cur.execute('SELECT * FROM article WHERE id = 6')
    # row = cur.fetchone()

    # message = row[0] + "/" + row[1] + "/" + row[2]
    # return message

    #ユーザーIDセット
    user_id = py_out["user_id"]
    #分析条件IDセット
    terms_id = py_out["terms_id"]
    #分析開始日付セット
    ymd_start = py_out["start_ymd"]

    #分析する通貨をセット
    curr = py_out["cur"]

    # 通貨設定マスタの読み込み
    cur_master = CurrencyLen.objects.filter(currency = curr,del_flg = 0).first()

    # チャートデータ(1h足)の読み込み
    ga60_datas = Gbpaud60.objects.all().order_by("row_no")

    cnt = 1
    #上昇・下落傾きフラグ
    pmFlg = "0"
    #一周カウントフラグ
    around_flg = "0"

    #利確、損切りpips
    profit_p = py_out["rikaku_val"]
    cost_p = py_out["songiri_val"]
    #各種設定値
    #傾き判断ローソク足数
    trend_val = 7

    sell_start = 0.0
    time_start = 0
    trend_list = []
    sell_pro = 0.0
    sell_cost = 0.0
    result_pips = 0.0

    attack_group = 0

    #trend_listは配列で直近maのローソク足（trend_val数に応じて）分のそれぞれの傾きがセットされている。
    #これをもとに現在の傾きを判断する。

    #1pipsあたりの値
    pips_1 = float(cur_master.pips)

    for ga60_data in ga60_datas:
        #初回の周回処理
        if around_flg == "0":
            #２つ目〜trend_val分までのデータ
            if cnt != 1 and cnt <= trend_val:
                if ma20 > float(ga60_data.ma):
                    #20MAが前回データより小さい場合は−１
                    trend_list.append(-1)
                else:
                    #20MAが前回データより大きい場合は＋１
                    trend_list.append(1)
            
                #trend_val分まで行ったか？
                if cnt == trend_val:
                    around_flg = "1"

            cnt += 1
            ma20 = float(ga60_data.ma)

        
        #trend_valの回数分一周したあと以降
        else:

            #現在のmaの傾きが上昇、下落、レンジなのか判断
            #傾き判断ローソク足数分を合計したときにプラスであれば＋１、マイナスであれば−１
            if sum(trend_list) < 0:
                pmFlg = "-1"
            elif sum(trend_list) > 0:
                pmFlg = "1"
            else:
                pmFlg = "0"
            
            #上昇中
            if pmFlg == '1':
                #まだショートキックしていない場合キックするかチェック
                if sell_start == 0.0:
                    #上昇中なのにMAが前回値より下がった
                    if ma20 > float(ga60_data.ma):
                        #ショートキックスタート
                        sell_start = float(ga60_data.close)
                        time_start = int(ga60_data.time)
                        #利確位置決定
                        sell_pro = sell_start - (pips_1  * float(profit_p))
                        #損失位置決定
                        sell_cost = sell_start + (pips_1 * float(cost_p))

            #売りが入っているか？
            if sell_start > 0.0 and time_start != int(ga60_data.time):

                #利確ポイントまで到達したか？
                if sell_pro >= float(ga60_data.low):
                    #利確ポイントに到達したので結果へ書き込み
                    result_pips = float(profit_p)
                    attack_group += 1

                    cre_result = ResultDetail.objects.create(
                        user_id = user_id,
                        terms_id = terms_id,
                        ymd_start = time_start,
                        value_start = sell_start,
                        ymd_end = int(ga60_data.time),
                        value_end = sell_pro,
                        p_a_l = result_pips,
                        buy_sell = py_out["buy_sell"],
                        start_no = attack_group,
                        end_no = 0,
                        del_f = "0",
                        created_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo')),
                        updated_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                    )
                    #利確のため売買リセット
                    sell_start = 0.0
                    time_start = 0
                    sell_pro = 0.0
                    sell_cost = 0.0

                #損切りポイントまで到達したか？
                elif sell_cost <= float(ga60_data.high):
                    #損切りポイントに到達したので結果へ書き込み
                    result_pips = float(cost_p) * -1
                    attack_group += 1

                    cre_result = ResultDetail.objects.create(
                        user_id = user_id,
                        terms_id = terms_id,
                        ymd_start = time_start,
                        value_start = sell_start,
                        ymd_end = int(ga60_data.time),
                        value_end = sell_cost,
                        p_a_l = result_pips,
                        buy_sell = py_out["buy_sell"],
                        start_no = attack_group,
                        end_no = 0,
                        del_f = "0",
                        created_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo')),
                        updated_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                    )
                    #損切りのため売買リセット
                    sell_start = 0.0
                    time_start = 0
                    sell_pro = 0.0
                    sell_cost = 0.0

            #傾きをラストイン・ファーストアウトして常にtrend_val数だけの要素数にする
            if ma20 > float(ga60_data.ma):
                del trend_list[0]
                trend_list.append(-1)
            else:
                del trend_list[0]
                trend_list.append(1)

            #どのような場合でもma20を更新
            ma20 = float(ga60_data.ma)


#4時間足で20MAが上昇中に１時間足で上昇中の20MAが前回ローソク足よりポイントがマイナスになったら売った場合
def ma14_sell_analysis(py_out):

    #ユーザーIDセット
    user_id = py_out["user_id"]
    #分析条件IDセット
    terms_id = py_out["terms_id"]
    #分析開始日付セット
    ymd_start = py_out["start_ymd"]

    #分析する通貨をセット
    curr = py_out["cur"]

    # 通貨設定マスタの読み込み
    cur_master = CurrencyLen.objects.filter(currency = curr,del_flg = 0).first()

    # チャートデータ(1h足)の読み込み
    ga60_datas = Gbpaud60.objects.all().order_by("row_no")

    # チャートデータ(4h足)の読み込み
    ga240_datas = Gbpaud240.objects.all().order_by("row_no")

    cnt = 1
    cnt_sub = 1
    #上昇・下落傾きフラグ
    #メイン処理分
    pmFlg = "0"
    #サブ処理分
    pmsFlg = "0"

    #一周カウントフラグ
    #メイン処理分
    around_flg = "0"
    #サブ処理分
    around_sub_flg = "0"

    #利確、損切りpips
    profit_p = py_out["rikaku_val"]
    cost_p = py_out["songiri_val"]
    #各種設定値
    #傾き判断ローソク足数
    #メイン処理分
    trend_val = 7
    #サブ処理分
    trend_sub_val = 7

    #メイン処理分
    sell_start = 0.0
    time_start = 0
    trend_list = []
    sell_pro = 0.0
    sell_cost = 0.0
    result_pips = 0.0

    attack_group = 0

    #サブ処理分
    trend_sub_list = []

    #trend_listは配列で直近maのローソク足（trend_val数に応じて）分のそれぞれの傾きがセットされている。
    #これをもとに現在の傾きを判断する。

    #サブである4hの傾きデータを抽出し仮データにセット
    for ga240_data in ga240_datas:
        #初回の周回処理
        if around_sub_flg == "0":
            #２つ目〜trend_sub_val分までのデータ
            if cnt_sub != 1 and cnt_sub <= trend_sub_val:
                if ma20_sub > float(ga240_data.ma):
                    trend_sub_list.append(-1)
                else:
                    trend_sub_list.append(1)
            
                #trend_sub_val分まで行ったか？
                if cnt_sub == trend_sub_val:
                    around_sub_flg = "1"


            cnt_sub += 1
            ma20_sub = float(ga240_data.ma)

        #trend_sub_valの回数分一周したあと以降
        else:

            #現在のmaの傾きが上昇、下落、レンジなのか判断
            if sum(trend_sub_list) < 0:
                pmsFlg = "-1"
            elif sum(trend_sub_list) > 0:
                pmsFlg = "1"
            else:
                pmsFlg = "0"
            
            #dataset_tempにmaの傾きデータをセット(１つ前の値までで傾きを判断)
            #(val1=time,str1=傾き)
            cre_sub = DatasetTemp.objects.create(
                user_id = user_id,
                terms_id = terms_id,
                val1 = ga240_data.time,
                str1 = pmsFlg
            )

            #傾きをラストイン・ファーストアウトして常にtrend_val数だけの要素数にする
            if ma20_sub > float(ga240_data.ma):
                del trend_sub_list[0]
                trend_sub_list.append(-1)
            else:
                del trend_sub_list[0]
                trend_sub_list.append(1)

            #どのような場合でもma20を更新
            ma20_sub = float(ga240_data.ma)

    #作成した結果を呼び出し
    sub_results = DatasetTemp.objects.filter(user_id = user_id, terms_id = terms_id).order_by("val1")

    #1pipsあたりの値
    pips_1 = float(cur_master.pips)

    i = 0

    for ga60_data in ga60_datas:
        #初回の周回処理
        if around_flg == "0":
            #２つ目〜trend_val分までのデータ
            if cnt != 1 and cnt <= trend_val:
                if ma20 > float(ga60_data.ma):
                    trend_list.append(-1)
                else:
                    trend_list.append(1)
            
                #trend_val分まで行ったか？
                if cnt == trend_val:
                    around_flg = "1"

            cnt += 1
            ma20 = float(ga60_data.ma)

        
        #trend_valの回数分一周したあと以降
        else:

            #現在のmaの傾きが上昇、下落、レンジなのか判断
            if sum(trend_list) < 0:
                pmFlg = "-1"
            elif sum(trend_list) > 0:
                pmFlg = "1"
            else:
                pmFlg = "0"
            
            #上昇中
            if pmFlg == '1':
                #まだショートキックしていない場合キックするかチェック
                if sell_start == 0.0:
                    #上昇中なのにMAが前回値より下がった
                    if ma20 > float(ga60_data.ma):
                        
                        sub_k = "0"

                        #サブデータ側が上昇中か
                        for sub_result in sub_results[i:]:
                            if ga60_data.time == sub_result.val1:
                                if sub_result.str1 == "1":

                                    #ショートキックスタート
                                    sell_start = float(ga60_data.close)
                                    time_start = int(ga60_data.time)
                                    #利確位置決定
                                    sell_pro = sell_start - (pips_1  * float(profit_p))
                                    #損失位置決定
                                    sell_cost = sell_start + (pips_1 * float(cost_p))

                                break
                            elif ga60_data.time < sub_result.val1:
                                if sub_k == "1":

                                    #ショートキックスタート
                                    sell_start = float(ga60_data.close)
                                    time_start = int(ga60_data.time)
                                    #利確位置決定
                                    sell_pro = sell_start - (pips_1  * float(profit_p))
                                    #損失位置決定
                                    sell_cost = sell_start + (pips_1 * float(cost_p))

                                break
                            
                            #前回分のサブ傾きをセット
                            sub_k = sub_result.str1

                            i += 1


            #売りが入っているか？
            if sell_start > 0.0 and time_start != int(ga60_data.time):

                #利確ポイントまで到達したか？
                if sell_pro >= float(ga60_data.low):
                    #利確ポイントに到達したので結果へ書き込み
                    result_pips = float(profit_p)
                    attack_group += 1

                    cre_result = ResultDetail.objects.create(
                        user_id = user_id,
                        terms_id = terms_id,
                        ymd_start = time_start,
                        value_start = sell_start,
                        ymd_end = int(ga60_data.time),
                        value_end = sell_pro,
                        p_a_l = result_pips,
                        buy_sell = py_out["buy_sell"],
                        start_no = 0,
                        end_no = 0,
                        del_f = "0",
                        created_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo')),
                        updated_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                    )
                    #利確のため売買リセット
                    sell_start = 0.0
                    time_start = 0
                    sell_pro = 0.0
                    sell_cost = 0.0

                #損切りポイントまで到達したか？
                elif sell_cost <= float(ga60_data.high):
                    #損切りポイントに到達したので結果へ書き込み
                    result_pips = float(cost_p) * -1
                    attack_group += 1

                    cre_result = ResultDetail.objects.create(
                        user_id = user_id,
                        terms_id = terms_id,
                        ymd_start = time_start,
                        value_start = sell_start,
                        ymd_end = int(ga60_data.time),
                        value_end = sell_cost,
                        p_a_l = result_pips,
                        buy_sell = py_out["buy_sell"],
                        start_no = 0,
                        end_no = 0,
                        del_f = "0",
                        created_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo')),
                        updated_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                    )
                    #損切りのため売買リセット
                    sell_start = 0.0
                    time_start = 0
                    sell_pro = 0.0
                    sell_cost = 0.0

            #傾きをラストイン・ファーストアウトして常にtrend_val数だけの要素数にする
            if ma20 > float(ga60_data.ma):
                del trend_list[0]
                trend_list.append(-1)
            else:
                del trend_list[0]
                trend_list.append(1)

            #どのような場合でもma20を更新
            ma20 = float(ga60_data.ma)


#4時間足のヒゲ発生による売買処理
#売り処理なのでアタック対象は上ヒゲ
#利確もしくは損切りするまで対象のローソク足があればアタック追加（ただし、指定した回数まで）
def hige_4hour_sell_analysis(py_out):

    #ユーザーIDセット
    user_id = py_out["user_id"]
    #分析条件IDセット
    terms_id = py_out["terms_id"]
    #分析開始日付セット
    if py_out["start_ymd"]:
        ymd_start_str = py_out["start_ymd"]
        ymd_start_str = ymd_start_str[:4] + "-" + ymd_start_str[4:6] + "-" + ymd_start_str[6:8] + " 00:00:00"
        ymd_start_dt = datetime.datetime.strptime(ymd_start_str, "%Y-%m-%d %H:%M:%S")
        ymd_start = datetime.datetime.timestamp(ymd_start_dt)
    else:
        ymd_start = 0

    #分析終了日付セット
    if py_out["end_ymd"]:
        ymd_end_str = py_out["end_ymd"]
        ymd_end_str = ymd_end_str[:4] + "-" + ymd_end_str[4:6] + "-" + ymd_end_str[6:8] + " 00:00:00"
        ymd_end_dt = datetime.datetime.strptime(ymd_end_str, "%Y-%m-%d %H:%M:%S")
        ymd_end_dt = ymd_end_dt + datetime.timedelta(days=1)
        ymd_end = datetime.datetime.timestamp(ymd_end_dt)
    else:
        ymd_end = 2147483647

    #分析する通貨をセット
    curr = py_out["cur"]

    # 通貨設定マスタの読み込み
    cur_master = CurrencyLen.objects.filter(currency = curr,del_flg = 0).first()

    #チャートのデータを取得
    parts_out = {
        "cur": curr,
        "chart_time": py_out["chart_time"],
        "ymd_start": int(ymd_start),
        "ymd_end": int(ymd_end)
    }
    main_datas = analysis_parts.maindatas_class(parts_out)

    # チャートデータ(4h足)の読み込み
    #ga240_datas = Gbpaud240.objects.all().order_by("row_no")

    #利確、損切りpips
    profit_p = Decimal(py_out["rikaku_val"])
    cost_p = Decimal(py_out["songiri_val"])

    #アタックフラグ
    attack_flg = "0"
    #アタック限界回数
    attack_lmt_cnt = 4

    #各種設定値
    #ヒゲの長さ指定（以上）（長い方）
    hige_long = Decimal("0.004")
    #ヒゲの長さ指定（以下）（短い方）
    hige_short = Decimal("0.002")

    up_hige = Decimal("0.0")
    down_hige = Decimal("0.0")
    sell_start = Decimal("0.0")
    start_datas = []
    sell_pro = Decimal("0.0")
    sell_cost = Decimal("0.0")
    result_pips = Decimal("0.0")
    Level1_lots = Decimal("10.0")
    Level2_lots = Decimal("10.0")
    fx_cost = Decimal("0.00015")

    attack_cnt = 0
    group_attack = 0


    #1pipsあたりの値
    pips_1 = Decimal(str(cur_master.pips))

    #ローソク足の上ヒゲと下ヒゲの長さを調べる
    for main_data in main_datas:

        #分析期間かチェック
        if int(main_data.time) >= int(ymd_start) and int(main_data.time) < int(ymd_end):

            #アタック中であれば利確か損切りに触れているかチェック
            if attack_cnt > 0 and start_datas[attack_cnt - 1]['time'] != int(main_data.time):

                #利確チェック
                if sell_pro >= Decimal(main_data.low):
                    #利確ポイントに到達したので結果へ書き込み
                    result_pips = profit_p

                    for start_data in start_datas:
                        cre_result = ResultDetail.objects.create(
                            user_id = user_id,
                            terms_id = terms_id,
                            ymd_start = int(start_data["time"]),
                            value_start = start_data["value"],
                            ymd_end = int(main_data.time),
                            value_end = sell_pro,
                            p_a_l = result_pips,
                            buy_sell = py_out["buy_sell"],
                            start_no = group_attack,
                            end_no = 0,
                            del_f = "0",
                            created_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo')),
                            updated_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                        )

                    #利確のため売買リセット
                    sell_start = Decimal("0.0")
                    start_datas = []
                    sell_pro = Decimal("0.0")
                    sell_cost = Decimal("0.0")
                    attack_cnt = 0

                #損切りチェック
                elif sell_cost <= Decimal(main_data.high):
                    #損切りポイントに到達したので結果へ書き込み
                    result_pips = cost_p * -1

                    for start_data in start_datas:
                            cre_result = ResultDetail.objects.create(
                                user_id = user_id,
                                terms_id = terms_id,
                                ymd_start = int(start_data["time"]),
                                value_start = start_data["value"],
                                ymd_end = int(main_data.time),
                                value_end = sell_cost,
                                p_a_l = result_pips,
                                buy_sell = py_out["buy_sell"],
                                start_no = group_attack,
                                end_no = 0,
                                del_f = "0",
                                created_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo')),
                                updated_at = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                            )
                    #損切りのため売買リセット
                    sell_start = Decimal("0.0")
                    start_datas = []
                    sell_pro = Decimal("0.0")
                    sell_cost = Decimal("0.0")
                    attack_cnt = 0

            #ローソク足が陽線か陰線かチェック
            #陽線の場合
            if Decimal(main_data.open) < Decimal(main_data.close):
                #上ヒゲの長さ
                up_hige = Decimal(main_data.high) - Decimal(main_data.close)
                #下ヒゲの長さ
                down_hige = Decimal(main_data.open) - Decimal(main_data.low)
            #陰線の場合
            else:
                #上ヒゲの長さ
                up_hige = Decimal(main_data.high) - Decimal(main_data.open)
                #下ヒゲの長さ
                down_hige = Decimal(main_data.close) - Decimal(main_data.low)
            
            #上ヒゲ対象のローソク足かチェック
            #上ヒゲが対象の場合
            if up_hige >= hige_long:
                #下ヒゲが上ヒゲに比べて小さい場合が対象
                if down_hige <= hige_short:
                    #対象のローソク足

                    #アタック開始もしくはアタック追加
                    #アタック後なので追加の場合
                    if attack_cnt > 0:
                        #アタック限界回数内かチェック（限界回数に到達していたら追加なし）
                        if attack_cnt < attack_lmt_cnt:
                            #アタック追加
                            attack_cnt += 1

                            #実際のプラマイゼロの位置を計算
                            sell_start = (sell_start + Decimal(main_data.close)) / Decimal(str(attack_cnt))
                            
                            #アタック時の値と時間を配列にセット
                            start_datas.append(
                                {
                                    "value":Decimal(main_data.close) \
                                    ,"time":int(main_data.time)
                                }
                            )

                            #利確位置決定
                            sell_pro = sell_start - (pips_1  * profit_p) / Decimal(str(attack_cnt))
                            #損失位置決定
                            sell_cost = sell_start + (pips_1 * cost_p) / Decimal(str(attack_cnt))


                    #アタック開始        
                    else:
                        #ショートキックスタート
                        attack_cnt += 1
                        group_attack += 1

                        #実際のプラマイゼロの位置を計算
                        sell_start = (sell_start + main_data.close) / Decimal(str(attack_cnt))
                        
                        #アタック時の値と時間を配列にセット
                        start_datas.append(
                            {
                                "value":Decimal(main_data.close) \
                                ,"time":int(main_data.time)
                            }
                        )

                        #利確位置決定
                        sell_pro = sell_start - (pips_1  * profit_p) / Decimal(str(attack_cnt))
                        #損失位置決定
                        sell_cost = sell_start + (pips_1 * cost_p) / Decimal(str(attack_cnt))


#
#サブ分析データ作成処理(sell)
def ma_sell_sub_create(py_out):
    result =1
    return result


#買いでの売買処理
def ma_buy_analysis(py_out):
    result = 1
    return result

