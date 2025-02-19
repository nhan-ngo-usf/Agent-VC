# VC Agent Data Pipeline

A data pipeline for collecting and processing startup information from various sources including Typeform submissions, LinkedIn profiles, and company websites.

## Features

- Collect startup data from Typeform submissions
- Extract and validate LinkedIn profiles using Proxycurl API
- Web crawling for company websites to gather additional insights
- Structured data storage in PostgreSQL
- Data validation and normalization
- Comprehensive testing suite

## Prerequisites

- Python 3.8+
- PostgreSQL
- Typeform account and API key
- Proxycurl API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/vc-agent-data-pipeline.git
cd vc-agent-data-pipeline
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create configuration file:

```bash
cp config/config.example.yaml config/config.yaml
```

5. Update `config.yaml` with your credentials:

```yaml
database:
  connection_string: 'postgresql://username:password@localhost:5432/vc_agent'

typeform:
  api_key: 'your_typeform_api_key'
  form_id: 'your_form_id'

proxycurl:
  api_key: 'your_proxycurl_api_key'

logging:
  level: 'INFO'
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

6. Initialize database:

```bash
python scripts/init_db.py
```

## Usage

### Import Data from Typeform

```bash
python scripts/import_typeform_data.py
```

This will:

1. Fetch responses from Typeform
2. Process and validate the data
3. Fetch LinkedIn profiles
4. Crawl company websites
5. Store all data in the database

### Test Website Crawler

```bash
python tests/test_website_crawler_live.py
```

## Data Models

### Startup

- Basic company information
- Founder details
- Metrics (users, revenue)
- Funding information

### LinkedIn Profile

- Professional background
- Work history
- Education
- Skills and accomplishments

### Website Data

- Company description
- Team information
- Technology stack
- Contact details
- Social media presence

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Features

1. Create new model in `src/models/`
2. Add data ingestion logic in `src/data_ingestion/`
3. Update database schema in `scripts/init_db.py`
4. Add tests in `tests/`

## Common Issues

1. API Rate Limits:

- Typeform: 10 requests/second
- Proxycurl: Varies by plan

2. Website Crawling:

- Some websites may block automated requests
- Use appropriate delays between requests

## Dependencies

```txt:requirements.txt
beautifulsoup4==4.12.2
requests==2.31.0
SQLAlchemy==2.0.25
psycopg2-binary==2.9.9
PyYAML==6.0.1
pytest==7.4.4
pytest-mock==3.12.0
python-dotenv==1.0.0
```
