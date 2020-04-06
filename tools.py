# -*- coding: utf-8 -*- 

import sys
import config
import pymssql
import json
import requests
import logging
import logging.handlers
import time

#global conn
#conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database'],charset="UTF-8") 

#获取access_token值
def getToken(GetTokenUrl):
    url = GetTokenUrl
    html = requests.get(url)
    data = json.dumps(html.json())
    access_token = json.loads(str(data)).get('data').get('access_token')
    #tools.log(access_token,'info');
    return access_token

#连接数据库-查询,数据加列名
def database(conn,sql):
    #conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database']) ,
    #conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database'],charset="UTF-8") 
    cursor = conn.cursor() 
    if not cursor: 
        raise Exception('数据库连接失败！') 
    cursor.execute(sql)
    cols = cursor.description
    results = cursor.fetchall() 
    cursor.close() 
    #conn.close() 
    i = 0 
    datas = [] 
    while i < len(results): 
        i = i+1 
        result = results[i-1] 
        result = result
        datas.append(result) 
    return datas,cols

#连接数据库-查询
def databaseSelect(conn,sql):
    #conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database']) ,
    #conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database'],charset="UTF-8") 
    cursor = conn.cursor() 
    if not cursor: 
        raise Exception('数据库连接失败！') 
    cursor.execute(sql) 
    results = cursor.fetchall() 
    cursor.close() 
    #conn.close() 
    i = 0 
    datas = [] 
    print (results)
    while i < len(results): 
        i = i+1 
        result = results[i-1] 
        result = checkdata(result) 
        datas.append(result) 
    return datas 

#连接数据库-增删改
def databasesql(conn,sql,dicts = None):
    #conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database']) ,
    #conn = pymssql.connect(config.DatabaseInfo['DatabaseUrl'],config.DatabaseInfo['UserName'],config.DatabaseInfo['Password'],config.DatabaseInfo['Database'],charset="UTF-8") 
    cursor = conn.cursor() 
    if not cursor: 
        raise Exception('数据库连接失败！')
    if dicts == None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, dicts)
    conn.commit() 
    cursor.close() 
    #conn.close() 
    return

#用于将sql查出的不同格式的数据格式化为[[str],[str],[str],[str]],
def checkdata(data):
    j = 0
    datas = []
    while j < len(data):
        if isinstance(data[j],str):
            items = data[j].encode('unicode-escape')
            datas.append(items)
            j += 1
        elif isinstance(data[j],(float,bool)) or data[j] is None:
            item = str(data[j])
            datas.append(item)
            j += 1
        else:
            item = str(data[j])
            datas.append(item)
            j += 1
    return datas


#Python logging库类
class FinalLogger: 
    logger=None 
    levels={"n":logging.NOTSET, "d":logging.DEBUG, "i":logging.INFO, "w":logging.WARN, "e":logging.ERROR, "c":logging.CRITICAL} 
    log_level="d" 
    log_file=config.logfile 
    log_max_byte=10*1024*1024; 
    log_backup_count=5 

    @staticmethod 
    def getLogger(): 
        if FinalLogger.logger is not None: 
            return FinalLogger.logger 
        FinalLogger.logger=logging.Logger("oggingmodule.FinalLogger") 
        log_handler=logging.handlers.RotatingFileHandler(filename=FinalLogger.log_file,maxBytes=FinalLogger.log_max_byte,backupCount=FinalLogger.log_backup_count) 
        log_fmt=logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] %(message)s") 
        log_handler.setFormatter(log_fmt) 
        FinalLogger.logger.addHandler(log_handler) 
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.log_level)) 
        return FinalLogger.logger 

#log函数，输入格式
# ============================================================================= 
# log("thisisadebugmsg!",'debug') 
# log("thisisainfomsg!",'info') 
# log("thisisawarnmsg!",'warn') 
# log("thisisaerrormsg!",'error') 
# log("thisisacriticalmsg!",'critical') 
# ============================================================================= 
#log函数，输出格式
# ============================================================================= 
# console：msg
# logFile: [datetime] [fileName:lineNum] [level] msg
# logFile: [2017-11-20 14:51:24,470] [tools.py:93] [INFO] this is the msg
# ============================================================================= 
#输出文件在config中定义
def log(msg,typeName): 
    print (msg); 
    logger=FinalLogger.getLogger() 
    if typeName == 'debug': 
        logger.debug(msg) 
    elif typeName == 'info': 
        logger.info(msg) 
    elif typeName == 'warn': 
        logger.warn(msg) 
    elif typeName == 'error': 
        logger.error(msg) 
    elif typeName == 'critical': 
        logger.critical(msg) 
    return msg



