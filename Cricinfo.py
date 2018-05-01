
# coding: utf-8

# In[1]:


import xlsxwriter
import urllib
from bs4 import BeautifulSoup
match_link="http://www.espncricinfo.com/series/8048/scorecard/1136591/royal-challengers-bangalore-vs-mumbai-indians-31st-match-ipl"
#Ensure you update this
match_no=31
innings=['RCB','MI']
man_of_the_match="%Watson%"
winning_team="MI"
#duck_out_in0ball_players_list=[""]
#not_out_in_0_players_list=[""]


# In[2]:


teams="31	RCB vs MI	Kiran	Rohit Sharma	AB de Villiers✈	Surya Kumar Yadav	Virat Kohli	Chris Woakes✈	Hardik Pandya	Quinton De Kock✈	Jasprit Bumrah	Yuzvendra Chahal	Mayank Markande	Krunal Pandya	Virat Kohli	Mayank Markande	RCB	31	RCB vs MI	Deepak	Virat Kohli	Evin Lewis✈	AB de Villiers✈	Ishan Kishan	Hardik Pandya	Rohit Sharma	Quinton De Kock✈	Murugan Ashwin	Mitchell McClenaghan✈	Jasprit Bumrah	Yuzvendra Chahal	Rohit Sharma	Rohit Sharma	MI	31	RCB vs MI	Kunal	Evin Lewis✈	Surya Kumar Yadav	Virat Kohli	AB de Villiers✈	Rohit Sharma	Hardik Pandya	Quinton De Kock✈	Krunal Pandya	Mitchell McClenaghan✈	Umesh Yadav	Yuzvendra Chahal	Virat Kohli	Rohit Sharma	RCB	31	RCB vs MI	Suresh	Surya Kumar Yadav	Rohit Sharma	Virat Kohli	AB de Villiers✈	Washington Sundar	Hardik Pandya	Brendon McCullum✈	Krunal Pandya	Jasprit Bumrah	Mustafizur Rahman✈	Yuzvendra Chahal	Brendon McCullum✈	Rohit Sharma	MI	31	RCB vs MI	Raj	Surya Kumar Yadav	Evin Lewis✈	Virat Kohli	AB de Villiers✈	Rohit Sharma	Mandeep Singh	Quinton De Kock✈	Yuzvendra Chahal	Mayank Markande	Krunal Pandya	Umesh Yadav	Virat Kohli	Evin Lewis✈	MI	31	RCB vs MI	Niranjan	Rohit Sharma	Virat Kohli	AB de Villiers✈	Mandeep Singh	Hardik Pandya	Pawan Negi	Quinton De Kock✈	Mayank Markande	Umesh Yadav	Mustafizur Rahman✈	Chris Woakes✈	Virat Kohli	AB de Villiers✈	RCB	31	RCB vs MI	Mitesh	Surya Kumar Yadav	Virat Kohli	Rohit Sharma	AB de Villiers✈	Kieron Pollard✈	Colin De Grandhomme✈	Ishan Kishan	Yuzvendra Chahal	Umesh Yadav	Tim Southee✈	Hardik Pandya	Virat Kohli	Rohit Sharma	RCB	"


# In[3]:


#Connect to cricinfo website and get the response into soup using beautiful soup library
sock = urllib.request.urlopen(match_link) 
htmlSource = sock.read()                  
soup = BeautifulSoup(htmlSource, 'html.parser')
batsmen_data=soup.find_all("div",{"class":"scorecard-section batsmen"})
bowlers_data=soup.find_all("div",{"class":"scorecard-section bowling"})
all_queries_list=[]


# In[4]:


#Function to get the batting scorecard
import pandas as pd

def extract_batting_scorecard(team_no,batsmen_data):
    batsmen_data_extract=batsmen_data[team_no-1]
    batsmen_data_header=batsmen_data_extract.find_all("div",{"class":"wrap header"})

    batsmen_header=[]
    for link in batsmen_data_header[0]:
        if(link.text!=''):
            batsmen_header.append(link.text.replace('BATSMEN','Player_Name'))

    team_bat=batsmen_data_extract.find_all("div",{"class":"cell batsmen"})

    team_batters=[]
    for a in team_bat:
        if(a.text!='' and a.text!='BATSMEN'):
            team_batters.append(a.text.replace(' †','').replace(' (c)',''))

    team_bat=batsmen_data_extract.find_all("div",{"class":"cell batsmen"})

    team_batters=[]
    for a in team_bat:
        if(a.text!='' and a.text!='BATSMEN'):
            team_batters.append(a.text.replace(' †','').replace(' (c)',''))

    is_out_list=[]
    team_commentary=batsmen_data_extract.find_all("div",{"class":"cell commentary"})
    for a in team_commentary:
        if(a.text!=''):
            if("not out" in a):
                is_out='N'
            elif("retired hurt" in a):
                is_out='N'
            else:
                is_out='Y'
            is_out_list.append(is_out)

    team_bat=batsmen_data_extract.find_all("div",{"class":"cell runs"})
    team_batters_score=[]
    for a in team_bat:
        if(a.text!='' and a.text!='BATSMEN'):
            team_batters_score.append(a.text.replace(' †','').replace(' (c)',''))

    team_batters_len=len(team_batters)+1
    team_runs=[]
    team_balls=[]
    team_4s=[]
    team_6s=[]
    team_sr=[]
    team_list=[]
    for i in range(1, team_batters_len):
        team_runs.append(int(team_batters_score[i*5]))
        team_balls.append(int(team_batters_score[i*5+1]))
        team_4s.append(int(team_batters_score[i*5+2]))
        team_6s.append(int(team_batters_score[i*5+3]))
        if(team_batters_score[i*5+4]=='-'):
            team_batters_score[i*5+4]='0'
        team_sr.append(float(team_batters_score[i*5+4]))
        team_list.append(str(innings[team_no-1]))

    
    score_card_batting=pd.DataFrame({'Player_Name' : team_batters,
     'is_out':is_out_list,
     'R' : team_runs,
     'B':team_balls,
     '4s':team_4s,'6s':team_6s,'SR':team_sr,'Team':team_list
     }, columns=batsmen_header.append('Team'))

    return score_card_batting


