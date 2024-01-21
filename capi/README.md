# CAPI (Central API)

## Endpoint: `/article`

### Description

The `/article` endpoint is designed to process articles by checking their existence in the database, classifying them using an NLP service, and then sending this data along with keywords to a RAD service for further processing. The endpoint returns the classification and related articles.

### HTTP Method: POST

### Request Format

The request should be a JSON object containing the following fields:

- `url` (string): The URL of the article.
- `text` (string): The selected text or content of the article.

Example:

```json
{
  "url": "http://example.com/article",
  "text": "The quick brown fox jumps over the lazy dog"
}
```

### Response Format

The response is a JSON object containing the following fields:

- `status` (string): Indicates the success or error status.
- `classification` (integer): -100 to 100. The classification of the article obtained from the NLP service.
- `related_articles` (array): A list of related articles as determined by the RAD service. Each article in the list is an object containing fields like `id`, `url`, `political_bias`, `created_at`, and `relevance`.

Example of a successful response:

```json
{
  "status": "success",
  "classification": 50,
  "related_articles": [
    {
      "id": 1,
      "url": "https://example.com/related_article",
      "political_bias": 50,
      "created_at": "2024-01-21 20:32:03",
      "relevance": 0
    }
    // ... other related articles ...
  ]
}
```

Example of an error response:

```json
{
  "status": "error",
  "message": "Missing url or text in the request"
}
```

### Error Handling

- If the request data is missing or incomplete, the API will respond with a 400 Bad Request status.
- If there are issues with classification or RAD service processing, the API will respond with a 500 Internal Server Error status.

---
