#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import json
import pymssql
import time
import tools
import requests
import config
import base64
from  DataETLClass import DataETLEntity

def DoSend(DataETLEntity):
    DataSourceUrl = DataETLEntity.DataSourceUrl
    UserName = DataETLEntity.UserName
    UserPassword = DataETLEntity.UserPassword
    Charset = DataETLEntity.Charset
    DataSourceType = DataETLEntity.DataSourceType
    DataSourceName = DataETLEntity.DataSourceName
    DataSourceTableName = DataETLEntity.DataSourceTableName
    DataSourceDescription = DataETLEntity.DataSourceDescription
    DataGetSQL = DataETLEntity.DataGetSQL
    DestinationHttpType = DataETLEntity.DestinationHttpType
    DestinationUrl = DataETLEntity.DestinationUrl  
    TaskTableName = DataETLEntity.TaskTableName
    DataSQLDict = DataETLEntity.DataSQLDict
    SendToken = DataETLEntity.SendToken
    GetTokenUrl = DataETLEntity.GetTokenUrl   
    keyColumn = DataETLEntity.keyColumn
    TaskSql = DataETLEntity.TaskSql
    
    conn = pymssql.connect(DataSourceUrl, UserName, base64.b64decode(UserPassword).decode("UTF-8"), DataSourceName, Charset)
    requestId = str(int(time.time()))
    try:
        TaskStartTime = "\'" + time.strftime("%Y-%m-%d %X", time.localtime()) + "\'"
        if TaskSql == 'Null':
            print ("this no taskID")
        else:
            #获取xml中TaskSql标签的数据，用于查找待处理的task
            TaskIds = tools.database(conn, TaskSql)[0]
            for i in range(len(TaskIds)):
                TaskId = TaskIds[i][0]
        
                #查询数据
                DataGetSQLByTaskId = DataGetSQL +" and TaskId = "+ str(TaskId)
                tools.log(DataGetSQLByTaskId, 'info')
                datas,cols = tools.database(conn, DataGetSQLByTaskId);
                #字段名称遍历
                colslist = []
                for i in range(len(cols)):
                    colslist.append(cols[i][0])
            
                tools.log(datas, 'info')
                 # 此处循环是当一个TaskId查出多条数据时，对每条数据调用该api
                fail_list = []
                errortimes = 0
                successtimes = 0
                if len(datas) == 0:
                    errortimes = errortimes + 1
                    tools.log('there is no data in ' + DataSourceTableName + ' where TaskId = ' + str(TaskId), 'error')
                    errorInfo = 'there is no data in ' + DataSourceTableName + ' where TaskId = ' + str(TaskId)
                    tools.noDataUpdate(TaskStartTime, errorInfo, TaskId, conn, TaskTableName)
                    tools.log(str(successtimes) + "success(es), + str(errortimes) + fail(s)", 'info')
                else:
                    for index,data in enumerate(datas):
                        params = {}
                        for index1,attr in enumerate(data):
                            params[colslist[index1]] = attr
            
                        if SendToken == "True":
                            access_token = tools.getToken(GetTokenUrl)
                            params['access_token'] = access_token
                        dataId = params[keyColumn]
                        tools.log(DestinationUrl, 'info')
                        headers = {'content-type': 'application/json', 'charset': 'UTF-8'}
                        r = None
                        if DestinationHttpType == 'GET':
                            r = requests.get(DestinationUrl, headers=headers, params=params)
                        elif DestinationHttpType == 'POST':
                            print('TODO')
                        re, data = tools.strtojson(r.text)
                        tools.log(re, 'info')
                        TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X", time.localtime()) + "\'"
                        StatusStr = 'status' #考虑放入xml
                        xmlSql = ''
                        if (re['msg'] == ""):
                            if (len(data) == 0):
                                errortimes = errortimes + 1
                                errorInfo = "错误返回示例"
                                tools.log(errorInfo, 'error')
                            elif (data[StatusStr] == '0'):
                                successtimes = successtimes + 1
                                # 任务成功，维护task表
                                # tools.successUpdate(TaskStartTime,TaskEndTime,TaskId,conn)
                                #任务成功，维护order表
                                for key in DataSQLDict:
                                    if key == '0':
                                        xmlSql = DataSQLDict[key]["SQL"]                                 
                                UpdateSql = xmlSql+ " and "+ keyColumn + " = " + str(dataId)

                                tools.databasesql(conn,UpdateSql)
                                tools.log(data['message'], 'info')
                            elif (data[StatusStr] == '1'):
                                errortimes = errortimes + 1
                                errorInfo = data['message']
                                # 任务失败，维护task表
                                # tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId,conn)
                                # 任务失败
                                for key in DataSQLDict:
                                    if key == '1':
                                        xmlSql = DataSQLDict[key]["SQL"]                                 
                                UpdateSql = xmlSql+ " and " + keyColumn + " = " +str(dataId)
                                tools.databasesql(conn,UpdateSql)                        
                                tools.log(errorInfo, 'error')
                        else:
                            errortimes = errortimes + 1
                            errorInfo = re['msg']
                            # 任务失败，维护task表
                            # tools.failUpdate(TaskStartTime,TaskEndTime,errorInfo,TaskId,conn)
                            tools.log(errorInfo, 'error')
            
                        #for key in DataSQLDict:
                            #thisSQL = DataSQLDict[key]["SQL"]
                            #thisParamsMap = DataSQLDict[key]["Params"]
                            ##如果没有属性直接执行sql
                            #if len(thisParamsMap) == 0:
                                #tools.databasesql(conn, thisSQL)
                            #else:
                                #tools.databasesql(conn, thisSQL, thisParamsMap)
            
                    TaskEndTime = "\'" + time.strftime("%Y-%m-%d %X", time.localtime()) + "\'"
                    if (successtimes == len(datas)):
                        tools.successUpdate(TaskStartTime, TaskEndTime, TaskId, conn,  TaskTableName)
                    else:        
                        errorInfo = "N"
                        tools.failUpdate(TaskStartTime, TaskEndTime, errorInfo, TaskId, conn, TaskTableName)
                    tools.log(str(successtimes) + "success(es), " + str(errortimes) + "fail(s)", 'info')
    except Exception as e:
        tools.log('Exception error','error')
        tools.log(e,'error')
        return
    finally:
        conn.close()