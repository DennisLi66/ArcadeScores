
from formConnectionModule import formConnection

def checkSession(userID,sessionID): #Check Session Valid
    connection = formConnection();
    query = """
    SELECT * FROM sessions RIGHT JOIN
    (select userID,max(sessionDate) as high from sessions group by userID) highDates
    ON highDates.userID = sessions.userID
    WHERE sessions.userID = %s AND sessions.sessionID = %s
    AND ((timeDuration = 'forever')
    OR (timeduration = "HOUR" AND NOW() < date_add(sessionDate,Interval 1 Hour)))
    """;
    cursor = connection.cursor(prepared=True);
    cursor.execute(query,(userID,sessionID));
    results = cursor.fetchall();
    connection.close();
    return len(results) == 1;

if __name__ == '__main__':
    print('Checking Session Module...')
