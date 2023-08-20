#!/bin/bash

# Default list of modules
default_modules=("golang" "kotlin" "ktor" "python")

# Check if a module name is provided as an argument
if [ $# -eq 0 ]; then
    echo "No module name provided. Building all modules."
else
    default_modules=("$@")
fi

for module in "${default_modules[@]}"; do
    echo "- $module"
    eval "./bin/build-$module.sh"
done
