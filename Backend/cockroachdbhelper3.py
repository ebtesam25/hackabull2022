from dataclasses import field
import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
import csv
# import pymongo
import psycopg2
from psycopg2.errors import SerializationFailure
import json
from secrets import secrets
import datetime

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

today = datetime.date.today()
lastweek = today - datetime.timedelta(days=7)

def create_users(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, email VARCHAR(200), userpassword VARCHAR(30), phone VARCHAR(20), name VARCHAR(30))"
        )
        cur.execute("UPSERT INTO users (id, email, userpassword, phone, name) VALUES (1, 'jon@fisherman.com', 'password1', '12524568877', 'jon stewart'), (2, 'joe@gmail.com', 'password1', '15685558989', 'joe someone')")
        logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    print ("users table created")


def add_users(conn, uname, pw, uphone, uemail):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)
        
        cur.execute("UPSERT INTO users (id, email, userpassword, phone, name) VALUES (" + i +", '" + uemail + "', '" + pw + "', '" + uphone +"', '" + uname +"')")
        logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    print ("user added")


def login(conn, uemail, pw):
    with conn.cursor() as cur:
        cur.execute("SELECT id, email, userpassword, phone, name FROM users")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        for row in rows:
            print(row)
            print (type(row))
            if row[1] == uemail and row[2] == pw:
                print ("found")
                return True, row[3], row[4]
        return False, 'none', 'none'

