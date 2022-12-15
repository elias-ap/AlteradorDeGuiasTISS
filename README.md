# Alterador de Guias TISS
 
## Prefácio

A ideia inicial desse projeto nasceu da necessidade de uma ferramenta
capaz de realizar alterações de dados em guias TISS (arquivos XML) de forma automatizada, com propósito
de otimizar o tempo gasto para essa tarefa que até então era feita de forma manual através
de editores de texto como ++Notepad, bloco de notas, etc.

## Objetivo

Realizar alterações de dados e/ou valores de forma automática após leitura de critícas informadas pelo requerente,
conforme os chamados: 2022040943, 2022110809 e 2022100571.

## Como utilizar

### Localização do software

O executável do software poderá ser usado sem a necessidade de instalação
de outros programas e está localizado em pasta compartilhada na rede:
<br>
<br>
<a>O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS</a><br><br>

### Funcionalidades

#### Leitura de críticas

<p>Para realização das alterações, será preciso adicionar as críticas manualmente nas tabelas da planilha localizada no diretório 
raiz do programa.</p>

<i>Tabela 1º Aba - Alteração de dados</i> 
<img src="resources\screenshot_excel_plan_data.png">

<p>Essa tabela é lida para alteração dos dados de procedimentos como: código de procedimento, tipo de tabela e
unidade de medida. Seus campos devem ser preenchidos de acordo com as colunas, caso o número da conta
não seja especificado, todos os procedimentos com codigo correspondente serão alterados.</p>

<i>Tabela 2º Aba - Alteração de valores</i> 
<img src="resources\screenshot_excel_plan_value.png">

<p>Essa tabela é lida para alteração de valores dos procedimentos. Caso os valores informados possuam casas decimais,
eles devem ser escritos com no máximo duas casas, separando o valor decimal com uma vírgula e se 
o número da conta não seja especificado, todos os procedimentos com codigo correspondente serão alterados.</p>

#### Botões

<p>Ao abrir o programa verá a janela principal e alguns botões:
<br>
<br>
<img src="resources/screenshot_main_window.png">
<br>
<ul>
    <li><b>Carregar Guia:</b> abre uma janela para escolha de <b>uma</b> guia que deseja realizar alterações;</li>
    <br>
    <li><b>Gerar hash:</b> abre uma janela para escolha de <b>uma ou mais</b> guias, após a escolha 
    automaticamente gera um novo código hash e salva a guia no diretório de origem;</li>
    <br>
    <li><b>Abrir planilha:</b> abre a planilha de alterações no diretório raiz.</li>
    <br>
</ul>
Após carregar uma guia é desbloqueado outras interações:
<br>
<br>
<img src="resources/screenshot_after_choose_guide.png">
<ul>
    <li><b>Alteração de dados:</b> define se a tabela de alteração de dados será lida e serão feitas as alterações;</li>
    <br>
    <li><b>Alteração de valor:</b> define se a tabela de alteração de valores será lida e serão feitas as alterações</li>
    <br>
    <li><b>Realizar alterações:</b> faz as alterações;</li>
    <br>
    <li><b>Cancelar:</b> retorna a janela padrão.</li>
</ul>

## Observações
<p>Para atender aos modelos de chamados citados no início e utilizar o software com máxima eficiência, muitas vezes será
possível o uso do clipboard na captura das críticas informadas no chamado e o inserçao das mesmas na
planilha de alterações, porém caso o formato não seja tabular, pode se utilzar o recurso no excel Texto para Colunas
e extrair/formatar as críticas corretamente.</p>
<p>A versão atual v.1.0 suporta alterações nas despesas de guias do tipo SP-SADT e Guia Resumo de Internação.</p>