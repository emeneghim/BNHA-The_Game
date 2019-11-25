import pygame 
from pygame.locals import *
from sys import exit
import sys, os
import time
import pickle
import sqlite3
from copy import deepcopy
#1440x900
#1366x768
#800x800
import random
pygame.font.init()
Preto = (0, 0, 0)
Branco = (255, 255, 255)
Cinza = (192,217,217)
Cinza_Escuro = (128,128,128)
fonte22 = pygame.font.Font(None,22)
fonte24 = pygame.font.Font(None,24)
fonte26 = pygame.font.Font(None,26)
fonte28 = pygame.font.Font(None,28)
fonte36 = pygame.font.Font(None,36)
fonte50 = pygame.font.Font(None,50)
fonte70 = pygame.font.Font(None,70)
pygame.display.set_caption('My Game')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.init()
db = sqlite3.connect('teste.db')
cursor = db.cursor()
clock = pygame.time.Clock()
check = pygame.image.load("assets/check.png").convert_alpha()
deku_slogan = pygame.image.load("assets/Deku.png").convert_alpha()
stop = pygame.image.load("assets/stop.png").convert_alpha()
stop_rect = stop.get_rect(topleft = (30,30))
background = pygame.Surface(screen.get_size())

class Spell():
    def __init__(self, nome, icone, ataque, mana, id):
        self.nome = nome
        self.icone = icone
        self.ataque = ataque
        self.mana = mana
        self.id = id

class Item():
    def __init__(self, nome, tipo, ataque, defesa, valor_venda, quantidade, equipado, nivel_necessario, id, preco_compra, nivel):
        self.nome = nome
        self.tipo = tipo
        self.ataque = ataque
        self.defesa = defesa
        self.valor_venda = valor_venda
        self.quantidade = quantidade
        self.equipado = equipado
        self.nivel_necessario = nivel_necessario
        self.nivel = nivel
        self.id = id
        self.preco_compra = preco_compra
        
    def aprimorar(self):
        new_item = Item(self.nome,self.tipo,self.ataque+10,self.defesa+10,self.valor_venda,1,0,self.nivel_necessario,self.id,self.preco_compra,self.nivel)
        new_item.aumentar_nivel()
        inventory.add_item(new_item)
        if self.quantidade==1:
            return False
        else:
            self.quantidade -= 1

    def aumentar_nivel(self):
        self.nivel +=1

    def definir_item_drop(self,lista):
        self.lista = lista

