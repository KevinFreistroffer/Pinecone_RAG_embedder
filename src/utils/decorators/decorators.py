def log_function(func):
    def wrapper():
        print("Starting function " + func.__name__ + " execution.")
        func()
        print("Ending function " + func.__name__ + " execution.")

    return wrapper
