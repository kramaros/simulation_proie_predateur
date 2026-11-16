"""
objectif:
========== ÉCOSYSTÈME : GÉNÉRATION 42 ==========

Environnement :
    Température : 23.4 °C
    Ressources disponibles : 785 unités
    Eau disponible : 420 unités

Population :
    Lapins      : 124 individus (+12)
    Renards     :  18 individus (-3)
    Herbe       : 847 unités (-125)

Événements :pass
    - 8 lapins sont morts de faim.
    - 3 renards sont morts de vieillesse.
    - 12 lapins sont nés.
    - Une sécheresse réduit les ressources de 15 %.

environement={} 
État de l'écosystème : STABLE
================================================
"""
import random
import matplotlib.pyplot as plt
import numpy as np
#manger ou se reproduire. (tout evolue en fonction de ca)
# reussir a coder une ia capable de gerer l'équilibre de l'environnement avec un max de 10 000 d'herbe par ex

class animal: # definissant predateur et proie
    def __init__(self,id,type,sexe,age,poids):
        self.id=id
        self.type=type
        self.sexe=sexe
        self.age=age #age max:10
        self.poids=poids

    def __str__(self):
        return f"ID: {self.id}\ntype: {self.type}\nsexe: {self.sexe}\nage: {self.age}\npoids: {self.poids}"

    def __repr__(self):
        return f"{self.id}"

# environnemen climat et ressources
env={
    "température":int,
    "ressources disponibles":int,
    "eau disponible":int,
    "max herbe":1000
}

population={
    "lapin":[],#composé d'herbe, d'eau, de température 
    "renard":[],
    "Herbe":0,
    "décès lapin":0,
    "décès renard":0,
    "naissance lapin":0,
    "naissance renard":0
}

# naissance d'un type (sans prise des gènes des parents) 
def naissance(type:str):
    x=animal(type+str(len(population[type])+1),type,random.choice(["male","female"]),0,random.randint(5,10))
    for i in population:
        if x.type==i:
            population[i].append(x)
    population[f"naissance {x.type}"]+=1
    return x

# generation du nb renard/lapin/vegetaux
def depart():
    fichier=open("save.txt","w")
    fichier.write("")
    x=int(input("nombre de predateur ?"))
    y=int(input("nombre de proie ?"))
    z=int(input("quantité d'herbe ?"))
    max_herbe=int(input("maximum d'herbe ?"))
    for i in range(x):
        naissance("renard")
    for i in range(y):
        naissance("lapin")
    population["Herbe"]=z
    population["naissance lapin"]-=y
    population["naissance renard"]-=x
    env["max herbe"]=max_herbe
    fichier.write(f"lapin: {len(population["lapin"])} renard: {len(population["renard"])} Herbe: {population["Herbe"]} dc_lapin: {population['décès lapin']} dc_renard: {population["décès renard"]} nc_lapin: {population['naissance lapin']} nc_renard: {population['naissance renard']}\n")
    return 


#action de manger animaux ou herbe(+gestion herbe) ou mourrir de faim
def manger(mangeur:object,mangé):
    if mangeur in population["renard"]:
        if mangé in population["lapin"]:
            mort(mangé)
    elif mangeur in population["lapin"]:
        if population["Herbe"]>0:
            population["Herbe"]-=4
        elif population["Herbe"]<=0:
            mort(mangeur)
    population["Herbe"]=max(0,min(population["Herbe"],env["max herbe"]))

    return population

#action de reproduction entre 2 meme espece
def reproduction(un,deux):
    if un.type==deux.type and un.sexe!=deux.sexe:
        return naissance(un.type)


#interaction entre tout les animaux (manger/reproduction) et gestion age et sauvegarde txt pour ensuite faire des graphs 
def interaction():
    sauvegarde=open('save.txt','a')
    all=population["lapin"]+population["renard"]
    for i in all:
        i.age+=1
        if i.age>=random.randint(5,10):
            mort(i)
        if i in population["lapin"] or i in population["renard"]:
            try:
                manger(i,random.choice(population["lapin"]))
            except:
                mort(i)
            if i in population["lapin"] or i in population["renard"]:
                try:
                    reproduction(i, random.choice(population[i.type]))
                except:
                    continue
    sauvegarde.write(f"lapin: {len(population["lapin"])} renard: {len(population["renard"])} Herbe: {population["Herbe"]} dc_lapin: {population['décès lapin']} dc_renard: {population["décès renard"]} nc_lapin: {population['naissance lapin']} nc_renard: {population['naissance renard']}\n")

    return population

