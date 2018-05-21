
# coding: utf-8

#    #                              Desafio Passei Direto - Lorena Bernardo Vianna
# 
# 
# Este código está dividido em XXXX partes:
# 1ª) Importação das bibliotecas/ pacotes necessários para a leitura dos arquivos e construção de análises
# 2ª) Leitura de cada arquivo
# 

# In[192]:


# Importando as bibliotecas necessárias:
import json 
import pandas as pd 
from pandas.io.json import json_normalize #pacote para transformar .json em dataframe
import matplotlib.pyplot as plt
import numpy as np 
import pylab # importante para redefinição dos tamanhos dos gráficos


# In[2]:


# Lendo os arquivos enviados:
with open(r'C:\Users\loren\Downloads\Passei Direto\friend_connection.json') as f:
    d = json.load(f)

friend_connection = json_normalize(d['friend_connection'])
friend_connection.head(3)


# In[3]:


#df = pd.DataFrame(data)
#df.head(3)
friend_connection.columns


# In[166]:


# verificando o que pode ser o conteúdo da base:
# pegando o primeiro FriendRequestId e verificando quantas vezes se repete
friend_connection[friend_connection['FriendRequestId'] =='29319610']


# In[167]:


friend_connection[friend_connection['Id'] =='40158628']


# ____________________________________________________________________________________________________________
# 
# Não foi possível identificar o que representa esta base de friend_connection. 
# ____________________________________________________________________________________________________________

# In[4]:


# Lendo os arquivos enviados:
with open(r'C:\Users\loren\Downloads\Passei Direto\friend_request.json') as f:
    d = json.load(f)

friend_request = json_normalize(d['friendrequest'])
friend_request.head(3)


# In[172]:


# Lendo os arquivos enviados:
with open(r'C:\Users\loren\Downloads\Passei Direto\student_aggregate.json') as f:
    d = json.load(f)

student_aggregate = json_normalize(d['student_aggregate'])
student_aggregate.head(10)


# In[168]:


# verificando o mesmo Id da base de friend_connection se aparece nesta base:
student_aggregate[student_aggregate['Id'] =='40158628']


# In[169]:


# verificando o mesmo Student1Id da base de friend_connection se aparece nesta base:
student_aggregate[student_aggregate['Id'] =='16474100']


# In[170]:


# verificando o mesmo FriendrequestId da base de friend_connection se aparece nesta base:
student_aggregate[student_aggregate['Id'] =='29319610']



# In[212]:


# fazendo join entre a tabela student_answer e student_aggregate pela chave Id:
result = pd.merge(friend_request, student_aggregate, on='Id')
result


# ____________________________________________________________________________________________________________
# 
# Com os comandos acima, tentei verificar se alguns dos Ids da base friend_connection apareciam na base student_aggregate 
# para tentar identificar o conteúdo das bases, mas como nenhum dos Ids da base de friend_connection  testado não aparece na
# base de student_aggregate que aparenta ser uma base com os dados agregados dos cadastrados, não é possível saber o conteúdo 
# da base de friend_connection. e muito menos realizar inferências entre quantidade de amigos e estado, curso, etc.
# ____________________________________________________________________________________________________________

# In[25]:


student_aggregate.RegisteredDate.min()


# In[26]:


student_aggregate.RegisteredDate.max()


# In[27]:


student_aggregate.LastLoginDate.min()


# In[28]:


student_aggregate.LastLoginDate.max()


# _____________________________________________________________________________________________________________________
# 
# Ou a base acima é uma foto dos registros realizados no dia 07 de dezembro de 2015, ou os campos de data estão com erro.
# 
# _____________________________________________________________________________________________________________________

# In[173]:


student_aggregate.groupby(u'Gender')[u'Fullname'].value_counts()


# In[174]:


# Com o resultado acima, supõe-se que Gender=True é sexo Masculino e Gender=False é sexo feminino
student_aggregate['Genero'] = '0'

for b in student_aggregate.itertuples():
    if b.Gender.find("false") != -1: 
        student_aggregate.Genero[b.Index] = 'Feminino' 
    if b.Gender.find("true") !=-1: 
        student_aggregate.Genero[b.Index] = 'Masculino'
   
