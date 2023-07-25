# `cli`

HealthFirstAI Prototype CLI

**Usage**:

```console
$ cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get-cached-plan`: Get diet plan from Redis
* `get-diet-plan`: Get a meal plan from the database
* `get-meal`: Get meal from the database given meal name
* `get-user-info`: Get user info from the database
* `reinsert-vectors`: Delete all vectors in nutrition_vectors...
* `store-plan`: Store a plan in the database
* `test-agent`: Test ReAct Diet Plan Agent

## `cli get-cached-plan`

Get diet plan from Redis

**Usage**:

```console
$ cli get-cached-plan [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--help`: Show this message and exit.

## `cli get-diet-plan`

Get a meal plan from the database

**Usage**:

```console
$ cli get-diet-plan [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--include-ingredients / --no-include-ingredients`: [default: include-ingredients]
* `--help`: Show this message and exit.

## `cli get-meal`

Get meal from the database given meal name

**Usage**:

```console
$ cli get-meal [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--include-ingredients / --no-include-ingredients`: [default: include-ingredients]
* `--include-nutrients / --no-include-nutrients`: [default: include-nutrients]
* `--meal-choice TEXT`: [default: b]
* `--help`: Show this message and exit.

## `cli get-user-info`

Get user info from the database

**Usage**:

```console
$ cli get-user-info [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--help`: Show this message and exit.

## `cli reinsert-vectors`

Delete all vectors in nutrition_vectors and insert new vectors

**Usage**:

```console
$ cli reinsert-vectors [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cli store-plan`

Store a plan in the database

**Usage**:

```console
$ cli store-plan [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--help`: Show this message and exit.

## `cli test-agent`

Test ReAct Diet Plan Agent

**Usage**:

```console
$ cli test-agent [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--input TEXT`: [default: What am I having for dinner?]
* `--help`: Show this message and exit.
