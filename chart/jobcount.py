from django.shortcuts import render
from account.models import Account
from urllib import parse
from django.conf import settings
from pyspark.sql.functions import desc, count
from datetime import datetime

now = datetime.now()
# Create your views here.

def job_end(request):
    jobendDf = settings.DF.select("job_posting_date")

    jobtemp = jobendDf.select("job_posting_date").groupBy("job_posting_date").agg(count("job_posting_date").alias("jobCount"))
    test = jobtemp.filter(jobtemp.job_posting_date != "").sort(desc("job_posting_date"))
    job_end = []
    for i in test:
        if(i!="상시"):
            arr=i.job_posting_date.split(".")
            first=datetime(arr[0],arr[1],arr[2])
            seconds = (first - now).total_seconds()
            if(seconds>=-7,776,000 and seconds<=0):
                job_end.append([i.job_posting_date,i.jobCount])
        else:
            job_end.append([i.job_posting_date,i.jobCount])
        
    # 각 스킬별 회사의 요구사항, Distinct Count
    return render(request, 'charts/skillDetail.html', {"job_end":job_end})