student_aggregate.groupby('Genero').count().Id


# In[290]:


# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (4.0, 4.0)

segmentos = student_aggregate['Genero'].value_counts().index    

values = student_aggregate['Genero'].value_counts()

cores = ['lightgreen', 'lightblue']    

#explode = (0.1, 0, 0, 0)  # somente explode primeiro pedaço 

total = sum(values)

plt.pie(values, labels=segmentos, colors=cores, autopct='%1.1f%%', shadow=False, startangle=90)
#autopct='%1.1f%%' coloca os as quantidades em %
#plt.axis('equal')
#plt.title('Distribuição por Gênero')

plt.show()


# In[292]:



# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (8.0, 8.0)
fig, ax = plt.subplots()
y_pos = np.arange(len(student_aggregate['CourseName'].value_counts().head(20)))
values = student_aggregate['CourseName'].value_counts().head(20)
segmentos = student_aggregate['CourseName'].value_counts().head(20).index #é necessário colocar esse .index para que os segmentos sejam na mesma ordem 
ax.barh(y_pos, values, align='center', color='gray')
ax.set_yticks(y_pos)
ax.set_yticklabels(segmentos)
ax.invert_yaxis()
#ax.set_xlabel('Qtd de estudantes')
#ax.set_title('Os 20 cursos que mais possuem estudantes cadastrados')
plt.show()


# In[295]:


contagem = student_aggregate[['CourseName','Id']].groupby(['CourseName'])['Id']                              .count()                              .reset_index(name='count')                              .sort_values(['count'], ascending=True)                              .head(40)

print (contagem)


# In[298]:


# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (8.0, 8.0)
fig, ax = plt.subplots()
y_pos = np.arange(len(student_aggregate['UniversityName'].value_counts().head(20)))
values = student_aggregate['UniversityName'].value_counts().head(20)
segmentos = student_aggregate['UniversityName'].value_counts().head(20).index #é necessário colocar esse .index para que os segmentos sejam na mesma ordem 
ax.barh(y_pos, values, align='center', color='gray')
ax.set_yticks(y_pos)
ax.set_yticklabels(segmentos)
ax.invert_yaxis()
#ax.set_xlabel('Qtd de estudantes')
#ax.set_title('Os 20 Universidades que mais possuem estudantes cadastrados')
plt.show()


# In[305]:


aux=student_aggregate[(student_aggregate['UniversityName']=='Universidade Estácio de Sá')
                     | (student_aggregate['UniversityName']=='Universidade Estácio de Sá - EAD')
                     | (student_aggregate['UniversityName']=='Universidade Paulista')]

# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (4.0, 4.0)

segmentos = aux['Genero'].value_counts().index    

values = aux['Genero'].value_counts()

cores = ['lightgreen', 'lightblue']    

#explode = (0.1, 0, 0, 0)  # somente explode primeiro pedaço 

total = sum(values)

plt.pie(values, labels=segmentos, colors=cores, autopct='%1.1f%%', shadow=False, startangle=90)
#autopct='%1.1f%%' coloca os as quantidades em %
#plt.axis('equal')
#plt.title('Distribuição por Gênero')

plt.show()


# In[39]:


student_aggregate.groupby('stateName').count().Id


# In[296]:


# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (8.0, 8.0)
fig, ax = plt.subplots()
#definindo o eixo y:
y_pos = np.arange(len(student_aggregate['stateName'].value_counts()))
#definindo o "tamanho" das barras:
values = student_aggregate['stateName'].value_counts()
# definindo os labels do eixo y:
segmentos = student_aggregate['stateName'].value_counts().index #é necessário colocar esse .index para que os segmentos sejam na mesma ordem 
#plotando o gráfico:
ax.barh(y_pos, values, align='center', color='gray')
ax.set_yticks(y_pos)
ax.set_yticklabels(segmentos)
ax.invert_yaxis() # para colocar em ordem decrescente
#ax.set_xlabel('') #descrição do eixo x
#ax.set_title('Número de Estudantes Inscritos por Estado') #título
plt.show()


