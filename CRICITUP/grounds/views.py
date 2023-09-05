from django.shortcuts import render
from django.db import connection
import cx_Oracle

def home(request):
    return render(request, 'cricitup/index.html')


def teams(request):
    return render(request, 'cricitup/team.html')

def players(request):
    return render(request, 'players/players.html')
def grounds(request):
    with connection.cursor() as cursor:
        query = """
        SELECT
            V.VENUE_ID,
            V.ADDRESS,
            V.CITY,
            V.STREET_NO,
			V.IMAGEURL
        FROM VENUE V
        """
        cursor.execute(query)
        venues_data = cursor.fetchall()

    context = {
        'venues': venues_data
    }

    return render(request, 'grounds/grounds.html', context)



def ground_details(request, venue_id):
    with connection.cursor() as cursor:

        # Call the STAT_OF_VENUE procedure
            # Call the PL/SQL function and capture the result as a string
        result = cursor.callfunc('GET_STATS_OF_VENUE', str, [venue_id])

            # Split the result string into a list of values
        values = result.split(',')
        values = [int(val) for val in values]

            # Convert the values to integers if needed
        highestrun, highestwicket, highestsix, highestfour, highestcatch = values

        # Retrieve names based on IDs
        cursor.execute("SELECT (FIRST_NAME||' '||LAST_NAME) FROM PERSON WHERE PERSONID = %s", [highestrun])
        highestrunner = cursor.fetchone()[0]

        cursor.execute("SELECT (FIRST_NAME||' '||LAST_NAME) FROM PERSON WHERE PERSONID = %s", [highestwicket])
        wicketer = cursor.fetchone()[0] 

        cursor.execute("SELECT (FIRST_NAME||' '||LAST_NAME) FROM PERSON WHERE PERSONID = %s", [highestsix])
        sixer = cursor.fetchone()[0] 

        cursor.execute("SELECT (FIRST_NAME||' '||LAST_NAME) FROM PERSON WHERE PERSONID = %s", [highestfour])
        fourer = cursor.fetchone()[0] 

        cursor.execute("SELECT (FIRST_NAME||' '||LAST_NAME) FROM PERSON WHERE PERSONID = %s", [highestcatch])
        catcher = cursor.fetchone()[0] 

        # Retrieve additional venue information
        cursor.execute("SELECT venue_id, address, city, street_no, capacity, imageurl FROM VENUE WHERE venue_id = %s", [venue_id])
        venue_info = cursor.fetchone()

    context = {
        'venue_id': venue_id,
        'highestrun': highestrun,
        'highestwicket': highestwicket,
        'highestsix': highestsix,
        'highestfour': highestfour,
        'highestcatch': highestcatch,
        'highestrunner': highestrunner,
        'wicketer': wicketer,
        'sixer': sixer,
        'fourer': fourer,
        'catcher': catcher,
        'venue_info': venue_info,
    }

    return render(request, 'grounds/ground_details.html', context)