# In[5]:


import operator
final_batting_scorecard=extract_batting_scorecard(1,batsmen_data)
try:
    final_batting_scorecard=final_batting_scorecard.append(extract_batting_scorecard(2,batsmen_data), ignore_index=True)
except:
    pass
final_batting_scorecard['4s_points']=final_batting_scorecard['4s']*5
final_batting_scorecard['6s_points']=final_batting_scorecard['6s']*10
final_batting_scorecard['runs_points']=0
final_batting_scorecard.loc[final_batting_scorecard['R'] >=15, 'runs_points'] =final_batting_scorecard['R']*1

final_batting_scorecard['runs_bonus_points']=0
final_batting_scorecard.loc[final_batting_scorecard['R'] >=50, 'runs_bonus_points'] = 25
final_batting_scorecard.loc[final_batting_scorecard['R'] >=100, 'runs_bonus_points'] = 50
final_batting_scorecard.loc[operator.and_(final_batting_scorecard['R']==0, final_batting_scorecard['is_out']!='N'), 'runs_bonus_points'] =-20
final_batting_scorecard['sr_points']=0
final_batting_scorecard.loc[operator.and_(operator.and_(operator.or_(final_batting_scorecard['R'] >=15, final_batting_scorecard['B'] >=15),final_batting_scorecard['SR']>=50 ),final_batting_scorecard['SR']<75), 'sr_points'] =-20
final_batting_scorecard.loc[operator.and_(operator.and_(operator.or_(final_batting_scorecard['R'] >=15, final_batting_scorecard['B'] >=15),final_batting_scorecard['SR']>=75 ),final_batting_scorecard['SR']<100), 'sr_points'] =-10
final_batting_scorecard.loc[operator.and_(operator.and_(operator.or_(final_batting_scorecard['R'] >=15, final_batting_scorecard['B'] >=15),final_batting_scorecard['SR']>=100), final_batting_scorecard['SR']<125), 'sr_points'] =0
final_batting_scorecard.loc[operator.and_(operator.and_(operator.or_(final_batting_scorecard['R'] >=15, final_batting_scorecard['B'] >=15),final_batting_scorecard['SR']>=125), final_batting_scorecard['SR']<175), 'sr_points'] =10
final_batting_scorecard.loc[operator.and_(operator.and_(operator.or_(final_batting_scorecard['R'] >=15, final_batting_scorecard['B'] >=15),final_batting_scorecard['SR']>=175), final_batting_scorecard['SR']<250), 'sr_points'] =20
final_batting_scorecard.loc[operator.and_(operator.and_(operator.or_(final_batting_scorecard['R'] >=15, final_batting_scorecard['B'] >=15),final_batting_scorecard['SR']>=250), final_batting_scorecard['SR']<1000), 'sr_points'] =30
final_batting_scorecard['total_batting_points']=final_batting_scorecard['4s_points']+final_batting_scorecard['6s_points']+final_batting_scorecard['runs_points']+final_batting_scorecard['sr_points']+final_batting_scorecard['runs_bonus_points']
final_batting_scorecard=final_batting_scorecard.sort_values(by=['Player_Name'])
final_batting_scorecard=final_batting_scorecard.reset_index()
del final_batting_scorecard['index']
final_batting_scorecard


# In[6]:


final_batting_scorecard['batting_pos'] = final_batting_scorecard.index


for index, row in final_batting_scorecard.iterrows():
    first, *middle, last = str(row["Player_Name"]).split()
    player_name_short=first[0].lower()+"%"+last.lower()
    all_queries_list.append("Update ipl_match_stats_new set batting_pos="+str(row["batting_pos"])+
           " where lower(player_name) like '"+player_name_short+"%' and team_name='"+row["Team"]+
           "' and match_no="+str(match_no)+";")

for index, row in final_batting_scorecard.iterrows():
    all_queries_list.append("Update ipl_match_stats_new set runs_scored="+str(row["R"])+
                            ",balls_faced="+str(row["B"])+
                            ",fours_scored="+str(row["4s"])+
                            ",sixes_scored="+str(row["6s"])+
                            ",is_out='"+str(row["is_out"])+
                            "' where batting_pos="+str(row["batting_pos"])+" and match_no="+str(match_no)+";")


# In[7]:


