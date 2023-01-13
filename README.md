<h1 align="center">Alterador de Guias TISS</h1>

<div align="center">
<img align="center" height="100px" width="100px" src="Resources/icon.ico">
 </div>

## Prefácio

<p align="justify">A ideia inicial desse projeto nasceu da necessidade de uma ferramenta capaz de realizar alterações de 
dados eletrônicos em guias médicas (arquivos XML) no <b>padrão TISS</b> definido pela ANS de forma automatizada, com propósito 
de otimizar o tempo gasto para essa tarefa que até então era feita de forma manual através de editores de texto como 
++Notepad, bloco de notas, etc.</p>

## Objetivo

<p align="justify">Realizar alterações de dados no arquivo XML de acordo com novos dados informados em uma planilha XLSX.</p>

---

### Localização e uso do software

<p align="justify">O executável do software pode ser usado sem a necessidade de instalação  de outros programas, porém, por medidas de 
segurança e versionamento, foi definido em seu código-fonte que a aplicação só poderá ser executada em seu 
diretório (origem) localizado na pasta compartilhada da rede:</p>

><a>O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS</a>

### Funcionalidades

#### Leitura de críticas

<p align="justify">Para realização das alterações, será preciso adicionar as críticas manualmente nas tabelas da planilha localizada no diretório 
raiz do software.</p>

_Tabela Dados - Alteração de dados_
<img src="Resources\Screenshots\plan_data.png">

Essa tabela é lida para alteração dos dados de procedimentos como: código de procedimento, tipo de tabela, grau 
de participação, código de despesa e unidade de medida. Seus campos devem ser preenchidos conforme as colunas,
caso o número da conta não seja especificado, todos os procedimentos com código correspondente serão alterados.

_Tabela Valores - Alteração de valores_<br>
<img src="Resources\Screenshots\plan_value.png">

Essa tabela é lida para alteração de valores dos procedimentos. Caso os valores informados possuam casas decimais,
eles devem ser escritos com no máximo duas casas, separando o valor decimal com uma vírgula e se 
o número da conta não for especificado, todos os procedimentos com codigo correspondente serão alterados.

#### Botões

Ao abrir o programa verá a janela principal e alguns de seus botões:

<img src="Resources\Screenshots\janela_principal.png">

- **Carregar guia:** abre uma janela para escolha de <b>uma</b> guia que deseja realizar alterações;
  

- **Gerar hash:** abre uma janela para escolha de <b>uma ou mais</b> guias, após a escolha 
automaticamente gera um novo código hash e salva a guia no diretório de origem do arquivo;


- **Abrir planilha:** abre a planilha de alterações no diretório raiz;


Após carregar uma guia outras interações são desbloqueadas:


<img src="Resources\Screenshots\depois_de_escolher_guia.png">


- **Alteração de dados:** define se a tabela de alteração de dados será lida e serão feitas as alterações nos dados;
    

- **Alteração de valor:** define se a tabela de alteração de valores será lida e serão feitas as alterações nos valores;


- **Realizar alterações:** realiza as alterações conforme os dados lidos nas linhas da planilha;


- **Cancelar:** retorna a janela padrão e desfaz qualquer alteração feita na guia carregada;


Caso as alterações tenham sido realizadas com sucesso, o botão de salvar a guia ficará disponível:

<img src="Resources\Screenshots\salvar_guia_depois_das_alteracoes.png">

- **Salvar guia:** salva a guia, gerando um novo código hash e um arquivo texto das alterações realizadas
na pasta Logs (diretório raiz)

## Observações

- Como medida de segurança e versionamento, **a aplicação só poderá ser executada a partir do diretório raiz**.
Entretanto, para facilitar a execução é possível criar um atalho vinculado ao programa em qualquer outro local;


- Qualquer alteração (mudança no caminho ou nomes) nos arquivos/diretório do software podem **causar mau funcionamento**
no sistema;


- As tabelas de leitura apenas trabalham com as colunas que possuem, alterações em tag como "quantidadeExecutada", entre outras
**não serão realizadas** pelo software;


- O software **não será executado** se aberto em modo administrador;

## Tecnologias utilizadas

- Linguagens:
    - Python;
  

- Bibliotecas:

  ````Python
  # IMPORTS
  import xml.etree.ElementTree as Et
  import customtkinter as ctk
  from sys import exit
  from os import getcwd, startfile, path
  from os.path import abspath, basename
  from hashlib import md5
  from pandas import read_excel
  from typing import Generator
  from tkinter import filedialog as fd
  from tkinter import messagebox as mb
  ````
  
---

<div align="center">
  <img height="100" width="100" align="center" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png"></img>
</div>