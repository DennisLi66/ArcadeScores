from formConnectionModule import formConnection

import string
import random

def makeSession(userID,timeDuration):
    connection = formConnection();
    sessionSequence = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    insertSessionQuery = """
    INSERT INTO sessions (sessionID,userID,sessionDate,timeDuration) VALUES (%s,%s,NOW(),%s)
    """
    cursor = connection.cursor(prepared = True);
    cursor.execute(insertSessionQuery,[sessionSequence,userID,timeDuration]);
    connection.commit();
    connection.close();
    return sessionSequence;





if __name__ == '__main__':
    print('Making Session Module...')
