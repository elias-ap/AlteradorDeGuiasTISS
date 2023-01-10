# Como usar o Alterador de Guias TISS

## Pré-requisitos

Para a facilitar o entendimento das funcionalidades e uso do software, é indispensável a leitura da documentação
***(README)*** no diretório raiz.

## 1º Exemplo

Para o seguinte exemplo usaremos o chamado do GLPI HelpDesk: **2022120202**.

### Passos

#### Com o chamado aberto:
<li type="1"><b>Abra a aplicação</b></li>

O executável do software está localizado no caminho: 

[O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS]([O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS])

Após executa-lo basta aguardar a janela principal se abrir:

<img src="Resources/Screenshots/janela_principal.png"></p>

**1 - Abra a planilha de críticas**

Ao clicar no botão ***Abrir planilha***, a planilha responsável por ler as críticas, localizada no diretório raiz será aberta.

**2 - Extração de críticas**

No chamado, o requerente passa as críticas que são necessárias alterações:

<img src="Resources/Screenshots/criticas.png">

Os retângulos em destaque representam as críticas que precisam ser extraídas e serão lidas para as alterações
de **dados** e **valores**, conforme o requerente específica.

**2.1 -  Alteração de dados**

Para extrair as críticas de dados com facilidade, é possível selecionar e copiar as críticas (Ctrl+C).

<img src="Resources/Screenshots/extraindo_criticas_dados.png">

Em seguida, inserir as críticas copiadas na planilha que foi aberta na aba de ***Dados*** e formate conforme instruído 
nas áreas destacadas na imagem abaixo:

<img src="Resources/Screenshots/inserir_dados.png">

Ao final teremos:

<img src="Resources/Screenshots/tabela_de_dados.png">

Após seguir os passos, salvar a planilha para a futura leitura.

**2.2 -  Alteração de valores**

Seguindo o mesmo feito no passo **2.1**, selecionando, copiando e formatando as críticas:

<img src="Resources/Screenshots/selecionando_valores.png">

<img src="Resources/Screenshots/inserir_valores.png">

<img src="Resources/Screenshots/tabela_de_valores.png">

Após seguir os passos, salvar a planilha para a futura leitura.

**3 - Escolhendo a guia para alteração:**

Feito o download da guia localizada no chamado, iremos seleciona-la para alteração dentro do software:

<img src="Resources/Screenshots/escolhendo_guia.png">

**4 - Definindo o tipo de alteração a ser realizada:**

Depois da escolha da guia, ficará disponível a escolha do tipo de alteração a ser realizada, alguns requerentes 
podem solicitar  apenas alterações de valores ou dados, nesse chamado em específico são ambos.
Então, vamos acionar os dois botões:

<img src="Resources/Screenshots/alterando_dados_e_valores.png">

**5 - Realizando as alterações:**

Com os tipos de alterações escolhidos, basta acionar o botão ***Realizar alterações***, que o software irá automaticamente
realizar as alterações lidas nas tabelas da planilha.

<img src="Resources/Screenshots/realizando_alteracoes.png">

Em seguida, caso as alterações tenham sido bem sucedidas, o botão de ***Salvar Guia*** estará disponível. Ao clicar,
será gerado uma nova guia com as alterações realizadas. 

<img src="Resources/Screenshots/arquivo_salvo.png">

**6 - Conferindo as alterações:**

Para conferir se todas alterações foram feitas de acordo, é possível verificar na pasta ***Logs*** no diretório raiz
da aplicação, busque pelo número da guia:

<img src="Resources/Screenshots/numero_da_guia.png">

<img src="Resources/Screenshots/log_da_guia.png">

<img src="Resources/Screenshots/log.png">

## Observações

**Em caso de dúvidas e identificação de erros, consultar a documentação do projeto para informações mais detalhadas.**