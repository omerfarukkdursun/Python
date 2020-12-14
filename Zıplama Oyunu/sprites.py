from settings import *
import pygame
vector = pygame.math.Vector2


class mermi(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = ates #genişlik ve yükseliği tuple olarak atadık
        #self.image.fill((0,255,0))#renk değerini verdik.
        self.rect = self.image.get_rect()#hitboxını belirtiyoruz ve eşitleyerek resim boyutuyla rect boyutu aynı olsun
        self.rect.x = x
        self.rect.y = y



class Player(pygame.sprite.Sprite): #Hareket eden objeyi oluşturuyoruz. Bir alt sınıf oluşturuyoruz.
    def __init__(self,oyun):
        super().__init__()
        self.oyun = oyun
        self.image = fisek.convert() #Yüzey oluşturuyoruz.
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2) #Parçacığın kordinatlarını belirtiyoruz.
        self.hiz = vector(0,0) #x ve y kordinatlarının başlangıçtaki hız değeri
        self.ivme = vector(0,0.5) # Aşşağıya doğru 0,5 ile ivmeleniyor.


    def zipla(self):
        self.rect.y += 1 #Kutumuzu alta kaydırdığımızda temas ediyorsa altta bir platform var demektir.
        temasVarmi = pygame.sprite.spritecollide(self,self.oyun.platforms,False)
        #1. parametre playerımız, 2. parametre kutumuz, çarpmada yok olmadığı için false veriyoruz.
        if temasVarmi:
            self.hiz.y -= 15 #Temas ediyorsak bir platforma zıplayalım ve hızımız 15 olsun.

    def atesEt(self,mermi):
        mermi.rect.x = self.rect.x+20 #Merminin başlangıç yeri playerın tam ortaasına gelmesi iç,n +20 dedik
        mermi.rect.y = self.rect.top #fişeğin en üst noktasına eşitledik

    def update(self, *args): #Hareket işlemlerini yapıyoruz.
        keys = pygame.key.get_pressed() #tuple tutuyor ve tuşa basıp basmadığımızı tutuyoruz.


        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]: #Sağa Yada Sola tıkladıysa gir
            if keys[pygame.K_RIGHT]: #sağa tıkladıysa
                if self.hiz.x < 7:# max hızımız 7 olana kadar artacak ivmeli bir şekilde artacak.
                    self.ivme.x = 0.5
                else:
                    self.ivme.x = 0

            if keys[pygame.K_LEFT]:
                if self.hiz.x > -7: #Aynı işlemi -7 ye kadar yaptık
                    self.ivme.x = -0.5
                else:
                    self.ivme.x = 0

            self.hiz.x += self.ivme.x #x ekseninde ivmeli bir şekilde hızlandırıcaz.

        else: #herhangi bir tuşa basmadığında yavaşça durdurma kısmı.
            if self.hiz.x > 0: #hızım 0 dan büyükse yavaşsa durduruyoruz.
                self.hiz.x -= 0.2
            if self.hiz.x < 0: #hızım 0 dan küçükse 0.2 ivme ile artsın
                self.hiz.x += 0.2

        self.hiz.y += self.ivme.y #(yer çekimi) y ekseninde ivmeli bir şekilde hızlandırıyoruz.

        self.rect.x += self.hiz.x
        self.rect.y += self.hiz.y


        if self.rect.x > WIDTH: #sağdan çıkınca soldan tekrar başlıyor soldan çıkınca sağdan tekrar başlıyor.
            self.rect.x = 0

        if self.rect.right < 0:
            self.rect.right = WIDTH

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):#kordinatları ve boyutlarını alması adına parametre aldık.
        super().__init__()
        self.image = platform #genişlik ve yükseliği tuple olarak atadık
        #self.image.fill((0,255,0))#renk değerini verdik.
        self.rect = self.image.get_rect()#hitboxını belirtiyoruz ve eşitleyerek resim boyutuyla rect boyutu aynı olsun
        self.rect.x = x #Verdiğimiz x ve parametresine göre platformumuz oluşacak
        self.rect.y = y

class Dusman(pygame.sprite.Sprite):
    def __init__(self, oyun, platform):
        super().__init__()
        self.oyun = oyun
        self.platform = platform
        self.image = bomba
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform.rect.midtop

    def update(self, *args):
        self.rect.midbottom = self.platform.rect.midtop # sürekli platformun orasında oluşsun

        if not self.oyun.platforms.has(self.platform): #Platform yoksa düşmanda olmasın
            self.kill()