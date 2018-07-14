from dweet import Dweet
import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')
RELE = GPIO.gpio_id('GPIO_A')
LED = GPIO.gpio_id('GPIO_C')
TOQUE = GPIO.gpio_id('GPIO_E')

pins = ((GPIO_CS, 'out'), (LED, 'out'), (RELE, 'out'), (TOQUE, 'in'),)

sensibilidade = 400
temperatura = 19
dwligatoque = 0

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

dweet = Dweet()

def luminosidade(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.5)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r2 = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r2[1] << 8) & 0b1100000000
	adcout = adcout | (r2[2] & 0xff)	

	return adcout


def temperatura(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.5)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r1 = spi.xfer2([0x01, 0x80, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	adcout = (r1[1] << 8) & 0b1100000000
	adcout = adcout | (r1[2] & 0xff)		

	adc_temp = (adcout *5.0/1023-0.5)*100

	
	return adc_temp



def ligarele():

	gpio.digital_write(RELE, GPIO.HIGH)

	#dweet.dweet_by_name(name="iplug_sabrina_q3", data={"rele":1})
	#resposta = dweet.latest_dweet(name="iplug_sabrina_q3")
	#print resposta['with'][0]['content']['button']


def desligarele():

	gpio.digital_write(RELE, GPIO.LOW)

	#dweet.dweet_by_name(name="iplug_sabrina_q3", data={"rele":0})
	#resposta = dweet.latest_dweet(name="iplug_sabrina_q3")
	#print resposta['content']


def ligaled():

	gpio.digital_write(LED, GPIO.HIGH)

	#dweet.dweet_by_name(name="iplug_sabrina_q3", data={"led":1})
	#resposta = dweet.latest_dweet(name="iplug_sabrina_q3")
	#print resposta['with'][0]['content']['led']


def desligaled():

	gpio.digital_write(LED, GPIO.LOW)

	#dweet.dweet_by_name(name="iplug_sabrina_q3", data={"led":0})
	#resposta = dweet.latest_dweet(name="iplug_sabrina_q3")
	#print resposta['content']

def respostadweet():
	resposta = dweet.latest_dweet(name="iplug_sabrina_q4")
	dwligarele = resposta['with'][0]['content']['rele']
	dwdesligarele = resposta['content']
	dwligaled = resposta['with'][0]['content']['led']
	dwdesligaled = resposta['content']		

with GPIO(pins) as gpio:
	while True:
			button_value = gpio.digital_read(TOQUE)
			resposta = dweet.latest_dweet(name="iplug_sabrina_q4")
			dwligatoque = resposta['with'][0]['content']['toque']
			dwligaled = resposta['with'][0]['content']['led']
			dwligarele = resposta['with'][0]['content']['rele']
			

			if button_value == 0 and dwligatoque == 0:
				vtemp = temperatura(gpio)
				vlumi = luminosidade(gpio)
				print "Sua casa esta sendo controlada automaticamente"
				#time.sleep(5)
	 			if vtemp > 23 and vlumi < sensibilidade:
					ligarele()
					ligaled()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":1, "rele":1, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})
					print ("Temperatura: %2.1f" %vtemp)
					print "Ar condiciondo ligado!"
					print ("Luminosidade: %d" %vlumi)
					print "Luz Ligada! Agora e noite!"
					time.sleep(5)
				elif vtemp > 23 and vlumi > sensibilidade:
					ligarele()
					desligaled()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":0, "rele":1, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})
					print ("Temperatura: %2.1f" %vtemp)
					print "Ar condiciondo ligado!"
					print ("Luminosidade: %d" %vlumi)
					print "Luz Desligada! Agora e dia!"
					time.sleep(5)
				elif vtemp < 23 and vlumi < sensibilidade:
					desligarele()
					ligaled()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":1, "rele":0, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})
					print ("Temperatura: %2.1f" %vtemp)
					print "Ar condiciondo desligado!"
					print ("Luminosidade: %d" %vlumi)
					print "Luz Ligada! Agora e noite!"
					time.sleep(5)
				else:		
					desligarele()
					desligaled()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":0, "rele":0, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})
					print ("Temperatura: %2.1f" %vtemp)
					print "Ar condiciondo desligado!"
					print ("Luminosidade: %d" %vlumi)
					print "Luz desligada. Agora e dia!"
					time.sleep(5)
	
			else:
				print "Voce acionou o controle manual! Agora pode decidir quando ligar ou desligar seus aparelhos!"
#				resposta = dweet.latest_dweet(name="iplug_sabrina_q4")
#				dwligarele = resposta['with'][0]['content']['rele']
#				dwligaled = resposta['with'][0]['content']['led']

				if dwligaled ==1 and dwligarele ==1:
					ligaled()
					ligarele()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":1, "rele":1, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})
				
				elif dwligaled ==1 and dwligarele ==0:
					ligaled()
					desligarele()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":1, "rele":0, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})
				
				elif dwligaled == 0 and dwligarele ==1:
					desligaled()
					ligarele()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":0, "rele":1, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})

				else:
					desligaled()
					desligarele()
					dweet.dweet_by_name(name="iplug_sabrina_q4", data={"led":0, "rele":0, "toque":dwligatoque, "Temperatura":vtemp, "Luminosidade":vlumi})	
			time.sleep(5)
