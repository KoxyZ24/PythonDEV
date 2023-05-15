import tkinter as tk
from tkinter import ttk
import random
import threading
import socket
import sqlite3




class Server:
    def __init__(self, port):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(2)
        self.thread_accept_client = threading.Thread(target=self.accept_client)
        self.thread_accept_client.start()

    def accept_client(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f'Client {address} connected.')

            if len(self.clients) == 2:
                threading.Thread(target=self.start_game).start()

    def start_game(self):
        self.clients[0].send(b'start')
        self.clients[1].send(b'start')
        while True:
            choix_joueur1 = self.clients[0].recv(1024).decode('utf-8')
            choix_joueur2 = self.clients[1].recv(1024).decode('utf-8')
            if choix_joueur1 == '' or choix_joueur2 == '':
                break
            resultat_manche = self.jouer_manche(choix_joueur1, choix_joueur2)
            self.clients[0].send(resultat_manche.encode('utf-8'))
            self.clients[1].send(resultat_manche.encode('utf-8'))
        self.clients[0].close()
        self.clients[1].close()
        self.clients = []
        print('Game finished.')

    @staticmethod
    def jouer_manche(choix_joueur1, choix_joueur2):
        if choix_joueur1 == choix_joueur2:
            return 'Egalité'
        elif choix_joueur1 == 'Pierre':
            if choix_joueur2 == 'Feuille':
                return 'Joueur 2 gagne'
            else:
                return 'Joueur 1 gagne'
        elif choix_joueur1 == 'Feuille':
            if choix_joueur2 == 'Ciseaux':
                return 'Joueur 2 gagne'
            else:
                return 'Joueur 1 gagne'
        elif choix_joueur1 == 'Ciseaux':
            if choix_joueur2 == 'Pierre':
                return 'Joueur 2 gagne'
            else:
                return 'Joueur 1 gagne'


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Pierre-Feuille-Ciseaux')
        self.root.resizable(False, False)
        self.numero_manche = 0
        self.nb_manche = 0
        self.nb_manche_gagnante = 0
        self.nb_victoires_joueur1 = 0
        self.nb_defaites_joueur1 = 0
        self.nb_victoires_joueur2 = 0
        self.nb_defaites_joueur2 = 0
        self.choix_joueur1 = None
        self.choix_joueur2 = None
        self.server = None

        self.label_titre = tk.Label(self.root, text='Pierre-Feuille-Ciseaux', font=('Arial', 24))
        self.label_titre.grid(row=0, column=0, columnspan=3, pady=10)

        self.frame_manche = ttk.Frame(self.root)
        self.frame_manche.grid(row=1, column=0, pady=10)

        self.label_manche = tk.Label(self.frame_manche, text='Manche 0 / 0', font=('Arial', 16))
        self.label_manche.grid(row=0, column=0, pady=5)

        self.label_choix_joueur1 = tk.Label(self.frame_manche, text='Joueur 1 : ', font=('Arial', 14))
        self.label_choix_joueur1.grid(row=1, column=0, pady=5)
        self.label_choix_joueur1_valeur = tk.Label(self.frame_manche, text='-', font=('Arial', 14))
        self.label_choix_joueur1_valeur.grid(row=1, column=1, pady=5)

        self.label_choix_joueur2 = tk.Label(self.frame_manche, text='Joueur 2 : ', font=('Arial', 14))
        self.label_choix_joueur2.grid(row=2, column=0, pady=5)
        self.label_choix_joueur2_valeur = tk.Label(self.frame_manche, text='-', font=('Arial', 14))
        self.label_choix_joueur2_valeur.grid(row=2, column=1, pady=5)

        self.frame_choix = ttk.Frame(self.root)
        self.frame_choix.grid(row=1, column=1, pady=10)

        self.label_choix = tk.Label(self.frame_choix, text='Choix', font=('Arial', 16))
        self.label_choix.grid(row=0, column=0, columnspan=3, pady=5)

        self.bouton_pierre = tk.Button(self.frame_choix, text='Pierre', font=('Arial', 14), command=lambda: self.choix('Pierre'))
        self.bouton_pierre.grid(row=1, column=0, padx=5, pady=5)

        self.bouton_feuille = tk.Button(self.frame_choix, text='Feuille', font=('Arial', 14), command=lambda: self.choix('Feuille'))
        self.bouton_feuille.grid(row=1, column=1, padx=5, pady=5)

        self.bouton_ciseaux = tk.Button(self.frame_choix, text='Ciseaux', font=('Arial', 14), command=lambda: self.choix('Ciseaux'))
        self.bouton_ciseaux.grid(row=1, column=2, padx=5, pady=5)

        self.frame_score = ttk.Frame(self.root)
        self.frame_score.grid(row=2, column=0, columnspan=2, pady=10)

        self.label_score = tk.Label(self.frame_score, text='Score', font=('Arial', 16))
        self.label_score.grid(row=0, column=0, columnspan=3, pady=5)

        self.label_joueur1 = tk.Label(self.frame_score, text='Joueur 1', font=('Arial', 14))
        self.label_joueur1.grid(row=1, column=0, padx=10, pady=5)
        self.label_joueur1_victoires = tk.Label(self.frame_score, text='0', font=('Arial', 14))
        self.label_joueur1_victoires.grid(row=2, column=0, padx=10, pady=5)
        self.label_joueur1_defaites = tk.Label(self.frame_score, text='0', font=('Arial', 14))
        self.label_joueur1_defaites.grid(row=3, column=0, padx=10, pady=5)

        self.label_joueur2 = tk.Label(self.frame_score, text='Joueur 2', font=('Arial', 14))
        self.label_joueur2.grid(row=1, column=2, padx=10, pady=5)
        self.label_joueur2_victoires = tk.Label(self.frame_score, text='0', font=('Arial', 14))
        self.label_joueur2_victoires.grid(row=2, column=2, padx=10, pady=5)
        self.label_joueur2_defaites = tk.Label(self.frame_score, text='0', font=('Arial', 14))
        self.label_joueur2_defaites.grid(row=3, column=2, padx=10, pady=5)

        self.bouton_quitter = tk.Button(self.root, text='Quitter', font=('Arial', 16), command=self.root.quit)
        self.bouton_quitter.grid(row=3, column=0, pady=10)

        self.root.protocol('WM_DELETE_WINDOW', self.quitter)

    def choix(self, choix_joueur1):
        self.choix_joueur1 = choix_joueur1
        self.label_choix_joueur1_valeur.configure(text=self.choix_joueur1)
        self.choix_joueur2 = random.choice(['Pierre', 'Feuille', 'Ciseaux'])
        self.label_choix_joueur2_valeur.configure(text=self.choix_joueur2)
        self.numero_manche += 1
        self.label_manche.configure(text=f'Manche {self.numero_manche} / {self.nb_manche}')
        self.verifier_gagnant()

    def verifier_gagnant(self):
        if self.choix_joueur1 == self.choix_joueur2:
            self.message.set('Égalité !')
            self.ajouter_resultat(self.nom_joueur1, 'Nul')
            self.ajouter_resultat(self.nom_joueur2, 'Nul')
        elif (self.choix_joueur1 == 'Pierre' and self.choix_joueur2 == 'Ciseaux') or \
                (self.choix_joueur1 == 'Feuille' and self.choix_joueur2 == 'Pierre') or \
                (self.choix_joueur1 == 'Ciseaux' and self.choix_joueur2 == 'Feuille'):
            self.victoires_joueur1 += 1
            self.message.set('Le joueur 1 gagne cette manche !')
            self.ajouter_resultat(self.nom_joueur1, 'Victoire')
            self.ajouter_resultat(self.nom_joueur2, 'Défaite')
        else:
            self.victoires_joueur2 += 1
            self.message.set('Le joueur 2 gagne cette manche !')
            self.ajouter_resultat(self.nom_joueur1, 'Défaite')
            self.ajouter_resultat(self.nom_joueur2, 'Victoire')

        self.mises_a_jour_score()

        if self.victoires_joueur1 == self.manche_gagnante:
            self.fin_partie(self.nom_joueur1)
        elif self.victoires_joueur2 == self.manche_gagnante:
            self.fin_partie(self.nom_joueur2)
        else:
            self.reset_choix()
            self.message.set('Manche suivante !')

    def quitter(self):
        self.bdd.commit()
        self.bdd.close()
        self.root.quit()

    def maj_resultat_bdd(self, nom_joueur_gagnant):
        with sqlite3.connect('resultats.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE resultats SET nb_victoires = nb_victoires + 1 WHERE nom_joueur = ?',
                      (nom_joueur_gagnant,))
            c.execute('SELECT nb_victoires FROM resultats WHERE nom_joueur = ?', (nom_joueur_gagnant,))
            nb_victoires = c.fetchone()[0]
            c.execute('UPDATE resultats SET nb_parties_jouees = nb_parties_jouees + 1 WHERE nom_joueur = ?',
                      (nom_joueur_gagnant,))
            c.execute('SELECT nb_parties_jouees FROM resultats WHERE nom_joueur = ?', (nom_joueur_gagnant,))
            nb_parties_jouees = c.fetchone()[0]
        return nb_victoires, nb_parties_jouees

    def lancer_matchmaking(self):
        self.nb_manche_gagnante = int(self.spin_manche.get())
        self.nb_manche = int(self.spin_manche_totale.get())
        self.label_manche.configure(text=f'Manche 1 / {self.nb_manche}')

        self.frame_matchmaking = ttk.Frame(self.root)
        self.frame_matchmaking.grid(row=0, column=0, columnspan=2)

        self.label_recherche = tk.Label(self.frame_matchmaking, text='Recherche de match...', font=('Arial', 16))
        self.label_recherche.pack(pady=10)

        self.bouton_annuler = tk.Button(self.frame_matchmaking, text='Annuler', font=('Arial', 14), command=self.annuler_matchmaking)
        self.bouton_annuler.pack(pady=10)

        self.root.after(5000, self.trouver_adversaire)

    def trouver_adversaire(self):
        self.label_recherche.configure(text='Match trouvé !')
        self.bouton_annuler.configure(text='Quitter la partie', command=self.quitter_matchmaking)
        self.creer_interface_jeu()

    def annuler_matchmaking(self):
        self.frame_matchmaking.destroy()
        self.root.after_cancel(self.trouver_adversaire)

    def quitter_matchmaking(self):
        self.frame_matchmaking.destroy()
        self.creer_interface_accueil()

    def creer_interface_jeu(self):
        self.frame_choix = tk.Frame(self.root)
        self.frame_choix.pack()

        self.label_choix_joueur1 = tk.Label(self.frame_choix, text='Joueur 1, choisissez votre arme :',
                                            font=('Arial', 16))
        self.label_choix_joueur1.grid(row=0, column=0, padx=20, pady=20)

        self.bouton_pierre = tk.Button(self.frame_choix, text='Pierre', font=('Arial', 14),
                                       command=lambda: self.choix('Pierre'))
        self.bouton_pierre.grid(row=1, column=0, padx=10, pady=10)

        self.bouton_feuille = tk.Button(self.frame_choix, text='Feuille', font=('Arial', 14),
                                        command=lambda: self.choix('Feuille'))
        self.bouton_feuille.grid(row=1, column=1, padx=10, pady=10)

        self.bouton_ciseaux = tk.Button(self.frame_choix, text='Ciseaux', font=('Arial', 14),
                                        command=lambda: self.choix('Ciseaux'))
        self.bouton_ciseaux.grid(row=1, column=2, padx=10, pady=10)

        self.frame_resultat = tk.Frame(self.root)
        self.frame_resultat.pack()

        self.label_resultat = tk.Label(self.frame_resultat, text='', font=('Arial', 16))
        self.label_resultat.grid(row=0, column=0, padx=20, pady=20)

        self.bouton_quitter = tk.Button(self.frame_resultat, text='Quitter', font=('Arial', 14),
                                        command=self.quitter_jeu)
        self.bouton_quitter.grid(row=1, column=0, padx=10, pady=10)

        self.frame_attente = tk.Frame(self.root)
        self.label_attente = tk.Label(self.frame_attente, text='En attente d\'un adversaire...', font=('Arial', 16))
        self.label_attente.pack(padx=20, pady=20)

        self.frame_choix.pack_forget()
        self.frame_resultat.pack_forget()
        self.frame_attente.pack_forget()

    def creer_interface_jeu(self):
        self.frame_matchmaking.destroy()
        self.frame_choix.pack(padx=10, pady=10)

        self.label_joueur1 = tk.Label(self.frame_choix, text='Joueur 1', font=('Arial', 16))
        self.label_joueur1.grid(row=0, column=0)

        self.label_joueur2 = tk.Label(self.frame_choix, text='Joueur 2', font=('Arial', 16))
        self.label_joueur2.grid(row=0, column=2)

        self.canvas_joueur1 = tk.Canvas(self.frame_choix, width=100, height=100)
        self.canvas_joueur1.grid(row=1, column=0, pady=10)
        self.canvas_joueur2 = tk.Canvas(self.frame_choix, width=100, height=100)
        self.canvas_joueur2.grid(row=1, column=2, pady=10)

        self.label_joueur1_victoires = tk.Label(self.frame_choix, text='0', font=('Arial', 16))
        self.label_joueur1_victoires.grid(row=2, column=0)
        self.label_joueur1_defaites = tk.Label(self.frame_choix, text='0', font=('Arial', 16))
        self.label_joueur1_defaites.grid(row=3, column=0)
        self.label_joueur2_victoires = tk.Label(self.frame_choix, text='0', font=('Arial', 16))
        self.label_joueur2_victoires.grid(row=2, column=2)
        self.label_joueur2_defaites = tk.Label(self.frame_choix, text='0', font=('Arial', 16))
        self.label_joueur2_defaites.grid(row=3, column=2)

        self.label_manche = tk.Label(self.frame_choix, text='', font=('Arial', 16))
        self.label_manche.grid(row=4, column=1, pady=20)

        self.canvas_joueur1.create_text(50, 50, text='?', font=('Arial', 36))
        self.canvas_joueur2.create_text(50, 50, text='?', font=('Arial', 36))

        self.choix_joueur1 = ''
        self.choix_joueur2 = ''

    def choix(self, choix_joueur1):
        self.choix_joueur1 = choix_joueur1
        self.canvas_joueur1.delete('all')
        if choix_joueur1 == 'Pierre':
            self.canvas_joueur1.create_oval(10, 10, 90, 90)
        elif choix_joueur1 == 'Feuille':
            self.canvas_joueur1.create_rectangle(10, 10, 90, 90)
        elif choix_joueur1 == 'Ciseaux':
            self.canvas_joueur1.create_polygon(10, 50, 50, 10, 90, 50, 50, 90)

        if self.choix_joueur2 != '':
            self.verifier_gagnant()


def verifier_gagnant(self):
    if self.choix_joueur1 == self.choix_joueur2:
        self.message.set('Égalité !')
    elif self.choix_joueur1 == 'Pierre' and self.choix_joueur2 == 'Ciseaux':
        self.victoires_joueur1 += 1
        self.message.set('Le joueur 1 gagne cette manche !')
    elif self.choix_joueur1 == 'Feuille' and self.choix_joueur2 == 'Pierre':
        self.victoires_joueur1 += 1
        self.message.set('Le joueur 1 gagne cette manche !')
    elif self.choix_joueur1 == 'Ciseaux' and self.choix_joueur2 == 'Feuille':
        self.victoires_joueur1 += 1
        self.message.set('Le joueur 1 gagne cette manche !')
    else:
        self.victoires_joueur2 += 1
        self.message.set('Le joueur 2 gagne cette manche !')

    self.mises_a_jour_score()

    if self.victoires_joueur1 == self.manche_gagnante:
        self.fin_partie('Joueur 1')
    elif self.victoires_joueur2 == self.manche_gagnante:
        self.fin_partie('Joueur 2')
    else:
        self.reset_choix()
        self.message.set('Manche suivante !')
