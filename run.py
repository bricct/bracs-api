from app import create_app

if __name__ == "__main__":
    app_instance = create_app(True)
    app_instance.run()
