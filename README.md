# Polarizer backend

## Installation
### Clone repo
```agsl
git clone git@github.com:digital-peace-talks/polarizer-backend.git
cd polarizer-backend
```
### Create virtualenv and install python dependencies
```agsl
python3 -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
``` 

## Usage
### Start server
```agsl
flask --app rest/server run -p 4080
```

### Register new session (required for any further API interactions)
```agsl
http :4080/register_session
```

### Get current layout
```agsl
http ':4080/<session_id>/layout'
```

### Get an edge's value
```agsl
http ':4080/<session_id>/edge?left=33&right=39'
```

### Update an edge (returns updated graph)
#### Parameter ranges:
`dissent : 0 to 10`\
`respect: -5 to 5`

```agsl
http ':4080/<session_id>/update?left=33&right=39&dissent=1&respect=3'
```

### Update an edge (POST version)
```agsl
http ':4080/<session_id>/update' left=33 right=39 dissent=1 respect=3
```

### Update an edge, returning an svg
#### Parameter ranges:
```agsl
http ':4080/<session_id>/update_svg?left=33&right=39&dissent=1&respect=3'
```

(Sorry for the brevity :))