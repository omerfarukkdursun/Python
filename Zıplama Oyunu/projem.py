import pygame,random,sys
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pygame.init() #Oyunun başladığını söylüyoruz.
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Ekran objesi üretiyoruz.
        pygame.display.set_caption(TITLE) #Oyunun title değeri
        self.clock = pygame.time.Clock() #fps ayarımızı sağlıyor

        self.running = True #Oyunun devam ettiğini belirtiyor.
        self.show = True
        self.skor = 0
        self.maksimumSkor = 0



    def new(self): #oyun çalışınca
        self.all_sprites = pygame.sprite.Group() #tüm spritesları tuttuğumuz bir yapı
        self.platforms = pygame.sprite.Group()#Platformumuz da sprite group objesi olacak.
        self.Dusmanlar = pygame.sprite.Group()
        p1 = Platform(WIDTH / 2 - 50, 480,1,1)  # Oyuncumuzun düşeceği kutuyu oluşturduk.
        p2 = Platform(300, WIDTH / 2 - 50,1,1)
        p3 = Platform(50, 400,1,1)
        p4 = Platform(400, 300,1,1)
        p5 = Platform(50, 40,1,1)
        p6 = Platform(420, 120,1,1)



        self.platforms.add(p1) #Gruplara platformları ekliyoruz.
        self.platforms.add(p2)
        self.platforms.add(p3)
        self.platforms.add(p4)
        self.platforms.add(p5)
        self.platforms.add(p6)


        self.player = Player(self) #Zıplamalarda temasın olup olmaduğunı kontrol etmek için objeyi gönderiyoruz.

        self.bizim_mermi = mermi(500,500,1,1) #mermiyi ekleme x ve y değerleri haritada görünmesin diye böyle değer verdik.

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.bizim_mermi)
        self.all_sprites.add(p1) #her program çalışıtığı zaman platform eklensin O yüzden all spritslara ekliyoruz.
        self.all_sprites.add(p2)
        self.all_sprites.add(p3)
        self.all_sprites.add(p4)
        self.all_sprites.add(p5)
        self.all_sprites.add(p6)

        self.run()

    def run(self):
        self.playing = True #Oynamaya devam ettiği sürece
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update() #Her değişimi yenileme işlemi


    def update(self):
        self.all_sprites.update() #tüm değerleri update ediyor.

        if not self.bizim_mermi.rect.x == 500: #eğer mermi 500 de değilse yukarı doğru hareket et.
            self.bizim_mermi.rect.y -=8


        if self.player.hiz.y > 0: #aşşağı düşüyorsa çarpmayı kontrol ediyoruz

            #alttaki fonksiyon ilk olarak bir tane sprite ojbesi alıyor ve platforma çarpıyor mu diye bakıyor
            #3.parametre dokill= çarpma olduğunda yok olma işlemi olsun mu diye bakıyor.
            carpismalar = pygame.sprite.spritecollide(self.player, self.platforms, dokill=False)

            if carpismalar:
                if carpismalar[0].rect.center[1] +8 > self.player.rect.bottom:
                #+8 tam orta nokta olmasında biraz daha aşşağısı olsun demektir.
                #centerın y değeri olmadığı için 1 diyorum orada zaten y değeri tutuluyor.
                #Ayrıca platformun yarısı benim playerımın geçiyor mu diye kontrol ediyoruz
                #Bu kontrolü yapmazsak zıplayan cismin ucu platforma değdiğinde çarpışma olur ve yukarı çıkar.
                #Çarpışma varsa buraya girer. Çarpışma olduğunda bir list objesi döndü.
                    self.player.hiz.y = 0 #hızımızı dikey düzlemde çarpma varsa durdurduk.
                    self.player.rect.bottom = carpismalar[0].rect.top
            # carpismaların ilk indexine cismin üstüne sabitlersek iç içse geçme olmaz. Yani platform ile oyuncu iç içe geçmedi


        if self.player.rect.top<HEIGHT /4:#Karasel cismin üst tarafı ekranın belirli sınırı geçince ayarlar yapıcaz.
            self.player.rect.y += max(abs(self.player.hiz.y),3)
            #kutuyuda aşşağıya doğru kaydırmamız lazım. Maxın görevi kutu duruyorkende hızı 3 yapıp kutuları aşşağı çekmek
            #Yani ekranın %75 lik uzunluğunun üstüne çıktığımda ekran aşşağıya kayacak.
            for plat in self.platforms: #tüm platformlarda gezdik
                plat.rect.y += max(abs(self.player.hiz.y),3)
                if plat.rect.top >= HEIGHT: #platformun üst kısmı yükseklikten büyükse bu platformu öldürürüz.
                    plat.kill()
                    self.skor += 10

        değme = pygame.sprite.spritecollide(self.player,self.Dusmanlar,True) #Düşmana Çarpma
        if değme:
            self.playing = False
            self.skor=0
            self.maksimumSkor = self.skor


        oldurme = pygame.sprite.spritecollide(self.bizim_mermi, self.Dusmanlar, True) #Mermiyle düşman öldürme


        if self.player.rect.top > HEIGHT: #Karakterin üst noktası platformandan büyükse yani düşmüşse
            for sprite in self.all_sprites: #Tüm spriteları gez.
                sprite.rect.y -= max(self.player.hiz.y, 15) #platformları yukarı kaydır
                if sprite.rect.bottom < 0: #Yukarı çıkan platformları öldürüyoruz
                    sprite.kill()

        if len(self.platforms) == 0: #Plartformlar 0 olduğunda oyun bitmiştir.
            #Oyun ilk açıldığında txt dosyam olmayacak bu yüzden hata verir.
            #Bu yüzden try catch leri kullanmamız gerekir.
            try:
                with open("skor.txt","r") as dosya:
                    kayıtlıSkor = int(dosya.read())
                    if self.skor > kayıtlıSkor:
                        with open("skor.txt", "w") as dosya:
                            dosya.writelines(str(self.skor))  # skoru yazdırıyor.
                        self.maksimumSkor = self.skor #buraya girdiyse demekki skor maxtır
                    else:
                        with open("skor.txt","r") as dosya:
                            skor = str(dosya.read())
                            self.maksimumSkor = skor

            except FileNotFoundError: #daha önce skor kaydetmediyse
                with open("skor.txt","w") as dosya:
                #ilk defa başladığımız daha önce skor olmadığı için direk skoru yazabiliyoruz.
                    dosya.writelines(str(self.skor))
                    self.maksimumSkor = skor


            self.skor = 0
            self.playing = False

        while len(self.platforms) < 6: #6 dan az platformum kalırsa döngüye gir ve random platform ekle.
            genislik = random.randrange(50,100)
            p = Platform(random.randrange(0,WIDTH-genislik),random.randrange(-40,0),genislik,30)
            #Oluşan platformumuz ekranın içinde oluşması için genişliği çıkartıyoruz. X ve ye için randomları aldık.
            self.platforms.add(p)
            self.all_sprites.add(p)

            if random.randint(1,10) == 1: #düsman ekleme %10 şansla oluşuyo
                dusman = Dusman(self,p)
                self.Dusmanlar.add(dusman)
                self.all_sprites.add(dusman)

        pygame.display.update() #tüm ekranı yenilemiş olucaz.

    def events(self):
        for event in pygame.event.get(): #Ekrandaki tüm eventları alıyoruz
            if event.type == pygame.QUIT: #Çıkış işlemini yapıyoruz.
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: #boşluk tuşuna basarsak zıplama fonksiyonu çalışacak.
                    self.player.zipla()
                if event.key == pygame.K_SPACE:
                    self.player.atesEt(self.bizim_mermi) #Space e basınca mermi istediğiz konuma geldi
                if event.key == pygame.K_x:  #
                    pygame.mixer_music.stop()
                if event.key == pygame.K_y:
                    pygame.mixer_music.play()

    def draw(self):
       # self.screen.fill((135,206,250)) #RGB anlamında bir görsel ekran
        self.screen.blit(arka_plan, (0, 0))
        self.Skor("Skor : {}".format(self.skor))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image,self.player.rect) # ön tarafa aldık playerı
        self.screen.blit(self.bizim_mermi.image,self.bizim_mermi.rect)

    def girisEkranı(self): #Giriş ekranı oluşturuyoruz

        pygame.mixer_music.stop()
        resim = pygame.image.load("giris.jpg")
        self.screen.blit(resim,resim.get_rect()) #ekrana yansıtıyoruz, ikinci değer kordinatlar.
        pygame.display.update()
        self.tusBekleme() #Giriş Ekranı hemen geçmemesi için bir fonksiyon yazıcaz.

    def bitisEkranı(self):
        resim = pygame.image.load("bitis.jpg")
        self.screen.blit(resim, resim.get_rect())  # ekrana yansıtıyoruz, ikinci değer kordinatlar.
        font = pygame.font.SysFont("Century Gothic", 25)
        text = font.render("En Yüksek Skor : {}".format(self.maksimumSkor), True, (255, 255, 255))

        self.screen.blit(text, (WIDTH / 2 - (text.get_size()[0] / 2), 380))


        pygame.display.update()
        self.tusBekleme()

    def tusBekleme(self):
        bekleme = True #Bir tuşa basmadığı sürece beklesin
        while bekleme:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Çarpıya basarsa kapatsın
                    bekleme= False
                    self.running = False
                if event.type == pygame.KEYDOWN: #Herhangi bir tuşa basarsa giriş ekranı bitsin.
                    bekleme = False

        pygame.mixer.music.load("sarki.mp3")
        pygame.mixer_music.play()
        pygame.mixer_music.set_volume((0.10))

    def Skor(self,yazi="Skor"):
        font = pygame.font.SysFont("Century Gothic", 25)
        text = font.render(yazi, True, (255, 255, 255))
        self.screen.blit(text, (WIDTH / 2 - (text.get_size()[0] / 2), 0))


game = Game()
game.girisEkranı() #Giriş ekranını oluşturduk
while game.running:
    game.new()
    game.bitisEkranı()