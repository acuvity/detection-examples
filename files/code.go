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
	secretAccessKey := "YOUR_SECRET_ACCESS_KEY"
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
