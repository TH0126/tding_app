from ..models import Gbpaud60
from ..models import Gbpaud240

#分析条件で指定されたデータを取得
def maindatas_class(parts_out):
    
    curr = parts_out["cur"]
    time = parts_out["chart_time"]
    ymd_start = parts_out["ymd_start"]
    ymd_end = parts_out["ymd_end"]

    #EUR/USD
    if curr == "1":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
    #USD/JPY
    elif curr == "2":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")

    #EUR/JPY
    elif curr == "3":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")

    #GBP/JPY
    elif curr == "4":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")

    #GBP/USD
    elif curr == "5":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")

    #AUD/JPY
    elif curr == "6":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")

    #AUD/USD
    elif curr == "7":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")

    #EUR/AUD
    elif curr == "8":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")

    #GBP/AUD
    elif curr == "9":
        #1分足
        if time == "1":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #5分足
        elif time == "2":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #30分足
        elif time == "3":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #1時間足
        elif time == "4":
            main_datas = Gbpaud60.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #4時間足
        elif time == "5":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #日足
        elif time == "6":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #週足
        elif time == "7":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
        #月足
        elif time == "8":
            main_datas = Gbpaud240.objects.filter(time__gte=ymd_start,time__lte=ymd_end).order_by("row_no")
    
    #取得したデータを戻す
    return main_datas
