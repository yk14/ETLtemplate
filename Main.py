#!/usr/bin/python
# -*- coding: UTF-8 -*-

import DataSend
import DataETLClass
import DataETL
import tools

if __name__ == '__main__':
    tools.log('-------start---------','info')
    DataETLList = DataETL.XmlParse('PH_api.xml')
    for DataETLClass in DataETLList:
        DataSend.DoSend(DataETLClass)
    tools.log('-------end---------','info')