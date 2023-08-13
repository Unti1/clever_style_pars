from tools import *
from settings import *

# if __name__ == "__main__":
#     q = Pars(True)
#     q.test()

exc_path = ChromeDriverManager().install()
exc_path = exc_path.rsplit("/",maxsplit=1)
exc_path[-1] = exc_path[-1].replace('.',f'_1.')
copy_name = "/".join(exc_path)
print(copy_name)
