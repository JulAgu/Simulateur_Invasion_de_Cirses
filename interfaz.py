import tkinter as tk
import tkinter.messagebox as tk_message
from Globals import *
from terreno import terreno
from drone import drone
from counters import countersTerrain
from statistique import statsNum as stat

def lancer():
    '''
    fonction qui est responsable de l'exécution du code où les objets sont créés et leurs méthodes sont appelées 
    à l'intérieur des cycles pour effectuer la simulation.
    '''
    def valider():
        '''fonction pour valider si les informations fournies par l'utilisateur sont adéquates.
        Cette fonction exécute le script en mode graphique ou numérique.
        '''
        global x_parcelle, y_parcelle, jour, mois, droneV, vitesse, lignes, colonnes, jourParMois,saison
        try:
            if value_lar.get() and value_long.get() and value_jour.get() and value_mois.get():
                x_parcelle = value_lar.get()*100
                y_parcelle = value_long.get()*100
                lignes = int(y_parcelle / UNITE_MESURE)
                colonnes = int(x_parcelle / UNITE_MESURE)
                jourParMois = [31, 28, 31, 30, 31, 30, 31, 30, 31, 30, 31, 30]
                if 0 < value_mois.get() <= 12 and jourParMois[value_mois.get()-1]>= value_jour.get() > 0:
                        jour = value_jour.get()
                        mois = value_mois.get()
                        droneV = value_drone.get()
                        vitesse = int(value_vitesse.get())
                        simulation = value_simulation.get()
                else:
                    tk_message.showerror("Error :", "Entrez une date valide !")
            else:
                tk_message.showerror("Error :", "Inserez au moins la date !")
        except:
            tk_message.showerror("Error :", "Les informations données ne sont pas valides")

        if simulation == "graphique":
            graphique()
        elif simulation == "numerique":
            numerique()
    
    def calculerSeasonReproductifNormal():
        '''
        Fonction chargée de calculer le jour et le mois réels en fonction de la date fournie par l'utilisateur. 
        Renvoie un booléen, positif si c'est la saison de reproduction normale
        '''
        global mois,jourReel
        if jourReel == jourParMois[mois-1] and mois + 1 > 12:
            mois = 1
            jourReel = 1
        elif jourReel == jourParMois[mois-1] :
            mois += 1
            jourReel = 1
        jourReel += 1

        if 10 > mois >= 4:
            return True
        else:
            return False



    def graphique():
        '''
        Fonction chargée d'exécuter la simulation graphique
        '''
        SimGraph= tk.Toplevel(fenetre)
        canvas = tk.Canvas(SimGraph, width = x_parcelle, height = y_parcelle+Y_INFOS)
        SimGraph.title("Simulation graphique")
        
        #Creation des menus
        menu1 = tk.Menu()
        menu1.add_command(label="Quitter", command=SimGraph.destroy)
        SimGraph.config(menu=menu1)

        ####### LABELS INFORMATIVES #########
        div = x_parcelle/5

        etiqueta1 = tk.Label(SimGraph, text="Jours", font = "Helvetica 10")
        etiqueta1.place (x=div/2, y = y_parcelle + 10)
        etiqueta2 = tk.Label(SimGraph, text="Vivantes", font = "Helvetica 10")
        etiqueta2.place (x=div/2 + div, y = y_parcelle + 10)
        etiqueta3 = tk.Label(SimGraph, text="Détectés", font = "Helvetica 10")
        etiqueta3.place (x=div/2 + div*2, y = y_parcelle + 10)
        etiqueta4 = tk.Label(SimGraph, text="Supprimés", font = "Helvetica 10")
        etiqueta4.place (x=div/2 + div*3, y = y_parcelle + 10)

        #########################################################
        def impression():
            global j, t, SeasonRedroductifNormal
            if droneV == "oui":
                if parcela.parcelleSaine():
                    SimGraph.after(5,impression)
                    if t % dron.vitesseRelative == 0 or t == 0:
                        j = int(t/dron.vitesseRelative)
                        SeasonRedroductifNormal = calculerSeasonReproductifNormal()
                        parcela.reproduction(SeasonRedroductifNormal)
                        counter1.counter(parcela)
                        etiqueta1.config(text=f'Jour : {j}')
                        etiqueta2.config(text=f'Vivantes : {int(counter1.cirsesvivantes)}')
                        etiqueta3.config(text=f'Détectés : {int(counter1.cirsesdetectes)}')
                        etiqueta4.config(text=f'Supprimés Acu. : {int(dron.counterelimination + dron2.counterelimination)}')
                        counter1.counterReset()
                    dron.deplacementHorizontal(parcela,SeasonRedroductifNormal)
                    dron2.deplacementVertical(parcela,SeasonRedroductifNormal)      
                    t += 1
            else:
                if parcela.parcelleSaine():
                    SimGraph.after(30,impression)
                    SeasonRedroductifNormal = calculerSeasonReproductifNormal()
                    parcela.reproduction(SeasonRedroductifNormal)
                    counter1.counter(parcela)
                    etiqueta1.config(text=f'Jour : {int(j)}')
                    etiqueta2.config(text=f'Vivantes : {int(counter1.cirsesvivantes)}')
                    counter1.counterReset()
                    j += 1

        # Declaration des objets
        global j, t, jourReel, SeasonRedroductifNormal
        parcela = terreno(canvas,lignes,colonnes,True)
        parcela.premierPlante()
        if droneV == "oui":
            dron = drone(parcela,vitesse,canvas,True)
            dron2 = drone(parcela,vitesse,canvas,True)
        counter1 = countersTerrain()
        # Initialisation des variables globales
        j = 0
        t = 0
        jourReel = jour
        SeasonRedroductifNormal = calculerSeasonReproductifNormal()
        impression()
        
        canvas.pack()
        canvas.mainloop()

    def numerique():
        '''
        fonction responsable de l'exécution de la simulation numérique
        '''
        global jourReel
        NumGraph= tk.Toplevel(fenetre)
        canvas = tk.Canvas(NumGraph, width = 700, height = 500)
        NumGraph.title("Simulation numerique")

        #Title de l'informe statistique
        etiqueta1 = tk.Label(NumGraph, text = "Quelques statistiques de votre simulation", font = "Helvetica 12 bold",foreground = "blue")
        etiqueta1.place (x=220, y = 20)

        # Creation des menus
        menu1 = tk.Menu()
        menu1.add_command(label = "Quitter", command = NumGraph.destroy)
        NumGraph.config(menu=menu1)

        ############### Simulation en utilisants les instances des clases et ses attributes ##############
        st = stat()
        rep = 0
        dronGagne = 0
        for i in range(50):
            parcela = terreno(canvas,lignes,colonnes,False)
            parcela.premierPlante()
            if droneV == "oui":
                dron = drone(parcela,vitesse,canvas,False)
                dron2 = drone(parcela,vitesse,canvas,False)
            counter1 = countersTerrain()
            rep +=1
            jours = 0
            jourReel = 1
            while parcela.parcelleSaine() and jours <= 360:
                st.J.append(jours)
                st.N_rep.append(rep)

                if droneV == "oui":
                    SeasonRedroductifNormal = calculerSeasonReproductifNormal()
                    parcela.reproduction(SeasonRedroductifNormal)
                    for i in range(dron.vitesseRelative):
                        dron.deplacementHorizontal(parcela,SeasonRedroductifNormal)
                        dron2.deplacementVertical(parcela,SeasonRedroductifNormal)
                    counter1.counter(parcela)

                    st.P_act.append(counter1.cirsesvivantes)
                    st.P_acc.append(parcela.plantesAcc)
                    st.D_act.append(counter1.cirsesdetectes)
                    st.D_acc.append(dron.counterdetection + dron2.counterdetection)
                    st.E_a.append(dron.counterelimination + dron2.counterelimination)

                    counter1.counterReset()

                    jours += 1

                else:
                    SeasonRedroductifNormal = calculerSeasonReproductifNormal()
                    parcela.reproduction(SeasonRedroductifNormal)
                    counter1.counter(parcela)

                    st.P_act.append(counter1.cirsesvivantes)
                    st.P_acc.append(parcela.plantesAcc)

                    counter1.counterReset()

                    jours += 1

                if jours == 100:
                    dronGagne += 1


        # Execution des fonctionnes statistiques
        st.creerDF(droneV)
        st.statsMaxJours(droneV)
        st.histograms(droneV)


        etiqueta2 = tk.Label(NumGraph, text = r"Jour où les cirses ont envahi plus de 95 % de votre parcelle :", font = "Helvetica 11 bold")
        etiqueta2.place (x=30, y = 60)

        etiqueta3 = tk.Label(NumGraph, text = f'Max : {st.Jmax}', font = "Helvetica 11")
        etiqueta3.place (x=30, y = 80)

        etiqueta4 = tk.Label(NumGraph, text = f'Min : {st.Jmin}', font = "Helvetica 11")
        etiqueta4.place (x=30, y = 100)

        etiqueta5 = tk.Label(NumGraph, text = f'Jour moyenne : {"%.3f" % st.Jmean}', font = "Helvetica 11")
        etiqueta5.place (x=30, y = 120)

        etiqueta6 = tk.Label(NumGraph, text = f'Jour écart-type : {"%.3f" % st.Jstd}', font = "Helvetica 11")
        etiqueta6.place (x=30, y = 140)

        etiqueta7 = tk.Label(NumGraph, text = r"Quantité de plantes accumulées :", font = "Helvetica 11 bold")
        etiqueta7.place (x=30, y = 160)

        etiqueta8 = tk.Label(NumGraph, text = f'Max : {st.PcumMax}', font = "Helvetica 11")
        etiqueta8.place (x=30, y = 180)

        etiqueta9 = tk.Label(NumGraph, text = f'Min : {st.PcumMin}', font = "Helvetica 11")
        etiqueta9.place (x=30, y = 200)

        etiqueta10 = tk.Label(NumGraph, text = f'Moyenne : {"%.3f" % st.PcumMean}', font = "Helvetica 11")
        etiqueta10.place (x=30, y = 220)

        etiqueta11 = tk.Label(NumGraph, text = f'Jour écart-type : {"%.3f" % st.PcumStd}', font = "Helvetica 11")
        etiqueta11.place (x=30, y = 240)

        if droneV == "oui":

            etiqueta17 = tk.Label(NumGraph, text = r"Détections cumulées : ", font = "Helvetica 11 bold")
            etiqueta17.place (x=30, y = 260)

            etiqueta18 = tk.Label(NumGraph, text = f'Max : {st.DcumMax}', font = "Helvetica 11")
            etiqueta18.place (x=30, y = 280)

            etiqueta19 = tk.Label(NumGraph, text = f'Min : {st.DcumMin}', font = "Helvetica 11")
            etiqueta19.place (x=30, y = 300)

            etiqueta20 = tk.Label(NumGraph, text = f'Moyenne : {"%.3f" % st.DcumMean}', font = "Helvetica 11")
            etiqueta20.place (x=30, y = 320)

            etiqueta21 = tk.Label(NumGraph, text = f'Écart-type : {"%.3f" % st.DcumStd}', font = "Helvetica 11")
            etiqueta21.place (x=30, y = 340)

            etiqueta22 = tk.Label(NumGraph, text = r"Éliminations cumulées : ", font = "Helvetica 11 bold")
            etiqueta22.place (x=30, y = 360)

            etiqueta23 = tk.Label(NumGraph, text = f'Max : {st.EcumMax}', font = "Helvetica 11")
            etiqueta23.place (x=30, y = 380)

            etiqueta24 = tk.Label(NumGraph, text = f'Min : {st.EcumMin}', font = "Helvetica 11")
            etiqueta24.place (x=30, y = 400)

            etiqueta25 = tk.Label(NumGraph, text = f'Moyenne : {"%.3f" % st.EcumMean}', font = "Helvetica 11")
            etiqueta25.place (x=30, y = 420)

            etiqueta26 = tk.Label(NumGraph, text = f'Écart-type : {"%.3f" % st.EcumStd}', font = "Helvetica 11")
            etiqueta26.place (x=30, y = 440)

            etiqueta27 = tk.Label(NumGraph, text = f'Les drones ont "gagné" : {dronGagne} fois en {50} reptitions, cad {"%.1f" % ((dronGagne/50)*100)} %', font = "Helvetica 11 bold", foreground = "red")
            etiqueta27.place (x=150, y = 460)

        canvas.pack()
        canvas.mainloop()

    ################################################################################################
    ##################################### MAIN WINDOW ##############################################
    ################################################################################################
    fenetre = tk.Tk()
    fenetre.geometry("700x750")
    fenetre.state("zoomed")
    fenetre.title("Simulateur d'invasion de cirses")

    # MENUS
    menu1 = tk.Menu()
    menu1.add_command(label = "Quitter", command = fenetre.destroy)
    fenetre.config(menu=menu1)

    # TITRE

    Frame1 = tk.Frame(fenetre, bg="green", height=70, width=600)
    Frame1.pack(side= "top")
    tk.Label(Frame1, text="Invasion de Cirses", font= "Helveltica 18 bold", bg='green').pack(padx=220, pady=35)

    # Insertion de la taille du champs
    label = tk.Label(fenetre, text = "Quelle est la taille de votre champs :", font = ("Helvetica"))
    label.pack()
    value_lar = tk.IntVar()
    scale = tk.Scale(fenetre, variable=value_lar, orient='horizontal', from_ = 5, to = 12,
        resolution = 1, tickinterval = 1, length = 350,
        label='Largeur (x100) :')
    scale.pack()
    value_long = tk.IntVar()
    scale = tk.Scale(fenetre, variable=value_long, orient='horizontal', from_ = 3, to = 6,
        resolution = 1, tickinterval = 1, length = 350,
        label='Longeur (x100) :')
    scale.pack()

    # Insertion du jour et mois
    label = tk.Label(fenetre, text="Dans quelle jour vous avez noté la premier \n infestation par cirse ?", font="Helvetica")
    label.pack()
    label = tk.Label(fenetre, text="Jour :")
    label.pack()
    value_jour = tk.IntVar(value = 1)
    entree = tk.Entry(fenetre, textvariable=value_jour, width=30)
    entree.pack()
    label = tk.Label(fenetre, text="Mois :")
    label.pack()
    value_mois = tk.IntVar(value = 1)
    entree = tk.Entry(fenetre, textvariable=value_mois, width=30)
    entree.pack()

    # Insertion du drone
    label = tk.Label(fenetre, text="Voulez-vouz faire une analyse d'infestation \n par image de drone et controle par herbicide ?", font= "Helvetica")
    label.pack()
    value_drone = tk.StringVar() 
    bouton1 = tk.Radiobutton(fenetre, text="Oui", variable=value_drone, value = "oui")
    bouton2 = tk.Radiobutton(fenetre, text="Non", variable=value_drone, value = "non")
    bouton1.select()
    bouton1.pack()
    bouton2.pack()

    # Vitesse du drone
    label = tk.Label(fenetre, text= "Le drone va-t-il passer a quelle vitesse ?", font = "Helvetica")
    label.pack()
    value_vitesse = tk.IntVar()
    scale = tk.Scale(fenetre, variable=value_vitesse, orient='horizontal', from_=1, to=3,
        resolution=1, tickinterval=1, length=350,
        label='vitesse du drone :')
    scale.pack()

    # Simulation graphique ou numerique?
    label = tk.Label(fenetre, text="Ici vous pouvez choisir soit une simulation \n grafique soit numerique :", font= "Helvetica")
    label.pack()
    value_simulation = tk.StringVar() 
    bouton1 = tk.Radiobutton(fenetre, text="Simulation graphique", variable=value_simulation, value='graphique')
    bouton2 = tk.Radiobutton(fenetre, text="Simulation numerique", variable=value_simulation, value='numerique')
    bouton1.select()
    bouton1.pack()
    bouton2.pack()

    button_valider = tk.Button(fenetre, text="Valider", command=valider)
    button_valider.pack()

    fenetre.mainloop()