def extract_bowling_scorecard(team_no,batsmen_data):
    bowling_data_extract=bowlers_data[team_no-1]

    bowling_data_header=bowling_data_extract.find_all("thead")
    bowling_data_header_th=bowling_data_header[0].find_all("th")
    
    bowling_header=[]
    for link in bowling_data_header_th:
        if(link.text!=''):
            bowling_header.append(link.text.replace("Bowling","Player_Name"))
            
    bowling_data_body=bowling_data_extract.find_all("tbody")
    bowling_data_header_td=bowling_data_body[0].find_all("td")
    bowling_data_header_td
    
    bowling_content=[]
    for link in bowling_data_header_td:
        if(link.text!=''):
            bowling_content.append(link.text)
    
    bowling_content_len=len(bowling_content)
    bowling_header_len=len(bowling_header)
    team_bowlers_len=int(bowling_content_len/bowling_header_len)
    
    bowlers=[]
    overs=[]
    maidens=[]
    runs=[]
    wickets=[]
    econ=[]
    zeroes=[]
    fours=[]
    sixes=[]
    wides=[]
    noballs=[]
    team_list=[]

    
    for i in range(0, team_bowlers_len):
        if(team_no==1):
            team_list.append(str(innings[team_no]))
        else:
            team_list.append(str(innings[team_no-2]))
        wides.append(0)
        noballs.append(0)
        bowlers.append(bowling_content[i*bowling_header_len])
        overs.append(float(bowling_content[i*bowling_header_len+1]))
        maidens.append(int(bowling_content[i*bowling_header_len+2]))
        runs.append(int(bowling_content[i*bowling_header_len+3]))
        wickets.append(int(bowling_content[i*bowling_header_len+4]))
        econ.append(float(bowling_content[i*bowling_header_len+5]))
        
        try:
            zeroes.append(int(bowling_content[i*bowling_header_len+6]))
            fours.append(int(bowling_content[i*bowling_header_len+7]))
            sixes.append(int(bowling_content[i*bowling_header_len+8]))
        except:
            zeroes.append(0)
            fours.append(0)
            sixes.append(0)
    
    score_card_bowling=pd.DataFrame({'Player_Name' : bowlers,'Team_BOWL':team_list,
         'O' : overs,
         'M': maidens,
         'R':runs,
         'W':wickets,
         'Econ':econ,
         '0s':zeroes,
         '4s':fours, 
         '6s':sixes,
         'WD':wides,
         'NB':noballs
         }, columns=['Player_Name','Team_BOWL','O','M','R','W','Econ','0s','4s','6s','WD','NB'])
    return score_card_bowling


# In[8]:


import operator
final_bowling_scorecard=extract_bowling_scorecard(1,bowlers_data)
try:
    final_bowling_scorecard=final_bowling_scorecard.append(extract_bowling_scorecard(2,bowlers_data), ignore_index=True)
except:
    pass
final_bowling_scorecard['wicket_points']=final_bowling_scorecard['W']*25
final_bowling_scorecard['wicket_bonus_points']=0
final_bowling_scorecard.loc[final_bowling_scorecard['W'] >=3, 'wicket_bonus_points'] = 25
final_bowling_scorecard.loc[final_bowling_scorecard['W'] >=4,'wicket_bonus_points'] = 50
final_bowling_scorecard.loc[final_bowling_scorecard['W'] >=5,'wicket_bonus_points'] = 75
final_bowling_scorecard.loc[final_bowling_scorecard['W'] >=5,'wicket_bonus_points'] = 75
final_bowling_scorecard['maiden_points']=final_bowling_scorecard['M']*25
final_bowling_scorecard['dot_ball_points']=0
final_bowling_scorecard['dot_ball_points']=4*(final_bowling_scorecard['0s']-final_bowling_scorecard['4s']-final_bowling_scorecard['6s']*1.5)

final_bowling_scorecard['econ_points']=0
final_bowling_scorecard.loc[operator.and_(operator.and_(final_bowling_scorecard['O'] >=2,final_bowling_scorecard['Econ']>0 ),final_bowling_scorecard['Econ']<=4), 'econ_points'] =25
final_bowling_scorecard.loc[operator.and_(operator.and_(final_bowling_scorecard['O'] >=2,final_bowling_scorecard['Econ']>4 ),final_bowling_scorecard['Econ']<=6), 'econ_points'] =15
final_bowling_scorecard.loc[operator.and_(operator.and_(final_bowling_scorecard['O'] >=2,final_bowling_scorecard['Econ']>6 ),final_bowling_scorecard['Econ']<=8), 'econ_points'] =10
final_bowling_scorecard.loc[operator.and_(operator.and_(final_bowling_scorecard['O'] >=2,final_bowling_scorecard['Econ']>8 ),final_bowling_scorecard['Econ']<=10), 'econ_points'] =0
final_bowling_scorecard.loc[operator.and_(operator.and_(final_bowling_scorecard['O'] >=2,final_bowling_scorecard['Econ']>=10 ),final_bowling_scorecard['Econ']<12), 'econ_points'] =-10
final_bowling_scorecard.loc[operator.and_(operator.and_(final_bowling_scorecard['O'] >=2,final_bowling_scorecard['Econ']>=12 ),final_bowling_scorecard['Econ']<14), 'econ_points'] =-15
final_bowling_scorecard.loc[operator.and_(operator.and_(final_bowling_scorecard['O'] >=2,final_bowling_scorecard['Econ']>=14 ),final_bowling_scorecard['Econ']<100), 'econ_points'] =-25
final_bowling_scorecard['total_bowling_points']=final_bowling_scorecard['maiden_points']+final_bowling_scorecard['wicket_points']+final_bowling_scorecard['wicket_bonus_points']+final_bowling_scorecard['dot_ball_points']+final_bowling_scorecard['econ_points']
final_bowling_scorecard=final_bowling_scorecard.sort_values(by=['Player_Name'])
final_bowling_scorecard=final_bowling_scorecard.reset_index()
del final_bowling_scorecard['index']
final_bowling_scorecard


