from region_service import create_app

app = create_app(False)

if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True)