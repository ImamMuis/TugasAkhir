# Konfigurasi Driver Servo & Motor
V_in    = 24 #V (Tegangan Maksimal untuk motor DC)
freq    = 50 #Hz (Frekuensi PWM)
PWM_Res = 2 ** 16 - 1 #Lebar bit PWM

def motorCalc(value, selector):
    valueError = 0
    perioda = 1 / freq * 1000
              
    if selector == "PWM":
        PWM_Out = value
        
        if PWM_Out > PWM_Res:
            print("Input", value, "PWM terlalu besar!")
            print("Input maksimal", PWM_Res, "PWM\n")
            valueError = 1

        else:    
            dutyCycle = PWM_Out / PWM_Res 
            V_Out = dutyCycle * V_in 
            T_on = dutyCycle * perioda
            T_off = perioda - T_on

    elif selector == "DUTYCYCLE":
        dutyCycle = value / 100
        
        if dutyCycle > 1:
            print("Input", str(value) + "% Duty Cycle terlalu besar!")
            print("Input maksimal 100% Duty Cycle\n")
            valueError = 1

        else:    
            V_Out = dutyCycle * V_in 
            PWM_Out = dutyCycle * PWM_Res
            T_on = dutyCycle * perioda
            T_off = perioda - T_on

    elif selector == "VOLT":
        V_Out = value
        
        if V_Out > V_in:
            print("Input", value, "Volt terlalu besar!")
            print("Input maksimal", V_in, "Volt\n")
            valueError = 1

        else:    
            dutyCycle = V_Out / V_in
            PWM_Out = dutyCycle * PWM_Res
            T_on = dutyCycle * perioda
            T_off = perioda - T_on
       
    else: 
        print("Parameter 'value' harus PWM, DUTYCYCLE atau VOUT!\n")
        valueError = 1
        
    if valueError == 0:
        print("Perioda   :", round(perioda, 2), "ms")
        print("PWM       :", round(PWM_Out, 2))
        print("Duty Cycle:", round(dutyCycle * 100, 2), "%")
        print("Voltage   :", round(V_Out, 2), "V")
        print("Time On   :", round(T_on, 2), "ms")
        print("Time Off  :", round(T_off, 2), "ms\n")

# Cara pakai:  
# motorCalc(26214, "PWM")
# motorCalc(40, "DUTYCYCLE")
# motorCalc(9.6, "VOLT")