# ___________________________________________________________________________________
# 
# A maior concentração de usuários está na região Sudeste.
# ___________________________________________________________________________________

# In[306]:


aux=student_aggregate[(student_aggregate['stateName']=='São Paulo')
                     | (student_aggregate['stateName']=='Rio de Janeiro')
                     | (student_aggregate['stateName']=='Minas Gerais')]

# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (4.0, 4.0)

segmentos = aux['Genero'].value_counts().index    

values = aux['Genero'].value_counts()

cores = ['lightgreen', 'lightblue']    

#explode = (0.1, 0, 0, 0)  # somente explode primeiro pedaço 

total = sum(values)

plt.pie(values, labels=segmentos, colors=cores, autopct='%1.1f%%', shadow=False, startangle=90)
#autopct='%1.1f%%' coloca os as quantidades em %
#plt.axis('equal')
#plt.title('Distribuição por Gênero')

plt.show()


# In[46]:


student_aggregate.groupby('IsMobileRegister').count().Id


# ___________________________________________________________________________________
# 
# Há pouquíssimos usuários com registro feito através de terminal móvel.
# ___________________________________________________________________________________

# In[6]:


# Lendo os arquivos enviados:
with open(r'C:\Users\loren\Downloads\Passei Direto\student_answer.json', encoding="utf8") as f:
    d = json.load(f)

student_answer = json_normalize(d['student_answer'])
student_answer.head(3)


# In[207]:


# verificando se Ids desta base(student_answer) aparecem na base de dados dos estudantes:
student_aggregate[(student_aggregate['Id'] =='17762776') 
                      | (student_aggregate['Id'] =='17762682') 
                      | (student_aggregate['Id'] == '17762395') ]


# In[211]:


# fazendo join entre a tabela student_answer e student_aggregate pela chave Id:
result = pd.merge(student_answer, student_aggregate, on='Id')
result


# ________________________________________________________________________________________________________
# 
# Como foi econtrado somente 3 Ids no join entre as tabelas tudent_answer e student_aggregate, não é possível 
# realizar inferências sobre quais cursos são os que mais respondem, ou quais são os estados mais participativos.
# 
# ________________________________________________________________________________________________________

# In[7]:


# Lendo os arquivos enviados:
with open(r'C:\Users\loren\Downloads\Passei Direto\student_comment.json', encoding="utf8") as f:
    d = json.load(f)

student_comment = json_normalize(d['student_comment'])
student_comment.head(3)


# In[113]:


student_comment['Client_padron'] = '0'

for b in student_comment.itertuples():
    if b.Client.find("Android") != -1: 
        student_comment.Client_padron[b.Index] = 'Android' 
    if b.Client.find("iOS") !=-1: 
        student_comment.Client_padron[b.Index] = 'iOS'
    if b.Client.find("Mobile") !=-1: 
        student_comment.Client_padron[b.Index] = 'Mobile'
    if b.Client.find("PDJobs") !=-1: 
        student_comment.Client_padron[b.Index] = 'PDJobs'    
    if b.Client.find("Website") !=-1: 
        student_comment.Client_padron[b.Index] = 'Website'       


# In[112]:


student_comment = student_comment.drop('Client_padron',axis=1)


# In[114]:


student_comment.groupby('Client_padron').count().Id


# In[291]:


# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (5.0, 5.0)
fig, ax = plt.subplots()
#definindo o eixo y:
y_pos = np.arange(len(student_comment['Client_padron'].value_counts()))
#definindo o "tamanho" das barras:
values = student_comment['Client_padron'].value_counts()
# definindo os labels do eixo y:
segmentos = student_comment['Client_padron'].value_counts().index #é necessário colocar esse .index para que os segmentos sejam na mesma ordem 
#plotando o gráfico:
ax.barh(y_pos, values, align='center', color='gray')
ax.set_yticks(y_pos)
ax.set_yticklabels(segmentos)
ax.invert_yaxis() # para colocar em ordem decrescente
#ax.set_xlabel('') #descrição do eixo x
#ax.set_title('Meio de Acesso') #título
plt.show()