def querylog(msg,typeName): 
    print (msg); 
    logger=QueryFinalLogger.getLogger() 
    if typeName == 'debug': 
        logger.debug(msg) 
    elif typeName == 'info': 
        logger.info(msg) 
    elif typeName == 'warn': 
        logger.warn(msg) 
    elif typeName == 'error': 
        logger.error(msg) 
    elif typeName == 'critical': 
        logger.critical(msg) 
    return msg


#任务开始处理，更新task表状态为 TaskState = 1,TaskStartTime = TaskStartTime
def taskStartInsert(TaskStartTime,InterfaceType,direction, conn, TaskTableName):
    #sql = "insert into " + TaskTableName + " (TaskState, TaskStartTime, InterfaceType, Direction) values (1," + TaskStartTime + ",\'" + InterfaceType + "\'," + str(direction) + ")"
    #print (sql)
    #databasesql(conn,sql)
    sql = "select TaskId from " + TaskTableName + " where  Direction = 1 and ( TaskState = 0 or TaskState = 3 or TaskState = 1) and TaskChannel = 'OPEN_API'"
    print ("insert:",sql)
    if len(database(conn, sql)[0])  == 0:
        TaskId = [0]
    else:
        TaskId = database(conn, sql)[0][0]
    return TaskId


#任务处理成功，更新task表状态为 TaskState = 2,TaskStartTime = TaskStartTime,TaskEndTime = TaskEndTime
def successUpdate(TaskStartTime,TaskEndTime,TaskId,conn, TaskTableName):
    sql = 'update ' + TaskTableName + ' set TaskState = 2,TaskStartTime = ' + TaskStartTime+ ',TaskEndTime = '+ TaskEndTime + ' where TaskId = ' + str(TaskId)
    databasesql(conn,sql)
    return 


#任务处理失败，更新task表状态为 TaskState = 3,TaskStartTime = TaskStartTime,TaskEndTime = TaskEndTime
def failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId,conn, TaskTableName):
    errorInfo = str(time.strftime("%Y-%m-%d %X", time.localtime())) + ':' +errorInfo
    sql = 'update ' + TaskTableName + ' set TaskState = 3,TaskStartTime = ' + TaskStartTime + ',TaskEndTime = '+ TaskEndTime + ",ErrorInfo = N'" + errorInfo + "' where TaskId = " + str(TaskId)
    sql= sql.encode('utf-8') 
    databasesql(conn,sql)
    return 



#任务对应的表没有数据，更新task表状态为 TaskState = 5,TaskStartTime = TaskStartTime,TaskEndTime = TaskEndTime，errorInfo = there is no data!
def noDataUpdate(TaskStartTime,errorInfo,TaskId,conn, TaskTableName):
    TaskEndTime = TaskStartTime
    errorInfo = str(time.strftime("%Y-%m-%d %X", time.localtime())) + ':' + errorInfo
    sql = 'update ' + TaskTableName + ' set TaskState = 5,TaskStartTime = ' + TaskStartTime + ',TaskEndTime = '+ TaskEndTime + ",ErrorInfo = N'" + errorInfo + "' where TaskId = " + str(TaskId)
    print(u'执行sql' + sql)
    sql= sql.encode('utf-8')
    databasesql(conn,sql)
    return

def strtojson(r):
    dataStart = r.find("{",1)
    dataEnd = r.find("}",-1)
    if dataStart == -1:
        re = json.loads(r)
        data = {u'status':u'',u'message':u''}
        return re,data
    else:
        data = r[dataStart:dataEnd-1]
        rightdata = data.replace("\"","'")
        rightjson = r.replace(data,rightdata)
        re = json.loads(rightjson)
        #data = str(re['data'])
        data =data.replace("'","\"")
        data = json.loads(data)
        return re,data



        
    