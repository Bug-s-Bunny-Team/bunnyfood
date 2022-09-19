#!/usr/bin/env bash

coverage run -m pytest tests
coverage report -m