class Inventory():    
    def __init__(self):
        self.items = []
        self.pagina = 0
        self.equipamentos_equipados = ["Material"]

    def add_item(self, item):
        igual = False
        for p in self.items:
            if item.nome == p.nome and item.nivel == p.nivel:
                p.quantidade += item.quantidade
                igual = True
                break
        if igual != True:
            self.items.append(item)
        self.items = sorted(self.items, key=lambda p: p.id)

    def remove_item(self, item):
        self.items.remove(item)
            

    def equip_item(self, item):
        pass
        if item.tipo == "Baú":
            item.quantidade -= 1
            if item.quantidade <= 0:
                self.items.remove(item)
            if item.tipo == "Baú":
                a = random.randint(1,6)
                if a == 1:
                    inventory.add_item(item.lista[0])
                    item = item.lista[0].nome
                elif a == 2:
                    inventory.add_item(item.lista[1])
                    item = item.lista[1].nome
                elif a == 3:
                    inventory.add_item(item.lista[2])
                    item = item.lista[2].nome
                elif a == 4:
                    inventory.add_item(item.lista[3])
                    item = item.lista[3].nome
                elif a == 5:
                    inventory.add_item(item.lista[4])
                    item = item.lista[4].nome
                elif a == 6:
                    inventory.add_item(item.lista[5])
                    item = item.lista[5].nome
                pop = pygame.image.load("assets/interface/mensagempopupsemfundo.png").convert_alpha()
                screen.blit(pop, (0,0))
                texto = "Você recebeu:"
                texto = fonte36.render(str(texto),True, Branco)
                texto_rect = texto.get_rect(center=(690,320))
                screen.blit(texto,(texto_rect))
                recebido = "1x "+str(item)
                recebido = fonte36.render(str(recebido),True, Branco)
                recebido_rect = recebido.get_rect(center=(690,440))
                screen.blit(recebido,(recebido_rect))
                pygame.display.flip()
                done = False
                while done == False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                x, y = pygame.mouse.get_pos()
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if x>=476 and x<=607 and y>=524 and y<=581:
                                jogo.mochila()
                            elif x>=767 and x<= 912 and y>=524 and y<=581:
                                jogo.mochila()
        if item.equipado == 0 and item.tipo not in self.equipamentos_equipados and per.nivel>item.nivel_necessario:
            item.equipado = 1
            per.ataque += item.ataque
            per.defesa += item.defesa
            self.equipamentos_equipados.append(item.tipo)
        elif item.equipado == 1:
            self.equipamentos_equipados.remove(item.tipo)
            per.ataque -= item.ataque
            per.defesa -= item.defesa
            item.equipado = 0
        jogo.mochila()
    
    def aprimorar_item(self,x,y):
        y = ((y-230)//27)+1
        y = y+((self.pagina)*16)
        c = (inventory.items[y-1])
        item = c
        if item.tipo not in self.equipamentos_equipados and item.nivel<10:
            a = item.aprimorar()
            if a == False:
                self.items.remove(item)
            jogo.mochila()


    def aumentar_pagina(self):
        self.pagina += 1
        if self.pagina*16>len(self.items):
            self.pagina -= 1
        jogo.mochila()
    
    def diminuir_pagina(self):
        if self.pagina != 0:
            self.pagina -= 1
            jogo.mochila()
    
    def info_item(self, x, y):
        y = ((y-230)//27)+1
        y = y+((self.pagina)*16)
        c = (inventory.items[y-1])
        inventory.equip_item(c)
        jogo.mochila()


    def print_items(self):
        y = 230
        atual = self.pagina*16
        objeto = 1
        aaa = 0
        pagina_atual = fonte50.render(str(self.pagina+1), True, Preto)
        screen.blit(pagina_atual,(210,130))
        for p in self.items:
            if aaa != atual:
                aaa += 1
                pass
            else:
                xa = fonte22.render(str(p.nivel_necessario), True, Branco)
                screen.blit(xa, (220, y))
                if p.nivel != 0:
                    nome = fonte22.render(str(p.nome)+' + '+str(p.nivel), True, Branco)
                else:
                    nome = fonte22.render(p.nome, True, Branco)
                screen.blit(nome, (270,y))
                ataque = fonte22.render(str(p.ataque), True, Branco)
                ataque_rect = ataque.get_rect(center =(595,y+9))
                screen.blit(ataque, (ataque_rect))
                defesa = fonte22.render(str(p.defesa), True, Branco)
                defesa_rect = defesa.get_rect(center =(765,y+9))
                screen.blit(defesa, (defesa_rect))
                preco = fonte22.render(str(p.valor_venda), True, Branco)
                preco_rect = preco.get_rect(center =(943,y+9))
                screen.blit(preco, (preco_rect))
                quantidade = fonte22.render(str(p.quantidade), True, Branco)
                quantidade_rect = quantidade.get_rect(center =(1110,y+9))
                screen.blit(quantidade, (quantidade_rect))
                if p.equipado == 1:
                    screen.blit(check, (100,y))
                y += 27
                objeto += 1
                if objeto % 17 == 0:
                    break
        pygame.display.flip()

class Quest():
    def __init__(self,nome,recompensa,itens,doador,objetivo,qnt_objetivo,cod_missao,tipo):
        self.nome = nome
        self.recompensa = recompensa
        self.doador = doador
        self.objetivo = objetivo
        self.qnt_atual = 0
        self.itens = itens
        self.qnt = qnt_objetivo
        self.cod = cod_missao
        self.tipo = tipo

class Personagem():
    def __init__(self, nick):
        self.dinheiro = 1000
        self.nick = nick
        self.ataque = 1
        self.defesa = 10
        self.nivel = 2
        self.xp = 0
        self.hp = 80
        self.mana = 200
        self.crit_chance = 20
        self.desv_chance = 20
        self.pontos = 0
    
    def acrescentar_xp(self,xp):
        self.xp += xp
        if self.xp >= 50:
            self.upar()
    
    def upar(self):
        self.nivel += 1
        print (self.nivel)
        self.pontos += 2
        self.xp = 0
        self.hp += 100

class Game():
    def __init__(self):
        self.lista_spells = []
        a = Spell("soco","assets/spells_icons/soco.jpg",25,0,2)
        self.lista_spells.append (a)
        self.lista_quests = []
        a = Quest("Teste",1,armadura_medieval,"All Might","Derrote One for All 1 vez!",0,1,1)
        b = Quest("Secundária Todoroki",100,armadura_medieval,"Todoroki","Derrote 5 inimigos usando gelo!",0,100,0)
        c = Quest("Secundária Gran Torino",100,armadura_medieval,"Gran Torino","Derrote 10 inimigos!",0,200,0)
        d = Quest("Secundária Uraraka",2500,armadura_medieval,"Uraraka","Derrote o robozao do teste de admissão!",0,300,0)
        e = Quest("Secundária Neito Monoma",1000,armadura_medieval,"Neito Monoma","Derrote 20 estudantes da turma A!",0,400,0)
        f = Quest("Secundária Yuga Aoyama",250,armadura_medieval,"Aoyama","Equipe 5 itens de raridade Laranja!",0,500,0)
        self.lista_quests.append(a)
        self.lista_quests.append(b)
        self.lista_quests.append(c)
        self.lista_quests.append(d)
        self.lista_quests.append(e)
        self.lista_quests.append(f)
        self.mapa_disp = 7
    def limpar_bd(self):
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='users';''')
        db.commit()
        a = cursor.fetchone()
        if a != None:
            cursor.execute('''drop table users''')
    def salvar(self):
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='users';''')
        a = cursor.fetchone()
        db.commit()
        if a == None:
            cursor.execute('''CREATE TABLE users(personagem VARCHAR(70))''')
            db.commit()
        cursor.execute('''INSERT INTO users VALUES (?)''', ((self.persona,)))
        db.commit()           
    def carregar(self):
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='users';''')
        db.commit()
        a = cursor.fetchone()
        if a != None:
            cursor.execute('''SELECT Personagem from users''')
            a = cursor.fetchone()
            self.persona = a[0]
            print(self.persona)
            self.tela_principal()
        else:
            self.escurecer(True)
            self.menu_inicial()
    def escurecer(self,escurecer):
        tela_rect = screen.get_rect(topleft=(0, 0))
        x = 0
        pygame.image.save(screen, "var.jpg")
        teste = pygame.image.load("var.jpg").convert()
        if escurecer == True:
            i = 128
            while x == 0:            
                screen.fill (Preto)
                Image = teste.copy()
                i = i-5
                Image.set_alpha(i)
                screen.blit(Image, (tela_rect))
                pygame.display.update()
                pygame.display.flip()
                if i < 5:
                    x += 1
                pygame.time.delay(5)
        elif escurecer == False:
            i = 0
            while x == 0:            
                screen.fill (Preto)
                Image = teste.copy()
                i = i+5
                Image.set_alpha(i)
                screen.blit(Image, (tela_rect))
                pygame.display.update()
                pygame.display.flip()
                if i > 120:
                    x += 1
                pygame.time.delay(5)
    def informacoes(self):
        done = False
        screen.fill(Preto)
        infoos = fonte22.render("Este jogo foi desenvolvido pelos alunos Eduardo Meneghim e Kamila Alexandre, do terceiro ano de informática do Instituto Federal Catarinense - Campus Blumenau.", True, Branco)
        infoos2 = fonte22.render("Este jogo foi programado com a linguagem Python usando o Pygame, tendo foco totalmente pedagógico.", True, Branco)
        emailedu = fonte22.render("eduardomeneghim@gmail.com", True, Branco)
        emailka = fonte22.render("kamilalskw@gmail.com", True, Branco)
        emailedu_rect = emailedu.get_rect(topleft=(533, 458))
        emailka_rect = emailka.get_rect(topleft=(565, 512))
        infoos2_rect = infoos2.get_rect(topleft=(277,266))
        infoos_rect = infoos.get_rect(topleft=(43, 202))
        screen.blit(infoos, (infoos_rect))
        screen.blit(infoos2, (infoos2_rect))
        screen.blit(emailedu, (emailedu_rect))
        screen.blit(emailka, (emailka_rect))
        back = fonte50.render("Voltar", True, Branco)
        back_rect = back.get_rect(topleft=(1173,53))
        screen.blit(back,(back_rect))
        screen.blit(stop, (stop_rect))
        pygame.display.flip()
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if back_rect.collidepoint(x, y):
                            done = True
                            self.menu_inicial()
                        elif stop_rect.collidepoint(x, y):
                            done = True
                            pygame.quit()
                            exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()           
    def tela_principal(self):
        done = False
        tela_principal = pygame.image.load("assets/interface/borda superior.png").convert()
        screen.blit(tela_principal,(0,0))
        pygame.display.flip()
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        if y<=104:
                            if x>185 and x<=336:
                                self.mapa()
                            elif x>336 and x<=514:
                                self.mochila()
                            elif x>514 and x<=763:
                                self.habilidades()
                            elif x>763 and x<=912:
                                self.forja()
                            elif x>912 and x<= 1057:
                                self.loja()
                            elif x>1057 and x<=1212:
                                self.quests()
                            elif x>1212:
                                done = True
                                pygame.quit()
                                exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    def verificar_spell(self,nome):
        for a in self.lista_spells:
            if a.nome == nome and len(self.lista_spells)>1:
                self.lista_spells.remove(a)
                self.bla = False
                self.printar_spells_ativas()
            if len(self.lista_spells)==1:
                self.bla = False
    def printar_spells_ativas(self):
        cont = 1
        reseter = pygame.image.load("assets/interface/reseter.png").convert_alpha()
        screen.blit(reseter, (0,0))
        for a in self.lista_spells:
            if cont == 1:
                hab = pygame.image.load(a.icone).convert_alpha()
                screen.blit(hab,(313,638))
            elif cont == 2:
                hab = pygame.image.load(a.icone).convert_alpha()
                screen.blit(hab,(466,638))
            elif cont == 3:
                hab = pygame.image.load(a.icone).convert_alpha()
                screen.blit(hab,(621,638))
            elif cont == 4:
                hab = pygame.image.load(a.icone).convert_alpha()
                screen.blit(hab,(776,638))
            elif cont == 5:
                hab = pygame.image.load(a.icone).convert_alpha()
                screen.blit(hab,(929,638))
            cont += 1
        pygame.display.flip()

    def nivel_necessario(self, nivel, hab):
        a = 0
        if len(str(nivel))==2:
            a = 6
        if hab == 1:
            loc = (218-a,367)
        elif hab == 2:
            loc = (434-a,367)
        elif hab == 3:
            loc = (642-a,367)
        elif hab == 4:
            loc = (852-a,367)
        elif hab == 5:
            loc = (1069-a,367)
        texto_nao_renderizado = "Nível "+str(nivel)
        texto = fonte28.render(texto_nao_renderizado, True, Branco)
        screen.blit(texto,(loc))
        pygame.display.flip()
        
    def habilidades(self):
        done = False
        cinza = pygame.image.load("assets/spells_icons/cinza.png").convert()
        cinza.set_alpha(200)
        imagem_principal = pygame.image.load("assets/interface/habilidades.png").convert_alpha()
        screen.blit(imagem_principal, (0,0))
        hab_1 = pygame.image.load("assets/spells_icons/soco.jpg").convert_alpha()
        hab_1_rect = hab_1.get_rect(center = (251,375))
        screen.blit(hab_1,(hab_1_rect))
        hab_2 = pygame.image.load("assets/spells_icons/chute.jpg").convert_alpha()
        hab_2_rect = hab_2.get_rect(center = (464,375))
        screen.blit(hab_2,(hab_2_rect))
        if per.nivel<3:
            screen.blit(cinza,(hab_2_rect))
            self.nivel_necessario(3,2)
        hab_3 = pygame.image.load("assets/spells_icons/delaware.jpg").convert_alpha()
        hab_3_rect = hab_3.get_rect(center = (673,375))
        screen.blit(hab_3,(hab_3_rect))
        if per.nivel<6:
            screen.blit(cinza,(hab_3_rect))
            self.nivel_necessario(6,3)
        pygame.display.flip()
        hab_4 = pygame.image.load("assets/spells_icons/aprimoramento.jpg").convert_alpha()
        hab_4_rect = hab_4.get_rect(center = (884,375))
        screen.blit(hab_4,(hab_4_rect))
        if per.nivel<4:
            screen.blit(cinza,(hab_4_rect))
            self.nivel_necessario(4,4)
        pygame.display.flip()
        hab_5 = pygame.image.load("assets/spells_icons/ataquerapido.png").convert_alpha()
        hab_5_rect = hab_5.get_rect(center = (1100,375))
        screen.blit(hab_5,(hab_5_rect))
        if per.nivel<8:
            screen.blit(cinza,(hab_5_rect))
            self.nivel_necessario(8,5)
        pagina_atual = 1
        self.printar_spells_ativas()
        pygame.display.flip()
        mudar = False
        var = False
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        self.bla = True
                        if hab_1_rect.collidepoint(x,y):
                            if pagina_atual == 1:
                                self.verificar_spell("soco")
                                if len(self.lista_spells)<5 and self.bla == True:
                                    self.lista_spells.append(Spell("soco","assets/spells_icons/soco.jpg",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 2:
                                self.verificar_spell("fortaleza")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 10:
                                    self.lista_spells.append(Spell("fortaleza","assets/spells_icons/fortaleza.jpg",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 3:
                                self.verificar_spell("gelofraco")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 12:
                                    self.lista_spells.append(Spell("gelofraco","assets/spells_icons/gelofraco.jpg",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 4:
                                self.verificar_spell("espelho")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 24:
                                    self.lista_spells.append(Spell("espelho","assets/spells_icons/espelho.jpg",25,0,2))
                                    self.printar_spells_ativas()
                        elif hab_2_rect.collidepoint(x,y):
                            if pagina_atual == 1:
                                self.verificar_spell("chute")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 3:
                                    self.lista_spells.append(Spell("chute","assets/spells_icons/chute.jpg",40,20,3))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 2:
                                self.verificar_spell("eletricofraco")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 12:
                                    self.lista_spells.append(Spell("eletricofraco","assets/spells_icons/eletricofraco.jpg",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 3:
                                self.verificar_spell("geloforte")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 20:
                                    self.lista_spells.append(Spell("geloforte","assets/spells_icons/geloforte.png",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 4:
                                self.verificar_spell("veneno")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 30:
                                    self.lista_spells.append(Spell("veneno","assets/spells_icons/veneno.png",25,0,2))
                                    self.printar_spells_ativas()
                        elif hab_3_rect.collidepoint(x,y):
                            if pagina_atual == 1:
                                self.verificar_spell("delaware")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 6:
                                    self.lista_spells.append(Spell("delaware","assets/spells_icons/delaware.jpg",60,40,1))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 2:
                                self.verificar_spell("eletricoforte")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 20:
                                    self.lista_spells.append(Spell("eletricoforte","assets/spells_icons/eletricoforte.png",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 3:
                                self.verificar_spell("fogofraco")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 12:
                                    self.lista_spells.append(Spell("fogofraco","assets/spells_icons/fogofraco.jpg",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 4:
                                self.verificar_spell("invasao")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 36:
                                    self.lista_spells.append(Spell("invasao","assets/spells_icons/invasao.jpg",25,0,2))
                                    self.printar_spells_ativas()
                        elif hab_4_rect.collidepoint(x,y):
                            if pagina_atual == 1:
                                self.verificar_spell("aprimoramento")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 4:
                                    self.lista_spells.append(Spell("aprimoramento","assets/spells_icons/aprimoramento.jpg",60,40,1))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 2:
                                self.verificar_spell("plantafraco")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 12:
                                    self.lista_spells.append(Spell("plantafraco","assets/spells_icons/plantafraco.jpg",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 3:
                                self.verificar_spell("fogoforte")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 20:
                                    self.lista_spells.append(Spell("fogoforte","assets/spells_icons/fogoforte.jpg",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 4:
                                self.verificar_spell("vampirismo")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 40:
                                    self.lista_spells.append(Spell("vampirismo","assets/spells_icons/vampirismo.jpg",25,0,2))
                                    self.printar_spells_ativas()
                        elif hab_5_rect.collidepoint(x,y):
                            if pagina_atual == 1:
                                self.verificar_spell("ataquerapido")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 8:
                                    self.lista_spells.append(Spell("ataquerapido","assets/spells_icons/ataquerapido.png",60,40,1))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 2:
                                self.verificar_spell("plantaforte")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 20:
                                    self.lista_spells.append(Spell("plantaforte","assets/spells_icons/plantaforte.png",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 3:
                                self.verificar_spell("cura")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 18:
                                    self.lista_spells.append(Spell("cura","assets/spells_icons/cura.png",25,0,2))
                                    self.printar_spells_ativas()
                            elif pagina_atual == 4:
                                self.verificar_spell("ninja")
                                if len(self.lista_spells)<5 and self.bla == True and per.nivel >= 46:
                                    self.lista_spells.append(Spell("ninja","assets/spells_icons/ninja.jpg",25,0,2))
                                    self.printar_spells_ativas()
                        if y>=630 and y<=750:
                            if x>=311 and x<=425:
                                if len(self.lista_spells)>1:
                                    self.lista_spells.pop(0)
                            elif x>=460 and x<= 580:
                                if len(self.lista_spells)>1:
                                    self.lista_spells.pop(1)
                            elif x>=610 and x<=745:
                                if len(self.lista_spells)>2:
                                    self.lista_spells.pop(2)
                            elif x>=768 and x<=890:
                                if len(self.lista_spells)>3:
                                    self.lista_spells.pop(3)
                            elif x>=920 and x<= 1040:
                                if len(self.lista_spells)>4:
                                    self.lista_spells.pop(4)
                            self.printar_spells_ativas()
                        if x>=128 and x<=162 and y>=351 and y<= 400:
                            if pagina_atual>1:
                                pagina_atual -= 1
                                mudar = True
                        elif x>=1183 and x<= 1218 and y>= 351 and y<=399:
                            if pagina_atual<4:
                                pagina_atual += 1
                                mudar = True
                        if mudar == True:
                            mudar = False
                            imagem_principal = pygame.image.load("assets/interface/habilidades.png").convert_alpha()
                            screen.blit(imagem_principal, (0,0))
                            if pagina_atual == 1:
                                self.habilidades()
                            elif pagina_atual == 2:
                                hab_1 = pygame.image.load("assets/spells_icons/fortaleza.jpg").convert_alpha()
                                screen.blit(hab_1,(hab_1_rect))
                                if per.nivel<10:
                                    screen.blit(cinza,(hab_1_rect))
                                    self.nivel_necessario(10,1)
                                hab_2 = pygame.image.load("assets/spells_icons/eletricofraco.jpg").convert_alpha()
                                screen.blit(hab_2,(hab_2_rect))
                                if per.nivel<12:
                                    screen.blit(cinza,(hab_2_rect))
                                    self.nivel_necessario(12,2)
                                hab_3 = pygame.image.load("assets/spells_icons/eletricoforte.png").convert_alpha()
                                screen.blit(hab_3,(hab_3_rect))
                                if per.nivel<20:
                                    screen.blit(cinza,(hab_3_rect))
                                    self.nivel_necessario(20,3)
                                hab_4 = pygame.image.load("assets/spells_icons/plantafraco.jpg").convert_alpha()
                                screen.blit(hab_4,(hab_4_rect))
                                if per.nivel<12:
                                    screen.blit(cinza,(hab_4_rect))
                                    self.nivel_necessario(12,4)
                                hab_5 = pygame.image.load("assets/spells_icons/plantaforte.png").convert_alpha()
                                screen.blit(hab_5,(hab_5_rect))
                                if per.nivel<20:
                                    screen.blit(cinza,(hab_5_rect))
                                    self.nivel_necessario(20,5)
                                pygame.display.flip()
                                self.printar_spells_ativas()
                            elif pagina_atual == 3:
                                hab_1 = pygame.image.load("assets/spells_icons/gelofraco.jpg").convert_alpha()
                                screen.blit(hab_1,(hab_1_rect))
                                if per.nivel<12:
                                    screen.blit(cinza,(hab_1_rect))
                                    self.nivel_necessario(12,1)
                                hab_2 = pygame.image.load("assets/spells_icons/geloforte.png").convert_alpha()
                                screen.blit(hab_2,(hab_2_rect))
                                if per.nivel<20:
                                    screen.blit(cinza,(hab_2_rect))
                                    self.nivel_necessario(20,2)
                                hab_3 = pygame.image.load("assets/spells_icons/fogofraco.jpg").convert_alpha()
                                screen.blit(hab_3,(hab_3_rect))
                                if per.nivel<12:
                                    screen.blit(cinza,(hab_3_rect))
                                    self.nivel_necessario(12,3)
                                hab_4 = pygame.image.load("assets/spells_icons/fogoforte.jpg").convert_alpha()
                                screen.blit(hab_4,(hab_4_rect))
                                if per.nivel<20:
                                    screen.blit(cinza,(hab_4_rect))
                                    self.nivel_necessario(20,4)
                                hab_5 = pygame.image.load("assets/spells_icons/cura.png").convert_alpha()
                                screen.blit(hab_5,(hab_5_rect))
                                if per.nivel<18:
                                    screen.blit(cinza,(hab_5_rect))
                                    self.nivel_necessario(18,5)
                                pygame.display.flip()
                                self.printar_spells_ativas()
                            elif pagina_atual == 4:
                                hab_1 = pygame.image.load("assets/spells_icons/espelho.jpg").convert_alpha()
                                screen.blit(hab_1,(hab_1_rect))
                                if per.nivel<24:
                                    screen.blit(cinza,(hab_1_rect))
                                    self.nivel_necessario(24,1)
                                hab_2 = pygame.image.load("assets/spells_icons/veneno.png").convert_alpha()
                                screen.blit(hab_2,(hab_2_rect))
                                if per.nivel<30:
                                    screen.blit(cinza,(hab_2_rect))
                                    self.nivel_necessario(30,2)
                                hab_3 = pygame.image.load("assets/spells_icons/invasao.jpg").convert_alpha()
                                screen.blit(hab_3,(hab_3_rect))
                                if per.nivel<36:
                                    screen.blit(cinza,(hab_3_rect))
                                    self.nivel_necessario(36,3)
                                hab_4 = pygame.image.load("assets/spells_icons/vampirismo.jpg").convert_alpha()
                                screen.blit(hab_4,(hab_4_rect))
                                if per.nivel<40:
                                    screen.blit(cinza,(hab_4_rect))
                                    self.nivel_necessario(40,4)
                                hab_5 = pygame.image.load("assets/spells_icons/ninja.jpg").convert_alpha()
                                screen.blit(hab_5,(hab_5_rect))
                                if per.nivel<46:
                                    screen.blit(cinza,(hab_5_rect))
                                    self.nivel_necessario(46,5)
                                pygame.display.flip()
                                self.printar_spells_ativas()
                            pygame.display.flip()
                        elif y<=104:
                            if x>185 and x<=336:
                                self.mapa()
                            elif x>336 and x<=514:
                                self.mochila()
                            elif x>514 and x<=763:
                                self.habilidades()
                            elif x>763 and x<=912:
                                self.forja()
                            elif x>912 and x<= 1057:
                                self.loja()
                            elif x>1057 and x<=1212:
                                self.quests()
                            elif x>1212:
                                done = True
                                pygame.quit()
                                exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    def forja(self):
        done = False
        imagem_principal = pygame.image.load("assets/interface/forja.png").convert_alpha()
        screen.blit(imagem_principal, (0,0))
        pygame.display.flip()
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        if y<=104:
                            if x>185 and x<=336:
                                self.mapa()
                            elif x>336 and x<=514:
                                self.mochila()
                            elif x>514 and x<=763:
                                self.habilidades()
                            elif x>763 and x<=912:
                                self.forja()
                            elif x>912 and x<= 1057:
                                self.loja()
                            elif x>1057 and x<=1212:
                                self.quests()
                            elif x>1212:
                                done = True
                                pygame.quit()
                                exit()
    def printar_loja(self,lista):
        pygame.display.flip()
        done = False
        imagem_principal = pygame.image.load("assets/interface/loja.png").convert_alpha()
        screen.blit(imagem_principal, (0,0))
        altura = 240
        a = 0
        contt = 0
        qnt_atual = 0
        qnt_total = 0
        contt = self.pagina_loja*11-11
        seta_esq1 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq1_rect = seta_esq1.get_rect(topleft=(1060,215))
        seta_esq2 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq2_rect = seta_esq2.get_rect(topleft=(1060, 249))
        seta_esq3 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq3_rect = seta_esq3.get_rect(topleft=(1060, 283))
        seta_esq4 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq4_rect = seta_esq4.get_rect(topleft=(1060, 317))
        seta_esq5 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq5_rect = seta_esq5.get_rect(topleft=(1060, 351))
        seta_esq6 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq6_rect = seta_esq6.get_rect(topleft=(1060, 385))
        seta_esq7 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq7_rect = seta_esq7.get_rect(topleft=(1060, 419))
        seta_esq8 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq8_rect = seta_esq8.get_rect(topleft=(1060, 453))
        seta_esq9 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq9_rect = seta_esq9.get_rect(topleft=(1060, 487))
        seta_esq10 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq10_rect = seta_esq10.get_rect(topleft=(1060, 521))
        seta_esq11 = pygame.image.load("assets/interface/setaesquerda.png")
        seta_esq11_rect = seta_esq11.get_rect(topleft=(1060, 555))
        seta_dir1 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir1_rect = seta_dir1.get_rect(topleft=(1114, 215))
        seta_dir2 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir2_rect = seta_dir2.get_rect(topleft=(1114, 249))
        seta_dir3 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir3_rect = seta_dir3.get_rect(topleft=(1114, 283))
        seta_dir4 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir4_rect = seta_dir4.get_rect(topleft=(1114, 317))
        seta_dir5 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir5_rect = seta_dir5.get_rect(topleft=(1114, 351))
        seta_dir6 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir6_rect = seta_dir6.get_rect(topleft=(1114, 385))
        seta_dir7 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir7_rect = seta_dir7.get_rect(topleft=(1114, 419))
        seta_dir8 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir8_rect = seta_dir8.get_rect(topleft=(1114, 453))
        seta_dir9 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir9_rect = seta_dir9.get_rect(topleft=(1114, 487))
        seta_dir10 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir10_rect = seta_dir10.get_rect(topleft=(1114, 521))
        seta_dir11 = pygame.image.load("assets/interface/setadireita.png")
        seta_dir11_rect = seta_dir11.get_rect(topleft=(1114, 555))
        try:
            var_lixo = self.carrinho
        except:
            self.carrinho = []
        try:
            var_lixo = self.preco_total
        except:
            self.preco_total = 0
        try:
            var_lixo = self.qnt_1
        except:
            self.qnt_1 = 0
            self.qnt_2 = 0
            self.qnt_3 = 0
            self.qnt_4 = 0
            self.qnt_5 = 0
            self.qnt_6 = 0
            self.qnt_7 = 0
            self.qnt_8 = 0
            self.qnt_9 = 0
            self.qnt_10 = 0
            self.qnt_11 = 0
        prec_total_vis = fonte28.render(str(self.preco_total), True, Branco)
        prec_total_vis_rect = prec_total_vis.get_rect(center =(548,662))
        screen.blit(prec_total_vis,(prec_total_vis_rect))
        for i in lista:
            qnt_atual+=1
            qnt_total = self.pagina_loja*11
            if qnt_atual <= qnt_total and contt==0:
                a +=1
                texto = fonte28.render(i.nome, True, Branco)
                texto_rect = texto.get_rect(center = (360,altura))
                screen.blit(texto,(texto_rect))
                if i.defesa == 0 and i.ataque > 0:
                    texto2 = fonte28.render(str("Ataque +"+str(i.ataque)),True,Branco)
                    texto2_rect = texto2.get_rect(center =(681,altura))
                    screen.blit(texto2,(texto2_rect))
                elif i.ataque == 0 and i.defesa > 0:
                    texto2 = fonte28.render(str("Defesa +"+str(i.defesa)),True,Branco)
                    texto2_rect = texto2.get_rect(center =(681,altura))
                    screen.blit(texto2,(texto2_rect))
                else:
                    texto2 = fonte28.render(str("Ataque +"+str(i.ataque)+"       Defesa +"+ str(i.defesa)),True,Branco)
                    texto2_rect = texto2.get_rect(center =(681,altura))
                    screen.blit(texto2,(texto2_rect))
                texto3 = fonte28.render(str(i.preco_compra), True, Branco)
                texto3_rect = texto3.get_rect(center =(942,altura))
                screen.blit(texto3,(texto3_rect))
                altura += 34
                if a == 1:
                    screen.blit(seta_esq1,(seta_esq1_rect))
                    screen.blit(seta_dir1,(seta_dir1_rect))
                    texto = fonte22.render(str(self.qnt_1),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))
                    self.prec_1 = i.preco_compra
                    self.item1 = i
                elif a == 2:
                    screen.blit(seta_esq2,(seta_esq2_rect))
                    screen.blit(seta_dir2,(seta_dir2_rect))
                    texto = fonte22.render(str(self.qnt_2),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))
                    self.prec_2 = i.preco_compra
                    self.item2 = i                  
                elif a == 3:
                    screen.blit(seta_esq3,(seta_esq3_rect))
                    screen.blit(seta_dir3,(seta_dir3_rect))
                    texto = fonte22.render(str(self.qnt_3),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))
                    self.prec_3 = i.preco_compra
                    self.item3 = i
                elif a == 4:
                    screen.blit(seta_esq4,(seta_esq4_rect))
                    screen.blit(seta_dir4,(seta_dir4_rect))
                    texto = fonte22.render(str(self.qnt_4),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))
                    self.prec_4 = i.preco_compra
                    self.item4 = i
                elif a == 5:
                    screen.blit(seta_esq5,(seta_esq5_rect))
                    screen.blit(seta_dir5,(seta_dir5_rect))
                    texto = fonte22.render(str(self.qnt_5),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))
                    self.prec_5 = i.preco_compra
                    self.item5 = i
                elif a == 6:
                    screen.blit(seta_esq6,(seta_esq6_rect))
                    screen.blit(seta_dir6,(seta_dir6_rect))
                    texto = fonte22.render(str(self.qnt_6),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect)) 
                    self.prec_6 = i.preco_compra
                    self.item6 = i
                elif a == 7:
                    screen.blit(seta_esq7,(seta_esq7_rect))
                    screen.blit(seta_dir7,(seta_dir7_rect))
                    texto = fonte22.render(str(self.qnt_7),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))  
                    self.prec_7 = i.preco_compra
                    self.item7 = i
                elif a == 8:
                    screen.blit(seta_esq8,(seta_esq8_rect))
                    screen.blit(seta_dir8,(seta_dir8_rect))
                    texto = fonte22.render(str(self.qnt_8),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))  
                    self.prec_8 = i.preco_compra
                    self.item8 = i
                elif a == 9:
                    screen.blit(seta_esq9,(seta_esq9_rect))
                    screen.blit(seta_dir9,(seta_dir9_rect))
                    texto = fonte22.render(str(self.qnt_9),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect)) 
                    self.prec_9 = i.preco_compra
                    self.item9 = i
                elif a == 10:
                    screen.blit(seta_esq10,(seta_esq10_rect))
                    screen.blit(seta_dir10,(seta_dir10_rect))
                    texto = fonte22.render(str(self.qnt_10),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect)) 
                    self.prec_10 = i.preco_compra
                    self.item10 = i
                elif a == 11:
                    screen.blit(seta_esq11,(seta_esq11_rect))
                    screen.blit(seta_dir11,(seta_dir11_rect))
                    texto = fonte22.render(str(self.qnt_11),True, Branco)
                    texto_rect = texto.get_rect(center =(1110,altura-32))
                    screen.blit(texto,(texto_rect))  
                    self.prec_11 = i.preco_compra
                    self.item11 = i
            elif contt >0:
                contt-=1
            else:
                break
        pygame.display.flip()
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        print (x,y)
                        if x>=211 and x<=245:
                            if y>=637 and y<=682 and self.pagina_loja>1:
                                self.pagina_loja-=1
                                self.qnt_1 = 0
                                self.qnt_2 = 0
                                self.qnt_3 = 0
                                self.qnt_4 = 0
                                self.qnt_5 = 0
                                self.qnt_6 = 0
                                self.qnt_7 = 0
                                self.qnt_8 = 0
                                self.qnt_9 = 0
                                self.qnt_10 = 0
                                self.qnt_11 = 0
                                self.carrinho = []                                    
                                self.preco_total = 0
                                self.printar_loja(lista)
                        elif x>=1137 and x<=1172:
                            if y>=635 and y<=683 and self.pagina_loja<3:
                                self.pagina_loja+=1
                                self.qnt_1 = 0
                                self.qnt_2 = 0
                                self.qnt_3 = 0
                                self.qnt_4 = 0
                                self.qnt_5 = 0
                                self.qnt_6 = 0
                                self.qnt_7 = 0
                                self.qnt_8 = 0
                                self.qnt_9 = 0
                                self.qnt_10 = 0
                                self.qnt_11 = 0
                                self.carrinho = []                                    
                                self.preco_total = 0
                                self.printar_loja(lista)
                        elif y<=104:
                            if x>185 and x<=336:
                                self.mapa()
                            elif x>336 and x<=514:
                                self.mochila()
                            elif x>514 and x<=763:
                                self.habilidades()
                            elif x>763 and x<=912:
                                self.forja()
                            elif x>912 and x<= 1057:
                                self.loja()
                            elif x>1057 and x<=1212:
                                self.quests()
                            elif x>1212:
                                done = True
                                pygame.quit()
                                exit()
                        if x > 500 and x<1400:
                            if seta_dir1_rect.collidepoint(x,y):
                                self.preco_total += self.prec_1
                                self.qnt_1 += 1
                                self.carrinho.append(self.item1)
                            elif seta_dir2_rect.collidepoint(x,y):
                                self.qnt_2 += 1
                                self.preco_total += self.prec_2
                                self.carrinho.append(self.item2)
                            elif seta_dir3_rect.collidepoint(x,y):
                                self.qnt_3 += 1
                                self.preco_total += self.prec_3
                                self.carrinho.append(self.item3)
                            elif seta_dir4_rect.collidepoint(x,y):
                                self.qnt_4 += 1
                                self.preco_total += self.prec_4
                                self.carrinho.append(self.item4)
                            elif seta_dir5_rect.collidepoint(x,y):
                                self.qnt_5 += 1
                                self.preco_total += self.prec_5
                                self.carrinho.append(self.item5)
                            elif seta_dir6_rect.collidepoint(x,y):
                                self.qnt_6 += 1
                                self.preco_total += self.prec_6
                                self.carrinho.append(self.item6)
                            elif seta_dir7_rect.collidepoint(x,y):
                                self.qnt_7 += 1
                                self.preco_total += self.prec_7
                                self.carrinho.append(self.item7)
                            elif seta_dir8_rect.collidepoint(x,y):
                                self.qnt_8 += 1
                                self.preco_total += self.prec_8
                                self.carrinho.append(self.item8)
                            elif seta_dir9_rect.collidepoint(x,y):
                                self.qnt_9 += 1
                                self.preco_total += self.prec_9
                                self.carrinho.append(self.item9)
                            elif seta_dir10_rect.collidepoint(x,y):
                                self.qnt_10 += 1
                                self.preco_total += self.prec_10
                                self.carrinho.append(self.item10)
                            elif seta_dir11_rect.collidepoint(x,y):
                                self.qnt_11 += 1
                                self.preco_total += self.prec_11
                                self.carrinho.append(self.item11)
                            elif seta_esq1_rect.collidepoint(x,y) and self.qnt_1>0:
                                self.qnt_1 -= 1
                                self.preco_total -= self.prec_1
                                self.carrinho.remove(self.item1)
                            elif seta_esq2_rect.collidepoint(x,y) and self.qnt_2>0:
                                self.qnt_2 -= 1
                                self.preco_total -= self.prec_2
                                self.carrinho.remove(self.item2)
                            elif seta_esq3_rect.collidepoint(x,y) and self.qnt_3>0:
                                self.qnt_3 -= 1
                                self.preco_total -= self.prec_3
                                self.carrinho.remove(self.item3)
                            elif seta_esq4_rect.collidepoint(x,y) and self.qnt_4>0:
                                self.qnt_4 -= 1
                                self.preco_total -= self.prec_4
                                self.carrinho.remove(self.item4)
                            elif seta_esq5_rect.collidepoint(x,y) and self.qnt_5>0:
                                self.qnt_5 -= 1
                                self.preco_total -= self.prec_5
                                self.carrinho.remove(self.item5)
                            elif seta_esq6_rect.collidepoint(x,y) and self.qnt_6>0:
                                self.qnt_6 -= 1
                                self.preco_total -= self.prec_6
                                self.carrinho.remove(self.item6)
                            elif seta_esq7_rect.collidepoint(x,y) and self.qnt_7>0:
                                self.qnt_7 -= 1
                                self.preco_total -= self.prec_7
                                self.carrinho.remove(self.item7)
                            elif seta_esq8_rect.collidepoint(x,y) and self.qnt_8>0:
                                self.qnt_8 -= 1
                                self.preco_total -= self.prec_8
                                self.carrinho.remove(self.item8)
                            elif seta_esq9_rect.collidepoint(x,y) and self.qnt_9>0:
                                self.qnt_9 -= 1
                                self.preco_total -= self.prec_9
                                self.carrinho.remove(self.item9)
                            elif seta_esq10_rect.collidepoint(x,y) and self.qnt_10>0:
                                self.qnt_10 -= 1
                                self.preco_total -= self.prec_10
                                self.carrinho.remove(self.item10)
                            elif seta_esq11_rect.collidepoint(x,y) and self.qnt_11>0:
                                self.qnt_11 -= 1
                                self.preco_total -= self.prec_11
                                self.carrinho.remove(self.item11)
                            if x>=927 and x<= 1078 and y>=635 and y<=685:
                                self.qnt_1 = 0
                                self.qnt_2 = 0
                                self.qnt_3 = 0
                                self.qnt_4 = 0
                                self.qnt_5 = 0
                                self.qnt_6 = 0
                                self.qnt_7 = 0
                                self.qnt_8 = 0
                                self.qnt_9 = 0
                                self.qnt_10 = 0
                                self.qnt_11 = 0
                                self.carrinho = []
                                self.preco_total = 0
                            if x >= 690 and x <= 905 and y >= 635 and y <=687:
                                done = False
                                popup = pygame.image.load("assets/interface/mensagempopupsemfundo.png").convert_alpha()
                                screen.blit(popup, (0,0))
                                texto = "Você deseja mesmo gastar "+str(self.preco_total)+" moedas?"
                                texto = fonte36.render(str(texto),True, Branco)
                                screen.blit(texto,(470,380))
                                pygame.display.flip()
                                while done == False:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            if event.button == 1:
                                                x, y = pygame.mouse.get_pos()
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                exit()
                                            if x>=476 and x<=607 and y>=524 and y<=581:
                                                if per.dinheiro >= self.preco_total:
                                                    per.dinheiro -= self.preco_total
                                                    for i in self.carrinho:
                                                        inventory.add_item(i)
                                                    self.qnt_1 = 0
                                                    self.qnt_2 = 0
                                                    self.qnt_3 = 0
                                                    self.qnt_4 = 0
                                                    self.qnt_5 = 0
                                                    self.qnt_6 = 0
                                                    self.qnt_7 = 0
                                                    self.qnt_8 = 0
                                                    self.qnt_9 = 0
                                                    self.qnt_10 = 0
                                                    self.qnt_11 = 0
                                                    self.carrinho = []
                                                    self.preco_total = 0
                                                    screen.blit(popup,(0,0))
                                                    texto = fonte36.render("Compra realizada com sucesso!",True, Branco)
                                                    screen.blit(texto,(520,380))
                                                    pygame.display.flip()
                                                    done2 = False
                                                    while done2 == False:
                                                        for event in pygame.event.get():
                                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                                if event.button == 1:
                                                                    x, y = pygame.mouse.get_pos()
                                                                if event.type == pygame.QUIT:
                                                                    pygame.quit()
                                                                    exit()
                                                                if x>=476 and x<=607 and y>=524 and y<=581:
                                                                    done2 = True
                                                                elif x>=767 and x<= 912 and y>=522 and y<=578:
                                                                    done2 = True
                                                    self.printar_loja(lista)
                                                else:
                                                    screen.blit(popup,(0,0))
                                                    texto = fonte36.render("Você não possui o dinheiro!",True, Branco)
                                                    screen.blit(texto,(490,380))
                                                    pygame.display.flip()
                                                    done2 = False
                                                    while done2 == False:
                                                        for event in pygame.event.get():
                                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                                if event.button == 1:
                                                                    x, y = pygame.mouse.get_pos()
                                                                if event.type == pygame.QUIT:
                                                                    pygame.quit()
                                                                    exit()
                                                                if x>=476 and x<=607 and y>=522 and y<=578:
                                                                    done2 = True
                                                                elif x>=767 and x<=912 and y>=522 and y<=578:
                                                                    done2 = True
                                                    self.printar_loja(lista)
                                            elif x>=767 and x<= 912 and y>=522 and y<=578:
                                                self.printar_loja(lista)
                                            if y<=104:
                                                if x>185 and x<=336:
                                                    self.mapa()
                                                elif x>336 and x<=514:
                                                    self.mochila()
                                                elif x>514 and x<=763:
                                                    self.habilidades()
                                                elif x>763 and x<=912:
                                                    self.forja()
                                                elif x>912 and x<= 1057:
                                                    self.loja()
                                                elif x>1057 and x<=1212:
                                                    self.quests()
                                                elif x>1212:
                                                    done = True
                                                    pygame.quit()
                                                    exit()
                            self.printar_loja(lista)                          
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def loja(self):
        done = False
        self.pagina_loja = 1
        imagem_principal = pygame.image.load("assets/interface/loja.png").convert_alpha()
        screen.blit(imagem_principal, (0,0))
        pygame.display.flip()
        lista = []
        lista.append(espada_madeira)
        lista.append(oculos_de_disfarce)
        lista.append(avental)
        lista.append(luvas_de_mendigo)
        lista.append(cueca_furada)
        lista.append(crocs)
        lista.append(espada_enferrujada)
        lista.append(touca)
        lista.append(camiseta)
        lista.append(braceletes)
        lista.append(sunga)
        lista.append(sandalhas)
        lista.append(espada_de_aco)
        lista.append(boina)
        lista.append(casaco)
        lista.append(luvas_sem_dedos)
        lista.append(bermuda_de_praia)
        lista.append(chinelos)
        lista.append(revolver_antigo)
        lista.append(bandana)
        lista.append(colete_de_couro)
        lista.append(luvas)
        lista.append(calca_moletom)
        lista.append(sapatos)
        lista.append(alabarda)
        lista.append(sombrero)
        lista.append(armadura_enferrujada)
        lista.append(luvas_de_pano)
        lista.append(calca_jeans)
        lista.append(tenis)
        self.printar_loja(lista)
        #( nome, tipo, ataque, defesa, valor_venda, quantidade, equipado, nivel, id, valor_compra):

    def mochila(self):
        imagem_principal = pygame.image.load("assets/interface/mochila.png").convert_alpha()
        screen.blit(imagem_principal, (0,0))
        pygame.display.flip()
        inventory.print_items()
        done = False
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        if y<=104:
                            if x>185 and x<=336:
                                self.mapa()
                            elif x>336 and x<=514:
                                self.mochila()
                            elif x>514 and x<=763:
                                self.habilidades()
                            elif x>763 and x<=912:
                                self.forja()
                            elif x>912 and x<= 1057:
                                self.loja()
                            elif x>1057 and x<=1212:
                                self.quests()
                            elif x>1212:
                                done = True
                                pygame.quit()
                                exit()
                        if x>1142 and x<1182 and y>654 and y<704:
                            inventory.aumentar_pagina()
                        elif x>201 and x< 245 and y>651 and y<705:
                            inventory.diminuir_pagina()
                        elif x>183 and x<1284 and y<649 and y>220:
                            inventory.info_item(x,y)
                        elif x>1212 and y<120:
                            pygame.quit()
                            exit()
                    elif event.button == 3 and x>183 and x<1284 and y<649 and y>220:
                        inventory.aprimorar_item(x,y)
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    def falas_quest(self,cod):
        if cod == 1:
            print("AAAAAAAAAA")
    def adicionar_quest(self,cod):
        mis = 0
        if cod == 2:
            mis = Quest("Missao2",999,armadura_medieval,"Endeavor","Chegue no nivel 3",1,cod,1)
            if per.nivel >= 3:
                mis.qnt_atual = 1
        elif cod == 101:
            mis = Quest("Todoroki parte 2",100,armadura_medieval,"Endeavor","Derrote o All Might usando gelo!",0,cod,0)
        elif cod == 102:
            mis = Quest("Todoroki parte 3",100,armadura_medieval,"Endeavor","Derrote o Bakugo!",0,cod,0)
        elif cod == 103:
            mis = Quest("Todoroki parte 4",100,armadura_medieval,"Endeavor","Aprimore 5 itens!",0,cod,0)
        elif cod == 104:
            mis = Quest("Todoroki parte 5",100,armadura_medieval,"Endeavor","Derrote Endeavor!",0,cod,0)
        elif cod == 201:
            mis = Quest("Gran Torino 2",10,armadura_medieval,"Gran Torino","Aprimore 5 itens!",0,cod,0)
        elif cod == 202:
            mis = Quest("Gran Torino 3",100,armadura_medieval,"Gran Torino","Chege no nivel x!",0,cod,0)
        elif cod == 203:
            mis = Quest("Gran Torino 4",10,armadura_medieval,"Gran Torino","Derrote os nomus!",0,cod,0)
        elif cod == 301:
            mis = Quest("Uraraka 2",10,armadura_medieval,"Uraraka","Adquira x dinheiros!",0,cod,0)
        if mis != 0 :
            self.lista_quests.append(mis)

        
    def dev_tool(self, image_url):
        dev = pygame.image.load(image_url).convert()
        pygame.image.save(screen, "var.jpg")
        teste = pygame.image.load("var.jpg").convert()
        x = 400
        y = 400
        screen.blit(teste,(0,0))
        screen.blit(dev,(x,y))
        a = 1
        done = False
        pygame.display.flip()
        while done == False:
            screen.blit(teste,(0,0)) 
            screen.blit(dev,(x,y))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        x -= 2
                    elif event.key == pygame.K_s:
                        y += 2
                    elif event.key == pygame.K_d:
                        x += 2
                    elif event.key == pygame.K_w:
                        y -= 2
                    elif event.key == pygame.K_e:
                        a = 2
                    print (x,y)
                if a == 2:
                    done = True      
    def atualizar_quests(self):
        y = 466
        self.quests_atuais = {}
        for x in self.lista_quests:        
            nome = fonte36.render(str(x.nome),True, Branco)
            if x.tipo == 1:
                nome_rect = nome.get_rect(center =(430,280))
                screen.blit(nome,(nome_rect))
                self.quests_atuais[x.nome]= 260
            elif x.tipo == 0:
                nome_rect = nome.get_rect(center =(430, y))
                screen.blit(nome,(nome_rect))
                y += 50
                self.quests_atuais[x.nome]= y

    def mapa(self):
        screen.fill(Preto)
        imagem = pygame.image.load("assets/interface/mapa1.png")
        screen.blit(imagem,(0,0))
        done = False
        level = fonte36.render(str(per.nivel), True, Branco)
        dinheiro = fonte36.render(str(per.dinheiro), True, Branco)
        level_rect = level.get_rect(center =(112,123))
        screen.blit(level,(level_rect))
        dinheiro_rect = dinheiro.get_rect(center =(112,164))
        screen.blit(dinheiro,(dinheiro_rect))
        lugar = ["Cidade","Campos da U.A","Unforeseen Simulation Joint","Festival de esportes da U.A","Exames Finais","The Beast's Forest","Esconderijo dos vilões"]
        desc = ["Ruas da cidade","Campo construído pela U.A","Área de simulações da U.A","Festival anual dos calouros","Campos de batalha personalizados da U.A","Floresta protegida por Pixie Bob","O esconderijo da Liga dos Vilões"]
        num = 250
        for a in lugar:
            local = fonte28.render(a, True, Branco)
            local_rect = local.get_rect(center = (400,num))
            screen.blit(local,(local_rect))
            num += 61
        num = 250
        for a in desc:
            desc = fonte28.render(a, True, Branco)
            desc_rect = desc.get_rect(center =(820,num))
            screen.blit(desc,(desc_rect))
            num += 61
        ir1 = pygame.image.load("assets/irverde.png")
        if self.mapa_disp>=2:
            ir2 = pygame.image.load("assets/irverde.png")
        else:
            ir2 = pygame.image.load("assets/ircinza.png")
        if self.mapa_disp>=3:
            ir3 = pygame.image.load("assets/irverde.png")
        else:
            ir3 = pygame.image.load("assets/ircinza.png")
        if self.mapa_disp>=4:
            ir4 = pygame.image.load("assets/irverde.png")
        else:
            ir4 = pygame.image.load("assets/ircinza.png")
        if self.mapa_disp>=5:
            ir5 = pygame.image.load("assets/irverde.png")
        else:
            ir5 = pygame.image.load("assets/ircinza.png")
        if self.mapa_disp>=6:
            ir6 = pygame.image.load("assets/irverde.png")
        else:
            ir6 = pygame.image.load("assets/ircinza.png")
        if self.mapa_disp>=7:
            ir7 = pygame.image.load("assets/irverde.png")
        else:
            ir7 = pygame.image.load("assets/ircinza.png")
        ir1_rect = ir1.get_rect(topleft= (1058,232))
        screen.blit(ir1,(ir1_rect))
        ir2_rect = ir2.get_rect(topleft=(1058,293))
        screen.blit(ir2,(ir2_rect))
        ir3_rect = ir3.get_rect(topleft=(1058,354))
        screen.blit(ir3,(ir3_rect))
        ir4_rect = ir4.get_rect(topleft=(1058,415))
        screen.blit(ir4,(ir4_rect))
        ir5_rect = ir5.get_rect(topleft=(1058,476))
        screen.blit(ir5,(ir5_rect))
        ir6_rect = ir6.get_rect(topleft=(1058,537))
        screen.blit(ir6,(ir6_rect))
        ir7_rect = ir7.get_rect(topleft=(1058,598))
        screen.blit(ir7,(ir7_rect))
        pygame.display.flip()

        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        if ir1_rect.collidepoint(x, y):
                            self.pagina_localizacao = 1
                            self.localizacao(1)
                        elif ir2_rect.collidepoint(x, y) and self.mapa_disp>=2:
                            self.pagina_localizacao = 1
                            self.localizacao(2)
                        elif ir3_rect.collidepoint(x,y) and self.mapa_disp>=3:
                            self.pagina_localizacao = 1
                            self.localizacao(3)
                        elif ir4_rect.collidepoint(x,y) and self.mapa_disp>=4:
                            self.pagina_localizacao = 1
                            self.localizacao(4)
                        elif ir5_rect.collidepoint(x,y) and self.mapa_disp>=5:
                            self.pagina_localizacao = 1
                            self.localizacao(5)
                        elif ir6_rect.collidepoint(x,y) and self.mapa_disp>=6:
                            self.pagina_localizacao = 1
                            self.localizacao(6)
                        elif ir7_rect.collidepoint(x,y) and self.mapa_disp>=7:
                            self.pagina_localizacao = 1
                            self.localizacao(7)
                        if y<=104:
                            if x>185 and x<=336:
                                self.mapa()
                            elif x>336 and x<=514:
                                self.mochila()
                            elif x>514 and x<=763:
                                self.habilidades()
                            elif x>763 and x<=912:
                                self.forja()
                            elif x>912 and x<= 1057:
                                self.loja()
                            elif x>1057 and x<=1212:
                                self.quests()
                            elif x>1212:
                                done = True
                                pygame.quit()
                                exit()
    def mostrar_inimigos(self,listainimigo,listadescricao):
        num = 250
        for a in listainimigo:
            inim = fonte28.render(a, True, Branco)
            inim_rect = inim.get_rect(center = (380,num))
            screen.blit(inim,(inim_rect))
            num += 61
        num = 250
        for a in listadescricao:
            desc = fonte28.render(a, True, Branco)
            desc_rect = desc.get_rect(center =(800,num))
            screen.blit(desc,(desc_rect))
            num += 61
        
    def localizacao (self, id):
        imagem = pygame.image.load("assets/interface/mapa2.png")
        screen.blit(imagem,(0,0))
        level = fonte36.render(str(per.nivel), True, Branco)
        dinheiro = fonte36.render(str(per.dinheiro), True, Branco)
        level_rect = level.get_rect(center =(112,123))
        screen.blit(level,(level_rect))
        dinheiro_rect = dinheiro.get_rect(center =(112,164))
        screen.blit(dinheiro,(dinheiro_rect))
        pygame.display.flip()
        try:
            var_lixo = self.pagina_localizacao 
        except:
            self.pagina_localizacao = 1
        if id == 1:
            if self.pagina_localizacao == 1:
                nom_inimigos = ["Bakugo Criança","Monstro de Lama","Gran Torino","Innsmouth","Gran Torino","Black Nomu","Nomu de 4 Olhos"]            
                desc = ["Nível 1","Nível 3","Nível 26","Nível 27","Nível 28","Nível 29","Nível 30"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=1:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1058,232))
                if per.nivel>=2:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1058,293))
                if per.nivel>=3:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1058,354))
                if per.nivel >=26 :
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1058,415))
                if per.nivel>=27:
                    ir5 = pygame.image.load("assets/irverde.png")
                else:
                    ir5 = pygame.image.load("assets/ircinza.png")
                ir5_rect = ir5.get_rect(topleft=(1058,476))
                if per.nivel>=28:
                    ir6 = pygame.image.load("assets/irverde.png")
                else:
                    ir6 = pygame.image.load("assets/ircinza.png")
                ir6_rect = ir6.get_rect(topleft=(1058,537))
                if per.nivel>=29:
                    ir7 = pygame.image.load("assets/irverde.png")
                else:
                    ir7 = pygame.image.load("assets/ircinza.png")
                ir7_rect = ir7.get_rect(topleft=(1058,598))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                screen.blit(ir5,(ir5_rect))
                screen.blit(ir6,(ir6_rect))
                screen.blit(ir7,(ir7_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=1142 and x<=1177 and y>=657 and y<=700 and self.pagina_localizacao<=1:
                                    self.pagina_localizacao += 1
                                    self.localizacao(1)
                                if ir1_rect.collidepoint(x, y):
                                    self.batalha("splash_enemy/bakugo_cri.png",3,1,10,0,"Bakugo Criança",{"D1":1,"D2":3,bau_nivel_1:1000})
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
            if self.pagina_localizacao == 2:
                nom_inimigos = ["Nomu de asas","Stain BOSS"]            
                desc = ["Nível 31","Nível 32"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=30:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=31:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=207 and x<=244 and y>=654 and y<=700 and self.pagina_localizacao>1:
                                    self.pagina_localizacao -= 1
                                    self.localizacao(1)
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
        elif id == 2:
            if self.pagina_localizacao>1:
                self.pagina_localizacao = 1
            if self.pagina_localizacao == 1:
                nom_inimigos = ["Vilão de 1 ponto","Vilão de 2 pontos","Bakugo","Iida"]            
                desc = ["Nível 4","Nível 5","Nível 6","Nível 7"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=4:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=5:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=6:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=7:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
        elif id == 3:
            if self.pagina_localizacao>1:
                self.pagina_localizacao = 1
            if self.pagina_localizacao == 1:
                nom_inimigos = ["Vilões da Invasão","Vilões Aquáticos","Kurogiri","Shigaraki","Nomu"]            
                desc = ["Nível 8","Nível 9","Nível 10","Nível 11","Nível 12"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=8:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=9:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=10:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=11:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                if per.nivel>=12:
                    ir5 = pygame.image.load("assets/irverde.png")
                else:
                    ir5 = pygame.image.load("assets/ircinza.png")
                ir5_rect = ir5.get_rect(topleft=(1060,476))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                screen.blit(ir5,(ir5_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
        elif id == 4:
            if self.pagina_localizacao>2:
                self.pagina_localizacao = 1
            if self.pagina_localizacao == 1:
                nom_inimigos = ["Batalha de Cavalaria","Bakugo","Shinso","Kaminari","Iida","Ashido","Tokoyami"]            
                desc = ["Nível 13","Nível 14","Nível 15","Nível 16","Nível 17","Nível 18","Nível 19"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=13:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=14:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=15:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=16:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                if per.nivel>=17:
                    ir5 = pygame.image.load("assets/irverde.png")
                else:
                    ir5 = pygame.image.load("assets/ircinza.png")
                ir5_rect = ir5.get_rect(topleft=(1060,476))
                if per.nivel>=18:
                    ir6 = pygame.image.load("assets/irverde.png")
                else:
                    ir6 = pygame.image.load("assets/ircinza.png")
                ir6_rect = ir6.get_rect(topleft=(1060,537))
                if per.nivel>=19:
                    ir7 = pygame.image.load("assets/irverde.png")
                else:
                    ir7 = pygame.image.load("assets/ircinza.png")
                ir7_rect = ir7.get_rect(topleft=(1060,598))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                screen.blit(ir5,(ir5_rect))
                screen.blit(ir6,(ir6_rect))
                screen.blit(ir7,(ir7_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=1142 and x<=1177 and y>=657 and y<=700 and self.pagina_localizacao<=1:
                                    self.pagina_localizacao += 1
                                    self.localizacao(4)
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
            elif self.pagina_localizacao == 2:
                nom_inimigos = ["Aoyama", "Aoyorozu","Kirishima","Bakugo","Todoroki","Todoroki BOSS"]            
                desc = ["Nível 20","Nível 21","Nível 22","Nível 23","Nível 24","Nível 25"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=20:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=21:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=22:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=23:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                if per.nivel>=24:
                    ir5 = pygame.image.load("assets/irverde.png")
                else:
                    ir5 = pygame.image.load("assets/ircinza.png")
                ir5_rect = ir5.get_rect(topleft=(1060,466))
                if per.nivel>=25:
                    ir6 = pygame.image.load("assets/irverde.png")
                else:
                    ir6 = pygame.image.load("assets/ircinza.png")
                ir6_rect = ir6.get_rect(topleft=(1060,527))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                screen.blit(ir5,(ir5_rect))
                screen.blit(ir6,(ir6_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=207 and x<=244 and y>=654 and y<=700 and self.pagina_localizacao>1:
                                    self.pagina_localizacao -= 1
                                    self.localizacao(4)
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
        elif id == 5:
            if self.pagina_localizacao>2:
                self.pagina_localizacao = 1
            if self.pagina_localizacao == 1:
                nom_inimigos = ["Cementoss","Ectoplasm","Power Loader","Aizawa","Thirteen","Nezu","Present Mic"]            
                desc = ["Nível 33","Nível 34","Nível 35","Nível 36","Nível 37","Nível 38","Nível 39"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=33:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=34:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=35:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=36:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                if per.nivel>=37:
                    ir5 = pygame.image.load("assets/irverde.png")
                else:
                    ir5 = pygame.image.load("assets/ircinza.png")
                ir5_rect = ir5.get_rect(topleft=(1060,476))
                if per.nivel>=38:
                    ir6 = pygame.image.load("assets/irverde.png")
                else:
                    ir6 = pygame.image.load("assets/ircinza.png")
                ir6_rect = ir6.get_rect(topleft=(1060,537))
                if per.nivel>=39:
                    ir7 = pygame.image.load("assets/irverde.png")
                else:
                    ir7 = pygame.image.load("assets/ircinza.png")
                ir7_rect = ir7.get_rect(topleft=(1060,598))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                screen.blit(ir5,(ir5_rect))
                screen.blit(ir6,(ir6_rect))
                screen.blit(ir7,(ir7_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=1142 and x<=1177 and y>=657 and y<=700 and self.pagina_localizacao<=1:
                                    self.pagina_localizacao += 1
                                    self.localizacao(5)
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
            elif self.pagina_localizacao == 2:
                nom_inimigos = ["Snipe", "Midnight","All Might BOSS"]            
                desc = ["Nível 40","Nível 41","Nível 42",]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=40:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=41:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=42:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=207 and x<=244 and y>=654 and y<=700 and self.pagina_localizacao>1:
                                    self.pagina_localizacao -= 1
                                    self.localizacao(5)
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
        elif id == 6:
            if self.pagina_localizacao>2:
                self.pagina_localizacao = 1
            if self.pagina_localizacao == 1:
                nom_inimigos = ["Pixie Bob","Magne","Spinner","Dabi","Muscular","Twice","Mustard"]            
                desc = ["Nível 43","Nível 44","Nível 45","Nível 46","Nível 47","Nível 48","Nível 49"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=43:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=44:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=45:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=46:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                if per.nivel>=47:
                    ir5 = pygame.image.load("assets/irverde.png")
                else:
                    ir5 = pygame.image.load("assets/ircinza.png")
                ir5_rect = ir5.get_rect(topleft=(1060,476))
                if per.nivel>=48:
                    ir6 = pygame.image.load("assets/irverde.png")
                else:
                    ir6 = pygame.image.load("assets/ircinza.png")
                ir6_rect = ir6.get_rect(topleft=(1060,537))
                if per.nivel>=49:
                    ir7 = pygame.image.load("assets/irverde.png")
                else:
                    ir7 = pygame.image.load("assets/ircinza.png")
                ir7_rect = ir7.get_rect(topleft=(1060,598))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                screen.blit(ir5,(ir5_rect))
                screen.blit(ir6,(ir6_rect))
                screen.blit(ir7,(ir7_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=1142 and x<=1177 and y>=657 and y<=700 and self.pagina_localizacao<=1:
                                    self.pagina_localizacao += 1
                                    self.localizacao(6)
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
            elif self.pagina_localizacao == 2:
                nom_inimigos = ["Moonfish", "Toga","Chainsaw Nomu","Mr. Compress"]            
                desc = ["Nível 50","Nível 51","Nível 52","Nível 53"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=50:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=51:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=52:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=53:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if x>=207 and x<=244 and y>=654 and y<=700 and self.pagina_localizacao>1:
                                    self.pagina_localizacao -= 1
                                    self.localizacao(6)
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit()
        elif id == 7:
            if self.pagina_localizacao>1:
                self.pagina_localizacao = 1
            if self.pagina_localizacao == 1:
                nom_inimigos = ["Kurogiri","Nomu","Dabi","Toga","Magne","Twice","All for One"]            
                desc = ["Nível 54","Nível 55","Nível 56","Nível 57","Nível 58","Nível 59","Nível 60"]
                self.mostrar_inimigos(nom_inimigos,desc)
                if per.nivel>=54:
                    ir1 = pygame.image.load("assets/irverde.png")
                else:
                    ir1 = pygame.image.load("assets/ircinza.png")
                ir1_rect = ir1.get_rect(topleft=(1060,232))
                if per.nivel>=55:
                    ir2 = pygame.image.load("assets/irverde.png")
                else:
                    ir2 = pygame.image.load("assets/ircinza.png")
                ir2_rect = ir2.get_rect(topleft=(1060,293))
                if per.nivel>=56:
                    ir3 = pygame.image.load("assets/irverde.png")
                else:
                    ir3 = pygame.image.load("assets/ircinza.png")
                ir3_rect = ir3.get_rect(topleft=(1060,354))
                if per.nivel>=57:
                    ir4 = pygame.image.load("assets/irverde.png")
                else:
                    ir4 = pygame.image.load("assets/ircinza.png")
                ir4_rect = ir4.get_rect(topleft=(1060,415))
                if per.nivel>=58:
                    ir5 = pygame.image.load("assets/irverde.png")
                else:
                    ir5 = pygame.image.load("assets/ircinza.png")
                ir5_rect = ir5.get_rect(topleft=(1060,476))
                if per.nivel>=59:
                    ir6 = pygame.image.load("assets/irverde.png")
                else:
                    ir6 = pygame.image.load("assets/ircinza.png")
                ir6_rect = ir6.get_rect(topleft=(1060,537))
                if per.nivel>=60:
                    ir7 = pygame.image.load("assets/irverde.png")
                else:
                    ir7 = pygame.image.load("assets/ircinza.png")
                ir7_rect = ir7.get_rect(topleft=(1060,598))
                screen.blit(ir1,(ir1_rect))
                screen.blit(ir2,(ir2_rect))
                screen.blit(ir3,(ir3_rect))
                screen.blit(ir4,(ir4_rect))
                screen.blit(ir5,(ir5_rect))
                screen.blit(ir6,(ir6_rect))
                screen.blit(ir7,(ir7_rect))
                pygame.display.flip()
                done = False
                while done is False:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if event.button == 1:
                                if y<=104:
                                    if x>185 and x<=336:
                                        self.mapa()
                                    elif x>336 and x<=514:
                                        self.mochila()
                                    elif x>514 and x<=763:
                                        self.habilidades()
                                    elif x>763 and x<=912:
                                        self.forja()
                                    elif x>912 and x<= 1057:
                                        self.loja()
                                    elif x>1057 and x<=1212:
                                        self.quests()
                                    elif x>1212:
                                        done = True
                                        pygame.quit()
                                        exit() 
    def quests(self):
        screen.fill(Preto)
        imagem = pygame.image.load("assets/interface/quest.png").convert()
        screen.blit(imagem,(0,0))
        self.atualizar_quests()
        done = False
        pygame.display.flip()
        if per.nivel>=3:
            for x in self.lista_quests:
                if x.cod == 2:
                    x.qnt_atual = 1
                    break
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        if x>=210 and x<=650:
                            check = False
                            qnt = 123
                            atu = 0
                            if y>=260 and y<= 300:
                                qnt = 0
                            elif y>=450 and y<= 490:
                                qnt = 1
                            elif y>=500 and y<= 540:
                                qnt = 2
                            elif y>=550 and y<= 590:
                                qnt = 3
                            elif y>=600 and y<= 640:
                                qnt = 4
                            elif y>=650 and y<= 690:
                                qnt = 5
                            if qnt >0:
                                for ob in self.lista_quests:
                                    if ob.tipo == 0:
                                        atu += 1
                                        if atu == qnt:
                                            objeto = ob
                                            check = True
                                            break
                            elif qnt == 0:
                                for ob in self.lista_quests:
                                    if ob.tipo == 1:
                                        objeto = ob
                                        check = True
                                        break
                            if check == True:
                                quest = pygame.image.load("assets/interface/quest.png").convert_alpha()
                                screen.blit(quest,(0,0))
                                self.atualizar_quests()
                                quest_atual = objeto
                                objetivo = fonte22.render(str(objeto.objetivo), True, Branco)
                                screen.blit(objetivo,(880-len(objeto.objetivo)*2.2, 260))
                                doador = fonte22.render(str(objeto.doador), True, Branco)
                                screen.blit(doador,(1090,670))
                                quantidade = fonte36.render(str(objeto.qnt_atual)+" / "+str(objeto.qnt),True,Branco)
                                p = len(str(objeto.qnt_atual)+" / "+str(objeto.qnt))
                                screen.blit(quantidade,(885-p*2.2,540))
                                recompensa = fonte36.render(str(objeto.recompensa),True,Branco)
                                coin = pygame.image.load("assets/dindin.png").convert_alpha()
                                screen.blit(coin,(854,630))
                                screen.blit(recompensa,(900,640))
                                if objeto.qnt_atual == objeto.qnt:
                                    check = pygame.image.load("assets/c.png").convert_alpha()
                                    screen.blit(check,(672,610))
                                    pygame.display.flip()
                        if x>672 and x<752 and y>610 and y<678:
                            for x in self.lista_quests:
                                if x.nome == quest_atual.nome and x.qnt_atual == x.qnt:
                                    per.dinheiro += x.recompensa
                                    self.adicionar_quest(x.cod+1)
                                    self.falas_quest(x.cod)
                                    a = x.itens
                                    print (a)
                                    inventory.add_item(a)
                                    print(str(per.dinheiro)+" Dinheiros")
                                    self.lista_quests.remove(x)
                                    self.quests()
                                    break
                        elif y<=104:
                            if x>185 and x<=336:
                                self.mapa()
                            elif x>336 and x<=514:
                                self.mochila()
                            elif x>514 and x<=763:
                                self.habilidades()
                            elif x>763 and x<=912:
                                self.forja()
                            elif x>912 and x<= 1057:
                                self.loja()
                            elif x>1057 and x<=1212:
                                self.quests()
                            elif x>1212:
                                done = True
                                pygame.quit()
                                exit()
                        pygame.display.flip()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    def menu_inicial(self):
        fundao = pygame.image.load("assets/interface/Tela de Inicio.jpg").convert()
        fundao_rect = fundao.get_rect(topleft=(0, 0))
        screen.blit(fundao, fundao_rect)
        done = False
        comecar = fonte70.render("Novo Jogo", True, Preto)
        carregar = fonte70.render("Carregar Jogo", True, Preto)
        info = fonte70.render("Informações", True, Preto)
        comecar_rect = comecar.get_rect(topleft=(90, 320))
        carregar_rect = carregar.get_rect(topleft=(90, 426))
        screen.blit(comecar, (comecar_rect))
        screen.blit(carregar, (carregar_rect))
        info_rect = info.get_rect(topleft=(90, 532))
        screen.blit(info, (info_rect))
        screen.blit(stop, (stop_rect))
        pygame.display.flip()

        while done is False:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:
                        if info_rect.collidepoint(x, y):
                            self.escurecer (True)
                            self.informacoes()
                        elif comecar_rect.collidepoint(x, y):
                            self.escurecer (True)
                            self.limpar_bd()
                            self.tela1()
                        elif carregar_rect.collidepoint(x, y):
                            self.carregar()
                            self.escurecer(True)
                            done = True
                            self.tela_principal()
                        elif stop_rect.collidepoint(x, y):
                            pygame.quit()
                            exit()
                            
                            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    pygame.display.flip()
    def tela1(self):   
        Midoriya = pygame.image.load("assets/Imagem1.png").convert_alpha()
        Bakugo = pygame.image.load("assets/Imagem2.png").convert_alpha()
        Todoroki = pygame.image.load("assets/Imagem3.png").convert_alpha()
        text = fonte22.render("Escolha seu personagem!", True, Preto)
        screen.fill(Branco)
        screen.blit(text, (555,30))
        todo_rect = Todoroki.get_rect(topleft=(1005, 213))
        mido_rect = Midoriya.get_rect(topleft=(575, 213))
        baku_rect = Bakugo.get_rect(topleft=(150, 213))
        screen.blit(Bakugo, (baku_rect))
        screen.blit(Midoriya, (mido_rect))
        screen.blit(Todoroki, (todo_rect))
        done = False
        screen.blit(deku_slogan, (1293,700))
        screen.blit(stop, (stop_rect))
        pygame.display.flip()
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.button == 1:
                        if baku_rect.collidepoint(x, y):
                            print ("Personagem selecionado: Bakugo! ")
                            self.persona = "Bakugo"
                            self.salvar()
                            self.tela2()
                        elif todo_rect.collidepoint(x, y):
                            print ("Personagem selecionado: Todoroki! ")
                            self.persona = "Todoroki"
                            self.salvar()
                            self.tela2()
                        elif mido_rect.collidepoint(x, y):
                            print ("Personagem selecionado: Midoriya! ")
                            self.persona = "Midoriya"
                            self.salvar()
                            self.tela2()
                        elif stop_rect.collidepoint(x, y):
                            pygame.quit()
                            exit()
    def tela2(self):
        done = False
        self.escurecer (True)
        fundo = pygame.image.load("assets/interface/tela.jpg").convert_alpha()
        screen.fill(Branco)
        fundo_rect = fundo.get_rect(topleft=(0,0))
        screen.blit(fundo, (fundo_rect))
        screen.blit(stop, (stop_rect))
        screen.blit(deku_slogan, (1293,700))
        pygame.display.flip()
        pygame.time.delay(1000)
        self.escurecer(True)
        self.tela_principal()
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if stop_rect.collidepoint(x, y):
                            pygame.quit()
                            exit()
    def timer(self,inimigo_url):
        for i in range(2):
            tempo = 2-i
            tempo = fonte50.render(str(tempo), True, Preto)
            self.atualizar_batalha(inimigo_url)
            screen.blit(tempo,(680,600))
            pygame.display.flip()
            time.sleep(1)
    def adicionar_objetivo(self,cod,quantidade):
        for x in self.lista_quests:
            if x.cod == cod:
                x.qnt_atual+=quantidade
                if x.qnt_atual>x.qnt:
                    x.qnt_atual = x.qnt
                    break
    def enemy_die(self, xp):
        per.acrescentar_xp(xp)
        self.adicionar_objetivo(1,1)
        self.tela_principal()
    def atualizar_batalha(self, inimigo_url):
            self.qnt = len(self.lista_spells)
            screen.fill(Cinza)
            pygame.draw.rect(screen,(Branco), (421,640, 524, 120))
            carta = pygame.image.load("assets/interface/teste.png").convert_alpha()
            if self.turno%2 == 0:
                self.hab1.set_alpha(255)
                if self.qnt>=2:
                    self.hab2.set_alpha(255)
                if self.qnt>=3:
                    self.hab3.set_alpha(255)
            else:
                self.hab1.set_alpha(150)
                if self.qnt>=2:
                    self.hab2.set_alpha(100)
                if self.qnt>=3:
                    self.hab3.set_alpha(100)
            if self.persona == 'Midoriya':
                classe = Midoriya = pygame.image.load("assets/Imagem1.png").convert_alpha()
            elif self.persona == 'Todoroki':
                classe = pygame.image.load("assets/Imagem3.png").convert_alpha()
            elif self.persona == "Bakugo":
                classe = pygame.image.load("assets/Imagem2.png").convert_alpha()
            inimigo = pygame.image.load(inimigo_url).convert_alpha()
            pygame.draw.rect(screen,Preto, (436,655, 90, 90))
            pygame.draw.rect(screen,Cinza_Escuro, (441,660, 80, 80))
            pygame.draw.rect(screen,Preto, (536,655, 90, 90))
            pygame.draw.rect(screen,Cinza_Escuro, (541,660, 80, 80))
            pygame.draw.rect(screen,Preto, (636,655, 90, 90))
            pygame.draw.rect(screen,Cinza_Escuro, (641,660, 80, 80))
            pygame.draw.rect(screen,Preto, (736,655, 90, 90))
            pygame.draw.rect(screen,Cinza_Escuro, (741,660, 80, 80))
            pygame.draw.rect(screen,Preto, (836,655, 90, 90))
            pygame.draw.rect(screen,Cinza_Escuro, (841,660, 80, 80))
            screen.blit(deku_slogan, (1293,700))
            screen.blit(stop, (stop_rect))
            screen.blit(carta,(30,100))
            screen.blit(carta,(800,100))
            classe_rect = classe.get_rect(center = (320,324))
            screen.blit(classe,(classe_rect))
            inimigo_rect = inimigo.get_rect(center=(1090,320))
            screen.blit(inimigo,(inimigo_rect))
            screen.blit(self.hab1, (self.hab1_rect))
            if self.qnt>=2:
                screen.blit(self.hab2, (self.hab2_rect))
            if self.qnt>=3:
                screen.blit(self.hab3, (self.hab3_rect))
            #screen.blit(self.hab3, (741, 660))
            #screen.blit(self.hab3, (841, 660))
            pygame.draw.rect(screen, (Branco), (165, 530, 310, 65))
            pygame.draw.rect(screen, (Branco), (935, 530, 310, 35))
            pygame.draw.rect(screen,self.cor_ali, (170,535, self.tamanho_barra_ali, 25))
            pygame.draw.rect(screen,self.cor_ini, (940,535, self.tamanho_barra_ini, 25))
            pygame.draw.rect(screen,(0,191,255), (170,565, self.tamanho_mana_ali, 25))
            self.vida_ali_texto_rect = self.vida_ali_texto.get_rect(center=(317,549))
            self.mana_ali_texto_rect = self.mana_ali_texto.get_rect(center=(317,579))
            self.vida_ini_texto_rect = self.vida_ini_texto.get_rect(center=(1090,549))
            screen.blit(self.vida_ali_texto,(self.vida_ali_texto_rect))
            screen.blit(self.mana_ali_texto,(self.mana_ali_texto_rect))
            screen.blit(self.vida_ini_texto,(self.vida_ini_texto_rect))
            self.texto_aliado = fonte24.render(self.texto_ali, True, Preto)
            self.texto_inimigo = fonte24.render(self.texto_ini, True, Preto)
            self.texto_aliado_rect = self.texto_aliado.get_rect(center = (710,400))
            self.texto_inimigo_rect = self.texto_inimigo.get_rect(center = (710,200))
            screen.blit(self.texto_aliado,(self.texto_aliado_rect))
            screen.blit(self.texto_inimigo,(self.texto_inimigo_rect))
            pygame.display.flip()
    def drop(self,dicionario):
        for key in dicionario:
            a = random.randint(0,1000)
            if key == "D1":
                dinheiro_min = dicionario[key]
                checker = True
            elif key == "D2":
                dinheiro_max = dicionario[key]
            elif a<=dicionario[key]:
                inventory.add_item(key)
        if checker == True:
            a = random.randint(0,100)
            if a <=20:
                din = random.randint(dinheiro_min,dinheiro_max)
                per.dinheiro += din
    def batalha(self, inimigo_url, vida_ini_total, dano_ini, xp, defesa_ini, ini_nome, dic):
        self.qnt = len(self.lista_spells)
        self.turno = 0
        var_atacar = 0
        self.texto_ali = ''
        self.texto_ini = ''
        done = False
        self.mana_ali = per.mana
        self.vida_ali = per.hp
        self.vida_ini = vida_ini_total
        a = 0
        while done is False:
            cont = 0
            crit = random.randint(0,100)
            if self.mana_ali > per.mana:
                self.mana_ali = per.mana
            if self.vida_ali > per.hp:
                self.vida_ali = per.hp
            if self.vida_ini > vida_ini_total:
                self.vida_ini = vida_ini_total
            if a == 0:
                self.hab1_rect = (105,105)
                self.hab2_rect = (105,105)
                self.hab3_rect = (105,105)
                self.hab4_rect = (105,105)
                self.hab5_rect = (105,105)
                for x in self.lista_spells:
                    if cont == 0:
                        self.nome_hab1 = x.nome
                        self.icone_hab1 = x.icone
                        self.ataque_hab1 = x.ataque
                        self.mana_hab1 = x.mana
                        self.id_hab1 = x.id
                        cont+=1
                    elif cont == 1:
                        self.nome_hab2 = x.nome
                        self.icone_hab2 = x.icone
                        self.ataque_hab2 = x.ataque
                        self.mana_hab2 = x.mana
                        self.id_hab2 = x.id
                        cont+=1
                    elif cont == 2:
                        self.nome_hab3 = x.nome
                        self.icone_hab3 = x.icone
                        self.ataque_hab3 = x.ataque
                        self.mana_hab3 = x.mana
                        self.id_hab3 = x.id
                        cont+=1
                    elif cont == 3:
                        self.nome_hab4 = x.nome
                        self.icone_hab4 = x.icone
                        self.ataque_hab4 = x.ataque
                        self.mana_hab4 = x.mana
                        self.id_hab4 = x.id
                        cont+=1
                    elif cont == 4:
                        self.nome_hab5 = x.nome
                        self.icone_hab5 = x.icone
                        self.ataque_hab5 = x.ataque
                        self.mana_hab5 = x.mana
                        self.id_hab5 = x.id
                a = 1
            self.hab1 = pygame.image.load(self.icone_hab1).convert_alpha()
            self.hab1_rect = self.hab1.get_rect(topleft=(441, 660))
            if self.qnt>=2:
                self.hab2 = pygame.image.load(self.icone_hab2).convert_alpha()
                self.hab2_rect = self.hab2.get_rect(topleft=(541, 660))
            if self.qnt>=3:
                self.hab3 = pygame.image.load(self.icone_hab3).convert_alpha()
                self.hab3_rect = self.hab3.get_rect(topleft=(641, 660))
            self.vida_ini_texto = fonte22.render(str(self.vida_ini)+str("/ "+str(vida_ini_total)), True, Preto)
            self.vida_ali_texto = fonte22.render(str(self.vida_ali)+str("/ "+str(per.hp)), True, Preto)
            self.mana_ali_texto = fonte22.render(str(self.mana_ali)+str("/ "+str(per.mana)), True, Preto)
            self.tamanho_mana_ali = round((self.mana_ali / per.mana) * 300)
            self.tamanho_barra_ali = round((self.vida_ali / per.hp) * 300)
            self.tamanho_barra_ini = round((self.vida_ini / vida_ini_total) * 300)
            if self.tamanho_barra_ini >150:
                self.cor_ini = (0,128,0)
            elif self.tamanho_barra_ini >100:
                self.cor_ini = (255,255,0)
            else:
                self.cor_ini = (255, 29, 11)
            if self.tamanho_barra_ali >150:
                self.cor_ali = (0,128,0)
            elif self.tamanho_barra_ali >100:
                self.cor_ali = (255,255,0)
            else:
                self.cor_ali = (255, 29, 11)
            if self.vida_ini <= 0:
                self.drop(dic)
                self.enemy_die(xp)
            elif self.vida_ali <= 0:
                self.menu_inicial()
            self.atualizar_batalha(inimigo_url)
            if self.turno%2 == 1:
                self.hab1.set_alpha(128)
                if self.qnt>=2:
                    self.hab2.set_alpha(128)
                if self.qnt>=3:
                    self.hab3.set_alpha(128)
                desv = random.randint(0,100)
                crit = random.randint(0,100)
                dano = round(dano_ini - (per.defesa*10//15))
                dano2 = dano_ini/100*10
                if dano < dano2:
                    dano = dano2
                dano = round(random.randint(int(round(dano - dano/100*20)), int(round(dano + dano/100*20))))
                self.timer(inimigo_url)
                if desv<= per.desv_chance:
                    self.texto_ini = 'Você Desviou!'
                elif crit<=30:
                    self.texto_ini = ini_nome+" te deu "+str(dano)+' de dano com um Acerto Crítico!'
                    self.vida_ali -= dano*2
                else:
                    self.texto_ini = ini_nome+" te deu "+str(dano)+' de dano!'
                    self.vida_ali -= dano
                self.mana_ali += 10
                self.turno += 1
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if stop_rect.collidepoint(x, y): 
                            pygame.quit()
                            exit()
                        #DANO
                        if self.hab1_rect.collidepoint(x,y) and self.mana_ali >= self.mana_hab1 and self.turno%2 == 0:
                            dano = round(self.ataque_hab1 + per.ataque - defesa_ini*2)
                            dano = round(random.randint(round(dano - dano/100*20), round(dano + dano/100*20)))
                            var_atacar = 1
                            self.mana_ali -= self.mana_hab1
                            self.turno += 1
                        elif self.hab2_rect.collidepoint(x,y) and self.mana_ali >= self.mana_hab2 and self.turno%2 == 0:
                            dano = round(self.ataque_hab2 + per.ataque - defesa_ini*2)
                            dano = round(random.randint(round(dano - dano/100*20), round(dano + dano/100*20)))
                            var_atacar = 1
                            self.mana_ali -= self.mana_hab2
                            self.turno += 1
                        elif self.hab3_rect.collidepoint(x,y) and self.mana_ali >= self.mana_hab3 and self.turno%2 == 0:
                            dano = round(self.ataque_hab3 + per.ataque - defesa_ini*2)
                            dano = round(random.randint(round(dano - dano/100*20), round(dano + dano/100*20)))
                            var_atacar = 1
                            self.mana_ali -= self.mana_hab3
                            self.turno += 1
                        elif self.hab4_rect.collidepoint(x,y) and self.mana_ali >= self.mana_hab4 and turno%2== 0:
                            dano = round(self.ataque_hab4 + per.ataque - defesa_ini*2)
                            dano = round(random.randint(round(dano - dano/100*20), round(dano + dano/100*20)))
                            var_atacar = 1
                            self.mana_ali -= self.mana_hab4
                            self.turno += 1
                        elif self.hab5_rect.collidepoint(x,y) and self.mana_ali >= self.mana_hab5 and turno%2== 0:
                            dano = round(self.ataque_hab5 + per.ataque - defesa_ini*2)
                            dano = round(random.randint(round(dano - dano/100*20), round(dano + dano/100*20)))
                            var_atacar = 1
                            self.mana_ali -= self.mana_hab5
                            self.turno += 1
                        if var_atacar == 1:
                            desv = random.randint(0,100)
                            if dano < 0:
                                dano = 0
                            if desv <= 20:
                                self.texto_ali= ini_nome+" desviou do seu ataque!"
                            elif crit <= per.crit_chance:
                                self.vida_ini -= dano*2
                                self.texto_ali='Você deu '+str(dano*2)+' de dano em '+ini_nome+' com um Acerto Crítico!'
                            else:
                                self.texto_ali='Você deu '+str(dano)+' de dano em '+ini_nome
                                self.vida_ini -= dano
                            self.mana_ali += 10
                            var_atacar = 0
            clock.tick(60)
            self.texto_aliado = fonte22.render(self.texto_ali, True, Preto)
            self.texto_aliado_rect = self.texto_aliado.get_rect(center=(400,400))
            self.texto_inimigo = fonte22.render(self.texto_ini, True, Preto)
            self.texto_inimigo_rect = self.texto_inimigo.get_rect(center=(600,600))                 
            pygame.display.flip()                        

inventory = Inventory()
per = Personagem("Teste")


x = 1
#Armas)
espada_madeira = Item("Espada de Madeira", "Arma", 2, 0, 1, 1, 0, 1, 101,5,0)
espada_enferrujada = Item("Espada enferrujada","Arma",4,2,5,1,0,2,102,25,0)
espada_de_aco = Item("Espada de aço","Arma",8,4,20,1,0,4,103,100,0)
revolver_antigo = Item("Revolver Antigo","Arma",20,0,50,1,0,8,104,250,0)
alabarda = Item("Alabarda","Arma",45,0,150,1,0,12,105,1000,0)
katana = Item("Katana","Arma",80,10,300,1,0,16,106,0,0)
fuzil = Item("Fuzil","Arma",180,0,450,1,0,20,107,0,0)
excalibur = Item("Excalibur","Arma",290,40,800,1,0,25,108,0,0)
kusanagi = Item("Kusanagi","Arma",450,60,1200,1,0,30,109,0,0)
muramasa = Item("Muramasa","Arma",700,80,1750,1,0,35,110,0,0)
noisy_cricket = Item("Noisy Cricket","Arma",1100,0,2500,1,0,40,111,0,0)
tridente_de_poseidon = Item("Tridente de Poseidon","Arma",1600,140,3500,1,0,44,112,0,0)
masamune = Item("Masamune","Arma",2200,200,5500,1,0,48,113,0,0)
tentetsutou = Item("Tentetsutou","Arma",3100,350,8000,1,0,52,114,0,0)
durendal = Item("Durendal","Arma",4200,300,15000,1,0,56,115,0,0)
mjolnir = Item("Mjolnir","Arma",5600,600,35000,1,0,60,116,0,0)
punhos_all = Item("Punhos do All Might","Arma",8000,1000,120000,1,0,60,117,0,0)
#Elmos)
oculos_de_disfarce = Item("Óculos de disfarce", "Elmo", 0, 1, 1, 1, 0, 1, 201, 5,0)
touca = Item("Touca","Elmo",0,2,5,1,0,2,202,25,0)
boina = Item("Boina","Elmo",0,3,20,1,0,4,203,100,0)
bandana = Item("Bandana","Elmo",0,5,50,1,0,8,204,250,0)
sombrero = Item("Sombrero","Elmo",0,8,150,1,0,12,205,1000,0)
balaclava = Item("Balaclava","Elmo",0,14,300,1,0,16,206,0,0)
mascara_de_gas = Item("Máscara de Gás","Elmo",0,18,450,1,0,20,207,0,0)
capacete_de_seguranca = Item("Capacete de Segurança","Elmo",0,35,800,1,0,25,208,0,0)
capacete_enferrujado = Item("Capacete Enferrujado","Elmo",0,70,1200,1,0,30,209,0,0)
elmo_de_ferro = Item("Elmo de Ferro","Elmo",0,90,1750,1,0,35,210,0,0)
capacete_medieval = Item("Capacete Medieval","Elmo",0,200,2500,1,0,10,211,0,0)
elmo_de_aco = Item("Elmo de Aço","Elmo",0,320,3500,1,0,44,212,0,0)
elmo_de_ouro = Item("Elmo de Ouro","Elmo",0,530,5500,1,0,48,213,0,0)
elmo_demoniaco = Item("Elmo Demoníaco","Elmo",0,720,8000,1,0,52,214,0,0)
capacete_de_sauron = Item("Capacete de Sauron","Elmo",0,800,15000,1,0,56,215,0,0)
oculos_de_eraser_head = Item("Óculos de Eraser Head","Elmo",0,1100,35000,1,0,60,216,0,0)
elmo_all = Item("Elmo do All Might","Elmo",0,1800,120000,1,0,60,217,0,0)
#Armaduras)
avental = Item("Avental", "Armadura", 0, 1, 1, 1, 0, 1, 301, 5,0)
camiseta = Item("Camiseta","Armadura",0,2,5,1,0,2,302,25,0)
casaco = Item("Casaco","Armadura",0,3,20,1,0,4,303,100,0)
colete_de_couro = Item("Colete de couro","Armadura",0,5,50,1,0,8,304,250,0)
armadura_enferrujada = Item("Armadura Enferrujada","Armadura",0,10,150,1,0,12,305,1000,0)
colete_balas = Item("Colete à Prova de Balas","Armadura",0,19,300,1,0,16,306,0,0)
peitoral_de_ferro = Item("Peitoral de Ferro","Armadura",0,23,450,1,0,20,307,0,0)
cota_de_malha = Item("Cota de Malha","Armadura",0,45,800,1,0,25,308,0,0)
peitoral_de_aco = Item("Peitoral de Aço","Armadura",0,80,1200,1,0,30,309,0,0)
peitoral_de_ouro = Item("Peitoral de Ouro","Armadura",0,130,1750,1,0,35,310,0,0)
armadura_medieval = Item("Armadura Medieval","Armadura",0,240,2500,1,0,40,311,0,0)
magic_plate_armor = Item("Magic Plate Armor","Armadura",0,380,3500,1,0,44,312,0,0)
peitoral_demoniaco = Item("Peitoral Demoníaco","Armadura",0,590,5500,1,0,48,313,0,0)
colete_de_kevlar = Item("Colete de Kevlar","Armadura",0,780,8000,1,0,52,314,0,0)
armadura_mk_50 = Item("Armadura MK-50","Armadura",0,1000,15000,1,0,56,315,0,0)
torso_do_muscular = Item("Torso do Muscular","Armadura",0,1500,35000,1,0,60,316,0,0)
peitoral_all = Item("Peitoral do All Might","Armadura",0,2500,120000,1,0,60,317,0,0)
#Luvas)
luvas_de_mendigo = Item("Luvas de Mendigo", "Luvas", 0, 1, 1, 1, 0, 1, 401, 5,0)
braceletes = Item("Braceletes","Luvas",0,2,5,1,0,2,402,25,0)
luvas_sem_dedos = Item("Luvas sem dedos","Luvas",0,3,20,1,0,4,403,100,0)
luvas = Item("Luvas","Luvas",0,4,50,1,0,8,404,250,0)
luvas_de_pano = Item("Luvas de pano","Luvas",0,6,150,1,0,12,405,1000,0)
luvas_taticas = Item("Luvas Táticas","Luvas",0,10,300,1,0,16,406,0,0)
luvas_de_boxe = Item("Luvas de Boxe","Luvas",0,13,450,1,0,20,407,0,0)
luvas_reforcadas = Item("Luvas Reforçadas","Luvas",0,20,800,1,0,25,408,0,0)
luvas_medievais = Item("Luvas Medievais","Luvas",0,30,1200,1,0,30,409,0,0)
soco_ingles = Item("Soco Inglês","Luvas",0,50,1750,1,0,35,410,0,0)
bagh_nakh = Item("Bagh Nakh","Luvas",0,100,2500,1,0,40,411,0,0)
lamina_oculta = Item("Lâmina Oculta","Luvas",0,170,3500,1,0,44,412,0,0)
luvas_demoniacas = Item("Luvas Demoníacas","Luvas",0,260,5500,1,0,48,413,0,0)
garras_do_wolwerine = Item("Garras do Wolwerine","Luvas",0,333,8000,1,0,52,414,0,0)
luvas_do_deku = Item("Luvas do Deku","Luvas",0,420,15000,1,0,56,415,0,0)
manopla_do_infinito = Item("Manopla do Infinito","Luvas",0,580,35000,1,0,60,416,0,0)
braceletes_all = Item("Braceltes do All Might","Luvas",0,700,120000,1,0,60,417,0,0)
#Calcas)
cueca_furada = Item("Cueca Furada","Calça",0,1,1,1,0,1,501,5,0)
sunga = Item("Sunga","Calça",0,2,5,1,0,2,502,25,0)
bermuda_de_praia = Item("Bermuda de praia","Calça",0,3,20,1,0,4,503,100,0)
calca_moletom = Item("Calça Moletom","Calça",0,5,50,1,0,8,504,250,0)
calca_jeans = Item("Calça jeans","Calça",0,8,150,1,0,12,505,1000,0)
joelheira = Item("Joelheira","Calça",0,14,300,1,0,16,506,0,0)
calca_de_couro = Item("Calça de Couro","Calça",0,16,450,1,0,20,507,0,0)
calca_medieval = Item("Calça Medieval","Calça",0,29,800,1,0,25,508,0,0)
calca_de_ferro = Item("Calça de Ferro","Calça",0,45,1200,1,0,30,509,0,0)
calca_de_aco = Item("Calça de Aço","Calça",0,67,1750,1,0,35,510,0,0)
pernas_do_deku = Item("Pernas do Deku","Calça",0,130,2500,1,0,40,511,0,0)
cinto_do_batman = Item("Cinto do Batman","Calça",0,220,3500,1,0,44,512,0,0)
calca_demoniaca = Item("Calça Demoníaca","Calça",0,332,5500,1,0,48,513,0,0)
pernas_do_gran_torino = Item("Pernas do Gran Torino","Calça",0,410,8000,1,0,52,514,0,0)
cinto_do_aoyama = Item("Cinto do Aoyama","Calça",0,520,15000,1,0,56,515,0,0)
pernas_do_iida = Item("Pernas do Iida","Calça",0,750,35000,1,0,60,516,0,0)
pernas_all = Item("Pernas do All Might","Calça",0,1250,120000,1,0,60,517,0,0)
#Botas)
crocs = Item("Crocs","Bota",0,1,1,1,0,1,601,5,0)
sandalhas = Item("Sandalhas","Bota",0,2,5,1,0,2,602,25,0)
chinelos = Item("Chinelos","Bota",0,3,20,1,0,4,603,100,0)
sapatos = Item("Sapatos","Bota",0,4,50,1,0,8,604,250,0)
tenis = Item("Tênis","Bota",0,7,150,1,0,12,605,1000,0)
botas = Item("Botas","Bota",0,12,300,1,0,16,606,0,0)
coturno = Item("Coturno","Bota",0,16,450,1,0,20,607,0,0)
botas_de_trilha = Item("Botas de Trilha","Bota",0,25,800,1,0,25,608,0,0)
botas_medievais = Item("Botas Medievais","Bota",0,38,1200,1,0,30,609,0,0)
calcados_de_ferro = Item("Calçados de Ferro","Bota",0,60,1750,1,0,35,610,0,0)
calcados_de_aco = Item("Calçados de Aço","Bota",0,120,2500,1,0,40,611,0,0)
botas_reforcadas = Item("Botas Reforçadas","Bota",0,205,3500,1,0,44,612,0,0)
calcados_de_hatsume = Item("Calçados de Hatsume","Bota",0,315,5500,1,0,48,613,0,0)
botas_de_hermes = Item("Botas de Hermes","Bota",0,400,8000,1,0,52,614,0,0)
botas_demoniacas = Item("Botas Demoníacas","Bota",0,500,15000,1,0,56,615,0,0)
botas_do_deku = Item("Botas do Deku","Bota",0,710,35000,1,0,60,616,0,0)
botas_all = Item("Botas do All Might","Bota",0,1000,120000,1,0,60,617,0,0)

inventory.add_item(espada_madeira)
inventory.add_item(Item("Madeira", "Material", 0, 0, 50, 1, 0, 0, 0, 0,0))
inventory.add_item(Item("Mistura", "Material", 0, 0, 80, 1, 0, 0, 0, 5,0))
inventory.add_item(Item("Cola", "Material", 0, 0, 80, 1, 0, 0, 6, 0,0))
inventory.add_item(Item("Cola", "Material", 0, 0, 80, 1, 0, 0, 6, 0,0))
bau_nivel_1 = Item("Baú nível 1", "Baú",0,0,0,1,0,0,1,0,0)
lista = (espada_madeira,oculos_de_disfarce,avental,luvas_de_mendigo,cueca_furada,crocs)
bau_nivel_1.definir_item_drop(lista)
bau_nivel_2 = Item("Baú nível 2", "Baú",0,0,0,1,0,0,2,0,0)
lista = (espada_madeira,oculos_de_disfarce,avental,luvas_de_mendigo,cueca_furada,crocs)
bau_nivel_2.definir_item_drop(lista)
bau_nivel_4 = Item("Baú nível 4", "Baú",0,0,0,1,0,0,3,0,0)
bau_nivel_8 = Item("Baú nível 8", "Baú",0,0,0,1,0,0,4,0,0)
bau_nivel_16 = Item("Baú nível 16", "Baú",0,0,0,1,0,0,5,0,0)
bau_nivel_20 = Item("Baú nível 20", "Baú",0,0,0,1,0,0,6,0,0)
bau_nivel_25 = Item("Baú nível 25", "Baú",0,0,0,1,0,0,7,0,0)
bau_nivel_30 = Item("Baú nível 30", "Baú",0,0,0,1,0,0,8,0,0)
bau_nivel_35 = Item("Baú nível 35", "Baú",0,0,0,1,0,0,9,0,0)
bau_nivel_40 = Item("Baú nível 40", "Baú",0,0,0,1,0,0,10,0,0)
bau_nivel_44 = Item("Baú nível 44", "Baú",0,0,0,1,0,0,11,0,0)
bau_nivel_48 = Item("Baú nível 48", "Baú",0,0,0,1,0,0,12,0,0)
bau_nivel_52 = Item("Baú nível 52", "Baú",0,0,0,1,0,0,13,0,0)
bau_nivel_56 = Item("Baú nível 56", "Baú",0,0,0,1,0,0,14,0,0)
bau_nivel_60 = Item("Baú nível 60", "Baú",0,0,0,1,0,0,15,0,0)
while x<3:
    inventory.add_item(armadura_enferrujada)
    x += 1

jogo = Game()
jogo.menu_inicial()
#(nome, tipo, ataque, defesa, valor_venda, quantidade, equipado, nivel, id, preco_compra)