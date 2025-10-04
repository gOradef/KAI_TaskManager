from App import setup, init, dump

if __name__ == '__main__':
    setup()
    app: App = init()
    app.dump()