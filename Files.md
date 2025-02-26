# Files files
## Piis

### PII SSN_1


Content:

```csv
Antoine,456-33-2345

```

Modality:
  - *document/csv*

Category:
  - *document/personal*

PIIs:
 - *ssn*:
   - start: 8, end: 19, score: 0.33 (`456-33-2345`)


Topics:
 - *category/personal: 0.66*
 - *domain/general: 0.66*
 - *extracted/csv_cell_content: 1.0*

### ssn.csv


Content:

```csv
Homer Simpson,548-19-7362,M
Marge Simpson,913-74-2856,F
Bart Simpson,274-81-6359,M
Lisa Simpson,681-29-4573,F
Maggie Simpson,739-26-5841,F

```

Modality:
  - *document/csv*

Category:
  - *document/personal*

PIIs:
 - *person*:
   - start: 0, end: 13, score: 0.85 (`Homer Simpson`)
   - start: 28, end: 41, score: 0.85 (`Marge Simpson`)
   - start: 56, end: 68, score: 0.85 (`Bart Simpson`)
   - start: 83, end: 95, score: 0.85 (`Lisa Simpson`)
   - start: 110, end: 124, score: 0.85 (`Maggie Simpson`)

 - *ssn*:
   - start: 14, end: 25, score: 0.33 (`548-19-7362`)
   - start: 42, end: 53, score: 0.33 (`913-74-2856`)
   - start: 69, end: 80, score: 0.33 (`274-81-6359`)
   - start: 96, end: 107, score: 0.33 (`681-29-4573`)
   - start: 125, end: 136, score: 0.33 (`739-26-5841`)


Topics:
 - *category/personal: 0.64*
 - *domain/general: 0.67*
 - *extracted/csv_cell_content: 1.0*
## Random

### public-cert.pem


Content:

```pem
-----BEGIN CERTIFICATE-----
MIIBaDCCAQ6gAwIBAgIRAIG2E+V20zUv4HSkuID33PcwCgYIKoZIzj0EAwIwETEP
MA0GA1UEAxMGc2F0eWFtMB4XDTI0MDMxOTE5MzUxN1oXDTI1MDMxNDE5MzUxN1ow
ETEPMA0GA1UEAxMGc2F0eWFtMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEGlqc
xcp16l8nApqshkSh0bNn6tr3rZll8gYeTj7gWGnFkJBxDvE5ceJqBTkw1qqD18cC
KL5RMcmR7aIvVWwNO6NHMEUwDgYDVR0PAQH/BAQDAgWgMBMGA1UdJQQMMAoGCCsG
AQUFBwMCMAwGA1UdEwEB/wQCMAAwEAYDVR0RBAkwB4EFY291b3UwCgYIKoZIzj0E
AwIDSAAwRQIhANl3VilyFQD20hsIEUelrC9VbeJaQywdxntgck7KpCPKAiBzG0Q/
HbWPI2JUkPjA8P1lkMydIaf9JsxDa8GBSmoRmw==
-----END CERTIFICATE-----

```

Modality:
  - *application/pem*

Category:
  - *application/pem*

Topics:
 - *contains/public_key: 1.0*
## Secrets

### code.go


Content:

```go
package main

import (
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
)

func main() {
	accessKeyID := "AKIA1234567890ABCDEF"
	secretAccessKey := "lDFOLjlO291/832nm&"
	myRegion := "us-west-2"

	// Initialize a session using Amazon S3
	sess, err := session.NewSession(&aws.Config{
		Region:      aws.String(myRegion),
		Credentials: credentials.NewStaticCredentials(accessKeyID, secretAccessKey, ""),
	})
	if err != nil {
		log.Fatalf("Error creating session: %s", err)
	}

	// Create S3 service client
	svc := s3.New(sess)

	// List the S3 buckets using the service client
	result, err := svc.ListBuckets(nil)
	if err != nil {
		log.Fatalf("Unable to list buckets: %s", err)
	}

	fmt.Println("Buckets:")
	for _, b := range result.Buckets {
		fmt.Printf("* %s\n", aws.StringValue(b.Name))
	}
}

```

Modality:
  - *code/go*

Category:
  - *code/go*

Secrets:
 - *aws_secret_key*:
   - start: 231, end: 251, score: 1.0 (`AKIA1234567890ABCDEF`)

 - *credentials*:
   - start: 274, end: 292, score: 0.64 (`lDFOLjlO291/832nm&`)



### private-key.pem


Content:

```pem
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIAHnEky1yE8coMrZVZ/ghcqCkq/+iJ0PHwyfMVXKd80/oAoGCCqGSM49
AwEHoUQDQgAEGlqcxcp16l8nApqshkSh0bNn6tr3rZll8gYeTj7gWGnFkJBxDvE5
ceJqBTkw1qqD18cCKL5RMcmR7aIvVWwNOw==
-----END EC PRIVATE KEY-----

```

Modality:
  - *application/pem*

Category:
  - *application/pem*

Secrets:
 - *private_key*:
   - start: 31, end: 197, score: 1.0 (`MHcCAQEEIAHnEky1yE8coMrZVZ/ghcqCkq/+iJ0PHwyfMVXKd80/oAoGCCqGSM49
AwEHoUQDQgAEGlqcxcp16l8nApqshkSh0bNn6tr3rZll8gYeTj7gWGnFkJBxDvE5
ceJqBTkw1qqD18cCKL5RMcmR7aIvVWwNOw==`)


