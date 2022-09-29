import os
import praw
import random
from supabase_py import create_client, Client
from Inorganicchemistry import *

from webserver import keep_alive
import time 

# CREATING REDDIT INSTANCE
reddit = praw.Reddit(
    username=os.environ.get('praw_REDDIT_USERNAME'),
    password=os.environ.get('praw_REDDIT_PASSWORD'),
    client_id=os.environ.get('praw_REDDITAPI_CLIENT'),
    client_secret=os.environ.get('praw_REDDITAPI_SECRET'),
    user_agent="RandomPYQBOT")

# SUPABSE CONNECTION
url: str = os.environ.get("SUPABASE_URLRB1")
key: str = os.environ.get("SUPABASE_KEYRB1")
supabase: Client = create_client(url, key)
comments = supabase.table("CommentsID").select("*").execute()
RESPONDED = [comment['id'] for comment in comments.get("data", [])]

Subreddit = reddit.subreddit("JEENEETards")

# TOPICS AND QUESTION DEFINITION AREA
ChemistryTopics = ['P','Hydrogen','Bonding','Period','S','Metallurgy','Env','DF']


PhysicsTopics = ['Magnetism and Matter']


#MathematicsTopics = ['Basic', 'Quad', 'Complex', 'PNC', 'Seq', 'PMI', 'Bino', 'TrigRat', 'TrigId', 'Line', 'Circle'
 #   , 'Parabola', 'Ellipse', 'Hyperbola', 'Limits', 'Reasoning', 'Stats', 'Heights', 'Triangles', 'Sets'
  #  , 'Matrice', 'Det', 'InverseTrig', 'Diff', 'AOD', 'INDEFIN', 'DefIN', 'AOC', 'DIFFEQ', 'Vector', '3D', 'Prob']



