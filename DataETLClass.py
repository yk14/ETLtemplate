# -*- coding: UTF-8 -*-

class DataETLEntity:
    DataSourceUrl = ''
    UserName = ''
    UserPassword = ''
    Charset = ''
    DataSourceType = ''
    DataSourceName = ''
    DataSourceTableName = ''
    DataSourceDescription = ''
    DataGetSQL = ''
    DestinationHttpType = ''
    DestinationUrl = ''
    TaskTableName = ''
    DataSQLDict = {}
    SendToken = True
    GetTokenUrl = ''
    keyColumn = ''
    TaskSql = ''
    
    def __init__(self, DataSourceUrl, UserName, UserPassword, Charset, DataSourceType, DataSourceName, DataSourceTableName,
                 DataSourceDescription, DataGetSQL, DestinationHttpType, DestinationUrl, TaskTableName, DataSQLDict, SendToken,GetTokenUrl,
                 keyColumn,TaskSql):
        self.DataSourceUrl = DataSourceUrl
        self.UserName = UserName
        self.UserPassword = UserPassword
        self.Charset = Charset
        self.DataSourceType = DataSourceType
        self.DataSourceName = DataSourceName
        self.DataSourceTableName = DataSourceTableName
        self.DataSourceDescription = DataSourceDescription
        self.DataGetSQL = DataGetSQL
        self.DestinationHttpType = DestinationHttpType
        self.DestinationUrl = DestinationUrl       
        self.TaskTableName = TaskTableName
        self.DataSQLDict = DataSQLDict
        self.SendToken = SendToken
        self.GetTokenUrl = GetTokenUrl        
        self.keyColumn = keyColumn
        self.TaskSql = TaskSql