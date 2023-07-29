# `cli`

HealthFirstAI Prototype CLI

**Usage**:

```console
$ cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `build-docs`: Runs a chain of functions to build the...
* `cache-diet-plan`: Stores diet plan as it is in the SQL...
* `edit-cached-meal`: Get diet plan from Redis
* `get-cached-meal`: Get meal from the Redis Cache given meal name
* `get-cached-plan`: Get diet plan from Redis
* `get-diet-plan`: Get a meal plan from the database
* `get-meal`: Get meal from the SQL database given meal...
* `get-user-info`: Get user info from the database
* `reinsert-vectors`: Delete all vectors in nutrition_vectors...
* `test-advice-agent`: Test the core functionality of the advice...
* `test-chat-agent`: Test ReAct Diet Plan Agent
* `test-openai-func-sql-agent`: Test OpenAI Function SQL Agent
* `test-std-sql-agent`: Test ReAct Diet Plan Agent

## `cli build-docs`

Runs a chain of functions to build the documentation

**Usage**:

```console
$ cli build-docs [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cli cache-diet-plan`

Stores diet plan as it is in the SQL database in Redis

**Usage**:

```console
$ cli cache-diet-plan [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--help`: Show this message and exit.

## `cli edit-cached-meal`

Get diet plan from Redis

**Usage**:

```console
$ cli edit-cached-meal [OPTIONS] AGENT_INPUT MEAL_CHOICE:{Breakfast|Lunch|Dinner|Snack|Drink|}
```

**Arguments**:

* `AGENT_INPUT`: [required]
* `MEAL_CHOICE:{Breakfast|Lunch|Dinner|Snack|Drink|}`: [required]

**Options**:

* `--user-id INTEGER`: [default: 1]
* `--include-ingredients / --no-include-ingredients`: [default: no-include-ingredients]
* `--store-in-cache / --no-store-in-cache`: [default: no-store-in-cache]
* `--help`: Show this message and exit.

## `cli get-cached-meal`

Get meal from the Redis Cache given meal name

**Usage**:

```console
$ cli get-cached-meal [OPTIONS]
```

**Options**:

* `--meal-choice [b|l|d|s|]`: [default: MealChoice.breakfast]
* `--uid INTEGER`: [default: 1]
* `--include-ingredients / --no-include-ingredients`: [default: no-include-ingredients]
* `--include-nutrients / --no-include-nutrients`: [default: no-include-nutrients]
* `--help`: Show this message and exit.

## `cli get-cached-plan`

Get diet plan from Redis

**Usage**:

```console
$ cli get-cached-plan [OPTIONS]
```

**Options**:

* `--uid INTEGER`: [default: 1]
* `--include-ingredients / --no-include-ingredients`: [default: include-ingredients]
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

Get meal from the SQL database given meal name

**Usage**:

```console
$ cli get-meal [OPTIONS]
```

**Options**:

* `--meal-choice [b|l|d|s|]`: [default: MealChoice.breakfast]
* `--uid INTEGER`: [default: 1]
* `--include-ingredients / --no-include-ingredients`: [default: no-include-ingredients]
* `--include-nutrients / --no-include-nutrients`: [default: no-include-nutrients]
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

## `cli test-advice-agent`

Test the core functionality of the advice agent

**Usage**:

```console
$ cli test-advice-agent [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cli test-chat-agent`

Test ReAct Diet Plan Agent

**Usage**:

```console
$ cli test-chat-agent [OPTIONS] INPUT
```

**Arguments**:

* `INPUT`: [required]

**Options**:

* `--uid INTEGER`: [default: 1]
* `--session-id TEXT`: [default: my-session]
* `--help`: Show this message and exit.

## `cli test-openai-func-sql-agent`

Test OpenAI Function SQL Agent

**Usage**:

```console
$ cli test-openai-func-sql-agent [OPTIONS] INPUT
```

**Arguments**:

* `INPUT`: [required]

**Options**:

* `--help`: Show this message and exit.

## `cli test-std-sql-agent`

Test ReAct Diet Plan Agent

**Usage**:

```console
$ cli test-std-sql-agent [OPTIONS] INPUT
```

**Arguments**:

* `INPUT`: [required]

**Options**:

* `--help`: Show this message and exit.
