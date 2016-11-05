; habiter(nationalite(Anglais),couleur(rouge))
(nationalite Anglais)
(couleur rouge)
(habiter NationaliteAnglais CouleurRouge)

; avoir(nationalite(Suedois),animal(chien))
(nationalite Suedois)
(animal chien)
(avoir NationaliteSuedois AnimalChien)

; boire(nationalite(Danois),the)
(nationalite Danois)
(boire NationaliteDanois the)

; a_gauche(couleur(vert),couleur(blanc))
(couleur vert)
(couleur blanc)
(a_gauche CouleurVert CouleurBlanc)

; boire(couleur(vert),cafe)
(couleur vert)
(boire CouleurVert cafe)

; fumer(\x.avoir(x,animal(oiseau)),Pall_Mall)
(animal oiseau)
(avoir personne0 AnimalOiseau)
(fumer AvoirPersonne0Animaloiseau Pall_Mall)

; fumer(couleur(jaune),Dunhill)
(couleur jaune)
(fumer CouleurJaune Dunhill)

; habiter(\x.boire(x,jus_d_orange),position(3))
(boire personne0 jus_d_orange)
(position 3)
(habiter BoirePersonne0Jus_D_Orange Position3)

; (habiter(nationalite(Norvegien),position(1)) & habiter(?np2,a_cote(couleur(bleu))))
; habiter(nationalite(Norvegien),position(1)) 
(nationalite Norvegien)
(position 1)
(habiter NationaliteNorvegien Position1)

;  habiter(?np2,a_cote(couleur(bleu)))
(couleur bleu)
(a_cote CouleurBleu)
(habiter NationaliteNorvegien A_CoteCouleurbleu)

(nationalite Norvegien)
(position 1)
(couleur bleu)
(habiter NationaliteNorvegien Position1)
(a_cote CouleurBleu)

; fumer(\s.habiter(s,a_cote(\x.avoir(x,animal(chat)))),Blend)
(animal chat)
(avoir personne1 AnimalChat)
(a_cote AvoirPersonne1Animalchat)
(habiter personne0 A_CoteAvoirpersonne1Animalchat)
(fumer HabiterPersonne0A_Coteavoirpersonne1Animalchat Blend)

; avoir(a_cote(\x.fumer(x,Dunhill)),animal(cheval))
(fumer personne0 Dunhill)
(animal cheval)
(a_cote FumerPersonne0Dunhill)
(avoir A_CoteFumerpersonne0Dunhill AnimalCheval)

; fumer(\x.boire(x,biere),Blue_Master)
(boire personne0 biere)
(fumer BoirePersonne0Biere Blue_Master)

; fumer(nationalite(Allemand),Prince)
(nationalite Allemand)
(fumer NationaliteAllemand Prince)

; fumer(\x.avoir(x,a_cote(\x.boire(x,eau))),Blend)
(boire personne0 eau)
(a_cote BoirePersonne0Eau)
(avoir personne0 A_CoteBoirepersonne0Eau)
(fumer AvoirPersonne0A_Coteboirepersonne0Eau Blend)

