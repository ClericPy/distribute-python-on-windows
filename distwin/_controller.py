import io
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from urllib.request import urlopen

import click

logging.basicConfig(
    format="%(levelname)-7s %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

__version__ = "0.0.1"


@click.command(
    context_settings={
        "help_option_names": ["-h", "--help"],
        "ignore_unknown_options": True,
    }
)
@click.version_option(__version__, "-V", "--version", prog_name="distwin")
@click.option(
    "--entry-point", "-e", default=None, help="entry_point format like `app:main`"
)
@click.option("--output-file", "-o", default="app.pyz", help="`app.pyz` by default.")
@click.option(
    "--download-url",
    "-d",
    default=None,
    help="the link where to download the python embed zip file.",
)
@click.option(
    "--python-bit",
    "-b",
    default=32,
    help="the link where to download the python embed zip file.",
)
@click.option(
    "--packages",
    "-p",
    default="",
    help="copy packages into site_packages folder, split by `,`.",
)
@click.option(
    "--site-packages",
    help="`site-packages` by default, including the packages which gotten without `pip`",
    default="site-packages",
)
@click.argument("pip_args", nargs=-1, type=click.UNPROCESSED)
def cli(*args, **kwargs):
    return ShivUtils.main(*args, **kwargs)


class ShivUtils(object):
    @classmethod
    def main(
        cls,
        shiv_path=None,
        python_bit=32,
        site_packages="site-packages",
        packages="",
        entry_point=None,
        output_file="app.pyz",
        download_url=None,
        pip_args=None,
    ):
        dist_path = "dist"
        # ensure shiv
        shiv_path = shiv_path or cls.get_shiv_path()
        if not shiv_path:
            raise FileNotFoundError("can not find shiv.exe.")
        logging.info("[find] shiv.exe at '%s'" % shiv_path)
        if not os.path.isdir(dist_path):
            os.mkdir(dist_path)
        # ensure python
        python_path = cls.prepare_python(
            bit=python_bit, dist_path=dist_path, download_url=download_url
        )
        if entry_point:
            packages = ",".join([entry_point.split(":")[0], (packages or "")])
        if packages:
            cls.prepare_site_packages(packages, site_packages=site_packages)
        # os.system(r"D:\Python3\scripts\shiv.exe -o ./dist/app.pyz -e run:main --site-packages site-packages -p ./python-execute/python.exe pyyaml")
        output_file_path = os.path.join(dist_path, output_file)
        cls.create_run_bat(
            dist_path=dist_path, python_path=python_path, output_file=output_file
        )
        args = [shiv_path, "-o", output_file_path, "-p", python_path]
        if entry_point:
            args.append("-e")
            args.append(entry_point)
        if site_packages:
            args.append("--site-packages")
            args.append(site_packages)
        if not pip_args:
            logging.debug("[pip_args] is null, so use `bottle` for shiv.")
            pip_args = ["bottle"]
        args.extend(pip_args)
        proc = subprocess.Popen(args, shell=1)
        proc.wait()
        logging.debug("removing folder: %s" % site_packages)
        cls.remove_dir(site_packages)
        logging.info("dist success, cd into `dist` folder and run the file `run.bat`.")
        # if input("remove the dir %s? (y/n)" % site_packages).lower() == "y":
        #     cls.remove_dir(site_packages)

    @staticmethod
    def get_shiv_path():
        python_path = sys.executable
        python_dir = os.path.dirname(python_path)
        shiv_path = os.path.join(python_dir, "scripts", "shiv.exe")
        if os.path.isfile(shiv_path):
            return shiv_path

    def fetch_url(url):
        r = urlopen(url)
        text = r.read().decode("u8")
        return text

    @classmethod
    def fetch_latest_release_url(cls, bit=32):
        url = "https://www.python.org/downloads/windows/"
        text = cls.fetch_url(url)
        # ignore rc version...
        match = re.search(
            '<a href="(https?://www.python.org/[^"]*\d+\.\d+-embed-(?:win|amd)%s.zip)">'
            % bit,
            text,
        ).group(1)
        return match

    @classmethod
    def prepare_python(cls, bit=32, force=False, dist_path="dist", download_url=None):
        if not download_url:
            download_url = cls.fetch_latest_release_url(bit=bit)
            logging.debug("[find] the latest python-%s-bit release ." % bit)
        dir_name = os.path.split(download_url)
        python_dir = dir_name[-1].replace(".zip", "")
        python_dir_path = os.path.join(dist_path, python_dir)
        python_exe_path = os.path.join(python_dir_path, "python.exe")
        if os.path.isfile(python_exe_path):
            logging.debug("[ignore] file %s exists." % python_exe_path)
            return os.path.join(python_dir, "python.exe")
        logging.debug("[downloading] python from %s." % download_url)
        start_time = time.time()
        r = urlopen(download_url)
        f = io.BytesIO()
        content = r.read()
        f.write(content)
        logging.debug(
            "download python zip file (%s) success in %s seconds."
            % (len(content), int(time.time() - start_time))
        )
        cls.unzip_python_file(f, python_dir_path)
        logging.debug("unzip python file to %s success" % python_dir_path)
        if not os.path.isfile(python_exe_path):
            raise FileNotFoundError("bad path (%s) for python.exe" % python_exe_path)
        return os.path.join(python_dir, "python.exe")

    @classmethod
    def unzip_python_file(cls, path=None, target="./python-execute"):
        zip_file = zipfile.ZipFile(path, "r")
        for file in zip_file.namelist():
            zip_file.extract(file, target)

    def move_package(string):
        module_name, function_name = string.split(":", 1)
        module = __import__(module_name)
        print(module)
        if not hasattr(module, function_name):
            raise RuntimeError("not found %s in %s" % (function_name, module_name))
        print(module.__package__, module.__file__)

    @classmethod
    def remove_dir(cls, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)

    @classmethod
    def refresh_dir(cls, path):
        cls.remove_dir(path)
        os.mkdir(path)

    @classmethod
    def prepare_site_packages(cls, paths_string, site_packages):
        logging.debug("refreshing site-packages folder: %s." % site_packages)
        cls.refresh_dir(site_packages)
        paths = paths_string.split(",")
        logging.debug("copy %s into %s" % (paths, site_packages))
        for path in paths:
            if os.path.isdir(path):
                dir_name = os.path.split(path)[-1]
                logging.debug("copy %s" % path)
                shutil.copytree(path, "./%s/%s" % (site_packages, dir_name))
            elif os.path.isfile(path + ".py"):
                file_name = path + ".py"
                logging.debug("copy %s" % file_name)
                shutil.copy(file_name, "./%s" % site_packages)
            else:
                logging.warning("%s not found" % path)

    @staticmethod
    def create_run_bat(dist_path="dist", python_path=None, output_file=None):
        cmd = r'start %s "%s"' % (python_path, output_file)
        with open(os.path.join(dist_path, "run.bat"), "w") as f:
            f.write(cmd)


if __name__ == "__main__":
    ""
    ShivUtils.main()
    # print(get_shiv_path())
    # print(unzip_python_file("python-32.zip"))
    # import shiv_me

    # print(dir(shiv_me.__loader__))
    # print(shiv_me.__package__)
    # import torequests

    # print(torequests.__package__)
    # import torequests.utils

    # print(torequests.utils.__package__)
    # move_package("torequests.utils:ttime")
    # create_run_bat()
    # import torequests.utils as ee
    # print(dir(ee))
    # print(ee.__package__)
    # print(dir(ee.__loader__))
    # print(ee.__loader__.resource_path())
