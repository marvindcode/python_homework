import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def my_decorator(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        logger.log(logging.INFO, "this string would be logged")
        return value
    return wrapper

@my_decorator
def hello_world():
    print("Hello, World!")

@my_decorator
def take_args(*args):
    print(f"Print positional args: {args}")
    return True

@my_decorator
def take_kwargs(**kwargs):
    print(f"Print keyword args: {kwargs}")
    return my_decorator

if __name__ == "__main__":
    hello_world()
    take_args(5, 10, 15)
    take_kwargs(x=1, y=2, z=3)
