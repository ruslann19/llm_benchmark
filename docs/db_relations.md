Структура базы данных

```mermaid
erDiagram
    LLM_RESPONSE ||--|{ TASK : "answers"
    LLM_RESPONSE ||--|{ LLMInfo : "uses"
    TASK {
        int id PK
        string question
        string answer
        string source_url
        date published_date
        datetime created_at
        string state
        int benchmark_version
    }
    LLM_RESPONSE {
        int id PK
        int task_id FK
        int llm_id FK
        string response
        bool is_valid
        date created_at
    }
    LLMInfo {
        int id PK
        string model_name
        string provider
        string api_url
    }
```
