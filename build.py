import tarfile
from contextlib import contextmanager
from gzip import GzipFile
from io import BytesIO
from posixpath import join as pjoin
from tempfile import NamedTemporaryFile

from poetry import poetry
from poetry.console import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.masonry import api, builder
from poetry.masonry.api import *
from poetry.masonry.builders import complete


def build_version_contents(version: str) -> bytes:
    return f'__version__ = {version!r}\n'.encode('utf-8')


@contextmanager
def version_file(version: str):
    with NamedTemporaryFile() as fp:
        fp.write(build_version_contents(version))
        fp.flush()
        fp.seek(0)
        yield fp


class WheelBuilder(api.WheelBuilder):
    def _write_metadata(self, wheel):
        with version_file(self._meta.version) as fp:
            self._add_file(wheel, fp.name, f'slack_channeler/version.py')

        super()._write_metadata(wheel)


class SdistBuilder(api.SdistBuilder):
    def build(self, target_dir=None):  # type: (Path) -> Path
        self._io.writeln(" - Building <info>sdist</info>")
        if target_dir is None:
            target_dir = self._path / "dist"

        if not target_dir.exists():
            target_dir.mkdir(parents=True)

        target = target_dir / "{}-{}.tar.gz".format(
            self._package.pretty_name, self._meta.version
        )
        gz = GzipFile(target.as_posix(), mode="wb")
        tar = tarfile.TarFile(
            target.as_posix(), mode="w", fileobj=gz, format=tarfile.PAX_FORMAT
        )

        try:
            tar_dir = "{}-{}".format(self._package.pretty_name, self._meta.version)

            files_to_add = self.find_files_to_add(exclude_build=False)

            for relpath in files_to_add:
                path = self._path / relpath
                tar_info = tar.gettarinfo(
                    str(path), arcname=pjoin(tar_dir, str(relpath))
                )
                tar_info = self.clean_tarinfo(tar_info)

                if tar_info.isreg():
                    with path.open("rb") as f:
                        tar.addfile(tar_info, f)
                else:
                    tar.addfile(tar_info)  # Symlinks & ?

            setup = self.build_setup()
            tar_info = tarfile.TarInfo(pjoin(tar_dir, "setup.py"))
            tar_info.size = len(setup)
            tar.addfile(tar_info, BytesIO(setup))

            version = build_version_contents(self._meta.version)
            tar_info = tarfile.TarInfo(pjoin(tar_dir, "slack_channeler/version.py"))
            tar_info.size = len(version)
            tar.addfile(tar_info, BytesIO(version))

            pkg_info = self.build_pkg_info()

            tar_info = tarfile.TarInfo(pjoin(tar_dir, "PKG-INFO"))
            tar_info.size = len(pkg_info)
            tar.addfile(tar_info, BytesIO(pkg_info))
        finally:
            tar.close()
            gz.close()

        self._io.writeln(" - Built <fg=cyan>{}</>".format(target.name))

        return target


class CompleteBuilder(complete.CompleteBuilder):
    def build(self):
        # We start by building the tarball
        # We will use it to build the wheel
        sdist_builder = SdistBuilder(self._poetry, self._env, self._io)
        sdist_file = sdist_builder.build()

        self._io.writeln("")

        dist_dir = self._path / "dist"
        with self.unpacked_tarball(sdist_file) as tmpdir:
            WheelBuilder.make_in(
                poetry.Poetry.create(tmpdir),
                self._env,
                self._io,
                dist_dir,
                original=self._poetry,
            )


class Builder(builder.Builder):
    _FORMATS = {"sdist": SdistBuilder, "wheel": WheelBuilder, "all": CompleteBuilder}


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Builds a wheel, places it in wheel_directory"""
    poetry = Poetry.create(".")

    return unicode(
        WheelBuilder.make_in(
            poetry, SystemEnv(Path(sys.prefix)), NullIO(), Path(wheel_directory)
        )
    )


def build_sdist(sdist_directory, config_settings=None):
    """Builds an sdist, places it in sdist_directory"""
    poetry = Poetry.create(".")

    path = SdistBuilder(poetry, SystemEnv(Path(sys.prefix)), NullIO()).build(
        Path(sdist_directory)
    )

    return unicode(path.name)


class BuildCommand(EnvCommand):
    """
    Builds a package, as a tarball and a wheel by default.

    build
        { --f|format= : Limit the format to either wheel or sdist. }
    """

    def handle(self):
        fmt = "all"
        if self.option("format"):
            fmt = self.option("format")

        package = self.poetry.package
        self.line(
            "Building <info>{}</> (<comment>{}</>)".format(
                package.pretty_name, package.version
            )
        )

        builder = Builder(self.poetry, self.env, self.output)
        builder.build(fmt)


def main():
    application = Application()
    application.add(BuildCommand())
    application.set_default_command('build')
    return application.run()


if __name__ == '__main__':
    main()
