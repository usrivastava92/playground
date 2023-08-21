#!/bin/bash

cd golang

if [ -z "$(find . -name '*.go')" ]; then
  echo "No Go files found. Skipping build and test."
  exit 0
fi

go build -v .
go test -v .
