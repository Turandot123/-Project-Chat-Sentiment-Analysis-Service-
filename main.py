from src.api import app


def main():
    app.run(host='localhost', port=8080)


if __name__ == '__main__':
    main()
