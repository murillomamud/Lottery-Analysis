import requests
import pandas as pd
import collections
import sys

url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'
#url = sys.argv[1] #first parameter

result = requests.get(url)
resultText = result.text

df = pd.read_html(resultText)
df = df[0].copy()

nr_pop = list(range(1,26))
evensList = [x for x in nr_pop if x % 2 == 0]
oddList = [x for x in nr_pop if x % 2 != 0]
primesList = [2,3,5,7,11,13,17,19,23]

comb = []
numbers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

fields = ['Bola1','Bola2','Bola3','Bola4','Bola5','Bola6','Bola7','Bola8','Bola9','Bola10','Bola11','Bola12','Bola13','Bola14','Bola15']

for index, row in df.iterrows():
    v_even = 0
    v_odd = 0
    v_prime = 0

    for field in fields:
        value = row[field]
        if value in evensList: 
            v_even += 1
        if value in oddList: 
            v_odd += 1            
        if value in primesList: 
            v_prime += 1           
        numbers[value] += 1

    comb.append(str(v_even) + 'p-' + str(v_odd) + 'i-' + str(v_prime) + 'pn')


freq_nr = []
l_times = 0
for number in numbers:
    if l_times != 0:
        freq_nr.append([l_times, number])
    l_times += 1

freq_nr.sort(key=lambda tup:tup[1])
freq_nr[0] #first
freq_nr[-1] #last

counter = collections.Counter(comb)

resultDF = pd.DataFrame(counter.items(), columns=['Combination', 'Frequency'])
resultDF['p_freq'] = resultDF['Frequency']/resultDF['Frequency'].sum()
resultDF = resultDF.sort_values(by='p_freq')

print('''
    Most frequently number is: {}
    Less frequently number is: {}
    Combination most frequently is: {} with frequency of: {}%
'''.format(freq_nr[-1][0], freq_nr[0][0], resultDF['Combination'].values[-1], int((resultDF['p_freq'].values[-1]*100)*100)/100))
