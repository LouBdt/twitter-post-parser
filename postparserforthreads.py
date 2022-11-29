#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 13:49:50 2022
@author: lou
Mastodon:
@Dykecyclette@eldritch.cafe
"""
import os

user = "@"+input("User @ (without \'@\'):")

def getUrlFromStr(string):
    start_url = False
    url = ""
    for char in string:
        if char==")":
            start_url = False
            break
        if start_url:            
            url += char
        if char=='(':
            start_url = True
    return url

def sortByColumn(tableau, col):
    n = len(tableau)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if tableau[j][col] > tableau[j + 1][col]:
                swapped = True
                tableau[j], tableau[j + 1] = tableau[j + 1], tableau[j]
        if not swapped:
            return tableau
    return tableau
    
def extraireDate(string):
    start_date = False
    date = ""
    annee = ""
    compte_espace = 0
    for char in string:
        if char==" " and start_date:
            compte_espace+=1
        if char==']':
            break
        if start_date and compte_espace>0 and compte_espace<3:
            date += char
        if start_date and compte_espace>4:            
            annee += char
        if char=='[' or compte_espace== 5:
            start_date = True
    return annee+" "+date

stats = [[">Nombre de tweets totaux (dont réponses et RTs)",0], 
         [">Nombre de retweets",0],
         [">Nombre de threads >2tweets", 0],
         [">Nombre de reponses a autrui", 0]]
autrestweets = []
retweets = []
reponses = []
threads = []
#Avant de lire les fichiers on va les mettre dans une liste par ordre chronologique
print("Scanning .md files (not the DM ones don\'t worry)...")
fichiers = []
for file in os.scandir('/home/lou/Documents/Archive Twitter/Programme perso/'):
    if '.md' in file.name and 'DMs' not in file.name:
        md = open(file, "r")
        fichiers.append([md, md.name])
        print("\r File"+md.name, end='')
fichiers = sortByColumn(fichiers, 1)

print("\r \n")
print("\r Extracting tweets from markdown files...\n", end='')
for file in fichiers:
    file = file[0]
    line = file.readline()
    tweet = []
    while line:
        if "----" in line:
            if "RT @" in tweet[0]:
                retweets.append(tweet)
                stats[1][1] +=1
            elif "Replying to ["+user in tweet[0]:
                threads.append(tweet)
            elif "Replying to [@" in tweet[0]:
                reponses.append(tweet)
                stats[3][1] += 1
            else:
                autrestweets.append(tweet)
            stats[0][1]+=1
            print("\r Tweet #"+str(stats[0][1]), end='')
            tweet = []
        else:
            if line !='\n':
                line = line.replace('\n','')
                tweet.append(line)
        line = file.readline()
        
    file.close()

print("\r \n")
print("\r Re-organizing threads...\n", end='')
#Réorganisation des Threads
liste_des_threads = []
compteur_avancement = 0
#On va voir dans les tweets normaux s'ils sont le début de threads
for tweet in autrestweets:
    x = 100*compteur_avancement/stats[0][1]
    print("\r Currently at: {:2.1f}%".format(x), end='')
    compteur_avancement+=1
    #recuperation de l'url du tweet
    url = getUrlFromStr(tweet[1])
    date = extraireDate(tweet[1])
    longueur_du_thread = 0
    #On va parcourrir tous les tweets de Thread pour voir si c'est le début d'un thread
    #On le fait à l'infini pour rajouter les tweets les uns après les autres
    reponse_trouvee = False
    for th in threads:
        #recuperation de l'url du tweet auquel on répond
        thurl = getUrlFromStr(th[0])
        if url == thurl:
            reponse_trouvee = True
            thread_en_cours = [tweet, th]
            url = getUrlFromStr(th[2])
            longueur_du_thread=2
            break
    while reponse_trouvee:
        reponse_trouvee = False
        for th in threads:
            #recuperation de l'url du tweet auquel on répond
            thurl = getUrlFromStr(th[0])
            if url == thurl:
                reponse_trouvee = True
                thread_en_cours.append(th)
                url = getUrlFromStr(th[2])
                longueur_du_thread+=1
                break
    if longueur_du_thread>0:
        liste_des_threads.append([longueur_du_thread,date, thread_en_cours])
        if longueur_du_thread>2:
            stats[2][1]+=1

    
#Maintenant on va voir si une réponse à un tweet de quelqu'un·e d'autre a démarré un thread.  
for tweet in reponses:
    x = 100*compteur_avancement/stats[0][1]
    print("\r Currently at: {:2.1f}%".format(x), end='')
    compteur_avancement+=1
    
    #recuperation de l'url du tweet
    url = getUrlFromStr(tweet[2])
    date = extraireDate(tweet[2])
    longueur_du_thread = 0
    #On va parcourrir tous les tweets de Thread pour voir si c'est le début d'un thread
    #On le fait à l'infini pour rajouter les tweets les uns après les autres
    reponse_trouvee = False
    for th in threads:
        #recuperation de l'url du tweet auquel on répond
        thurl = getUrlFromStr(th[0])
        if url == thurl:
            reponse_trouvee = True
            thread_en_cours = [tweet, th]
            url = getUrlFromStr(th[2])
            longueur_du_thread=2
            break
    while reponse_trouvee:
        reponse_trouvee = False
        for th in threads:
            #recuperation de l'url du tweet auquel on répond
            thurl = getUrlFromStr(th[0])
            if url == thurl:
                reponse_trouvee = True
                thread_en_cours.append(th)
                url = getUrlFromStr(th[2])
                longueur_du_thread+=1
                break
    if longueur_du_thread>0:
        liste_des_threads.append([longueur_du_thread, date, thread_en_cours])
        if longueur_du_thread>2:
            stats[2][1]+=1
        
#Et enfin on va voir si un retweet de quelqu'un·e d'autre a démarré un thread.  
for tweet in retweets:
    x = 100*compteur_avancement/stats[0][1]
    print("\r Currently at: {:2.1f}%".format(x), end='')
    compteur_avancement+=1
    
    #recuperation de l'url du tweet
    url = getUrlFromStr(tweet[-1])
    date = extraireDate(tweet[-1])
    longueur_du_thread = 0
    #On va parcourrir tous les tweets de Thread pour voir si c'est le début d'un thread
    #On le fait à l'infini pour rajouter les tweets les uns après les autres
    reponse_trouvee = False
    for th in threads:
        #recuperation de l'url du tweet auquel on répond
        thurl = getUrlFromStr(th[0])
        if url == thurl:
            reponse_trouvee = True
            thread_en_cours = [tweet, th]
            url = getUrlFromStr(th[2])
            longueur_du_thread=2
            break
    while reponse_trouvee:
        reponse_trouvee = False
        for th in threads:
            #recuperation de l'url du tweet auquel on répond
            thurl = getUrlFromStr(th[0])
            if url == thurl:
                reponse_trouvee = True
                thread_en_cours.append(th)
                url = getUrlFromStr(th[2])
                longueur_du_thread+=1
                break
    if longueur_du_thread>0:
        liste_des_threads.append([longueur_du_thread,date, thread_en_cours])
        if longueur_du_thread>2:
            stats[2][1]+=1
            
print("\r Currently at: {:2.1f}%".format(100), end='')

liste_des_threads = sortByColumn(liste_des_threads,0)
liste_des_threads.reverse()

print("\n")
import shutil
#Sauvegarde des résultats
cwd = os.getcwd()
target_dir1 = cwd +'/Resultats'
if not os.path.exists(target_dir1):
    os.mkdir(target_dir1)
if input("Effaçage des données de "+target_dir1+" ? [y/n]").lower()=="y":
    print("Sauvegarde des résultats")
    shutil.rmtree(target_dir1)
    if not os.path.exists(target_dir1):
        os.mkdir(target_dir1)
    with open(target_dir1+'/'+'stats.txt', 'w') as f:
        f.write('===Statistiques de l\'archive twitter de '+user+'===\n')
        for ligne in stats:
            f.write(ligne[0]+': '+str(ligne[1]))
            f.write('\n')
    target_dir2 = target_dir1+'/Threads'
    if not os.path.exists(target_dir2):
        os.mkdir(target_dir2)
    for thread in liste_des_threads:
        with open(target_dir2+'/'+str(thread[0])+'tweets - '+thread[1]+'.txt', 'w') as f:
            for t in thread[2]:
                if len(t)==2:
                    f.write(t[0]+'\n')
                else:
                    f.write(t[1]+'\n')
                f.write('\n')
    print("Résultats sauvegardés dans "+target_dir1)
else:
    print("Sauvegarde des résultats impossible !")
    print("Fin du programme")
