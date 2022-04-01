# Josué's Automatic Watering Can - RegaBão

### Basic Endpoint Configurations
CRUD of plant information:
- GET plants/{with or without id} (retrieve the list of registered plants)
- POST plants (register new plant)
- PUT plants/{id} (update plant)
- DELETE plants/{id} (delete plant)

CRUD from watering can settings:
- GET watering cans/{with or without id} (retrieve the list of registered watering cans)
- POST watering cans (register new watering can)
- PUT watering cans/{id} (update watering can)
- DELETE watering cans/{id} (delete watering can)

### How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:
```
$ .\env\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:
```
$ (env) python app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```