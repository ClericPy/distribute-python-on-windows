def main():
    import bottle
    import sys
    import os

    python_path = sys.executable
    print("1/5 success pip install bottle, version: ", bottle.__version__)
    print("2/5 using python located from:", python_path)


if __name__ == "__main__":
    main()
