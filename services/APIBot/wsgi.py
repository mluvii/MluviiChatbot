from main import app
from settings import set_base_url

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-hostname')
    args = parser.parse_args()
    hostname = args.hostname
    if hostname is None:
        print("No hostname parameter")
        quit()
    print("Hostname is "+ hostname)
    set_base_url(hostname)
    app.run(host='0.0.0.0', port=5000)
