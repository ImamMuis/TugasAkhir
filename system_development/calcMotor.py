
motorMIN_Volt = 5
motorMAX_Volt = 24

print(motorMIN_Volt)
print(motorMAX_Volt)

def setSpeed(speedMin, speedMax):
	Vmax = 24
	PWM_width = 2 ** 16 - 1

	dutyCycle = speedMin / Vmax
	motorMIN_PWM = int(round(dutyCycle * PWM_width, 0))

	dutyCycle = speedMax / Vmax
	motorMAX_PWM = int(round(dutyCycle * PWM_width, 0))

	return motorMIN_PWM, motorMAX_PWM

motorMIN, motorMAX = setSpeed(motorMIN_Volt, motorMAX_Volt)

print(motorMIN)
print(motorMAX)