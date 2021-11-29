
from formConnectionModule import formConnection

def checkSession(): #Check Session Valid
    parser = reqparse.RequestParser();
    parser.add_argument('userID',required=True);
    parser.add_argument('sessionID',required=True);
    args = parser.parse_args();
    try:
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
        cursor.execute(query,(args['userID'],args['sessionID']));
        connection.commit();
        results = cursor.fetchall();
        connection.close();
        print(results);
        return results;
    except:
        raise ValueError('Querying Failed');


if __name__ == '__main__':
    print('Checking Session Module...')