# In[9]:


final_bowling_scorecard['bowling_pos'] = final_bowling_scorecard.index

for index, row in final_bowling_scorecard.iterrows():
    first, *middle, last = str(row["Player_Name"]).split()
    player_name_short=first[0].lower()+"%"+last.lower()
    all_queries_list.append("Update ipl_match_stats_new set bowling_pos="+str(row["bowling_pos"])+
           " where lower(player_name) like '"+player_name_short+"%' and team_name='"+row["Team_BOWL"]+
           "' and match_no="+str(match_no)+";")


for index, row in final_bowling_scorecard.iterrows():
    all_queries_list.append("Update ipl_match_stats_new set overs_bowled="+str(row["O"])+
           ",maidens="+str(row["M"])+
           ",runs_given="+str(row["R"])+
           ",wickets="+str(row["W"])+
           ",economy="+str(row["Econ"])+
           ",dots="+str(row["0s"])+
           ",fours="+str(row["4s"])+
           ",sixes="+str(row["6s"])+
           " where bowling_pos="+str(row["bowling_pos"])+" and match_no="+str(match_no)+";")


# In[10]:


#Function to get the batting scorecard
import pandas as pd

def extract_fielding_scorecard(team_no,batsmen_data):
    batsmen_data_extract=batsmen_data[team_no-1]
    batsmen_data_header=batsmen_data_extract.find_all("div",{"class":"wrap header"})

    batsmen_header=[]
    for link in batsmen_data_header[0]:
        if(link.text!=''):
            batsmen_header.append(link.text.replace('BATSMEN','Player_Name'))

    team_bat=batsmen_data_extract.find_all("div",{"class":"cell batsmen"})

    team_batters=[]
    for a in team_bat:
        if(a.text!='' and a.text!='BATSMEN'):
            team_batters.append(a.text.replace(' †','').replace(' (c)',''))

    team_bat=batsmen_data_extract.find_all("div",{"class":"cell batsmen"})

    team_batters=[]
    for a in team_bat:
        if(a.text!='' and a.text!='BATSMEN'):
            team_batters.append(a.text.replace(' †',' ').replace(' (c)',''))

    team_bat=batsmen_data_extract.find_all("div",{"class":"cell commentary"})
    team_fielders_score=[]
    for a in team_bat:
        if(a.text!='' and a.text!='BATSMEN'):
            team_fielders_score.append(a.text.replace(' †',' ').replace(' (c)',''))

    team_batters_len=len(team_fielders_score)
    team_fielders=[]
    direct_run_out_list=[]
    part_of_run_out_list=[]
    stumpings_list=[]

    #team_commentary=[]

    for i in range(0, team_batters_len):
        test_string=team_fielders_score[i]
        test_string=test_string.replace("retired hurt","not out")
        ##Just for the 31st match
        test_string=test_string.replace("run out (Pandya)","run out (Hardik Pandya)")

        #team_commentary.append(test_string)
        st_pos=test_string.find('st ')

        if(("c & b") in test_string):
            test_string=test_string.replace("c & b","c")+test_string.replace("c & b"," b")
        if test_string[0]=="c" and test_string[1]==" ":
            test_string=test_string[2::]
        elif test_string[0]=="c" and test_string[1]!=" ":
            test_string=test_string[1::]
        bpos=test_string.rfind(' b ')
        if(bpos!=-1):
            test_string=test_string[0:bpos].strip()
        
        run_out_pos=test_string.find('run out (')

        if(test_string!='' and test_string!='lbw'  and test_string!='not out'):
            if(st_pos!=0) and (run_out_pos!=0):
                team_fielders.append(test_string)
        if(run_out_pos==0 and '/' not in test_string):
            test_string=test_string.replace("run out (","")
            test_string=test_string.replace(")","")
            test_string=test_string.replace("†","").strip()
            direct_run_out=test_string
            if(direct_run_out_list!=''):
                direct_run_out_list.append(direct_run_out)
        if(run_out_pos==0 and '/' in test_string):
            run_out_pos=test_string.find('run out (')
            if(run_out_pos==0):
                test_string=test_string.replace("run out (","")
                test_string=test_string.replace(")","")
            test_string=test_string.replace("†","").strip()
            part_of_run_out_guys=test_string.split("/")
            for part_of_run_out in part_of_run_out_guys:
                #print(part_of_run_out)
                if(part_of_run_out!='/'):
                    part_of_run_out_list.append(part_of_run_out)
                    #print(part_of_run_out_list)
        if(st_pos==0):
            test_string=test_string[3::]
            test_string=test_string.replace("†","").strip()
            stumpings_list.append(test_string)

    fielding_list=[]
    fielding_list.append(pd.DataFrame({'Catches':team_fielders
     }, columns=['Catches']))
    
    fielding_list.append(pd.DataFrame({'direct_run_out_list':direct_run_out_list
     }, columns=['direct_run_out_list']))

    fielding_list.append(pd.DataFrame({'part_of_run_out_list':part_of_run_out_list
     }, columns=['part_of_run_out_list']))
    
    fielding_list.append(pd.DataFrame({'stumpings_list':stumpings_list
     }, columns=['stumpings_list']))


    return fielding_list


