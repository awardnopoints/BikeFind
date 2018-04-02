#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 03:17:01 2018

@author: eoin
"""
import pandas as pd
from sqlalchemy import create_engine, exc
from sqlalchemy.orm.session import sessionmaker
from bikefind.dbClasses import dynamicData
import sys

def main():
    if len(sys.argv) != 2:
        print(str(sys.argv))
        sys.exit("Requires csv file as argument.")
    else:
        my_csv = sys.argv[1]
    df = pd.read_csv(my_csv)
    db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
    
    engine = create_engine(db_connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    rows = len(df.index)
    
    for index, row in df.iterrows():
        print(index, '/', rows)
        address = row['address']
        last_update = row['time']
        totalBikeStands = row['totalBikeStands']
        availableBikeStands = row['availableBikeStands']
        availableBikes = row['availableBikes']
        status = row['status']
        
        dynamic_row = dynamicData(time = last_update, address = address, 
                                  totalBikeStands = totalBikeStands, 
                                  availableBikeStands = availableBikeStands, 
                                  availableBikes = availableBikes, status = status )
        session.add(dynamic_row)
        try:
            session.commit()
            print("success")
        except exc.IntegrityError:
            session.rollback()
            print("failure")
        
if __name__ == '__main__':
    main()


