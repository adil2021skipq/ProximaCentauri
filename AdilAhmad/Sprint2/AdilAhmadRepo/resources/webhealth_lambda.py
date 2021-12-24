# import datetime
# import urllib3
# import constants as constants
# from cloudwatch_putMetric import cloudwatchPutMetric
# from s3bucket import S3Bucket as s3b

# def lambda_handler(events, context):
#     CW = cloudwatchPutMetric()
#     URLS_MONITORED = s3b('adilahmadbucket').load('urls.json')
#     K=list(URLS_MONITORED['URLS'][0].keys())
#     values = {"URLS": []}
    
#     for i in range(len(K)):
#         dimensions = [
#         {'Name': 'URL', 'Value': URLS_MONITORED['URLS'][0][K[i]]}
#         ]
    
#         avail = get_availibility(URLS_MONITORED['URLS'][0][K[i]])
#         CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
#         latency = get_latency(URLS_MONITORED['URLS'][0][K[i]])
#         CW.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
    
#         val_dict={
#             "availability": avail,
#             "latency": latency
#             }
        
#         values['URLS'].append(val_dict)

#     return values
    
# def get_availibility(url):
    
#     http = urllib3.PoolManager()
#     response = http.request("GET", url)
#     if response.status == 200:
#         return 1.0
#     else:
#         return 0.0
        
# def get_latency(url):
    
#     http = urllib3.PoolManager()
#     start = datetime.datetime.now()
#     response = http.request("GET", url)
#     end = datetime.datetime.now()
#     diff = end - start
#     latency = round(diff.microseconds * 0.000001, 6)
#     return latency