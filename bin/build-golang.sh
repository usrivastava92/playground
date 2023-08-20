#!/bin/bash

if [ -z "$(find . -name '*.go')" ]; then
  echo "No Go files found. Skipping build and test."
  exit 0
fi

cd golang
go build -v .
go test -v .
