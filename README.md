# ssh_primitive_reverse

Authores: Alessandro C. Rosão, Yago J. Ramos

Colaboradores: Bruno C. Marini, Alexandre Queiroz

Equipe de Suporte: Julio, Diego, Kayle, Jean

## Sobre

Projeto feito com o único intuito de servir como base e referência de estudo, nosso objetivo aqui é expor os perigos que estamos nos colocando ao baixar softwares de terceiros não licenciados (Crackeados), acessar sites impróprios, clicar em links duvidosos (Phising), e qualquer outro tipo de falha, seja humana, ou de sistema.

## Como Funciona?

Nosso Script atua com uma conexão cliente/servidor onde ocorre troca de dados via sockets de rede, a magia acontece quando invertemos essa conexão, ao invés do cliente requisitar coisas ao servidor, é o nosso servidor que faz as requisições ao cliente, usando algumas bibliotecas e um pouco de engenharia reversa conseguimos enviar comandos e parâmetros para serem executado na máquina da vítima, tendo acesso a navegar nas suas pastas, ver seus arquivos e até copiá-los para o nosso servidor, desta forma, o script pode ser hospedado em uma nuvem (AWS, por exemplo) e receber várias conexões (infecções) de vários clientes (Vitimas), assim podendo criar um ataque coordenado onde todos responde ao mesmo comando, ou até mesmo gerando ataques individuais (em desenvolvimento).
