#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 00:02:21 2018

@author: eoin
"""

import pandas as pd
import time
import datetime

db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"

df = pd.read_sql_table(table_name="dynamicData", con=db_connection_string)
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y_%H%M%S')
df.to_csv('dynamicData_' + st + '.csv', index=False)
