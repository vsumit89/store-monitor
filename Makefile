# Makefile for store monitoring

# Load environment variables from .env file
include .env

# Targets
.PHONY: create_tables

create_tables:
	cd scripts && ./create_tables.sh
