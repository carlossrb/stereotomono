
# Library para gráficos, arrays e extração de som
import scipy.io.wavfile as sciwave # Leitura e escrita de arquivos .wav
import matplotlib.pyplot as plotGraph # Plotagem de gráficos
import winsound # Tocar a música
import os, glob, numpy as np # import outras libs

nomeDir="Sounds"
nomeExt = "wav"
nomeDirMono = "SoundsMono"
nomeDirEffects = "SoundsEffects"
x = 1 #valor inicial para nomear arquivos do diretório

# Function para transformar audio de stereo para mono
def stereoToMono(audiodata):
    newaudiodata = []
    audiodata = audiodata.astype(float)
    for i in range(len(audiodata)):
        #d = (audiodata[:,0] + audiodata[:,1]) / 2
        d = (audiodata[i][0])/2 + (audiodata[i][1])/2
        newaudiodata.append(d)
    return np.array(newaudiodata, dtype='int16')

# Criar uma função de fade in e eescrever arquivos

def fade(audiodata,fatorInicial=0):
    fatorInicial = 0.01 #Multiplicação por cada elemento do array de data da musica
    percentMusic = 0.6 #Percentual da musica até onde o fade irá
    fatorFade = fatorInicial
    newFade = []
    audiodata = audiodata.astype(float)
    
    for i in range(len(audiodata)):
        newFade.append([audiodata[i][0]*fatorFade, audiodata[i][1]*fatorFade])
        #Aumenta o fator progressivamente (até 1) para que haja aumento do volume da música
        if fatorFade<1:
            fatorFade+=(1-fatorInicial)/(len(audiodata)*percentMusic)  
        else: 
            fatorFade=1
    

    return np.array(newFade, dtype='int16')

# Renomeia musicas do diretório e as escreve (mono) em outro
for i in os.listdir(nomeDir):

    if  i.endswith(nomeExt):
        os.rename(os.path.join(nomeDir,i), os.path.join(nomeDir,'0'+str(x)+"."+nomeExt))  
    SampleRat, audioData = sciwave.read(nomeDir+'\\'+'0'+str(x)+'.wav') #função retorna um sample rate e um array numpy com dados
    sciwave.write(nomeDirMono+'\\'+'0'+str(x)+'MONO.wav',SampleRat,stereoToMono(audioData)) #escreve arquivos mono
    sciwave.write(nomeDirEffects+'\\'+'0'+str(x)+'FADE.wav',SampleRat,fade(audioData,0)) #fade
    x+=1 
    
print('Arquivos renomeados!')
print('Arquivos convertidos!')

# Para plot dos graficos
# Lê as amostras de audio
SampleRat, audioData = sciwave.read("Sounds\\01.wav") #Lê arquivo stereo
SampleRat2, audioMonoData = sciwave.read("SoundsMono\\01MONO.wav") #Lê arquivo mono

timeNumber = (len(audioData)/SampleRat) # Tempo em s = tamanho do vetor/sample rate
Time=np.linspace(0,timeNumber,num=len(audioData)) # Obtendo um vetor de espaços suficientes para plotar em função da amplitude
# seleciona gráficos para ambos os canais
# plotGraph.plot(Time, audioData) #Plota dois canais de audio
plotGraph.plot(Time, audioMonoData) #Plota um canal de audio
# Nomeia os eixos
plotGraph.ylabel("Amplitude")
plotGraph.xlabel("Time (s)")
# Coloca o título do gráfico
plotGraph.title("Amplitude x Tempo")
# Mostra o gráfico
plotGraph.show()







 

