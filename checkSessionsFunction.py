
from formConnectionModule import formConnection

def checkSession(userID,sessionID): #Check Session Valid
    parser = reqparse.RequestParser();
    args = parser.parse_args();
    connection = formConnection();
    query = """
    SELECT * FROM sessions RIGHT JOIN
    (select userID,max(sessionDate) as high from sessions group by userID) highDates
    ON highDates.userID = sessions.userID
    WHERE userID = %s AND sessionID = %s
    AND ((timeDuration = 'forever')
    OR (timeduration = "HOUR" AND NOW() < date_add(sessionDate,Interval 1 Hour)))
    """;
    cursor = connection.cursor(prepared=True);
    cursor.execute(query,(userID,sessionID));
    connection.commit();
    results = cursor.fetchall();
    connection.close();
    return len(results) == 1;

if __name__ == '__main__':
    print('Checking Session Module...')
