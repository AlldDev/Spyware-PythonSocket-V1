# Spyware via Sockets.py

**Authores:** @AlldDev, @YRammus

**Colaboradores:** @bcmarini, Alexandre Queiroz

**Equipe de Suporte:** Julio C. Fernandes, Diego S. Fernandes, Kayle, Jean

## Sobre

> Projeto feito com o único intuito de servir como base e referência de estudo, nosso objetivo aqui é expor os perigos que estamos nos colocando ao baixar softwares de terceiros não licenciados (Crackeados), acessar sites impróprios, clicar em links duvidosos (Phising), e qualquer outro tipo de falha, seja humana, ou de sistema.

## Como Funciona?

> Nosso Script atua com uma conexão cliente/servidor onde ocorre troca de dados via sockets de rede, a magia acontece quando invertemos essa conexão, ao invés do cliente requisitar coisas ao servidor, é o nosso servidor que faz as requisições ao cliente, usando algumas bibliotecas e um pouco de engenharia reversa conseguimos enviar comandos e parâmetros para serem executado na máquina da vítima, tendo acesso a navegar nas suas pastas, ver seus arquivos e até copiá-los para o nosso servidor, desta forma, o script pode ser hospedado em uma nuvem (AWS, por exemplo) e receber várias conexões (infecções) de vários clientes (Vitimas), assim podendo criar um ataque coordenado onde todos responde ao mesmo comando, ou até mesmo gerando ataques individuais (em desenvolvimento).

## Para Dev's
> Foi utilizado a linguagem de programação python 3.11.4 com algumas bibliotecas descritas no início do código.

[!IMPORTANT]
> Esse é um projeto em desenvolvimento, erros e bugs podem ocorrer!

[!WARNING]
> Esse Script pode causar problemas em sua máquina, problemas com terceiros ou problemas com a LEI, Reforço aqui que serve apenas para Estudo, Não queremos gerar danos a **NINGUEM**, então se não sabe o que está fazendo, ou como funciona, por favor **NÃO MEXA**