# In[11]:


pos=1
fielding_list=extract_fielding_scorecard(pos,batsmen_data)
final_fielding_scorecard=fielding_list[0]
final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['Catches'] ).size()}).reset_index()
final_fielding_scorecard_pd.rename(columns = {'Catches':'Player_Name'}, inplace = True)
final_fielding_scorecard_pd["Team"]=innings[pos]
catch_scorecard=final_fielding_scorecard_pd
final_fielding_scorecard_pd


# In[12]:


try:
    pos=2
    fielding_list=extract_fielding_scorecard(pos,batsmen_data)
    final_fielding_scorecard=fielding_list[0]
    final_fielding_scorecard['Catches']=final_fielding_scorecard['Catches']
    final_fielding_scorecard_gp=final_fielding_scorecard.groupby(['Catches']).size()
    final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['Catches'] ).size()}).reset_index()
    final_fielding_scorecard_pd.rename(columns = {'Catches':'Player_Name'}, inplace = True)
    final_fielding_scorecard_pd["Team"]=innings[pos-2]
except:
    pass
    final_fielding_scorecard_pd=pd.DataFrame()
catch_scorecard = catch_scorecard.append(final_fielding_scorecard_pd)
catch_scorecard.rename(columns = {'count':'Catches'}, inplace = True)
catch_scorecard


# In[13]:


def extract_player_name(player_name):
    player_name_list=player_name.split()
    player_first_name_part=""
    player_name_final="%"+player_name_list[-1]+"%"
    if len(player_name_list)>1:
        player_first_name_part="%"+player_name_list[0][0]+""
        player_name_final=player_first_name_part+player_name_final
        # only problem is Hardik and Krunal Pandya
        if("%h%pandya%" in player_name_final.lower()):
            player_name_final="h%pandya%"
        elif("%k%pandya%" in player_name_final.lower()):
            player_name_final="k%pandya%"
    player_name_final=player_name_final.lower().replace("(","").replace(")","")
    return player_name_final


# In[14]:


extract_player_name('Hardik Pandya')


# In[15]:


for index, row in catch_scorecard.iterrows():
    player_name_final=extract_player_name(str(row["Player_Name"]))
    all_queries_list.append("Update ipl_match_stats_new set catches="+str(row["Catches"])+
           " where lower(player_name) like '"+player_name_final+"' and team_name='"+row["Team"]+
           "' and match_no="+str(match_no)+";")


# In[16]:


pos=1
fielding_list=extract_fielding_scorecard(pos,batsmen_data)
final_fielding_scorecard=fielding_list[1]
final_fielding_scorecard['direct_run_out_list']=final_fielding_scorecard['direct_run_out_list']
final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['direct_run_out_list'] ).size()}).reset_index()
final_fielding_scorecard_pd["Team"]=innings[pos]
direct_run_out_scorecard=final_fielding_scorecard_pd


# In[17]:


try:
    pos=2
    fielding_list=extract_fielding_scorecard(pos,batsmen_data)
    final_fielding_scorecard=fielding_list[1]
    final_fielding_scorecard['direct_run_out_list']=final_fielding_scorecard['direct_run_out_list']
    final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['direct_run_out_list'] ).size()}).reset_index()
    final_fielding_scorecard_pd["Team"]=innings[pos-2]
except:
    pass
    final_fielding_scorecard_pd=pd.DataFrame()
direct_run_out_scorecard = direct_run_out_scorecard.append(final_fielding_scorecard_pd)
direct_run_out_scorecard.rename(columns = {'count':'Direct_Run_Out'}, inplace = True)
direct_run_out_scorecard.rename(columns = {'direct_run_out_list':'Player_Name'}, inplace = True)
direct_run_out_scorecard


# In[18]:


for index, row in direct_run_out_scorecard.iterrows():
    player_name_final=extract_player_name(str(row["Player_Name"]))
    all_queries_list.append("Update ipl_match_stats_new set direct_run_out="+str(row["Direct_Run_Out"])+
           " where lower(player_name) like '"+player_name_final+"' and team_name='"+row["Team"]+
           "' and match_no="+str(match_no)+";")


# In[19]:


pos=1
fielding_list=extract_fielding_scorecard(pos,batsmen_data)
final_fielding_scorecard=fielding_list[2]
final_fielding_scorecard['part_of_run_out_list']=final_fielding_scorecard['part_of_run_out_list']
final_fielding_scorecard.groupby(['part_of_run_out_list']).size()
final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['part_of_run_out_list'] ).size()}).reset_index()
final_fielding_scorecard_pd["Team"]=innings[pos]
part_of_run_out_scorecard=final_fielding_scorecard_pd
part_of_run_out_scorecard


# In[20]:


try:
    pos=2
    fielding_list=extract_fielding_scorecard(pos,batsmen_data)
    final_fielding_scorecard=fielding_list[2]
    final_fielding_scorecard['part_of_run_out_list']=final_fielding_scorecard['part_of_run_out_list']
    #final_fielding_scorecard.groupby(['part_of_run_out_list']).size()
    final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['part_of_run_out_list'] ).size()}).reset_index()
    final_fielding_scorecard_pd["Team"]=innings[pos-2]
except:
    pass
    final_fielding_scorecard_pd=pd.DataFrame()
