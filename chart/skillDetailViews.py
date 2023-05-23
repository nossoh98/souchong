from django.shortcuts import render
from account.models import Account
from urllib import parse
from django.conf import settings
from pyspark.sql.functions import explode, count, desc, countDistinct
from pyspark.sql.functions import explode, asc, desc, count
from pyspark.sql.functions import col
from pyspark.sql.functions import array_contains
from pyspark.sql.functions import round
from datetime import datetime

now = datetime.now()
# Create your views here.

def skillDetail(request,skill):
    # skill = "SQL"
    #  각 스킬별 채용 공고에 나타난 횟수
    temp = settings.DF.select(explode(settings.DF.skill_stacks).alias("skill"), "company_name")
    # skillCount = temp.groupBy("skill")\
    #                 .agg(count("skill").alias("skillCount"))\
    #                 .filter(temp.skill == skill)\
    #                 .sort(desc("skillCount"))
    
    # companyCount = temp.groupBy("skill")\
    #             .agg(countDistinct("company_name").alias("companyCount"))\
    #             .filter(temp.skill == skill)\
    #             .sort(desc("companyCount")) 
    temp = settings.JOINED_DF            
    temp = temp.filter(temp.skill == skill)
                    
    skillCount = temp.collect()[0]["skillCount"]
    companyCount = temp.collect()[0]["companyCount"]
    rank = temp.collect()[0]['index']
    
    skillStacksDf = settings.DF.select("skill_stacks")
    
    relatedRows = skillStacksDf.filter(array_contains(skillStacksDf.skill_stacks, skill))
    rowNum = relatedRows.count()

    relatedSkillCount = relatedRows.select(explode(relatedRows.skill_stacks).alias("skill"))
    relatedSkillCount = relatedSkillCount.groupBy("skill")\
                .agg(round((count("skill") / rowNum * 100), 2).alias("skillCount"))\
                .filter(relatedSkillCount.skill != skill)\
                .sort(desc("skillCount"))\
                .head(5)
    relatedSkills = []
    for i in relatedSkillCount:
        relatedSkills.append([i.skill,i.skillCount])
        
    jobendDf=settings.DF.select("skill_stacks","job_posting_date")
    jobtest2=jobendDf.filter(array_contains(jobendDf.skill_stacks, skill))
    jobtest=jobtest2.filter(jobtest2.job_posting_date!="").sort(asc("job_posting_date")).take(100000)
    job_end=[]
    job_end2=[]
    for i in jobtest:
        if i.job_posting_date !='상시':
            arr=i.job_posting_date.split('.')
            first=datetime(int(arr[0]),int(arr[1]),int(arr[2]))
            seconds = (first - now).total_seconds()
            if seconds>=-5184000 and seconds<=2592000:
                job_end2.append([i.job_posting_date])
        else:
            job_end2.append([i.job_posting_date])
    job_end.append(["",1])
    j=0
    sangsi=[]
    sangsi.append(["상시",0])
    for i in job_end2:
        if job_end[j][0]=="":
            job_end[j][0]=i[0]
        if i[0] == job_end[j][0]:
            job_end[j][1]=job_end[j][1]+1
        elif i[0]!='상시':
            job_end.append([i[0],1])
            j=j+1
        else:
            sangsi[0][1]=sangsi[0][1]+1
        
    # 각 스킬별 회사의 요구사항, Distinct Count
    
    
    #popular skilSet
    popularSkillCount = relatedRows.groupBy("skill_stacks")\
                .agg(count("skill_stacks").alias("skillCount"))\
                .sort(desc("skillCount"))\
                .select("skill_stacks")
    popularSkillCount = popularSkillCount.collect()
    popularSkillList = []
    popularSkillListSize = 12
    flag = False
    for i in popularSkillCount:
        if flag:
            break
        for popularSkill in i.skill_stacks:
            if popularSkill != skill and popularSkill not in popularSkillList:
                if popularSkill.find("/"):
                    popularSkill = popularSkill.replace("/","and")
                popularSkillList.append(popularSkill)
                if len(popularSkillList) == popularSkillListSize:
                    flag = True
                    break
             
                
    return render(request, 'charts/skillDetail.html', {"rank":rank, "skill":skill, "skillCount":skillCount, "companyCount":companyCount, "relatedSkills":relatedSkills, "job_end":job_end, "popularSkillList":popularSkillList, "sangsi":sangsi})