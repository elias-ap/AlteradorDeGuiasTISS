<h1 align="center">Como usar o Alterador de Guias TISS</h1>

## Pr�-requisitos

Para a facilitar o entendimento das funcionalidades e uso do software, � indispens�vel a leitura da documenta��o
***(README)*** no diret�rio raiz.

## Exemplo

Para o seguinte exemplo usaremos o chamado do GLPI HelpDesk: **2022120202**.

### Passos

Com o chamado aberto:

1. **Abra a aplica��o:**

O execut�vel do software est� localizado no caminho: 

> [O:\Informatica\Geral\Funcionais\Faturamento de Conv�nios\Alterador de Guias TISS]([O:\Informatica\Geral\Funcionais\Faturamento de Conv�nios\Alterador de Guias TISS])

Ap�s executa-lo basta aguardar a janela principal se abrir:

<img src="Resources/Screenshots/janela_principal.png"></p>

2. **Abra a planilha de cr�ticas:**

Ao clicar no bot�o `Abrir planilha`, a planilha respons�vel por ler as cr�ticas, localizada no diret�rio raiz ser� aberta.

3. **Extra��o de cr�ticas:**

No chamado, o requerente passa as cr�ticas que s�o necess�rias altera��es:

<img src="Resources/Screenshots/criticas.png">

Os ret�ngulos em destaque representam as cr�ticas que precisam ser extra�das e ser�o lidas para as altera��es
de **dados** e **valores**, conforme o requerente espec�fica.

4. **Altera��o de dados:**

Para extrair as cr�ticas de dados com facilidade, � poss�vel selecionar e copiar as cr�ticas (Ctrl+C).

<img src="Resources/Screenshots/extraindo_criticas_dados.png">

Em seguida, inserir as cr�ticas copiadas na planilha que foi aberta na aba de `Dados` e formate conforme instru�do 
nas �reas destacadas na imagem abaixo:

<img src="Resources/Screenshots/inserir_dados.png">

Ao final teremos:

<img src="Resources/Screenshots/tabela_de_dados.png">

Ap�s seguir os passos, salvar a planilha para a futura leitura.

5. **Altera��o de valores:**

Seguindo o mesmo feito no passo **4**, selecionando, copiando e formatando as cr�ticas:

<img src="Resources/Screenshots/selecionando_valores.png">

<img src="Resources/Screenshots/inserir_valores.png">

<img src="Resources/Screenshots/tabela_de_valores.png">

Ap�s seguir os passos, salvar a planilha para a futura leitura.

6. **Escolhendo a guia para altera��o:**

Feito o download da guia localizada no chamado, iremos seleciona-la para altera��o no software:

<img src="Resources/Screenshots/escolhendo_guia.png">

7. **Definindo o tipo de altera��o a ser realizada:**

Depois da escolha da guia, ficar� dispon�vel a escolha do tipo de altera��o a ser realizada, alguns requerentes 
podem solicitar apenas altera��es de valores ou dados, nesse chamado em espec�fico s�o ambos.
Ent�o, vamos acionar os dois bot�es:

<img src="Resources/Screenshots/alterando_dados_e_valores.png">

8. **Realizando as altera��es:**

Com os tipos de altera��es escolhidos, basta acionar o bot�o `Realizar altera��es`, que o software ir� automaticamente
realizar as altera��es lidas nas tabelas da planilha.

<img src="Resources/Screenshots/realizando_alteracoes.png">

Em seguida, caso as altera��es tenham sido bem sucedidas, o bot�o de `Salvar Guia` estar� dispon�vel. Ao clicar,
ser� gerado uma nova guia com as altera��es realizadas. 

<img src="Resources/Screenshots/guia_salva.png">

9. **Conferindo as altera��es:**

Para conferir se todas as altera��es foram feitas de acordo, � poss�vel verificar na pasta `Logs` no diret�rio raiz
da aplica��o, busque pelo n�mero da guia:

<img src="Resources/Screenshots/numero_da_guia.png">

<img src="Resources/Screenshots/log_da_guia.png">

<img src="Resources/Screenshots/log.png">

## Observa��es

**Em caso de d�vidas e identifica��o de erros, consultar a documenta��o do projeto para informa��es mais detalhadas.**