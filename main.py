import pygame
import sys
import time
import copy
import statistics

ADANCIME_MAX = 2

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """

    JMIN = None
    JMAX = None
    CULOARE_X = (77, 162, 232)
    CULOARE_ZERO = (232, 144, 77)
    GOL = "#"
    NR_LINII = None
    NR_COLOANE = None
    scor_maxim = 0

    def __init__(self, matr=None, cutii=None):
        self.ultima_mutare = None

        if matr:
            # e data tabla, deci suntem in timpul jocului
            self.matr = matr

        else:
            # nu e data tabla deci suntem la initializare
            self.matr = [Joc.GOL for _ in range((Joc.NR_LINII * (Joc.NR_COLOANE - 1)) + (Joc.NR_COLOANE * (Joc.NR_LINII - 1)))]

        self.scor_x = 0
        self.scor_zero = 0
        if cutii:
            # e data tabla, deci suntem in timpul jocului
            self.cutii = cutii
            
            puncte_list = [(i for i in line) for line in self.cutii]

            for p in puncte_list:
                if p != Joc.GOL:
                    if p == "x":
                        self.scor_x += 1
                    elif p == "0":
                        self.scor_zero += 1
        else:
            # nu e data tabla deci suntem la initializare
            self.cutii = [
                [self.__class__.GOL] * (self.__class__.NR_COLOANE - 1)
                for _ in range(self.__class__.NR_LINII - 1)
            ]
        



    @classmethod
    def initializeaza(cls, display, NR_LINII=6, NR_COLOANE=7, dim_celula=100):
        cls.NR_LINII = NR_LINII
        cls.NR_COLOANE = NR_COLOANE

        ######## calculare scor maxim ###########
        if cls.scor_maxim == 0:
            cls.scor_maxim = (cls.NR_LINII - 1) * (cls.NR_COLOANE - 1)

        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load("ics.png")
        cls.x_img = pygame.transform.scale(cls.x_img, (int(dim_celula * 0.8), int(dim_celula * 0.8)))
        cls.zero_img = pygame.image.load("zero.png")
        cls.zero_img = pygame.transform.scale(cls.zero_img, (int(dim_celula * 0.8), int(dim_celula * 0.8)))
        cls.linii = []  # este lista cu linii de pe tabla
        for linie in range(NR_LINII):
            for coloana in range(NR_COLOANE):
                if coloana < cls.NR_COLOANE - 1:
                    patr = pygame.Rect( # linie orizontala
                        dim_celula // 2 + cls.dim_celula * coloana + 5,
                        dim_celula // 2 + cls.dim_celula * linie - 5,
                        dim_celula - 10,
                        10,
                    )
                    cls.linii.append(patr)

                if linie < cls.NR_LINII - 1:
                    patr = pygame.Rect( # linie verticala
                        dim_celula // 2 + cls.dim_celula * coloana - 5,
                        dim_celula // 2 + cls.dim_celula * linie + 5,
                        10,
                        dim_celula - 10,
                    )
                    cls.linii.append(patr)
    
    def deseneaza_grid(self, stare=None):

        def get_which_image(line, column):
            """Determina ce imagine ar trebui afisata in cutie

            Args:
                line (int): linia deasupra cutiei
                column (int): coloana la stanga cutiei
            """
            if self.cutii[line][column] == Joc.GOL:
                return None
            else:
                return Joc.x_img if self.cutii[line][column] == "x" else Joc.zero_img
                


        black = (0, 0, 0)
        mid = 255 // 1.5
        gray = (mid, mid, mid)

        self.__class__.display.fill((255, 255, 255))

        for linie in range(len(Joc.linii)):
            if self.matr[linie] != Joc.GOL:
                if linie == self.ultima_mutare and stare is not None:
                    pygame.draw.rect(self.__class__.display,
                                 color=Joc.CULOARE_X if stare.j_curent == "x" else Joc.CULOARE_ZERO,
                                 rect=Joc.linii[linie])
                else:
                    pygame.draw.rect(self.__class__.display,
                                    color=black,
                                    rect=Joc.linii[linie])
            else:
                pygame.draw.rect(self.__class__.display,
                                 color=gray,
                                 rect=Joc.linii[linie])
                
        

        for linie in range(self.__class__.NR_LINII):
            for coloana in range(self.__class__.NR_COLOANE):
                pygame.draw.circle(self.__class__.display, 
                                   color=black,
                                   center=[self.__class__.dim_celula // 2 + self.__class__.dim_celula * coloana,
                                           self.__class__.dim_celula // 2 + self.__class__.dim_celula * linie],
                                   radius=10)
                
                if linie < self.__class__.NR_LINII - 1 and coloana < self.__class__.NR_COLOANE - 1 and (imagine := get_which_image(linie, coloana)):
                        self.__class__.display.blit(imagine, 
                                                    (self.__class__.dim_celula // 2 + self.__class__.dim_celula * coloana + int(self.__class__.dim_celula * 0.1),
                                                    self.__class__.dim_celula // 2 + self.__class__.dim_celula * linie + int(self.__class__.dim_celula * 0.1)))
        
        display = Joc.display
        font = "arial"
        dimFont = 16
        culoareFont = black

        text_x = "Scor X: " + str(self.scor_x)
        text_zero = "Scor 0: " + str(self.scor_zero)

        fontObj = pygame.font.SysFont(font, dimFont)
        text_x = fontObj.render(text_x, True, culoareFont)
        text_zero = fontObj.render(text_zero, True, culoareFont)

        w, _ = display.get_size()
        dreptunghi_x = text_x.get_rect()
        dreptunghi_zero = text_zero.get_rect()

        dreptunghi_x.topleft = (Joc.dim_celula // 2, Joc.NR_LINII * Joc.dim_celula - int(Joc.dim_celula * (1/4)) - 8)
        dreptunghi_zero.topleft = (Joc.dim_celula // 2, Joc.NR_LINII * Joc.dim_celula - int(Joc.dim_celula * (1/4)) + 16 - 8)

        display.blit(text_x, dreptunghi_x)
        display.blit(text_zero, dreptunghi_zero)
        
        pygame.display.update()

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        if not self.ultima_mutare:  # daca e inainte de prima mutare
            return False
        

        puncte_necesare_schimbare = abs(self.scor_x - self.scor_zero) + 1
        puncte_disponibile = (self.__class__.scor_maxim - (self.scor_zero + self.scor_x))

        if puncte_necesare_schimbare > puncte_disponibile and max(self.scor_x, self.scor_zero) > (self.__class__.scor_maxim // 2): # daca punctele disponibile sunt mai putine decat cele necesare ca sa se schimbe ierarhia, putem sa terminam devreme
            if self.scor_x > self.scor_zero:
                return "x"
            elif self.scor_x < self.scor_zero:
                return "0"
            else:
                return "remiza"
        elif puncte_disponibile == 0:
            if self.scor_x > self.scor_zero:
                return "x"
            elif self.scor_x < self.scor_zero:
                return "0"
            else:
                return "remiza"
        else: # daca mai sunt suficiente puncte disponibile, nu e final
            return False

    def indecsi_contur(self, linie, coloana):
        up = linie * (2 * Joc.NR_COLOANE - 1) + 2 * coloana
        left = up + 1
        if coloana == Joc.NR_COLOANE - 2:
            right = up + 2
        else:
            right = up + 3
        
        if linie == Joc.NR_LINII - 2:
            down = (linie + 1) * (2 * Joc.NR_COLOANE - 1) + coloana
        else:
            down = up + (2 * Joc.NR_COLOANE - 1)

        return up, left, down, right


    def completeaza_cutii(self, jucator):
        """Completeaza cutiile inchise si ajusteaza scorul

        Args:
            jucator (string): simbolul jucatorului
        """

        scor_x = 0
        scor_zero = 0
        for line in range(len(self.cutii)):
            for column in range(len(self.cutii[line])):
                if self.cutii[line][column] == Joc.GOL: # Daca cutia nu e Joc.GOL, a fost deja inchisa. Nu mai verificam

                    up, left, down, right = self.indecsi_contur(line, column)      

                    if self.matr[up] != Joc.GOL and self.matr[down] != Joc.GOL and self.matr[left] != Joc.GOL and self.matr[right] != Joc.GOL:
                        self.cutii[line][column] = jucator

                if self.cutii[line][column] == "x":
                    scor_x += 1
                elif self.cutii[line][column] == "0":
                    scor_zero += 1
        
        self.scor_x = scor_x
        self.scor_zero = scor_zero

    def mutari(self, jucator):
        l_mutari = []
        for line_index in range(len(self.matr)):
            if self.matr[line_index] == self.__class__.GOL:
                matr_copy = copy.deepcopy(self.matr)
                matr_copy[line_index] = jucator

                cutii_copy = copy.deepcopy(self.cutii)

                joc_nou = Joc(matr_copy, cutii_copy)

                # cutii noi?
                joc_nou.completeaza_cutii(jucator)
                joc_nou.ultima_mutare = line_index
                l_mutari.append(joc_nou)
        
        return l_mutari
                

    def cutie_deschisa(self, index, jucator, mod_estimare="default"):
        """Returneaza daca cutia nu a fost inchisa inca

        Args:
            index ((int, int))): indexul cutiei in joc.cutii
            jucator (string): simbolul jucatorului

        Returns:
            int: Numarul de linii de pe conturul cutiei nefolosite
        """
        
        if mod_estimare != "default":
            jucator_opus = self.jucator_opus(jucator)

            if self.cutii[index[0]][index[1]] != jucator_opus:
                return 1
            return 0
        
        ## Else
        if jucator == self.cutii[index[0]][index[1]]:
            return 4 # 4 laturi

        if self.cutii[index[0]][index[1]] == Joc.GOL:
            up, left, down, right = self.indecsi_contur(index[0], index[1])

            return sum(1 if self.matr[i] == Joc.GOL else 0 for i in [up, left, down, right])
        return 0

    def cutii_deschise(self, jucator, mod_estimare="default"):

        linii = 0
        
        for i in range(len(self.cutii)):
            for j in range(len(self.cutii[i])):
                linii += self.cutie_deschisa((i, j), jucator, mod_estimare)

        return linii

    def estimeaza_scor(self, adancime, mod_estimare="default"):
        t_final = self.final()
        
        if t_final == self.__class__.JMAX:
            return self.__class__.scor_maxim + adancime
        elif t_final == self.__class__.JMIN:
            return -self.__class__.scor_maxim - adancime
        elif t_final == "remiza":
            return 0
        else:
            return self.cutii_deschise(self.__class__.JMAX, mod_estimare) -\
                   self.cutii_deschise(self.__class__.JMIN, mod_estimare)
    
    def sirAfisare(self):
        sir = [
            ["+" for _ in range(2 * Joc.NR_COLOANE - 1)]
            for _ in range(2 * Joc.NR_LINII - 1)
        ]

        for line in range(len(self.cutii)):
            for column in range(len(self.cutii[line])):
                up, left, down, right = self.indecsi_contur(line, column)

                
                sir[2 * line][2 * column + 1] = "-" if self.matr[up] != Joc.GOL else " "

                sir[2 * (line + 1)][2 * column + 1] = "-" if self.matr[down] != Joc.GOL else " "
                
                sir[2 * line + 1][2 * column] = "|" if self.matr[left] != Joc.GOL else " "
                
                sir[2 * line + 1][2 * (column + 1)] = "|" if self.matr[right] != Joc.GOL else " "
                

                if self.cutii[line][column] == Joc.GOL:
                    sir[2 * line + 1][2 * column + 1] = " "
                else:
                    sir[2 * line + 1][2 * column + 1] = self.cutii[line][column]
        
        sir = map(lambda x: "".join(x), sir)
        sir2 = "\n".join(sir)
        return sir2

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()

class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime - 1, parinte=self)
            for mutare in l_mutari
        ]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "\n(Juc curent:" + self.j_curent + ")\n"
        sir += "scor x: " + str(self.tabla_joc.scor_x) + "\nscor 0: " + str(self.tabla_joc.scor_zero)
        return sir

    def __repr__(self):
        sir = str(self.tabla_joc) + "\n(Juc curent:" + self.j_curent + ")\n"
        sir += "scor x: " + str(self.tabla_joc.scor_x) + "\nscor 0: " + str(self.tabla_joc.scor_zero)
        return sir

class Buton:
    def __init__(
        self,
        display=None,
        left=0,
        top=0,
        w=0,
        h=0,
        culoareFundal=(53, 80, 115),
        culoareFundalSel=(89, 134, 194),
        text="",
        font="arial",
        fontDimensiune=16,
        culoareText=(255, 255, 255),
        valoare="",
    ):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(
        self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0
    ):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += spatiuButoane + b.w

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta"),
        ],
        indiceSelectat=1,
    )
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="x", valoare="x"),
            Buton(display=display, w=35, h=30, text="zero", valoare="0"),
        ],
        indiceSelectat=0,
    )
    btn_dif = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Usor", valoare="1"),
            Buton(display=display, w=80, h=30, text="Mediu", valoare="2"),
            Buton(display=display, w=80, h=30, text="Greu", valoare="3"),
        ],
        indiceSelectat=0,
    )
    ok = Buton(
        display=display,
        top=240,
        left=30,
        w=40,
        h=30,
        text="ok",
        culoareFundal=(155, 0, 55),
    )
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dif.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                tabla_curenta.__class__.display.fill((255, 255, 255))
                                tabla_curenta.deseneaza_grid()
                                print()
                                print(str(tabla_curenta))
                                print()
                                return btn_juc.getValoare(), btn_alg.getValoare(), int(btn_dif.getValoare())
        pygame.display.update()

def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False

def stop_game(stare):
    """Afiseaza castigatorul si opreste jocul

    Args:
        stare (Stare): starea finala
    """

    display = Joc.display
    font = "arial"
    dimFont = 16
    culoareFont = (0,0,0)
    text = ""
    if stare.tabla_joc.scor_x < stare.tabla_joc.scor_zero:
        culoareFont = Joc.CULOARE_ZERO
        text = "A castigat " + stare.j_curent
    elif stare.tabla_joc.scor_x > stare.tabla_joc.scor_zero:
        culoareFont = Joc.CULOARE_X
        text = "A castigat " + stare.j_curent
    else:
        text = "Remiza!"

    fontObj = pygame.font.SysFont(font, dimFont)
    textRandat = fontObj.render(text, True, culoareFont)

    w, _ = display.get_size()
    dreptunghi = textRandat.get_rect()
    dreptunghi.center = (w // 2, Joc.dim_celula // 4)

    display.blit(textRandat, dreptunghi)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


################################################################################
##                               MINIMAX                                      ##
################################################################################

def min_max(stare):

    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        if len(mutari_scor) > 0:
            stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        if len(mutari_scor) > 0:
            stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


################################################################################
##                              ALPHA-BETA                                    ##
################################################################################

def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, "not default")
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float("-inf")

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float("inf")

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare

times = []
t_final = -1

def main():
    global ADANCIME_MAX, times, t_final

    pygame.init()
    pygame.display.set_caption("Croitoru Tudor - Dots & Boxes")
    nl = 6
    nc = 7
    w = 100
    ecran = pygame.display.set_mode(
        size=(nc * (w + 1) - 1, nl * (w + 1) - 1)
    )  # N *100+ N-1= N*(100+1)-1

    ecran.fill((255, 255, 255))
    pygame.display.update()
    Joc.initializeaza(ecran, NR_LINII=nl, NR_COLOANE=nc, dim_celula=w)
    joc = Joc()

    Joc.JMIN, tip_algoritm, dificultate = deseneaza_alegeri(ecran, joc)
    Joc.JMAX = "0" if Joc.JMIN == "x" else "x"
    print(Joc.JMIN, tip_algoritm)

    ADANCIME_MAX = dificultate
    print(dificultate)

    # creare stare initiala
    stare_curenta = Stare(joc, "x", ADANCIME_MAX)

    # preiau timpul in milisecunde de dinainte de mutare
    t_inainte = int(round(time.time() * 1000))

    while True:

        if stare_curenta.j_curent == Joc.JMIN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului

                    for np in range(len(Joc.linii)):
                        if Joc.linii[np].collidepoint(pos) and stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                            stare_curenta.tabla_joc.matr[np] = stare_curenta.j_curent

                            t_dupa = int(round(time.time() * 1000))

                            stare_curenta.tabla_joc.ultima_mutare = np

                            ## Verificare daca a fost inchisa vreo cutie noua
                            stare_curenta.tabla_joc.completeaza_cutii(stare_curenta.j_curent)

                            stare_curenta.tabla_joc.deseneaza_grid(stare_curenta)
                            print()
                            print("Tabla dupa mutarea utilizatorului\n" + str(stare_curenta))

                            print(
                                'Utilizatorul a "gandit" timp de '
                                + str(t_dupa - t_inainte)
                                + " milisecunde."
                            )
                            print()

                            # testez daca jocul a ajuns intr-o stare finala
                            # si afisez un mesaj corespunzator in caz ca da
                            if afis_daca_final(stare_curenta):
                                stop_game(stare_curenta)
                                return

                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                            t_inainte = int(round(time.time() * 1000))
                            break
        else: # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            if tip_algoritm == "minimax":
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc


            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))

            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            print(
                'Calculatorul a "gandit" timp de '
                + str(t_dupa - t_inainte)
                + " milisecunde."
            )
            print("Estimare: " + str(stare_actualizata.stare_aleasa.scor))

            times.append(t_dupa - t_inainte)
            t_final = t_dupa

            stare_curenta.tabla_joc.deseneaza_grid(stare_curenta)
            if afis_daca_final(stare_curenta):
                stop_game(stare_curenta)
                return 

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

    

                        

if __name__ == "__main__":
    t_inceput = int(round(time.time() * 1000))
    main()
    print("Jocul a durat " + str(t_final - t_inceput) + "ms\n")

    print("Statistics")
    print("Min time: {}ms\nMedian time: {}ms\nMax time: {}ms\n".format(min(times), statistics.median(times), max(times)))