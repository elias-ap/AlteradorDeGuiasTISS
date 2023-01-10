# Alterador de Guias TISS
 
## Prefácio

A ideia inicial desse projeto nasceu da necessidade de uma ferramenta capaz de realizar alterações de 
dados eletrônicos em guias médicas (arquivos XML) no padrão TISS definido pela ANS de forma automatizada, com propósito 
de otimizar o tempo gasto para essa tarefa que até então era feita de forma manual através de editores de texto como 
++Notepad, bloco de notas, etc.

## Objetivo

Realizar alterações de dados dentro do arquivo XML de acordo com novos dados informados em uma planilha XLSX.

### Localização e uso do software

O executável do software pode ser usado sem a necessidade de instalação  de outros programas, porém, por medidas de 
segurança e versionamento, foi definido em seu código fonte que a aplicação só poderá ser executada em seu 
diretório (origem) localizado na pasta compartilhada da rede:

<a>O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS</a>

### Funcionalidades

#### Leitura de críticas

Para realização das alterações, será preciso adicionar as críticas manualmente nas tabelas da planilha localizada no diretório 
raiz do software.

_Tabela 1º Aba - Alteração de dados_
<br>
<img src="Resources\Screenshots\plan_data.png">

Essa tabela é lida para alteração dos dados de procedimentos como: código de procedimento, tipo de tabela, grau 
de participação, código de despesa, unidade de medida. Seus campos devem ser preenchidos de acordo com as colunas,
caso o número da conta não seja especificado, todos os procedimentos com codigo correspondente serão alterados.

_Tabela 2º Aba - Alteração de valores_
<br>
<img src="Resources\Screenshots\plan_value.png">

Essa tabela é lida para alteração de valores dos procedimentos. Caso os valores informados possuam casas decimais,
eles devem ser escritos com no máximo duas casas, separando o valor decimal com uma vírgula e se 
o número da conta não for especificado, todos os procedimentos com codigo correspondente serão alterados.

#### Botões

Ao abrir o programa verá a janela principal e alguns de seus botões:

<img src="Resources\Screenshots\janela_principal.png">

<li><b>Carregar guia:</b> abre uma janela para escolha de <b>uma</b> guia que deseja realizar alterações;</li>
<br>
<li><b>Gerar hash:</b> abre uma janela para escolha de <b>uma ou mais</b> guias, após a escolha 
automaticamente gera um novo código hash e salva a guia no diretório de origem do arquivo;</li>
<br>
<li><b>Abrir planilha:</b> abre a planilha de alterações no diretório raiz;</li>

Após carregar uma guia outras interações são desbloqueadas:

<img src="Resources\Screenshots\depois_de_escolher_guia.png">

<li><b>Alteração de dados:</b> define se a tabela de alteração de dados será lida e serão feitas as alterações nos dados;</li>
    <br>
<li><b>Alteração de valor:</b> define se a tabela de alteração de valores será lida e serão feitas as alterações nos valores;</li>
    <br>
<li><b>Realizar alterações:</b> realiza as alterações de acordo com os dados lidos nas linhas da planilha;</li>
    <br>
<li><b>Cancelar:</b> retorna a janela padrão e desfaz qualquer alteração feita na guia carregada;</li>

Caso as alterações tenham sido realizadas com sucesso, o botão de salvar a guia ficará disponível:

<img src="Resources\Screenshots\salvar_guia_depois_das_alteracoes.png">

<li><b>Salvar guia:</b> salva a guia, gerando um novo código hash e um arquivo texto das alterações realizadas
na pasta Logs (diretório raiz);</li>

## Observações

Como medida de segurança e versionamento, a aplicação **só poderá ser executada a partir do diretório raiz**.
Entretanto, para facilitar a execução é possível criar um atalho vinculado ao programa. 

Qualquer alteração (mudança no caminho ou nomes) nos arquivos/diretório do software podem causar mau funcionamento
no sistema.

As tabelas de leitura apenas trabalham com as colunas que possuem, alterações em tag como "quantidadeExecutada", entre outras
não serão realizadas pelo software.

O software não será executado ser aberto em modo administrador. 