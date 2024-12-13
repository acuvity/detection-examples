[<- Back to README.md](README.md)
<img src="https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/icons/acuvity.png" width="100" height="100">

## Detection Files with outputs

### Upload any of the following options with the prompts to see the detection capabilities.

**1. Document Name:** [code.go](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/code.go) <br>
- **Prompt:** Explain the code <br>
- **Type:** Code <br>
- **Expectation:**
code/go, aws_secret_key, credentials <br>
- **Findings:** <br>
  - extractor:files <br>
  - modality:code/go <br>
  - secret:aws_secret_key <br>
  - secret:credentials <br>
  - topic:unclassified <br>
- **Matches** Yes <br><br>

**2. Document Name:** [private-key.pem](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/private-key.pem) <br>
- **Prompt:** N/A <br>
- **Type:** pem <br>
- **Expectation:**
application/pem, private_key <br>
- **Findings:**
  - extractor:files <br>
  - modality:application/pem <br>
  - secret:private_key <br>
  - topic:unclassified <br>
- **Matches** Yes<br><br>

**3. Document Name:** [public-cert.ppt](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/public-cert.ppt) <br>
- **Prompt:**  N/A<br>
- **Type:** ppt<br>
- **Expectation:**
 application/pem, cryptography/public_key<br>
- **Findings:** <br>
  - extractor:files <br>
  - modality:application/pem <br>
  - topic:cryptography/public_key <br>
- **Matches** Yes<br><br>

**4. Document Name:**
[ssn.csv](https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/files/ssn.csv) <br>
- **Prompt:**  Summarize<br>
- **Type:** csv<br>
- **Expectation:**
 PII ssn<br>
- **Findings:** <br>
  - extractor:files
  - modality:document/csv
  - language:french
  - pii:person
  - pii:ssn
  - topic:unclassified
- **Matches** Yes<br><br>
