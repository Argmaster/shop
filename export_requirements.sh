#!/bin/bash
poetry export --with=dev >> app/requirements.txt
poetry export >> app/requirements.prod.txt