part_of_run_out_scorecard = part_of_run_out_scorecard.append(final_fielding_scorecard_pd)
part_of_run_out_scorecard.rename(columns = {'count':'Part_Of_Run_Out'}, inplace = True)
part_of_run_out_scorecard.rename(columns = {'part_of_run_out_list':'Player_Name'}, inplace = True)
part_of_run_out_scorecard


# In[21]:


for index, row in part_of_run_out_scorecard.iterrows():
    player_name_final=extract_player_name(str(row["Player_Name"]))
    all_queries_list.append("Update ipl_match_stats_new set part_of_run_out="+str(row["Part_Of_Run_Out"])+
           " where lower(player_name) like '"+player_name_final+"' and team_name='"+row["Team"]+
           "' and match_no="+str(match_no)+";")


# In[22]:


pos=1
fielding_list=extract_fielding_scorecard(pos,batsmen_data)
final_fielding_scorecard=fielding_list[3]
final_fielding_scorecard['stumpings_list']=final_fielding_scorecard['stumpings_list']
#final_fielding_scorecard.groupby(['stumpings_list']).size()
final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['stumpings_list'] ).size()}).reset_index()
final_fielding_scorecard_pd["Team"]=innings[pos]
stumpings_scorecard=final_fielding_scorecard_pd


# In[23]:


try:
    pos=2
    fielding_list=extract_fielding_scorecard(pos,batsmen_data)
    final_fielding_scorecard=fielding_list[3]
    final_fielding_scorecard['stumpings_list']=final_fielding_scorecard['stumpings_list']
    #final_fielding_scorecard.groupby(['stumpings_list']).size()
    final_fielding_scorecard_pd=pd.DataFrame({'count' : final_fielding_scorecard.groupby( ['stumpings_list'] ).size()}).reset_index()
    final_fielding_scorecard_pd
    final_fielding_scorecard_pd["Team"]=innings[pos-2]
except:
    pass
    final_fielding_scorecard_pd=pd.DataFrame()
stumpings_scorecard=stumpings_scorecard.append(final_fielding_scorecard_pd)
stumpings_scorecard.rename(columns = {'count':'Stumpings'}, inplace = True)
stumpings_scorecard.rename(columns = {'stumpings_list':'Player_Name'}, inplace = True)
stumpings_scorecard


# In[24]:


for indexs, rows in stumpings_scorecard.iterrows():
    player_name_final=extract_player_name(str(rows["Player_Name"]))
    all_queries_list.append("Update ipl_match_stats_new set stumpings="+str(rows["Stumpings"])+
           " where lower(player_name) like '"+player_name_final+"' and team_name='"+rows["Team"]+
           "' and match_no="+str(match_no)+";")


# In[25]:


#for duck_out_player in duck_out_in0ball_players_list:
    #if(duck_out_player!=""):
        #all_queries_list.append("update ipl_match_stats_new  set is_out='Y' where match_no="+str(match_no)+"  and balls_faced =0 and lower(player_name) like lower('"+duck_out_player+"');")


# In[26]:


#all_queries_list.append("update ipl_match_stats_new  set is_out='Y' where match_no="+str(match_no)+"  and balls_faced >0;")
all_queries_list.append("update ipl_match_stats_new  set strike_rate=ROUND((runs_scored*100/balls_faced),2) where match_no="+str(match_no)+" and balls_faced>0;")
all_queries_list.append("update ipl_match_stats_new  set economy=ROUND((runs_given/(floor(overs_bowled)+(overs_bowled-floor(overs_bowled))/6*10)),2) where match_no="+str(match_no)+"  and overs_bowled>0;")

all_queries_list.append("\n------------Manually update if any update has zero records updated add replace based on player name \n\n\n\n")
all_queries_list.append("\nupdate ipl_match_stats_new  set is_part_of_winning_team='Y' where match_no="+str(match_no)+"  and team_name='"+winning_team+"';") 
all_queries_list.append("update ipl_match_stats_new  set is_part_of_winning_team='N' where match_no="+str(match_no)+"  and team_name<>'"+winning_team+"';") 
all_queries_list.append("update ipl_match_stats_new  set is_mom='Y' where match_no="+str(match_no)+" and player_name like '%"+man_of_the_match+"%';") 

#for not_out_player in not_out_in_0_players_list:
    #if(not_out_player!=""):
        #all_queries_list.append("update ipl_match_stats_new  set is_out='N' where match_no="+str(match_no)+"  and balls_faced >0 and lower(player_name) like lower('"+not_out_player+"');")
        


# In[27]:


import numpy as np
import re
result = pd.concat([final_batting_scorecard.set_index('Player_Name'), final_bowling_scorecard.set_index('Player_Name')], axis=1)
result=result.fillna(0)
result2=finaldata=pd.DataFrame()
result2['total_batting_points']=result['total_batting_points']
result2['total_bowling_points']=result['total_bowling_points']
result2['Team_BAT']=result['Team']
result2['Team_BOWL']=result['Team_BOWL']


conditions = [
    result2['Team_BAT']=='0', 
    result2['Team_BAT']!='0']

choices = [result2['Team_BOWL'], result2['Team_BAT']]

result2['Team'] = np.select(conditions, choices)


result2.loc[result2['Team']=='0','Team'] =result['Team_BOWL']

