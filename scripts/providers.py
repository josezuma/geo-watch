#!/usr/bin/env python3
"""LLM provider adapters."""
def query_openai(prompt):
    return {'provider': 'openai', 'response': 'mock'}
