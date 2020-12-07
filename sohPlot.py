#!/Users/steve/miniconda3/bin/python

import argparse
import sys
import obspy
from obspy import read
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
client = Client("IRIS")
import datetime

if len(sys.argv) < 2:
    print ("USAGE: sohPlot.py STA (or -h for complete listing of options")
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument('sta', help="Station")
parser.add_argument('net', nargs='?', default='UW', help="network")
parser.add_argument('-n', type=int, default=14, help='Number of days to plot')
parser.add_argument('-s', default='now', help='Stop or end of time (YYYYMMDD)')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose')
parser.add_argument('-e', dest='type', default='all', action='store_const', const='equip', help="plot equip paramters")
parser.add_argument('-t', dest='type', default='all', action='store_const', const='time', help="plot time paramters")
parser.add_argument('-o', dest='output', action='store_true', help="Plot to file")
args = parser.parse_args()
if args.verbose:
   print("Arguments: ", args)
ndays=args.n
stop=args.s
net=args.net
sta=args.sta

# list of channel codes
pairs={'GAN': '-GPS_antenna_0-OK',
'GNS': '-GPS_num_satallites',
'GST': '-GPS_status_0-off_1-unlock_2-locked',
'LCE': '-Clock_phase_error_uSec',
'LCL': '-Clock_time_loss_mins',
'LCQ': '-Percent_Clock_locked',
'VCO': '-VCO_control_voltage',
'VDT': '-Digitizer_tem_mDegreeC',
'VEA': '-GPS_antenna_current',
'VEC': '-System_current_mAmp',
'VEI': '-System_voltage_mV',
'VEP': '-System_voltage_150mV',
'VKI': '-Equipment_temperature',
'VM1': '-Boom_position-Z',
'VM2': '-Boom_position-E',
'VM3': '-Boom_position-N',
'VPB': '-Percent_buffer_full'}

# Set start and end times
if stop == 'now':
   T2 = datetime.datetime.today()
else:
   T2 = datetime.datetime.strptime('20201201', '%Y%m%d')
T1 = T2 - datetime.timedelta(days=ndays)

#chan='GNS,LCE,LCQ,VEA,VEC,VCO,VKI,VEP,VPB,GPL'
if args.type == 'all':
   chan='GAN,GNS,GPL,GST,LCE,LCQ,VCO,VDT,VEC,VEI,VM1,VM2,VM3,VKI,VPB'
elif args.type == 'equip':
   chan='VEC,VEP,VEI,VKI,VCO,VDT,VPB,VM1,VM2,VM3'
elif args.type == 'time':
   chan = 'GPL,GNS,GAN,LCE,LCQ,LCL,VEA'

loc='*'

print ("Doing ", sta,net, chan, " \nBetween these times: ",UTCDateTime(T1), UTCDateTime(T2))

st = client.get_waveforms(net,sta,loc,chan,UTCDateTime(T1),UTCDateTime(T2))
inv = client.get_stations(network=net,station=sta,starttime=UTCDateTime(T1),endtime=UTCDateTime(T2),level='response')

#print(str)
if args.verbose:
   print("Station Information:")
   print (inv)

if args.verbose:
   print('')
   ch=chan.split(",")
   for (c) in ch:
      try:
         match=pairs[c]
      except KeyError:
         print("Channel name, not found in info file", c)
      else:
         print(c, match)

if args.output:
   on=UTCDateTime(T1).strftime("%Y%m%dT%H:%M")
   outname="%s.%s.png" %(sta,UTCDateTime(T1).strftime("%Y%m%d_%H:%M"))
   print("Plotting to: ", outname)
   st.plot(outfile=outname, size=(1000,850), equal_scale=0)
else:
   st.plot(size= (1000,850), equal_scale=0 )