# submission.reply(body=bot_reply) future praw 8
keep_alive()
# submission.reply(body=bot_reply) future praw 8
while True:
  
    comments = supabase.table("CommentsID").select("*").execute()
    RESPONDED = [comment['id'] for comment in comments.get("data", [])]
    for submission in Subreddit.new(limit=60):
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]  
        while comment_queue:
            comment = comment_queue.pop(0)
            if 'pyq' in comment.body.lower()  and comment.id not in RESPONDED:
                ChapterChosen=random.choice(ChemistryTopics)
                



               
                if ChapterChosen=='P':
                    QuestionChosen= random.choice(P_BLOCKQ)
                    i=P_BLOCKQ.index(QuestionChosen)
                    REPLY = '''Here is a random jee previous year question for ya : 
                Q)  %s  
                >!Solution = %s!<   <--- Solution

                Chapter= P block
                
                 A)  %s
                   
                 B)  %s
                        
                 C)  %s
                        
                 D)  %s
                         ''' % (
              P_BLOCKQ[i],P_BLOCKSOLUTION[i], P_BLOCKA[i], P_BLOCKB[i], P_BLOCKC[i],P_BLOCKD[i])
                    comment.reply(REPLY)
                    data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
            
                elif ChapterChosen=='Period':
                        QuestionChosen= random.choice(PeriodicitySQ)
                        i=PeriodicitySQ.index(QuestionChosen)
                        REPLY = '''Here is a random jee previous year question for ya : 
                Q)  %s   
                 >!Solution = %s!<   <--- Solution

                Chapter= Periodicity
                 
                A)  %s
                        
                B)  %s
                        
                C)  %s
                        
                D)  %s
                         ''' % (
                        PeriodicitySQ[i],PeriodicitySol[i], PeriodicityA[i], PeriodicityB[i], PeriodicityC[i], PeriodicityD[i])
                        comment.reply(REPLY)
                        data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
                elif ChapterChosen=='Bonding':
                    QuestionChosen= random.choice(BondingSQ)
                    i=BondingSQ.index(QuestionChosen)
                    REPLY = '''Here is a random jee previous year question for ya :  
                Q)%s   
                >!Solution = %s!<  <--- Solution

                Chapter= Chemical Bonding
                        
                A)  %s
                        
                B)  %s
                        
                C)  %s
                        
                D)  %s
                        ''' % (
                    BondingSQ[i],BondingSol[i], BondingA[i], BondingB[i], BondingC[i], BondingD[i])
                    comment.reply(REPLY)
                    data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
                elif ChapterChosen=='Hydrogen':
                    QuestionChosen= random.choice(HydrogenSQ)
                    i=HydrogenSQ.index(QuestionChosen)
                    REPLY = '''Here is a random jee previous year question for ya : 
                Q)  %s  
                >!Solution = %s!<  <--- Solution

                Chapter= Hydrogen

                A)  %s
                        
                B)  %s
                        
                C)  %s
                        
                D)  %s
                         ''' % (
                    HydrogenSQ[i],HydrogenSol[i], HydrogenA[i], HydrogenB[i], HydrogenC[i], HydrogenD[i] )
                    comment.reply(REPLY)
                    data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
                elif ChapterChosen=='S':
                    QuestionChosen= random.choice(SBLOCKSQ)
                    i=SBLOCKSQ.index(QuestionChosen)
                    REPLY = '''Here is a random jee previous year question for ya : 
                Q)  %s   
                 >!Solution = %s!<   <--- Solution

                 Chapter= S block and Hydrogen
                 
                A)  %s
                        
                B)  %s
                        
                C)  %s
                        
                D)  %s
                         ''' % (
                    SBLOCKSQ[i],SBLOCKSOL[i], SBLOCKA[i], SBLOCKB[i], SBLOCKC[i], SBLOCKD[i])
                    comment.reply(REPLY)
                    data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
                elif ChapterChosen=='Metallurgy':
                    QuestionChosen= random.choice(MetallurgySQ)
                    i=MetallurgySQ.index(QuestionChosen)
                    REPLY = '''Here is a random jee previous year question for ya : 
                Q)  %s   
                 >!Solution = %s!<   <--- Solution

                 Chapter = Metallurgy
                 
                A)  %s
                        
                B)  %s
                        
                C)  %s
                        
                D)  %s
                         ''' % (
                    MetallurgySQ[i],MetallurgySol[i], MetallurgyA[i], MetallurgyB[i], MetallurgyC[i], MetallurgyD[i])
                    comment.reply(REPLY)
                    data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
                elif ChapterChosen=='Env':
                    QuestionChosen= random.choice(EnvSQ)
                    i=EnvSQ.index(QuestionChosen)
                    REPLY = '''Here is a random jee previous year question for ya : 
                Q)  %s   
                 >!Solution = %s!<   <--- Solution

                 Chapter= Environmental Chemistry 
                 
                A)  %s
                        
                B)  %s
                        
                C)  %s
                        
                D)  %s
                         ''' % (
                    EnvSQ[i],EnvSOL[i], EnvA[i], EnvB[i], EnvC[i], EnvD[i])
                    comment.reply(REPLY)
                    data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
                elif ChapterChosen=='DF':
                    QuestionChosen= random.choice(DFBLOCKSQ)
                    i=DFBLOCKSQ.index(QuestionChosen)
                    REPLY = '''Here is a random jee previous year question for ya : 
                Q)  %s   
                 >!Solution = %s!<   <--- Solution

                 Chapter= D and F block 
                 
                A)  %s
                        
                B)  %s
                        
                C)  %s
                        
                D)  %s
                         ''' % (
                    DFBLOCKSQ[i],DFBLOCKSOL[i], DFBLOCKA[i], DFBLOCKB[i], DFBLOCKC[i], DFBLOCKD[i])
                    comment.reply(REPLY)
                    data = supabase.table("CommentsID").insert({"id": comment.id, "COMMENTBODY": comment.body}).execute()
                time.sleep(20)
                  



            comment_queue.extend(comment.replies)
            
