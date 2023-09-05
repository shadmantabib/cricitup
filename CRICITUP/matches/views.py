from django.shortcuts import render
from django.db import connection

def matches_view(request):
    with connection.cursor() as cursor:
        query = """
        SELECT MATCH_ID,
               (SELECT TEAM_NAME FROM TEAM T WHERE T.TEAM_ID=M.TEAM1_ID) || ' vs ' ||
               (SELECT TEAM_NAME FROM TEAM T WHERE T.TEAM_ID=M.TEAM2_ID) || ' -' || MATCH_ID AS NAME
        FROM MATCH M
        """
        cursor.execute(query)
        results = cursor.fetchall()

    context = {'matches': results}
    return render(request, 'matches/matches.html', context)
def match_details(request, match_id):
    first_team_batting=[]
    # Define the SQL query using placeholders for parameters
    query = """
    SELECT MATCH_ID,
           (SELECT TEAM_NAME FROM TEAM T WHERE T.TEAM_ID=M.TEAM1_ID) || ' vs ' || (SELECT TEAM_NAME FROM TEAM T WHERE T.TEAM_ID=M.TEAM2_ID) || ' -' || MATCH_ID AS NAME,
           MAN_OF_THE_MATCH,WEATHER,WINNER,(SELECT ADDRESS FROM VENUE V WHERE V.VENUE_ID=M.VENUE_ID) GROUND
    FROM MATCH M
		
    WHERE MATCH_ID = %s
    """
    query2="""SELECT PLAYER_ID,(SELECT (FIRST_NAME||' '||LAST_NAME) FROM PERSON PR WHERE PR.PERSONID=S.PLAYER_ID) NAME , TOTAL_RUNS AS RUN ,TOTAL_BALLS_FACED AS BALL,TOTAL_SIXES_HIT AS SIX,TOTAL_FOURS_HIT AS FOUR  FROM SCORECARD S
	WHERE match_id=%s
	AND player_id IN (	SELECT PLAYERID player_id from player where team_id =(	SELECT team1_id from match
	where match_id=%s))
	ORDER by player_id
"""
    query3="""
 SELECT (SELECT team_name from team t where t.team_id=m.team1_id) name   from match m
	where match_id=%s
"""


    # Execute the PL/SQL query to fetch team details
    with connection.cursor() as cursor:
        cursor.execute(query, [match_id])
        match = cursor.fetchone()  # Fetch the result
        match_winner=cursor.callfunc('Find_Match_Winner',str,[match_id])
        highest_scorer=cursor.callfunc('Find_Highest_Scorer',str,[match_id])
        cursor.execute(query2,[match_id,match_id])
        first_team_batting=cursor.fetchall()
        cursor.execute(query3, [match_id])
        first_team_name=cursor.fetchone()[0]



    context = {
        'match': match,
        'match_winner':match_winner,
        'highest_scorer':highest_scorer,
        'first_team_batting':first_team_batting,
        'first_team_name':first_team_name,
    }
    return render(request, 'matches/match_details.html', context)
