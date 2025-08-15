# API Decryptor

API desenvolvida em Django REST para automatizar o processamento de comprovantes de pagamento recebidos via WhatsApp. O sistema permite o upload de arquivos criptografados (.enc), realiza a descriptografia, extrai informações relevantes de PDFs e imagens utilizando OCR, e disponibiliza esses dados por meio de endpoints seguros e autenticados. Ideal para integrar fluxos de validação financeira, auditoria ou automação de recebimento de comprovantes.

## Funcionalidades

- Upload e descriptografia de mídias (.enc) do WhatsApp
- Extração de texto de PDFs e imagens via OCR
- API JWT para autenticação
- Painel administrativo customizado (Jazzmin)

## Instalação

```sh
git clone https://github.com/seuusuario/api-decrypt.git
cd api-decrypt
python -m venv venv-decrypt
source venv-decrypt/Scripts/activate  # Windows
source venv-decrypt/bin/activate      # Linux/Mac

pip install -r requirements.txt
```

## Migração do banco

```sh
python manage.py migrate
```

## Execução

```sh
python manage.py runserver
```

## Autenticação

Utilize os endpoints JWT em [`authentication/urls.py`](authentication/urls.py):

- `/api/v1/authentication/token/`
- `/api/v1/authentication/token/refresh/`
- `/api/v1/authentication/token/verify/`

## Endpoints principais

Veja [`decryptor/urls.py`](decryptor/urls.py):

- `POST /api/v1/paymentproof/` — Cria comprovante
- `GET /api/v1/paymentproof/` — Lista comprovantes
- `GET /api/v1/paymentproof/<id>/readfile/` — Lê texto do comprovante
- `GET /api/v1/paymentproof/readfile/` — Lê todos os comprovantes processados

## Estrutura

- [`core/settings.py`](core/settings.py): configurações do projeto
- [`decryptor/models.py`](decryptor/models.py): modelo principal
- [`decryptor/utils.py`](decryptor/utils.py): funções de descriptografia e leitura
- [`decryptor/views.py`](decryptor/views.py): views da API


## Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django_5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-FFDD00?style=for-the-badge&logo=python&logoColor=black)
![JWT](https://img.shields.io/badge/JWT%20Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
