from django.shortcuts import render
from django.conf import settings
from pyspark.sql.functions import explode, count, desc, countDistinct, lower, monotonically_increasing_id
from django.http import HttpResponse
# Create your views here.

def top100Skills(request):
    #  각 스킬별 채용 공고에 나타난 횟수
    # temp = settings.DF.select(explode(settings.DF.skill_stacks).alias("skill"), "company_name")
    # skillCount = temp.groupBy("skill")\
    #                 .agg(count("skill").alias("skillCount"))\
    #                 .filter(temp.skill != "")\
    #                 .sort(desc("skillCount"))
    # skillCount.collect()

    # companyCount = temp.groupBy("skill")\
    #             .agg(countDistinct("company_name").alias("companyCount"))\
    #             .filter(temp.skill != "")\
    #             .sort(desc("companyCount"))
    # companyCount.collect()                
    # joined_df = skillCount.join(companyCount, ['skill'], 'outer')
    # joined_df = joined_df\
    #                     .filter(joined_df.skill!="")\
    #                     .sort(desc("skillCount")).take(100)
    joined_df = settings.JOINED_DF.take(100)
    # joined_df = joined_df.withColumn("index", monotonically_increasing_id()+1)
    skills = []
    for idx,i in enumerate(joined_df):
        if i.skill.find("/"):
            temp = i.__getattr__("skill").replace("/","and")
            skills.append([idx+1,temp,i.skillCount,i.companyCount])
            continue
        skills.append([idx+1,i.skill,i.skillCount,i.companyCount])

    
    # 각 스킬별 회사의 요구사항, Distinct Count
    return render(request, 'charts/top100Skills.html', {"skills":skills})
    
def searchResult(request):
    if "skill" in request.GET:
        searchedSkillName = request.GET['skill']

        joined_df = settings.JOINED_DF
        searchResult = joined_df.filter(lower(joined_df.skill).contains(searchedSkillName.lower()))\
                                .sort(desc("skillCount"))\
                                .collect()
        
        skills = []
        for idx, i in enumerate(searchResult):
            if i.skill.find("/"):
                temp = i.__getattr__("skill").replace("/","and")
                skills.append([idx+1,temp,i.skillCount,i.companyCount])
                continue
            skills.append([idx+1,i.skill,i.skillCount,i.companyCount])
        return render(request, 'charts/searchResult.html', {"skills":skills, "searchedSkillName":searchedSkillName})
        


    

def test(request):
    skill = ""
    if 'skill' in request.GET:
        skill = request.GET['skill']
    return HttpResponse(skill)






















# class ChartView(TemplateView):
#     template_name = 'chart/chart.html'
    
#     def __init__(self) -> None:
#         conf = pyspark.SparkConf().set('spark.jars.packages','org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')
#         sc = SparkContext(conf=conf).getOrCreate()
#         sqlContext = SQLContext(sc)
#         my_spark = SparkSession \
#             .builder \
#             .master('local')\
#             .appName("myApp") \
#             .config("spark.mongodb.input.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/wanted.wanted?readPreference=primaryPreferred") \
#             .config("spark.mongodb.output.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/test.wanted") \
#             .getOrCreate()
#         self.df  = my_spark.read.format("mongo").option("uri","mongodb://165.132.172.93/wanted.wanted").load()
#         # test = self.df.filter("UPPER(job_title) LIKE UPPER('%JAVA%')")
#         test = self.df.filter(sql_fun.lower(self.df.job_title).contains("java"))
#         print(test.count())

#     def get_context_data(self, **kwargs):
#         # print(self.df.printSchema())
#         context = super().get_context_data(**kwargs)
#         context["qs"] = Editors.objects.all()
#         context = dict(context)
#         for c in context:
#             print(type(c))
#         return context
    

# class Mongo_DB:
#     def __init__(self, mongo_uri, account, passwd):
#         self.mongo_uri = mongo_uri
#         self.account = account
#         self.passwd= passwd
#         url = 'mongodb://%s:%s@%s:27017/?authSource=admin' % (self.account, parse.quote_plus(self.passwd), self.mongo_uri)
#         client = pymongo.MongoClient(url)
#         self.db = client['wanted']

# def test(request):
#     conn = Mongo_DB('165.132.172.93','thwhd1','thwhd1')
#     cursor = conn.db['wanted'].find({})
#     df = pd.DataFrame(list(cursor))
#     print(df)