result2['total_bat_bowl_points']=result2['total_batting_points']+result2['total_bowling_points']
result2['Temp_Player_Name'] = result2.index
result2=result2.reset_index()
del result2['index']
result2.insert(0, 'Player_Name', result2['Temp_Player_Name'])
del result2['Temp_Player_Name']

result3=finaldata=pd.DataFrame()

result2_rows_list=[]

for index, row in result2.iterrows():
    if(row["Team_BAT"]==0):
        row["Team"]=row["Team_BOWL"]
    if(row["Team_BOWL"]==0):
        row["Team"]=row["Team_BAT"]
    row["catches_points"]=0
    row["part_of_run_out_points"]=0
    row["direct_run_out_points"]=0
    row["stumpings_points"]=0

    player_name=row["Player_Name"]
    for indexc, rowc in catch_scorecard.iterrows():
        pattern=extract_player_name(rowc["Player_Name"]).replace("%",".").replace("h.pandya.","hh.pandya.")
        compiled = re.compile(pattern)
        ms = compiled.search(player_name.lower()+" ")
        try:
            if(ms.string!=''):
                row["catches_points"]=rowc["Catches"]*5
                break
        except:
            pass
    
    for indexdr, rowdr in direct_run_out_scorecard.iterrows():
        pattern=extract_player_name(rowdr["Player_Name"]).replace("%",".").replace("h.pandya.","hh.pandya.")
        #print("pattern:::"+pattern)
        compiled = re.compile(pattern)
        ms = compiled.search(player_name.lower()+" ")
        try:
            if(ms.string!=''):
                #print(player_name)
                row["direct_run_out_points"]=rowdr["Direct_Run_Out"]*15
                break
        except:
            pass
    
    
    for indexpr, rowpr in part_of_run_out_scorecard.iterrows():
        pattern=extract_player_name(rowpr["Player_Name"]).replace("%",".").replace("h.pandya.","hh.pandya.")
        compiled = re.compile(pattern)
        ms = compiled.search(player_name.lower()+" ")
        try:
            if(ms.string!=''):
                row["part_of_run_out_points"]=rowpr["Part_Of_Run_Out"]*5
                break
        except:
            pass
    
    
    for indexs, rows in stumpings_scorecard.iterrows():
        pattern=extract_player_name(rows["Player_Name"]).replace("%",".").replace("h.pandya.","hh.pandya.")
        compiled = re.compile(pattern)
        ms = compiled.search(player_name.lower()+" ")
        try:
            if(ms.string!=''):
                row["stumpings_points"]=rows["Stumpings"]*10
                break
        except:
            pass
    
    row["Total_Batting_Points"]=row["total_batting_points"]
    row["Total_Bowling_Points"]=row["total_bowling_points"]

    row["Total_Fielding_Points"]=row["stumpings_points"]+row["part_of_run_out_points"]+row["direct_run_out_points"]+row["catches_points"]
    row["Total_Points"]=row["total_batting_points"]+row["total_bowling_points"]+row["Total_Fielding_Points"]
    
    result2_rows_list.append(row)
result3 = pd.DataFrame(result2_rows_list)
del result3['Team_BAT']
del result3['Team_BOWL']
del result3['stumpings_points']
del result3['part_of_run_out_points']
del result3['direct_run_out_points']
del result3['catches_points']
del result3['total_bat_bowl_points']
del result3['total_batting_points']
del result3['total_bowling_points']


result3


# In[28]:


teams_list=teams.split("\t")
teams_list_len=len(teams_list)-1
person_count=int(teams_list_len/17)

match_no_list=[]
match_title_list=[]
person_name_list=[]
captain_list=[]
mom_list=[]
winner_list=[]
player_list=[]

for i in range(0, person_count):
    for j in range(0, 11):
        match_no_list.append(teams_list[(i*17)+0])
        match_title_list.append(teams_list[(i*17)+1])
        person_name_list.append(teams_list[(i*17)+2])
        captain_list.append(teams_list[(i*17)+14])
        mom_list.append(teams_list[(i*17)+15])
        winner_list.append(teams_list[(i*17)+16])

    player_list.append(teams_list[(i*17)+3])
    player_list.append(teams_list[(i*17)+4])
    player_list.append(teams_list[(i*17)+5])
    player_list.append(teams_list[(i*17)+6])
    player_list.append(teams_list[(i*17)+7])
    player_list.append(teams_list[(i*17)+8])
    player_list.append(teams_list[(i*17)+9])
    player_list.append(teams_list[(i*17)+10])
    player_list.append(teams_list[(i*17)+11])
    player_list.append(teams_list[(i*17)+12])
    player_list.append(teams_list[(i*17)+13])
team_selected_list=pd.DataFrame({'Match_No' : match_no_list,'Match_Title':match_title_list,
         'Person_Name' : person_name_list,
         'Player_Name': player_list,
         'Captain':captain_list,
         'Man_of_the_Match':mom_list,
         'winner':winner_list
         }, columns=['Match_No','Match_Title','Person_Name','Player_Name','Captain','Man_of_the_Match','winner'])
team_selected_list['Is_Captain']="N"
team_selected_list['Is_MoM']="N"
team_selected_list.loc[team_selected_list['Player_Name']==team_selected_list["Captain"],'Is_Captain'] = "Y"
team_selected_list.loc[team_selected_list['Player_Name']==team_selected_list["Man_of_the_Match"],'Is_MoM'] = "Y"

