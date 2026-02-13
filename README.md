# PROJETO ARBOVITA

SOBRE O PROJETO
-----------------------------------------------------------------------------
O ArboVita é uma plataforma dedicada à transformação urbana de Belém do Pará
através da arborização. O projeto visa combater ilhas de calor, melhorar a
qualidade de vida e promover o plantio consciente de mudas.

Funcionalidades principais:
- Mapa Arbóreo (Blog/Visualização).
- Cadastro de mudas e histórico de plantio.
- Sistema de "Selo Verde" para empresas parceiras.
- Conteúdo educativo sobre benefícios ambientais e cuidados com plantas.

EQUIPE
-----------------------------------------------------------------------------
- Francisco Begot: Chefe da Liderança
- Theo Mello: Chefe de Produção Audiovisual
- José Júnior: Líder de Desenvolvimento
- Manoel Clipes: Coordenador de Desenvolvimento

-----------------------------------------------------------------------------
COMO CONFIGURAR O AMBIENTE (Instalação)
-----------------------------------------------------------------------------
Este projeto utiliza Python para o servidor backend. Siga os passos abaixo
para preparar seu computador.

PRÉ-REQUISITOS:
- Python instalado (versão 3.12 ou superior recomendada).
- Navegador de internet (Chrome, Firefox, Edge, etc.).

PASSO 1: PREPARAR O AMBIENTE VIRTUAL
Recomendamos usar um ambiente virtual para não misturar as bibliotecas do
projeto com o seu sistema.

1. Abra o terminal (Linux/Mac) ou CMD/PowerShell (Windows) na pasta do projeto.

2. Crie o ambiente virtual (caso a pasta 'venv' não exista ou queira recriar):
   > python -m venv venv

3. Ative o ambiente virtual:

   - No Windows (PowerShell):
     > .\venv\Scripts\Activate

   - No Windows (CMD):
     > venv\Scripts\activate.bat

   - No Linux/Mac:
     > source venv/bin/activate

   (Você saberá que funcionou se aparecer "(venv)" antes do comando no terminal).

PASSO 2: INSTALAR DEPENDÊNCIAS
Com o ambiente virtual ativado, instale as bibliotecas necessárias listadas
no arquivo requirements.txt:

   > pip install -r requirements.txt

-----------------------------------------------------------------------------
COMO RODAR O PROJETO
-----------------------------------------------------------------------------

1. Certifique-se de que o ambiente virtual está ativado (Passo 1.3).

2. Execute o servidor Python:
   > python server.py

3. O terminal mostrará um endereço local (geralmente http://127.0.0.1:5000).
   Abra esse endereço no seu navegador para visualizar o site.

-----------------------------------------------------------------------------
ESTRUTURA DE PASTAS
-----------------------------------------------------------------------------
/assets
   -> Contém imagens (img), estilos (css), scripts (js) e bibliotecas (vendor).

/templates
   -> Arquivos HTML renderizados pelo Flask.

server.py
   -> O "cérebro" do backend, responsável pelas rotas e lógica.

-----------------------------------------------------------------------------
BANCO DE DADOS (SQLite)
-----------------------------------------------------------------------------
O projeto utiliza um banco de dados SQLite, que é leve e não requer instalação
de servidores complexos.

- Arquivo: database.db (criado automaticamente na raiz do projeto).
- Gerenciamento: O arquivo server.py verifica se o banco existe ao iniciar.
  Se não existir, ele cria o arquivo e as tabelas automaticamente.

Estrutura das tabelas:
- users: Armazena dados de cadastro e login.
- messages: Guarda as mensagens enviadas pelo formulário de contato.
- newsletter: Lista de emails inscritos para novidades.

-----------------------------------------------------------------------------
SISTEMA DE PAGAMENTO (Simulação)
-----------------------------------------------------------------------------
O projeto inclui um fluxo de assinatura (Billing) para fins de demonstração
de interface e experiência do usuário.

- Funcionamento: O formulário de assinatura envia os dados para a API.
- Backend: A rota /api/subscribe simula o processamento e retorna sucesso
  imediato.
- Segurança: Nenhuma cobrança real é efetuada. Dados de cartão de crédito
  NÃO são salvos no banco de dados. O frontend utiliza o armazenamento do
  navegador (localStorage) apenas para persistir o estado de "Assinante"
  durante a navegação.


