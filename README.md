# Rabe Leads

CRM interno para pesquisar empresas, analisar sites e priorizar oportunidades comerciais.

## O que este projeto faz

- Pesquisa empresas pela API oficial Google Places.
- Salva nome, categoria, cidade, UF, telefone, site e URL do Google Maps.
- Analisa site, HTTPS, responsividade, formulário, WhatsApp e redes sociais.
- Consulta PageSpeed para performance, acessibilidade e SEO.
- Calcula score de oportunidade.
- Organiza o funil: novo, contatado, respondeu, reunião, proposta, fechado e perdido.
- Gera textos personalizados para primeiro contato.
- Exporta os leads para CSV.

## Limites importantes

Este projeto não raspa LinkedIn ou Instagram. As APIs dessas plataformas possuem permissões e usos específicos, e não oferecem uma busca pública irrestrita de empresas e contatos.

Também não dispara e-mail ou WhatsApp em massa. O contato é aberto manualmente pelo usuário. Isso reduz bloqueios e permite validar finalidade, necessidade, transparência, oposição e a lista “não contatar”.

## Estrutura

```text
rabe-leads/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   ├── crud.py
│   ├── schemas.py
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
├── scripts/
│   ├── init_db.py
│   ├── seed_cities.py
│   ├── collect_places.py
│   └── analyze_leads.py
├── .env.example
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.11+
- MySQL 8+
- Chave da API Google Places
- Chave PageSpeed opcional

## Banco MySQL

```sql
CREATE DATABASE rabe_leads
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'rabe_leads'@'localhost' IDENTIFIED BY 'troque-esta-senha';
GRANT ALL PRIVILEGES ON rabe_leads.* TO 'rabe_leads'@'localhost';
FLUSH PRIVILEGES;
```

## Instalação local

```bash
cd rabe-leads

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

Edite o `.env`:

```env
MYSQL_DATABASE=rabe_leads
MYSQL_USER=rabe_leads
MYSQL_PASSWORD=troque-esta-senha
GOOGLE_PLACES_API_KEY=sua-chave
GOOGLE_PAGESPEED_API_KEY=sua-chave
```

Crie as tabelas:

```bash
python -m scripts.init_db
```

Opcionalmente, carregue os municípios do IBGE:

```bash
python -m scripts.seed_cities
```

## Rodar no VS Code

```bash
uvicorn app.main:app --reload
```

Acesse:

```text
http://127.0.0.1:8000
```

## Coletar leads pelo terminal

```bash
python -m scripts.collect_places \
  --category "empresa" \
  --city "Cuiabá" \
  --state "MT"
```

Outros exemplos:

```bash
python -m scripts.collect_places --category "consultoria" --city "Goiânia" --state "GO"
python -m scripts.collect_places --category "loja" --city "Campinas" --state "SP"
python -m scripts.collect_places --category "transportadora" --city "Joinville" --state "SC"
```

## Analisar sites e gerar score

Sem PageSpeed:

```bash
python -m scripts.analyze_leads --limit 50
```

Com PageSpeed:

```bash
python -m scripts.analyze_leads --limit 20 --pagespeed
```

Use PageSpeed com moderação porque há cotas e custo operacional.

## Estratégia de score

- Sem site: +45
- Sem HTTPS: +15
- Não responsivo: +20
- Sinais de site antigo: +15
- Performance muito baixa: até +15
- SEO baixo: +8
- Telefone: +5
- E-mail: +5
- Instagram: +4
- WhatsApp no site: +3

O score é limitado a 100.

## Uso responsável

- Utilize apenas dados empresariais publicamente disponibilizados.
- Registre a origem do dado.
- Mantenha uma lista de oposição em `do_not_contact`.
- Não contate novamente quem solicitar remoção.
- Evite números pessoais quando não houver relação clara com a atividade empresarial.
- Personalize o primeiro contato.
- Não envie anexos ou mensagens repetidas antes de obter interesse.
- Defina prazo de retenção e remova dados sem utilidade.
