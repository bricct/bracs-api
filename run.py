from app import create_app

if __name__ == '__main__':
  app_instance = create_app()
  app_instance.run()