del team_selected_list["Captain"]
del team_selected_list["Man_of_the_Match"]
#team_selected_list["Winner"]=team_selected_list["winner"]
#del team_selected_list["winner"]
#team_selected_list


# In[29]:


for ii in range (1,3):
    teams_selected_fuzzy_list=[]
    for index1, row1 in team_selected_list.iterrows():
        prev_match_score=0
        my_player_name=""
        name_list_1 = row1["Player_Name"].split();
        player_name1=name_list_1[0][0]+name_list_1[-1]
        for index2, row2 in result3.iterrows():
            name_list_2 = row2["Player_Name"].split();
            if(row1["Player_Name"]=="Krunal Pandya"):
                row1["Player_Name"]="KH Pandya"
            elif(row1["Player_Name"]=="Hardik Pandya"):
                row1["Player_Name"]="HH Pandya"
            elif(row1["Player_Name"]=="Mujeeb Zadran"):
                row1["Player_Name"]="Mujeeb Ur Rahman"
            elif(row1["Player_Name"]=="Dinesh Karthik"):
                row1["Player_Name"]="KD Karthik"
            elif(row1["Player_Name"]=="Rashid Khan Arman"):
                row1["Player_Name"]="Rashid Khan"
            elif(row1["Player_Name"]=="Gowtham Krishnappa"):
                row1["Player_Name"]="Krishnappa Gowtham"
                
            player_name2=name_list_2[0][0]+name_list_2[-1]
            
    
    
            if(player_name2==player_name1):
                #print("****"+row2["Player_Name"]+"  "+player_name2)
                #if(player_name2=="KWilliamson"):
                    #print(str(row2["Total_Points"])+"  "+row2["Player_Name"])
                #row1["Old_Player_Name"]=row1["Player_Name"]
                player_name_new=row2["Player_Name"]
                row1["Player_Name"]=player_name_new
                row1["points"]=int(row2["Total_Points"])
                if(row1["Is_Captain"]=='Y'):
                    row1["points"]=int(row1["points"]*2)
            row1["Player_Name"]=row1["Player_Name"].replace("✈","")
        teams_selected_fuzzy_list.append(row1)
    
    teams_selected_fuzzy = pd.DataFrame(teams_selected_fuzzy_list)
    
    
    #del(teams_selected_fuzzy["Old_Player_Name"])
    del(teams_selected_fuzzy["Is_MoM"])
    del(teams_selected_fuzzy["Is_Captain"])
    
    
    
    teams_selected_fuzzy["points_1"]=teams_selected_fuzzy["points"]*-1
    teams_selected_fuzzy=teams_selected_fuzzy.sort_values(by=['Person_Name','points_1'])
    del(teams_selected_fuzzy["points_1"])
    teams_selected_fuzzy_pd=pd.DataFrame({'sum' : teams_selected_fuzzy.groupby( ['Person_Name'] )["points"].sum()}).reset_index()
    teams_selected_fuzzy_pd
    
    teams_selected_fuzzy_pd2=pd.DataFrame({'winner' : teams_selected_fuzzy.groupby( ['Person_Name'] )["winner"].max()}).reset_index()
    teams_selected_fuzzy_pd2["winner_points"]= -50
    teams_selected_fuzzy_pd2.loc[teams_selected_fuzzy_pd2["winner"]==winning_team, 'winner_points'] = 50
    
    teams_selected_fuzzy_pd3=pd.DataFrame()
    
    teams_selected_fuzzy_pd3 = pd.concat([teams_selected_fuzzy_pd.set_index('Person_Name'), teams_selected_fuzzy_pd2.set_index('Person_Name')], axis=1)
    del(teams_selected_fuzzy_pd3["winner"])
    teams_selected_fuzzy_pd3["total_points"]=teams_selected_fuzzy_pd3["sum"]+teams_selected_fuzzy_pd3["winner_points"]
    del(teams_selected_fuzzy_pd3["sum"])
    del(teams_selected_fuzzy_pd3["winner_points"])
    print("")


# In[30]:


print("Player Points")
teams_selected_fuzzy=teams_selected_fuzzy.sort_values(by=['Person_Name'],ascending=True)
teams_selected_fuzzy


# In[31]:


print("Player Points#Summary")
teams_selected_fuzzy_pd=teams_selected_fuzzy_pd.sort_values(by=['sum'],ascending=False)
teams_selected_fuzzy_pd


# In[32]:


print("Winner Team Points")
teams_selected_fuzzy_pd2


# In[33]:


print("Total Points")
teams_selected_fuzzy_pd3
teams_selected_fuzzy_pd3=teams_selected_fuzzy_pd3.sort_values(by=['total_points'],ascending=False)
teams_selected_fuzzy_pd3


# In[34]:


all_queries_str="\n".join(all_queries_list)

all_queries_str=all_queries_str.replace("k%karthik","d%karthik")
all_queries_str=all_queries_str.replace("k%gowtham","%gowtham%k%");
all_queries_str=all_queries_str.replace("lower(player_name) like 'm%rahman%' and team_name='KXIP'","lower(player_name) like 'mujeeb%' and team_name='KXIP'");
all_queries_str=all_queries_str.replace("klaasen%","kla%sen%");
all_queries_str=all_queries_str.replace("k%sharma%","karn%sharma%");
all_queries_str=all_queries_str.replace("like '%sharma%' and team_name='CSK'","like 'karn%sharma%' and team_name='CSK'")
print ("--Update queries below:\n"+all_queries_str)

