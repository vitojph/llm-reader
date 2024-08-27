# README

This contains an LLM-based reader that finds and summarizes interesting readings.

## Install

```shell
uv install
```

## Commands

### Create the database

```shell
make db
```

###  Find intereting readings

```shell
make analyze
```

###  Clean database and and find interesting readings

```shell
make all
```

###  Send emails with the latest interesting readings

```shell
make send
```
