# Sistema Bancário em Python

Este projeto é um **sistema bancário simples** desenvolvido em Python, utilizando conceitos de programação orientada a objetos. O sistema permite o cadastro de clientes, criação de contas correntes, depósitos, saques e consulta de extrato, tudo via interface de linha de comando.

## Funcionalidades

- **Cadastro de Usuários:** Crie clientes informando nome, CPF, data de nascimento e endereço.
- **Criação de Contas Correntes:** Associe contas a clientes já cadastrados.
- **Depósitos:** Realize depósitos em contas existentes.
- **Saques:** Efetue saques respeitando limites de valor, saldo e quantidade diária.
- **Extrato:** Consulte o histórico de transações e saldo da conta.
- **Listagem de Contas:** Visualize todas as contas cadastradas no sistema.

## Estrutura do Projeto

O sistema é composto pelas seguintes classes principais:

- `Cliente` e `PessoaFisica`: Representam clientes do banco.
- `Conta` e `ContaCorrente`: Modelam contas bancárias, incluindo saldo, limite e restrições de saque.
- `Transacao`, `Deposito`, `Saque`: Representam operações financeiras e seu registro.
- `Historico`: Gerencia o extrato de cada conta.
- `SistemaBancario`: Controla o fluxo principal do programa, cadastro, operações e menu.

## Como Executar

1. **Pré-requisitos:**  
   - Python 3.x instalado.

2. **Execução:**  
   Salve o código em um arquivo, por exemplo, `banco.py`, e execute no terminal:


