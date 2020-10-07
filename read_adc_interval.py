# -*- coding: utf-8 -*-
#一定間隔でサンプリング
#ポーリングor割り込み禁止などをすると早くなる？
#プログラム自体はteraailにあったものを参考にした
#https://teratail.com/questions/16629
#
import RPi.GPIO as GPIO
import time
import spidev

# MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
def readadc_spidev(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    command1 = 0x6 | (adcnum & 0x4)>>2
    command2 = (adcnum & 0x3)<<6
    ret=spi.xfer2([command1,command2,0])
    adcout = (ret[1]&0xf)<<8 | ret[2]
    return adcout

GPIO.setmode(GPIO.BCM)
spi=spidev.SpiDev()
spi.open(0, 0) # bus0, CE0
spi.max_speed_hz = 2000000 # 2MHz



list_time = []
list_value = []

interval = 0.0001 #サンプリング周波数の逆数（秒）
duration = 0.1 #10s
sample_num = 100000
counter = 0
wave = 'sin'
hz = '4500'

try:
    time_start = time.perf_counter()
    time_expired = time_start + interval
    time_end = time_start + duration
    while True:
        time_curr = time.perf_counter()
        if(time_curr >= time_expired):
            time_curr = time.perf_counter()
            list_value.append(readadc_spidev(0))
            #time_curr = time.perf_counter()
            list_time.append(time_curr - time_start)
            time_expired += interval
            #counter += 1
        #if(counter == sample_num):
        if(time_curr >= time_end):
            break

except KeyboardInterrupt:
    pass

#f = open('/home/pi/data/adc_photor_2/spidev_output_interval='+str(interval)+'s_sample='+str(sample_num),mode = 'w')
f = open('/home/pi/data/adc_func_gen/spidev_output_interval='+str(interval)+'s_duration='+str(duration)+'s_wave='+wave+'_freq='+hz+'Hz',mode = 'w')
for i in range(len(list_time)):
    f.write('%s %s \n'%(list_time[i],list_value[i]))
    #print(list_time[i],list_value[i])
f.close()
spi.close()