# In[132]:


# Lendo os arquivos enviados:
with open(r'C:\Users\loren\Downloads\Passei Direto\student_download.json', encoding="utf8") as f:
    d = json.load(f)

student_download = json_normalize(d['student_download'])
student_download.head(3)


# In[161]:



contagem = student_download[['Fullname','Id']].groupby(['Fullname'])['Id']                              .count()                              .reset_index(name='count')                              .sort_values(['count'], ascending=False)                              .head(20)

print (contagem)


# In[163]:



contagem = student_download[['Id','Fullname']].groupby(['Id'])['Fullname']                              .count()                              .reset_index(name='count')                              .sort_values(['count'], ascending=False)                              .head(20)

print (contagem)


# In[216]:


student_download[student_download['Id'] =='17711766']
#Tentando verificar de quem é o Id qu emais aparece na consulta acima. Somente para ter certeza que o Id é o Id do aluno


# In[221]:


# criando uma tabela com o Id e a quantidade de download realizado:

contagem = student_download[['Id','DownloadID']].groupby(['Id'])['DownloadID']                              .count()                              .reset_index(name='Qtd_Download')                              .sort_values(['Qtd_Download'], ascending=False) 
# fazendo join entre a tabela student_answer e student_aggregate pela chave Id:
result = pd.merge(contagem, student_aggregate, on='Id')
result.head(5)


# In[239]:


result.groupby('Genero')['Qtd_Download'].describe()


# In[310]:


dadosF=result[result[u'Genero']==u'Feminino'].Qtd_Download
dadosM=result[result[u'Genero']==u'Masculino'].Qtd_Download
# definindo o tamanho do gráfico
pylab.rcParams['figure.figsize'] = (5.0, 5.0)

# agrupa tabela
tabela_completa = (dadosM, dadosF)
 
# determina cor de cada estado no grafico
cores = ("blue", "red")
 
# cria um label para os grupos
Genero = ("Masc: Média=2.45 e Desv=3.04", "Fem: Média=2.85 e Desv=4.88")
 
# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, facecolor="1.0")
 
for data, color, group in zip(tabela_completa, cores, Genero):
    y = data
    x = range(len(data))
    ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)
 
    # titulo do grafico
   # plt.title('Dispersão Qtd. de Download')
 
    # insere legenda dos estados
    plt.legend(loc=1)
plt.show()    


# In[278]:


result.groupby('stateName')['Qtd_Download'].describe()


# In[145]:


with open(r'C:\Users\loren\Downloads\Passei Direto\student_evaluation.json', encoding="utf8") as f:
    d = json.load(f)

student_evaluation = json_normalize(d['student_evaluation'])
student_evaluation.head(3)


# In[10]:


with open(r'C:\Users\loren\Downloads\Passei Direto\student_file_upload.json', encoding="utf8") as f:
    d = json.load(f)

student_file_upload = json_normalize(d['student_file_upload'])
student_file_upload.head(3)


# In[22]:


with open(r'C:\Users\loren\Downloads\Passei Direto\student_loginlog_aggreagate.json', encoding="utf8") as f:
    d = json.load(f)

student_login = json_normalize(d['student_loginlog_aggreagate'])
student_login.head(3)


# In[21]:


student_login.LastLoginDate.min()


# In[20]:


student_login.LastLoginDate.max()


# In[23]:


student_login.RegisteredDate.min()


# In[24]:


student_login.RegisteredDate.max()


# _________________________________________________________
# 
# Com os resultados acima, é possível ver que o banco está com problemas nestes campos de data, pois por mais que esta base seja uma foto do dia 2015-12-07, é muito estranho o mínimo e o máximo tanto do último login quanto da data de registro serem exatamente iguais.
# _________________________________________________________

# In[12]:


with open(r'C:\Users\loren\Downloads\Passei Direto\student_question.json', encoding="utf8") as f:
    d = json.load(f)

student_question = json_normalize(d['student_question'])
student_question.head(3)


