from django.db import models

# Create your models here.
class CurrencyLen(models.Model):
    cur_id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=10)
    int_len = models.SmallIntegerField()
    decimal_len = models.SmallIntegerField()
    pips = models.FloatField()
    history = models.SmallIntegerField()
    del_flg = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'currency_len'


class DatasetTemp(models.Model):
    user_id = models.SmallIntegerField()
    terms_id = models.IntegerField()
    val1 = models.IntegerField(blank=True, null=True)
    val2 = models.IntegerField(blank=True, null=True)
    val3 = models.IntegerField(blank=True, null=True)
    val4 = models.IntegerField(blank=True, null=True)
    val5 = models.IntegerField(blank=True, null=True)
    str1 = models.CharField(max_length=128, blank=True, null=True)
    str2 = models.CharField(max_length=128, blank=True, null=True)
    str3 = models.CharField(max_length=128, blank=True, null=True)
    str4 = models.CharField(max_length=128, blank=True, null=True)
    str5 = models.CharField(max_length=128, blank=True, null=True)
    num1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    num2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_temp'


class Gbpaud240(models.Model):
    row_no = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    ymd = models.DateTimeField(blank=True, null=True)
    open = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    high = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    low = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    close = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_pivot = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_r1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_s1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_r2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_s2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_pivot = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_r1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_s1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_r2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_s2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    mtf_ma = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    mtf_ma1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    mtf_ma2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    ma = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    ma_1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    ma_2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gbpaud_240'


class Gbpaud60(models.Model):
    row_no = models.AutoField(primary_key=True)
    time = models.IntegerField()
    ymd = models.DateTimeField(blank=True, null=True)
    open = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    high = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    low = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    close = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_pivot = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_r1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_s1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_r2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    daily_s2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_pivot = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_r1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_s1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_r2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    weekly_s2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    mtf_ma = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    mtf_ma1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    mtf_ma2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    ma = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    ma_1 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)
    ma_2 = models.DecimalField(max_digits=6, decimal_places=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gbpaud_60'


class ResultDetail(models.Model):
    user_id = models.SmallIntegerField()
    terms_id = models.IntegerField()
    ymd_start = models.IntegerField()
    value_start = models.DecimalField(max_digits=10, decimal_places=5)
    ymd_end = models.IntegerField(blank=True, null=True)
    value_end = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    p_a_l = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    buy_sell = models.CharField(max_length=1)
    start_no = models.IntegerField()
    end_no = models.IntegerField(blank=True, null=True)
    del_f = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'result_detail'


class TermsTable(models.Model):
    user_id = models.IntegerField()
    currency = models.CharField(max_length=2)
    chart_time = models.CharField(max_length=2)
    b_from_ymd = models.CharField(max_length=14)
    b_to_ymd = models.CharField(max_length=14, blank=True, null=True)
    rikaku = models.DecimalField(max_digits=6, decimal_places=2)
    songiri = models.DecimalField(max_digits=6, decimal_places=2)
    wait = models.CharField(max_length=1)
    trend = models.CharField(max_length=1, blank=True, null=True)
    trend_ma1 = models.SmallIntegerField(blank=True, null=True)
    trend_ma2 = models.SmallIntegerField(blank=True, null=True)
    trend_ma3 = models.SmallIntegerField(blank=True, null=True)
    trend_mtf1 = models.CharField(max_length=6, blank=True, null=True)
    trend_mtf2 = models.CharField(max_length=6, blank=True, null=True)
    trend_mtf3 = models.CharField(max_length=6, blank=True, null=True)
    nehaba = models.CharField(max_length=1, blank=True, null=True)
    vola_from = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    vola_to = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pips_from = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    pips_to = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    period = models.CharField(max_length=1, blank=True, null=True)
    wave = models.SmallIntegerField(blank=True, null=True)
    hour_from = models.SmallIntegerField(blank=True, null=True)
    hour_to = models.SmallIntegerField(blank=True, null=True)
    term_1 = models.CharField(max_length=3, blank=True, null=True)
    term_2 = models.CharField(max_length=3, blank=True, null=True)
    term_3 = models.CharField(max_length=3, blank=True, null=True)
    term_4 = models.CharField(max_length=3, blank=True, null=True)
    buy_sell = models.CharField(max_length=1, blank=True, null=True)
    tran_count = models.SmallIntegerField(blank=True, null=True)
    win_rate = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    del_f = models.CharField(max_length=1)
    total_pips = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'terms_table'


class UserMaster(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    power = models.CharField(max_length=1)
    history_no = models.SmallIntegerField()
    del_f = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_master'


