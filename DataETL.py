# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import DataETLClass

def XmlParse(XmlPath):
    DataETLList = []
    DOMTree = xml.dom.minidom.parse(XmlPath)
    actions = DOMTree.documentElement
    # 获取顶级标签actions下面的所有标签action
    actionlist = actions.getElementsByTagName("Action")
    for action in actionlist:
        DataSQLDict = {}
        ActionName = action.getAttribute('ActionName')
        ActionNo = action.getAttribute('ActionNo')
        DataSource = action.getElementsByTagName('DataSource')[0]
        Destination = action.getElementsByTagName('Destination')[0]
        Callback = action.getElementsByTagName('Callback')[0]
    
        # 数据库连接相关
        DataSourceUrl = DataSource.getElementsByTagName('DataSourceUrl')[0].childNodes[0].data
        UserName = DataSource.getElementsByTagName('UserName')[0].childNodes[0].data
        UserPassword = DataSource.getElementsByTagName('UserPassword')[0].childNodes[0].data
        Charset = DataSource.getElementsByTagName('Charset')[0].childNodes[0].data
        DataSourceType = DataSource.getElementsByTagName('DataSourceType')[0].childNodes[0].data
        DataSourceName = DataSource.getElementsByTagName('DataSourceName')[0].childNodes[0].data
        DataSourceTableName = DataSource.getElementsByTagName('TableName')[0].childNodes[0].data
        DataSourceDescription = DataSource.getElementsByTagName('DataSourceDescription')[0].childNodes[0].data
        DataGetSQL = DataSource.getElementsByTagName('DataGetSQL')[0].childNodes[0].data
        TaskTableName = DataSource.getElementsByTagName('TaskTableName')[0].childNodes[0].data
        SendToken = DataSource.getElementsByTagName('SendToken')[0].childNodes[0].data
        GetTokenUrl = DataSource.getElementsByTagName('GetTokenUrl')[0].childNodes[0].data
        TaskSql = DataSource.getElementsByTagName('TaskSql')[0].childNodes[0].data
        keyColumn = DataSource.getElementsByTagName('keyColumn')[0].childNodes[0].data
    
        # 数据目标地点
        DestinationType = Destination.getAttribute('type')
     
        # 目前只有SendToInterface
        if DestinationType == 'SendToInterface':
            DestinationHttpType = Destination.getElementsByTagName('Type')[0].childNodes[0].data
            DestinationUrl = Destination.getElementsByTagName('Url')[0].childNodes[0].data
            # Extra_params先不写
    
        # Auto:使用表名自动更新status Customize:使用标签配置更新数据库状态
        CallbackLocation = Callback.getAttribute('location')
        if CallbackLocation == 'Auto':
            DataSQLDict[1] = {'SQL': 'update ' + DataSourceTableName + ' set api_status = ' + '1', 'Params': []}
        elif CallbackLocation == 'Customize':
            DataSQLList = Callback.getElementsByTagName('DataSQL')
            for DataSQL in DataSQLList:
                thisid = DataSQL.getAttribute('id')
                thisSQL = DataSQL.getElementsByTagName('SQL')[0].childNodes[0].data
                thisParams = DataSQL.getElementsByTagName('Params')[0]
                thisParamDict = {}
                for index, param in enumerate(thisParams.getElementsByTagName('Param')):
                    thisParamDict[param.getAttribute('rsname')] = param.getAttribute('dbname')
                DataSQLDict[thisid] = {'SQL': thisSQL, 'Params': thisParamDict}
        XmlDate = DataETLClass.DataETLEntity(DataSourceUrl, UserName, UserPassword, Charset, DataSourceType, DataSourceName, DataSourceTableName,
                 DataSourceDescription, DataGetSQL, DestinationHttpType, DestinationUrl, TaskTableName, DataSQLDict, SendToken,GetTokenUrl,
                 keyColumn,TaskSql)
        DataETLList.append(XmlDate)
    return DataETLList
        