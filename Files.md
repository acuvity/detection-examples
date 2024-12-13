[<- Back to README.md](README.md)
<img src="https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/icons/acuvity.png" width="100" height="100">

## Detection Files with outputs

### Upload any of the following options with the prompts to see the detection capabilities.

#### 1. Document Name: [code.go](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/code.go)

- **Prompt:** Explain the code
- **Type:** Code
- **Expectation:** code/go, aws_secret_key, credentials
- **Findings:**
  - extractor:files
  - modality:code/go
  - secret:aws_secret_key
  - secret:credentials
  - topic:unclassified
- **Matches** Yes

#### 2. Document Name: [private-key.pem](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/private-key.pem)

- **Prompt:** N/A
- **Type:** pem
- **Expectation:** application/pem, private_key
- **Findings:**
  - extractor:files
  - modality:application/pem
  - secret:private_key
  - topic:unclassified
- **Matches** Yes

#### 3. Document Name: [public-cert.ppt](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/public-cert.ppt)

- **Prompt:** N/A
- **Type:** ppt
- **Expectation:** application/pem, cryptography/public_key
- **Findings:**
  - extractor:files
  - modality:application/pem
  - topic:cryptography/public_key
- **Matches** Yes

#### 4. Document Name: [ssn.csv](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/ssn.csv)

- **Prompt:**  Summarize
- **Type:** csv
- **Expectation:** PII ssn, PII person
- **Findings:**
  - extractor:files
  - modality:document/csv
  - pii:person
  - pii:ssn
  - topic:unclassified
- **Matches** Yes
