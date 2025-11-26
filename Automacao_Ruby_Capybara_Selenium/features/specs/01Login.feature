#language:pt

@01Login
Funcionalidade: Acessar Página Login
    Para que eu possa Efetuar Login
    Sendo um usuário 
    Posso acessar a funcionalidade

Contexto: Acesso ao SPD
    Dado que eu estou na página de login da aplicação

    @EfetuarLogin
    Cenário: Efetuar Login

    Quando preencho o campo de usuario
    E preencho o campo de senha
    E aciono a opção de Acessar
    Então acesso a aplicacao

    @LoginIncorretoUsuario
    Cenário: Efetuar Login

    Quando preencho o campo de usuario incorretamente
    E preencho o campo de senha
    E aciono o botão Acessar
    Então não acesso a aplicacao

    @LoginIncorretoSenha
    Cenário: Efetuar Login

    Quando preencho o campo de usuario 
    E preencho o campo de senha incorretamente
    E aciono o botão Acessar
    Então não acesso a aplicacao