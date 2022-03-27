import json
import requests
import psycopg2
import re
import time


def connector():
    
    conn=psycopg2.connect("dbname='charging-bull-344.defaultdb' user='hackabull2022' password='geturown' host='free-tier11.gcp-us-east1.cockroachlabs.cloud' port='26257'")
    return conn

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


def addSweat(conn, reading):
    with conn.cursor() as cur:
        tst = int(time.time())
      
        for hr in reading:
            tst +=5
            ts = str(tst)
            cur.execute("UPSERT INTO sweat (timestamp, gsr, deltahumid) VALUES ('" + ts + "','" + str(hr[0]) + "', '" + str(hr[1]) + "')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()  
    


def lambda_handler(event, context):
    # TODO implement
    # key1 = event['key1']
    # estr = json.loads(str(event['body']))
    
    # estr = json.loads(event['body'])
    
    estr = event['body']
    es = json.dumps(estr)
    
    es = es.replace('\n', '')
    es = es.replace('\r', '')
    es = es.replace('\\n', '')
    es = es.replace('\\r', '')
    es = es.replace('\\', '')
    
    # estr = json.loads(es)
    
    # action = estr['action']
    conn = connector()
    results = []
    if 'action' in es and 'getheartrate' in es:
        results = gethrates(conn)

    if 'action' in es and 'getrespiration' in es:
        results = getresp(conn)

    if 'action' in es and 'getstress' in es:
        results = getstress(conn)  
    
    if 'action' in es and 'getsweat' in es:
        results = getsweat(conn) 

    if 'action' in es and 'uploadsweat' in es:
        

        # text = 'gfgfdAAA1234ZZZuijjk'
        
        m = re.search('#(.+?)$', es)
        if m:
            results = m.group(1)
            results.replace('$', '')
            sep = '$\"  }\"'
            results = results.split(sep, 1)[0]
            
            jsr = json.loads(results)
            addSweat(conn, jsr)
            
        # results = 
        # results = getsweat(conn)

    
    return {
        'statusCode': 200,
        "Content-Type":"application/json",
        # 'body': json.dumps('Hello from Lambda! output is ' + es)
        # 'body': json.dumps(estr)
        'body': json.dumps(results)
        
    }
