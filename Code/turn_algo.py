Stop_condition = 0
Mode = 0 # 0 for master
Stop_counter = 1
Stop_0 = 0 #Own Stop_condition
Stop_1 = 0 #Other robot's Stop_condition
L_turn_condition = 0
U_turn_condition = 0

# Tek sıkıntı change direction

def Mode_check():
    if: # master
        Mode = 0
    else: # slave
        Mode = 1

def Stop_who(): # Checks who is stopped
    if : #durduk
        if : #engel varsa
            Stop_0 = 1
            Stop_1 = 0
        else: #engel yoksa bizim önümüzde
            Stop_0 = 0
            Stop_1 = 1
    elif : # açı -+ 90 ise
        Stop_0 = 1
        Stop_1 = 1
    else: #durmadık
        Stop_0 = 0
        Stop_1 = 0

def Turn_condition(): # mazeden gelecek turn type and nerde engel yoksa
    if : # sağ empty ise
        # sağdaki turn type seç
    else:
        # soldaki turn type seç

def Stop_check(): #Durduk mu durmadık mı
    Stop_who()
    if ( Stop_0 or Stop_1 ): # durduysak
        Stop_condition = 1
    else: # durmadıysak
        Stop_condition = 0

def No_turn():
    pass #No turn code

def Stop_release(): # stop release conditions
    Stop_condition = 0
    Stop_0 = 0
    Stop_1 = 0

def Turn():
    if Stop_0 and Stop_1 : # bu +-90 derece iken oluyo ikisi de beklicek dedim
        pass
        #Wait 10 sec
    elif Stop_0: # biz durduysak dön
        pass #Turn
    else: # o durduysa bekle
        pass
        #Wait 10 sec
    Stop_release()

def Speed_in_turn(): # L dönüsü icin hız ayarı angle ile
    pass

def L_turn(): # L dönüsü
    Turn() # dön
    while True: # döndükten sonra hız ayarlı bi sekilde git bi dahki durmaya kadar
        Speed_in_turn() # bu belki üste alınabilir !değişim!
        Stop_check()
        if ( Stop_condition ):
            Turn()
            L_turn_condition = 0
            break

def Change_direction(): # Yön degistir
    pass #Change_direction

def U_turn(): # U dönüsü
    while True:
        Stop_check()
        if ( Stop_counter == 1 ):
            L_turn()
            Stop_counter += 1

        elif ( Stop_counter == 2 ) :
            if not Mode : # master bişi yapmıyo
                pass
            else: # slave yön değiştiriyo
                Change_direction()
            Stop_counter += 1

        elif Stop_counter > 2 and Stop_condition:
            if ( ( not Mode and Stop_0 ) or ( Mode and not Stop_0 ) ):
                while True:
                    Stop_check()
                    if Stop_condition and Stop_counter == 3:
                        if Mode:
                            Change_direction()
                        else:
                            pass
                        Turn()
                        Stop_counter += 1
#004
                    elif Stop_condition and Stop_counter == 4:
                        if not Mode:
                            Change_direction()
                        else:
                            pass
                        Turn() # eğer bekleme olursa bu conditionda bu kalkmaz
                                #olmazsa kalkıcak, kalkarsa release ekle
                        Stop_counter += 1
#005
                    elif Stop_condition and Stop_counter == 5:
                        Turn()
                        Stop_counter += 1
#006

                    elif Stop_condition and Stop_counter == 6:
                        if not Mode:
                            Change_direction()
                        else:
                            pass
                        L_turn()
                        Stop_counter = 1
                        break

            else:
                while True:
                    Stop_check()
                    if Stop_condition and Stop_counter == 3:
                        Turn()
                        Stop_counter += 1
                        pass

                    elif Stop_condition and Stop_counter == 4:
                        if Mode:
                            Change_direction()
                        else:
                            pass
                        Turn()
                        Stop_counter += 1

                    elif Stop_condition and Stop_counter == 5:
                        if not Mode:
                            Change_direction()
                        else:
                            pass
                        Turn()
                        Stop_counter += 1

                    elif Stop_condition and Stop_counter == 6:
                        if not Mode:
                            Change_direction()
                        else:
                            pass
                        L_turn()
                        Stop_counter = 1
                        break

        if ( Stop_counter == 1 ):
            U_turn_condition = 0
            break


while True:
    Mode_check() # Checks mode
    Stop_check() # Checks if any stop conditions occur
    Turn_condition() # Checks Turn conditions

    if Stop_condition : # if stop conditions occurs

        if( L_turn_condition ): # İf L turn conditions occurs
            L_turn()

        elif( U_turn_condition ): # İf U turn conditions occurs
            U_turn()
    else: # Yoksa Düz git
        No_turn()