def delete_users(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM defaultdb.users")
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    with conn.cursor() as cur:
        cur.execute("DROP TABLE users")
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()

    print ("users table deleted")


def connector():
    # conn=psycopg2.connect("dbname='nifty-puma-91.defaultdb' user='muntaser' password='rootpassword' host='free-tier.gcp-us-central1.cockroachlabs.cloud' port='26257'")
    conn=psycopg2.connect(secrets['dbconn'])
    return conn
   

def initmongo(): 
    db = ""
    
    return db


def initHr(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS hrate (hid INT GENERATED ALWAYS AS IDENTITY, value VARCHAR(5), timestamp VARCHAR(18), PRIMARY KEY (hid))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    print ("heartrate table created")
    
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS hrmeta (mid INT GENERATED ALWAYS AS IDENTITY, upk VARCHAR(10), cdate VARCHAR(10), maxhr VARCHAR(5), minhr VARCHAR(5), resthr VARCHAR(5), avresthr VARCHAR(5), endts VARCHAR(30))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()  



def addHr(conn, reading):
    with conn.cursor() as cur:
        # print ("UPSERT INTO hrmeta (upk, cdate, maxhr, minhr, resthr, avresthr, endts) VALUES ('" + str(reading['userProfilePK']) +"', '" + reading["calendarDate"] + "', '" + str(reading["maxHeartRate"]) + "', '" + str(reading["minHeartRate"]) + "',  '" + str(reading["restingHeartRate"]) + "',  '" + str(reading["lastSevenDaysAvgRestingHeartRate"]) + "', '" + reading["endTimestampLocal"] + "')")
        cur.execute("UPSERT INTO hrmeta (upk, cdate, maxhr, minhr, resthr, avresthr, endts) VALUES ('" + str(reading['userProfilePK']) +"', '" + reading["calendarDate"] + "', '" + str(reading["maxHeartRate"]) + "', '" + str(reading["minHeartRate"]) + "',  '" + str(reading["restingHeartRate"]) + "',  '" + str(reading["lastSevenDaysAvgRestingHeartRate"]) + "', '" + reading["endTimestampLocal"] + "')")
        
        for hr in reading['heartRateValues']:
            cur.execute("UPSERT INTO hrate (value, timestamp) VALUES ('" + str(hr[1]) + "', '" + str(hr[0]) + "')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
 

def gethrates(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT timestamp, value FROM hrate")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        results = []
        for row in rows:
            # q = {}
            print(row)
            # print (type(row))
            # q['timestamp'] = str(row[0])
            # q['value'] = str(row[1])
            q = []
            q.append(str(row[0]))
            q.append(str(row[1]))

            results.append(q)

        return results    
 
 
def initResp(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS resp (rid INT GENERATED ALWAYS AS IDENTITY, value VARCHAR(5), timestamp VARCHAR(18), PRIMARY KEY (rid))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    print ("respiration table created")
    
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS respmeta (mid INT GENERATED ALWAYS AS IDENTITY, upk VARCHAR(10), cdate VARCHAR(10), maxresp VARCHAR(5), minresp VARCHAR(5), avresp VARCHAR(5), endts VARCHAR(30))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()  



def addResp(conn, reading):
    with conn.cursor() as cur:
        # print ("UPSERT INTO hrmeta (upk, cdate, maxhr, minhr, resthr, avresthr, endts) VALUES ('" + str(reading['userProfilePK']) +"', '" + reading["calendarDate"] + "', '" + str(reading["maxHeartRate"]) + "', '" + str(reading["minHeartRate"]) + "',  '" + str(reading["restingHeartRate"]) + "',  '" + str(reading["lastSevenDaysAvgRestingHeartRate"]) + "', '" + reading["endTimestampLocal"] + "')")
        cur.execute("UPSERT INTO respmeta (upk, cdate, maxresp, minresp, avresp, endts) VALUES ('" + str(reading['userProfilePK']) +"', '" + reading["calendarDate"] + "', '" + str(reading["highestRespirationValue"]) + "', '" + str(reading["lowestRespirationValue"]) + "',  '" + str(reading["avgWakingRespirationValue"]) + "',  '"  + reading["endTimestampLocal"] + "')")
        
        for hr in reading['respirationValuesArray']:
            cur.execute("UPSERT INTO resp (value, timestamp) VALUES ('" + str(hr[1]) + "', '" + str(hr[0]) + "')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()


def getresp(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT timestamp, value FROM resp")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        results = []
        for row in rows:
            # q = {}
            print(row)
            # print (type(row))
            # q['timestamp'] = str(row[0])
            # q['value'] = str(row[1])
            q = []
            q.append(str(row[0]))
            q.append(str(row[1]))

            results.append(q)

        return results 
    

def initSweat(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS sweat (stid INT GENERATED ALWAYS AS IDENTITY, gsr VARCHAR(10), deltahumid VARCHAR(10), timestamp VARCHAR(18), PRIMARY KEY (stid))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    print ("sweat table created")


    
    
def addSweat(conn, reading):
    with conn.cursor() as cur:
        tst = int(time.time())
      
        for hr in reading:
            tst +=5
            ts = str(tst)
            cur.execute("UPSERT INTO sweat (timestamp, gsr, deltahumid) VALUES ('" + ts + "','" + str(hr[0]) + "', '" + str(hr[1]) + "')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()    
    


def getsweat(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT timestamp, gsr, deltahumid FROM sweat")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        results = []
        for row in rows:
            # q = {}
            print(row)
            # print (type(row))
            # q['timestamp'] = str(row[0])
            # q['value'] = str(row[1])
            q = []
            q.append(str(row[0]))
            q.append(str(row[1]))
            q.append(str(row[2]))

            results.append(q)

        return results 




def initStress(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS stress (stid INT GENERATED ALWAYS AS IDENTITY, value VARCHAR(5), timestamp VARCHAR(18), PRIMARY KEY (stid))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    print ("heartrate table created")
    
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS stressmeta (mid INT GENERATED ALWAYS AS IDENTITY, upk VARCHAR(10), cdate VARCHAR(10), maxst VARCHAR(5), avst VARCHAR(5),  endts VARCHAR(30))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()  


def getstress(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT timestamp, value FROM stress")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        results = []
        for row in rows:
            # q = {}
            print(row)
            # print (type(row))
            # q['timestamp'] = str(row[0])
            # q['value'] = str(row[1])
            q = []
            q.append(str(row[0]))
            q.append(str(row[1]))

            results.append(q)

        return results 


def addStress(conn, reading):
    with conn.cursor() as cur:
        # print ("UPSERT INTO hrmeta (upk, cdate, maxhr, minhr, resthr, avresthr, endts) VALUES ('" + str(reading['userProfilePK']) +"', '" + reading["calendarDate"] + "', '" + str(reading["maxHeartRate"]) + "', '" + str(reading["minHeartRate"]) + "',  '" + str(reading["restingHeartRate"]) + "',  '" + str(reading["lastSevenDaysAvgRestingHeartRate"]) + "', '" + reading["endTimestampLocal"] + "')")
        cur.execute("UPSERT INTO stressmeta (upk, cdate, maxst, avst, endts) VALUES ('" + str(reading['userProfilePK']) +"', '" + reading["calendarDate"] + "', '" + str(reading["maxStressLevel"]) + "', '" + str(reading["avgStressLevel"]) + "',  '"  + reading["endTimestampLocal"] + "')")
        
        for hr in reading['stressValuesArray']:
            cur.execute("UPSERT INTO stress (value, timestamp) VALUES ('" + str(hr[1]) + "', '" + str(hr[0]) + "')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()







def initSteps(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS steps (sid INT GENERATED ALWAYS AS IDENTITY, starting VARCHAR(100), ending VARCHAR(100), steps VARCHAR(5), level VARCHAR(20), PRIMARY KEY (sid))"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    print ("steps table created")
    

def addSteps(conn, reading):
    with conn.cursor() as cur:
    
        for hr in reading:
            cur.execute("UPSERT INTO steps (starting, ending, steps, level) VALUES ('" + str(hr['startGMT']) + "', '" + str(hr['endGMT']) + "', '" + str(hr['steps']) + "', '" + str(hr['primaryActivityLevel']) + "')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    

def purgedb(conn):


    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM defaultdb.resp")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE resp")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()

    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM defaultdb.respmeta")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE respmeta")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()


    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM defaultdb.stress")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE stress")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()

    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM defaultdb.stressmeta")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE stressmeta")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    
    
    with conn.cursor() as cur:
        cur.execute("DELETE FROM defaultdb.sweat")
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    
    with conn.cursor() as cur:
        cur.execute("DROP TABLE sweat")
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()


    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM defaultdb.hrate")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE hrate")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()

    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM defaultdb.hrmeta")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE hrmeta")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()

    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM defaultdb.steps")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE steps")
    #     logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    # conn.commit()

    print ("tables deleted")


##testing
conn = connector() #connec to db 
try: 
    api = Garmin(secrets['email'], secrets['password'])
    api.login()
except:
    print("Could not log in")
initHr(conn) #generate table
initSteps(conn) #generate table
initStress(conn) #generate table
initResp(conn) #generate table

# f = open('hrate.json') 
# testdata = json.load(f)


##testing
conn = connector()
# purgedb(conn)
# initResp(conn)
# initHr(conn)
# initSteps(conn)
# initStress(conn)
# initSweat(conn)



# f = open('sweat.json')
# testdata = json.load(f)

# print(testdata)

# addSweat(conn, testdata)


r = getsweat(conn)

print(r)



# f = open('respiration.json')
# testdata = json.load(f)

# print(testdata)

# addResp(conn, testdata)

# r = getresp(conn)

# print(r)

# f = open('stress.json')
# testdata = json.load(f)

# print(testdata)

# addStress(conn, testdata)


# r = getstress(conn)

# print(r)


# f = open('hrate.json')
# testdata = json.load(f)

# print(testdata)

# addHr(conn, testdata)

# r = gethrates(conn)

# print(r)


# f = open('steps.json')
# testdata = json.load(f)

# print(testdata)

# addSteps(conn, testdata)


# purgedb(conn)


# print(testdata)
hrdata = api.get_heart_rates(today.isoformat())
addHr(conn, hrdata) #add data to table change testdata 

stepsdata = api.get_steps_data(today.isoformat())
addSteps(conn, stepsdata)

stressdata = api.get_stress_data(today.isoformat())
addStress(conn, stressdata)

respsdata = api.get_respiration_data(today.isoformat())
addResp(conn, respsdata)

#purgedb(conn) #

print("SUCCESS!")