#décès boost l'herbe de {mort.poids}% (passer a +5)et remove l'animal
def mort(qqun):
    #population["Herbe"]+=population["Herbe"]*qqun.poids/100
    population["Herbe"]+=5
    for i in population:
        try:
            population[i].remove(qqun)
            population[f"décès {qqun.type}"]+=1
        except:
            continue
    
    population["Herbe"]=max(0,min(population["Herbe"],env["max herbe"]))
    return population

#passage d'une unité de tempŝ
def génération(temps:int):
    for i in range(temps):
        pluie()
        interaction()
    return f"lapin: {len(population["lapin"])} renard: {len(population["renard"])} Herbe: {population["Herbe"]} dc_lapin: {population['décès lapin']} dc_renard: {population["décès renard"]} nc_lapin: {population['naissance lapin']} nc_renard: {population['naissance renard']}"

# permettant de continuer ou d'arreter la simulation ou chasse au renard  (a verifier )
def gestion():
    script=True
    while script==True:
        cb=int(input("combien de génération ?"))
        print(génération(cb))
        ask=int(input("1.continuer / 2.arreter / 3.chasser renard "))
        if ask==1:
            script=True
        if ask==2:
            script=False
            choix_graph()
        if ask==3:
            nb=int(input("combien a tuer ?"))
            test=0
            print(len(population["renard"]))
            for i in population["renard"].copy():
                if test<nb:
                    population["renard"].remove(i)
                    population["décès renard"]+=1
                test+=1
            print(len(population["renard"]))

#pluie augmente de 10% l'herbe
def pluie():
    x=random.randint(1,2)
    if x==1:
        population["Herbe"]+=population["Herbe"]*10/100
        population["Herbe"]=max(0,min(population["Herbe"],env["max herbe"]))
        print("pluie")
    return

# graphique de l'évolution renard lapin avec herbe
def graph_env():
    fichier=open("save.txt", "r")
    nb_lapin=[]
    nb_renard=[]
    herbe=[]
    for i in fichier:
        colonne=i.strip().split()
        nb_lapin.append(int(colonne[1]))
        nb_renard.append(int(colonne[3]))
        herbe.append(round(float(colonne[5])))
    y1=np.array(nb_lapin)
    y2=np.array(nb_renard)
    y3=np.array(herbe)
    

   
    plt.xlabel("generations")
    plt.ylabel("population")
    plt.title("courbe d'évolution des populations de lapin et de renard au fil des générations")

    plt.plot(y1, label="lapin")
    plt.plot(y2, label="renard")
    plt.plot(y3, label="herbe")
    plt.legend()
    return     plt.show()

#graphique naissance et décès  
def graph_ratio(x:int,y:int,esp:str):
    fichier=open("save.txt",'r')
    nc=[]
    dc=[]
    for i in fichier:
        colonne=i.strip().split()
        nc.append(int(colonne[x]))
        dc.append(int(colonne[y]))
    nc_initial = nc.copy()
    dc_initial = dc.copy()

    for x in range(1, len(nc)):
        nc[x] = nc_initial[x] - nc_initial[x-1]
        dc[x] = dc_initial[x] - dc_initial[x-1]

    y1=np.array(nc)
    y2=np.array(dc)

    plt.plot(y1, label="naissance")
    plt.plot(y2, label="décès")
    plt.legend()
    plt.xlabel("générations")
    plt.ylabel("individus")
    plt.title(f"naissance et décès des {esp}")    

    return     plt.show()

# graphique naissance et décès renard
def graph_lap():
    return graph_ratio(11,7,"lapins")

def graph_ren():
    return graph_ratio(13,9,"renards")

# choix du graphique pour finir
def choix_graph():
    end=True
    while end==True:
        graph=input("1.graph ecosystème / 2.graph lapins / 3.graph renards / 4. quitter")
        if graph=="1":
            graph_env()
        if graph=="2":
            graph_lap()
        if graph=="3":
            graph_ren()
        if graph=="4":
            end=False
            return 


def main():
    depart()
    gestion()


    
if __name__=="__main__":
    main()